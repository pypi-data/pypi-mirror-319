from __future__ import annotations

import typing as t
import datetime

from sqlglot import exp, generator, parser, tokens
from sqlglot.dialects.dialect import (
    Dialect,
    NormalizationStrategy,
    arg_max_or_min_no_count,
    build_formatted_time,
    inline_array_sql,
    json_extract_segments,
    json_path_key_only_name,
    no_pivot_sql,
    build_json_extract_path,
    rename_func,
    sha256_sql,
    var_map_sql,
    timestamptrunc_sql,
    unit_to_var,
    trim_sql,
    binary_from_function,
)
from sqlglot.generator import Generator
from sqlglot.helper import is_int, seq_get
from sqlglot.tokens import Token, TokenType
from sqlglot.dialects.doris import Doris

DATEΤΙΜΕ_DELTA = t.Union[exp.DateAdd, exp.DateDiff, exp.DateSub, exp.TimestampSub, exp.TimestampAdd]


def _build_date_format(args: t.List) -> exp.TimeToStr:
    expr = build_formatted_time(exp.TimeToStr, "clickhouse")(args)

    timezone = seq_get(args, 2)
    if timezone:
        expr.set("zone", timezone)

    return expr


def _unix_to_time_sql(self: ClickHouse.Generator, expression: exp.UnixToTime) -> str:
    scale = expression.args.get("scale")
    timestamp = expression.this

    if scale in (None, exp.UnixToTime.SECONDS):
        return self.func("fromUnixTimestamp", exp.cast(timestamp, exp.DataType.Type.BIGINT))
    if scale == exp.UnixToTime.MILLIS:
        return self.func("fromUnixTimestamp64Milli", exp.cast(timestamp, exp.DataType.Type.BIGINT))
    if scale == exp.UnixToTime.MICROS:
        return self.func("fromUnixTimestamp64Micro", exp.cast(timestamp, exp.DataType.Type.BIGINT))
    if scale == exp.UnixToTime.NANOS:
        return self.func("fromUnixTimestamp64Nano", exp.cast(timestamp, exp.DataType.Type.BIGINT))

    return self.func(
        "fromUnixTimestamp",
        exp.cast(
            exp.Div(this=timestamp, expression=exp.func("POW", 10, scale)), exp.DataType.Type.BIGINT
        ),
    )


def _lower_func(sql: str) -> str:
    index = sql.index("(")
    return sql[:index].lower() + sql[index:]


def _quantile_sql(self: ClickHouse.Generator, expression: exp.Quantile) -> str:
    quantile = expression.args["quantile"]
    args = f"({self.sql(expression, 'this')})"

    if isinstance(quantile, exp.Array):
        func = self.func("quantiles", *quantile)
    else:
        func = self.func("quantile", quantile)

    return func + args


def _build_count_if(args: t.List) -> exp.CountIf | exp.CombinedAggFunc:
    if len(args) == 1:
        return exp.CountIf(this=seq_get(args, 0))

    return exp.CombinedAggFunc(this="countIf", expressions=args, parts=("count", "If"))


def _build_str_to_date(args: t.List) -> exp.Cast | exp.Anonymous:
    if len(args) == 3:
        return exp.Anonymous(this="STR_TO_DATE", expressions=args)

    strtodate = exp.StrToDate.from_arg_list(args)
    return exp.cast(strtodate, exp.DataType.build(exp.DataType.Type.DATETIME))


def _datetime_delta_sql(name: str) -> t.Callable[[Generator, DATEΤΙΜΕ_DELTA], str]:
    def _delta_sql(self: Generator, expression: DATEΤΙΜΕ_DELTA) -> str:
        if not expression.unit:
            return rename_func(name)(self, expression)

        return self.func(
            name,
            unit_to_var(expression),
            expression.expression,
            expression.this,
        )

    return _delta_sql


def _timestrtotime_sql(self: ClickHouse.Generator, expression: exp.TimeStrToTime):
    tz = expression.args.get("zone")
    datatype = exp.DataType.build(exp.DataType.Type.TIMESTAMP)
    ts = expression.this
    if tz:
        # build a datatype that encodes the timezone as a type parameter, eg DateTime('America/Los_Angeles')
        datatype = exp.DataType.build(
            exp.DataType.Type.TIMESTAMPTZ,  # Type.TIMESTAMPTZ maps to DateTime
            expressions=[exp.DataTypeParam(this=tz)],
        )

        if isinstance(ts, exp.Literal):
            # strip the timezone out of the literal, eg turn '2020-01-01 12:13:14-08:00' into '2020-01-01 12:13:14'
            # this is because Clickhouse encodes the timezone as a data type parameter and throws an error if it's part of the timestamp string
            ts_without_tz = (
                datetime.datetime.fromisoformat(ts.name).replace(tzinfo=None).isoformat(sep=" ")
            )
            ts = exp.Literal.string(ts_without_tz)

    return self.sql(exp.cast(ts, datatype, dialect=self.dialect))


def _handle_tostart_(args: t.List) -> exp.Expression:
    this = seq_get(args, 0)
    unit = str(seq_get(args, 1)).split()[-1].upper()

    if unit == "YEAR":
        return exp.ToStartOfYear(this=this)
    elif unit == "MONTH":
        return exp.ToStartOfMonth(this=this)
    elif unit == "DAY":
        return exp.ToStartOfDay(this=this)

    return exp.ToStartOfMinute(this=this)


def _build_toStartOf(args: t.List) -> exp.TimeRound:
    this = seq_get(args, 0)
    period = seq_get(args, 1)
    period_num = getattr(period, "alias_or_name", None)
    unit = (
        period.args.get("unit").alias_or_name
        if period is not None and period.args.get("unit") is not None
        else None
    )
    return exp.TimeRound(this=this, period=period_num, unit=unit)


def _build_DateSub(args: t.List) -> exp.DateSub:
    if len(args) == 3:
        return exp.DateSub(
            this=seq_get(args, 2), expression=seq_get(args, 1), unit=seq_get(args, 0)
        )
    return exp.DateSub.from_arg_list(args)


def _build_DateAdd(args: t.List) -> exp.DateAdd:
    if len(args) == 3:
        return exp.DateAdd(
            this=seq_get(args, 2), expression=seq_get(args, 1), unit=seq_get(args, 0)
        )
    return exp.DateAdd.from_arg_list(args)


def _build_multi_if(args: t.List) -> exp.Case:
    if len(args) % 2 != 1:
        raise ValueError("MULTIIF function requires an odd number of arguments")
    ifs = []
    for i in range(0, len(args) - 1, 2):
        condition = args[i]
        result = args[i + 1]
        ifs.append(exp.If(this=seq_get(args, i), true=result, condition=condition))

    return exp.Case(ifs=ifs, default=seq_get(args, -1))


def build_todate(args: t.List) -> exp.TimeStrToDate | exp.ConvertTz:
    if len(args) == 1:
        return exp.TimeStrToDate.from_arg_list(args)
    else:
        return exp.ConvertTz(this=seq_get(args, 0), to_tz=seq_get(args, 1))


def build_neighbor(args: t.List) -> exp.Lead | exp.Lag:
    this = seq_get(args, 0)
    offset = seq_get(args, 1)
    # The dialect attribute is added to be compatible with the neighbor function.
    # For this purpose, an over () needs to be added to improve the lead and lag functions in doris.
    dialects = "clickhouse"
    if offset is not None:
        if len(args) == 2:
            if offset.find(exp.Neg):
                return exp.Lag(this=this, offset=offset.alias_or_name, dialect=dialects)
            else:
                return exp.Lead(this=this, offset=offset.alias_or_name, dialect=dialects)
        else:
            if offset.find(exp.Neg):
                return exp.Lag(
                    this=this,
                    offset=offset.alias_or_name,
                    default=seq_get(args, 2),
                    dialect=dialects,
                )
            else:
                return exp.Lead(
                    this=this,
                    offset=offset.alias_or_name,
                    default=seq_get(args, 2),
                    dialect=dialects,
                )
    return exp.Lead.from_arg_list(args)


def _handle_cast(args: t.List) -> exp.Coalesce:
    this = seq_get(args, 0)
    to = seq_get(args, 1)
    cast_to_value = (
        Doris.Generator.CLICKHOUSE_TYPE_MAPPING.get(to.name.lower()) if to is not None else None
    )
    return exp.Coalesce(
        this=exp.CastToStrType(
            this=this,
            to=cast_to_value,
        ),
        expressions=exp.Literal.number(0),
    )


class ClickHouse(Dialect):
    NORMALIZE_FUNCTIONS: bool | str = False
    NULL_ORDERING = "nulls_are_last"
    SUPPORTS_USER_DEFINED_TYPES = False
    SAFE_DIVISION = True
    LOG_BASE_FIRST: t.Optional[bool] = None
    FORCE_EARLY_ALIAS_REF_EXPANSION = True

    # https://github.com/ClickHouse/ClickHouse/issues/33935#issue-1112165779
    NORMALIZATION_STRATEGY = NormalizationStrategy.CASE_SENSITIVE

    UNESCAPED_SEQUENCES = {
        "\\0": "\0",
    }

    CREATABLE_KIND_MAPPING = {"DATABASE": "SCHEMA"}

    SET_OP_DISTINCT_BY_DEFAULT: t.Dict[t.Type[exp.Expression], t.Optional[bool]] = {
        exp.Except: False,
        exp.Intersect: False,
        exp.Union: None,
    }

    class Tokenizer(tokens.Tokenizer):
        COMMENTS = ["--", "#", "#!", ("/*", "*/")]
        IDENTIFIERS = ['"', "`"]
        STRING_ESCAPES = ["'", "\\"]
        BIT_STRINGS = [("0b", "")]
        HEX_STRINGS = [("0x", ""), ("0X", "")]
        HEREDOC_STRINGS = ["$"]

        KEYWORDS = {
            **tokens.Tokenizer.KEYWORDS,
            "ATTACH": TokenType.COMMAND,
            "DATE32": TokenType.DATE32,
            "DATETIME64": TokenType.DATETIME64,
            "DICTIONARY": TokenType.DICTIONARY,
            "ENUM8": TokenType.ENUM8,
            "ENUM16": TokenType.ENUM16,
            "FINAL": TokenType.FINAL,
            "FIXEDSTRING": TokenType.FIXEDSTRING,
            "FLOAT32": TokenType.FLOAT,
            "FLOAT64": TokenType.DOUBLE,
            "GLOBAL": TokenType.GLOBAL,
            "INT256": TokenType.INT256,
            "LOWCARDINALITY": TokenType.LOWCARDINALITY,
            "MAP": TokenType.MAP,
            "NESTED": TokenType.NESTED,
            "SAMPLE": TokenType.TABLE_SAMPLE,
            "TUPLE": TokenType.STRUCT,
            "UINT128": TokenType.UINT128,
            "UINT16": TokenType.USMALLINT,
            "UINT256": TokenType.UINT256,
            "UINT32": TokenType.UINT,
            "UINT64": TokenType.UBIGINT,
            "UINT8": TokenType.UTINYINT,
            "IPV4": TokenType.IPV4,
            "IPV6": TokenType.IPV6,
            "AGGREGATEFUNCTION": TokenType.AGGREGATEFUNCTION,
            "SIMPLEAGGREGATEFUNCTION": TokenType.SIMPLEAGGREGATEFUNCTION,
            "SYSTEM": TokenType.COMMAND,
            "PREWHERE": TokenType.PREWHERE,
        }
        KEYWORDS.pop("/*+")

        SINGLE_TOKENS = {
            **tokens.Tokenizer.SINGLE_TOKENS,
            "$": TokenType.HEREDOC_STRING,
        }

    class Parser(parser.Parser):
        # Tested in ClickHouse's playground, it seems that the following two queries do the same thing
        # * select x from t1 union all select x from t2 limit 1;
        # * select x from t1 union all (select x from t2 limit 1);
        MODIFIERS_ATTACHED_TO_SET_OP = False
        INTERVAL_SPANS = False

        FUNCTIONS = {
            **parser.Parser.FUNCTIONS,
            "ACCURATECASTORDEFAULT": _handle_cast,
            "ADDYEARS": exp.YearsAdd.from_arg_list,
            "ADDMONTHS": exp.MonthsAdd.from_arg_list,
            "ADDWEEKS": exp.WeeksAdd.from_arg_list,
            "ADDDAYS": exp.DaysAdd.from_arg_list,
            "ADDHOURS": exp.HoursAdd.from_arg_list,
            "ADDMINUTES": exp.MinutesAdd.from_arg_list,
            "ADDSECONDS": exp.SecondsAdd.from_arg_list,
            "ADDQUARTERS": exp.QuartersAdd.from_arg_list,
            "AES_ENCRYPT_MYSQL": exp.Encrypt.from_arg_list,
            "AES_DECRYPT_MYSQL": exp.Decrypt.from_arg_list,
            "ANY": exp.AnyValue.from_arg_list,
            "ARRAYAVG": exp.ArrayAvg.from_arg_list,
            "ARRAYCOMPACT": exp.ArrayCompact.from_arg_list,
            "ARRAYCUMSUM": exp.ArrayCumSum.from_arg_list,
            "ARRAYCONCAT": exp.ArrayConcat.from_arg_list,
            "ARRAYDIFFERENCE": exp.ArrayDifference.from_arg_list,
            "ARRAYDISTINCT": exp.ArrayDistinct.from_arg_list,
            "ARRAYELEMENT": exp.ArrayElement.from_arg_list,
            "ARRAYENUMERATE": exp.ArrayEnumerate.from_arg_list,
            "ARRAYENUMERATEUNIQ": exp.ArrayEnumerateUniq.from_arg_list,
            "ARRAYEXISTS": exp.ArrayExists.from_arg_list,
            "ARRAYFIRST": exp.ArrayFirst.from_arg_list,
            "ARRAYFIRSTINDEX": exp.ArrayFirstIndex.from_arg_list,
            "ARRAYINTERSECT": exp.ArrayIntersect.from_arg_list,
            "ARRAYLAST": exp.ArrayLast.from_arg_list,
            "ARRAYLASTINDEX": exp.ArrayLastIndex.from_arg_list,
            "ARRAYMAP": exp.ArrayMap.from_arg_list,
            "ARRAYPRODUCT": exp.ArrayProduct.from_arg_list,
            "ARRAYPOPBACK": exp.ArrayPopback.from_arg_list,
            "ARRAYPOPFRONT": exp.ArrayPopfront.from_arg_list,
            "ARRAYPUSHBACK": exp.ArrayPushback.from_arg_list,
            "ARRAYPUSHFRONT": exp.ArrayPushfront.from_arg_list,
            "ARRAYSLICE": exp.ArraySlice.from_arg_list,
            "ARRAYREVERSESORT": exp.ArrayReverseSort.from_arg_list,
            "ARRAYSORT": exp.SortArray.from_arg_list,
            "ARRAYSTRINGCONCAT": exp.ArrayStringConcat.from_arg_list,
            "ARRAYSUM": exp.ArraySum.from_arg_list,
            "ARRAYUNIQ": exp.ArrayUniq.from_arg_list,
            "ARRAYZIP": exp.ArrayZip.from_arg_list,
            "ARRAYCOUNT": exp.ArrayCount.from_arg_list,
            "ARRAYREVERSE": exp.ArrayReverse.from_arg_list,
            "ARRAYSHUFFLE": exp.Shuffle.from_arg_list,
            "ARRAYMIN": exp.ArrayMin.from_arg_list,
            "ARRAYMAX": exp.ArrayMax.from_arg_list,
            "REVERSE": exp.ArrayReverse.from_arg_list,
            "BASE64ENCODE": exp.ToBase64.from_arg_list,
            "BASE64DECODE": exp.FromBase64.from_arg_list,
            "BITCOUNT": exp.BitCount.from_arg_list,
            "BITMAPSUBSETINRANGE": exp.BitmapSubsetInRange.from_arg_list,
            "BITMAPSUBSETLIMIT": exp.BitmapSubsetLimit.from_arg_list,
            "BITMAPAND": exp.BitmapAnd.from_arg_list,
            "BITMAPANDCARDINALITY": exp.BitmapAndCount.from_arg_list,
            "BITMAPANDNOT": exp.BitmapAndNot.from_arg_list,
            "BITMAPANDNOTCARDINALITY": exp.BitmapAndNotCount.from_arg_list,
            "BITMAPBUILD": exp.BitmapFromArray.from_arg_list,
            "BITMAPCARDINALITY": exp.BitmapCount.from_arg_list,
            "BITMAPCONTAINS": exp.BitmapContains.from_arg_list,
            "BITMAPOR": exp.BitmapOr.from_arg_list,
            "BITMAPORCARDINALITY": exp.BitmapOrCount.from_arg_list,
            "BITMAPXOR": exp.BitmapXor.from_arg_list,
            "BITMAPXORCARDINALITY": exp.BitmapXOrCount.from_arg_list,
            "BITMAPHASALL": exp.BitmapHasAll.from_arg_list,
            "BITMAPHASANY": exp.BitmapHasAny.from_arg_list,
            "BITMAPTOARRAY": exp.BitmapToArray.from_arg_list,
            "BITMAPMIN": exp.BitmapMin.from_arg_list,
            "BITMAPMAX": exp.BitmapMax.from_arg_list,
            "PLUS": binary_from_function(exp.Add),
            "BITSHIFTLEFT": binary_from_function(exp.BitwiseLeftShift),
            "BITSHIFTRIGHT": binary_from_function(exp.BitwiseRightShift),
            "COUNTIF": _build_count_if,
            "COUNTDISTINCT": lambda args: exp.Count(this=exp.Distinct(expressions=args)),
            "DIVIDE": binary_from_function(exp.Div),
            "DATE_ADD": _build_DateAdd,
            "DATEADD": _build_DateAdd,
            "ADDDATE": _build_DateAdd,
            "DATE_DIFF": lambda args: exp.DateDiff(
                this=seq_get(args, 2), expression=seq_get(args, 1), unit=seq_get(args, 0)
            ),
            "DATEDIFF": lambda args: exp.DateDiff(
                this=seq_get(args, 2), expression=seq_get(args, 1), unit=seq_get(args, 0)
            ),
            "DATE_FORMAT": _build_date_format,
            "DATE_SUB": _build_DateSub,
            "DATESUB": _build_DateSub,
            "SUBDATE": _build_DateSub,
            "EMPTY": exp.Empty.from_arg_list,
            "ENDSWITH": exp.EndsWith.from_arg_list,
            "EXP2": lambda args: exp.Pow(
                this="2",
                expression=seq_get(args, 0),
            ),
            "EXP10": lambda args: exp.Pow(
                this="10",
                expression=seq_get(args, 0),
            ),
            "EXTRACTALL": exp.RegexpExtractAll.from_arg_list,
            "FLATTEN": exp.ArrayConcat.from_arg_list,
            "FORMATDATETIME": _build_date_format,
            # "FORMATDATETIME": exp.TsOrDsToDate.from_arg_list,
            "GROUPARRAY": exp.ArrayAgg.from_arg_list,
            "GROUPBITAND": exp.GroupBitAnd.from_arg_list,
            "GROUPBITOR": exp.GroupBitOr.from_arg_list,
            "GROUPBITXOR": exp.GroupBitXor.from_arg_list,
            "GROUPBITMAP": exp.GroupBitMap.from_arg_list,
            "GROUPBITMAPSTATE": exp.GroupBitMapState.from_arg_list,
            "GROUPBITMAPMERGESTATE": exp.GroupBitMapOrState.from_arg_list,
            "GROUPBITMAPORSTATE": exp.GroupBitMapOrState.from_arg_list,
            "GROUPBITMAPORSTATEORDEFAULT": exp.GroupBitMapOrStateOrDefault.from_arg_list,
            "GENERATEUUIDV4": exp.Uuid.from_arg_list,
            "HAS": exp.ArrayContains.from_arg_list,
            "HASANY": exp.HasAny.from_arg_list,
            "IPV4NUMTOSTRING": exp.Ipv4NumToString.from_arg_list,
            "IPV6NUMTOSTRING": exp.Ipv6NumToString.from_arg_list,
            "IPV4STRINGTONUM": exp.Ipv4StringToNum.from_arg_list,
            "IPV4STRINGTONUMORDEFAULT": exp.Ipv4StringToNumOrDefault.from_arg_list,
            "IPV4STRINGTONUMORNULL": exp.Ipv4StringToNumOrNull.from_arg_list,
            "IPV4CIDRTORANGE": exp.Ipv4CidrToRange.from_arg_list,
            "IPV6CIDRTORANGE": exp.Ipv6CidrToRange.from_arg_list,
            "IPV6STRINGTONUM": exp.Ipv6StringToNum.from_arg_list,
            "IPV6STRINGTONUMORDEFAULT": exp.Ipv6StringToNumOrDefault.from_arg_list,
            "IPV6STRINGTONUMORNULL": exp.Ipv6StringToNumOrNull.from_arg_list,
            "TOIPV4": exp.ToIpv4.from_arg_list,
            "TOIPV4ORDEFAULT": exp.ToIpv4OrDefault.from_arg_list,
            "TOIPV4ORNULL": exp.ToIpv4OrNull.from_arg_list,
            "TOIPV6": exp.ToIpv6.from_arg_list,
            "TOIPV6ORDEFAULT": exp.ToIpv6OrDefault.from_arg_list,
            "TOIPV6ORNULL": exp.ToIpv6OrNull.from_arg_list,
            "TOWEEK": exp.Week.from_arg_list,
            "ISIPV4STRING": exp.IsIpv4String.from_arg_list,
            "ISIPV6STRING": exp.IsIpv6String.from_arg_list,
            "ISNOTNULL": exp.IsNotNull.from_arg_list,
            "INDEXOF": exp.ArrayPosition.from_arg_list,
            "INTDIV": binary_from_function(exp.IntDiv),
            "INTDIVORZERO": lambda args: exp.Coalesce(
                this=exp.IntDiv(this=seq_get(args, 0), expression=seq_get(args, 1)),
                expressions=exp.Literal.number(0),
            ),
            "JSONEXTRACTINT": build_json_extract_path(
                exp.JSONExtractScalar, zero_based_indexing=False
            ),
            "JSONEXTRACTRAW": build_json_extract_path(
                exp.JSONExtractScalar, zero_based_indexing=False
            ),
            "JSONEXTRACTSTRING": build_json_extract_path(
                exp.JSONExtractScalar, zero_based_indexing=False
            ),
            "JSONHAS": exp.JSONArrayContains.from_arg_list,
            "JSONLENGTH": exp.JsonArrayLength.from_arg_list,
            "LENGTHUTF8": exp.Length.from_arg_list,
            "OCTET_LENGTH": exp.LengthB.from_arg_list,
            "LOWERUTF8": exp.Lower.from_arg_list,
            "MAP": parser.build_var_map,
            "MAPCONTAINS": exp.MapContainsKey.from_arg_list,
            "MAPKEYS": exp.MapKeys.from_arg_list,
            "MAPVALUES": exp.MapValues.from_arg_list,
            "MATCH": exp.RegexpLike.from_arg_list,
            "MID": exp.Substring.from_arg_list,
            "MULTIMATCHANY": exp.MultiMatchAny.from_arg_list,
            "MINUS": binary_from_function(exp.Sub),
            "MULTIPLY": binary_from_function(exp.Mul),
            "MINIF": lambda args: exp.Min(
                this=exp.func("IF", seq_get(args, 1), seq_get(args, 0), "NULL")
            ),
            "MULTIIF": _build_multi_if,
            "MODULO": binary_from_function(exp.Mod),
            "MODULOORZERO": lambda args: exp.Coalesce(
                this=exp.Mod(this=seq_get(args, 0), expression=seq_get(args, 1)),
                expressions=exp.Literal.number(0),
            ),
            "NEGATE": lambda args: exp.Neg(this=seq_get(args, 0)),
            "NEIGHBOR": build_neighbor,
            "NOTEMPTY": exp.NotEmpty.from_arg_list,
            "NUMBERS": exp.NumbersTable.from_arg_list,
            "RANDCANONICAL": exp.Rand.from_arg_list,
            "STR_TO_DATE": _build_str_to_date,
            "RANGE": exp.ArrayRange.from_arg_list,
            "REPLACEALL": exp.Replace.from_arg_list,
            "REPLACEREGEXPONE": exp.RegexpReplaceOne.from_arg_list,
            "REPLACEREGEXPALL": exp.RegexpReplace.from_arg_list,
            "PARSEDATETIME": exp.StrToDate.from_arg_list,
            "PARSEDATETIMEORNULL": exp.StrToDate.from_arg_list,
            "POSITIONUTF8": exp.StrPosition.from_arg_list,
            "POSITIONCASEINSENSITIVEUTF8": lambda args: exp.StrPosition(
                this=exp.func("LOWER", seq_get(args, 0)),
                substr=exp.func("LOWER", seq_get(args, 1)),
            ),
            "POSITIONCASEINSENSITIVE": lambda args: exp.StrPosition(
                this=exp.func("LOWER", seq_get(args, 0)),
                substr=exp.func("LOWER", seq_get(args, 1)),
            ),
            "SPLITBYCHAR": lambda args: exp.Split(
                this=seq_get(args, 1),
                expression=seq_get(args, 0),
            ),
            "SPLITBYSTRING": lambda args: exp.Split(
                this=seq_get(args, 1),
                expression=seq_get(args, 0),
            ),
            "STARTSWITH": exp.StartsWith.from_arg_list,
            "STDDEVPOP": exp.StddevPop.from_arg_list,
            "STDDEVSAMP": exp.StddevSamp.from_arg_list,
            "SUBTRACTMINUTES": lambda args: exp.DateSub(
                this=seq_get(args, 0),
                expression=seq_get(args, 1),
                unit="MINUTE",
            ),
            "SUBTRACTHOURS": lambda args: exp.DateSub(
                this=seq_get(args, 0),
                expression=seq_get(args, 1),
                unit="HOUR",
            ),
            "SUBTRACTDAYS": lambda args: exp.DateSub(
                this=seq_get(args, 0),
                expression=seq_get(args, 1),
                unit="DAY",
            ),
            "SUBTRACTWEEKS": lambda args: exp.DateSub(
                this=seq_get(args, 0),
                expression=seq_get(args, 1),
                unit="WEEK",
            ),
            "SUBBITMAP": exp.SubBitmap.from_arg_list,
            "SUBSTRINGUTF8": exp.Substring.from_arg_list,
            "SUBTRACTYEARS": exp.YearsSub.from_arg_list,
            "SUBTRACTMONTHS": exp.MonthsSub.from_arg_list,
            "SUBTRACTSECONDS": exp.SecondsSub.from_arg_list,
            "SUBTRACTQUARTERS": exp.QuartersSub.from_arg_list,
            "TIMESTAMP_ADD": exp.DateAdd.from_arg_list,
            "TIMESTAMPADD": exp.DateAdd.from_arg_list,
            "TIMESTAMP_SUB": lambda args: exp.DateSub(
                this=seq_get(args, 2),
                expression=seq_get(args, 1),
                unit=seq_get(args, 0),
            ),
            "TIMESTAMPSUB": lambda args: exp.DateSub(
                this=seq_get(args, 2),
                expression=seq_get(args, 1),
                unit=seq_get(args, 0),
            ),
            "TODAY": exp.Today.from_arg_list,
            "TODATE": build_todate,
            "TODATEORNULL": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="DATE",
            ),
            "TODATEORZERO": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="DATE",
                ),
                expressions=exp.Literal.string("1970-01-01"),
            ),
            "TODATE32": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="DATE",
            ),
            "TODATE32ORNULL": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="DATE",
            ),
            "TODATE32ORZERO": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="DATE",
                ),
                expressions=exp.Literal.number(0),
            ),
            "TODATETIME": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="DATETIME",
            ),
            "TODATETIMEORNULL": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="DATETIME",
            ),
            "TODATETIMEORZERO": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="DATETIME",
                ),
                expressions=exp.Literal.string("1970-01-01 00:00:00"),
            ),
            "TODAYOFYEAR": exp.DayOfYear.from_arg_list,
            "TODAYOFMONTH": exp.DayOfMonth.from_arg_list,
            "TODAYOFWEEK": exp.DayOfWeek.from_arg_list,
            "TODATETIME64": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="DATETIME",
            ),
            "TODATETIME64ORNULL": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="DATETIME",
            ),
            "TODATETIME64ORZERO": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="DATETIME",
                ),
                expressions=exp.Literal.string("1970-01-01 00:00:00"),
            ),
            "TODECIMAL32": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="DECIMAL(32, {})".format(seq_get(args, 1)),
            ),
            "TODECIMAL64": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="DECIMAL(38, {})".format(seq_get(args, 1)),
            ),
            "TODECIMAL32ORNULL": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="DECIMAL(32, {})".format(seq_get(args, 1)),
            ),
            "TODECIMAL64ORNULL": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="DECIMAL(38, {})".format(seq_get(args, 1)),
            ),
            "TODECIMAL32ORZERO": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="DECIMAL(32, {})".format(seq_get(args, 1)),
                ),
                expressions=exp.Literal.number(0),
            ),
            "TODECIMAL64ORZERO": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="DECIMAL(38, {})".format(seq_get(args, 1)),
                ),
                expressions=exp.Literal.number(0),
            ),
            "TOFLOAT32": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="FLOAT",
            ),
            "TOFLOAT64": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="DOUBLE",
            ),
            "TOFLOAT32ORNULL": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="FLOAT",
            ),
            "TOFLOAT64ORNULL": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="DOUBLE",
            ),
            "TOFLOAT32ORZERO": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="FLOAT",
                ),
                expressions=exp.Literal.number(0),
            ),
            "TOFLOAT64ORZERO": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="DOUBLE",
                ),
                expressions=exp.Literal.number(0),
            ),
            "TOHOUR": exp.Hour.from_arg_list,
            "TOINT64": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="BIGINT",
            ),
            "TOINT64ORNULL": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="BIGINT",
            ),
            "TOINT64ORZERO": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="BIGINT",
                ),
                expressions=exp.Literal.number(0),
            ),
            "TOINT64ORDEFAULT": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="BIGINT",
                ),
                expressions=seq_get(args, 1),
            ),
            "TOINT8": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="TINYINT",
            ),
            "TOINT8ORNULL": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="TINYINT",
            ),
            "TOINT8ORZERO": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="TINYINT",
                ),
                expressions=exp.Literal.number(0),
            ),
            "TOINT8ORDEFAULT": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="TINYINT",
                ),
                expressions=seq_get(args, 1),
            ),
            "TOINT16": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="SMALLINT",
            ),
            "TOINT16ORNULL": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="SMALLINT",
            ),
            "TOINT16ORZERO": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="SMALLINT",
                ),
                expressions=exp.Literal.number(0),
            ),
            "TOINT32": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="INT",
            ),
            "TOINT32ORNULL": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="INT",
            ),
            "TOINT32ORZERO": lambda args: exp.Coalesce(
                this=exp.CastToStrType(
                    this=seq_get(args, 0),
                    to="INT",
                ),
                expressions=exp.Literal.number(0),
            ),
            "TOINTERVALSECOND": lambda args: exp.Interval(
                this=seq_get(args, 0),
                unit=exp.Literal.string("second"),
            ),
            "TOINTERVALMINUTE": lambda args: exp.Interval(
                this=seq_get(args, 0),
                unit=exp.Literal.string("minute"),
            ),
            "TOINTERVALHOUR": lambda args: exp.Interval(
                this=seq_get(args, 0),
                unit=exp.Literal.string("hour"),
            ),
            "TOINTERVALDAY": lambda args: exp.Interval(
                this=seq_get(args, 0),
                unit=exp.Literal.string("day"),
            ),
            "TOINTERVALWEEK": lambda args: exp.Interval(
                this=seq_get(args, 0),
                unit=exp.Literal.string("week"),
            ),
            "TOINTERVALMONTH": lambda args: exp.Interval(
                this=seq_get(args, 0),
                unit=exp.Literal.string("month"),
            ),
            "TOINTERVALQUARTER": lambda args: exp.Interval(
                this=exp.Literal.number(3) * seq_get(args, 0),
                unit=exp.Literal.string("month"),
            ),
            "TOINTERVALYEAR": lambda args: exp.Interval(
                this=seq_get(args, 0),
                unit=exp.Literal.string("year"),
            ),
            "TOLASTDAYOFMONTH": exp.LastDay.from_arg_list,
            "TOMONTH": exp.Month.from_arg_list,
            "TOMINUTE": exp.Minute.from_arg_list,
            "TOQUARTER": exp.Quarter.from_arg_list,
            "TOSTRING": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="STRING",
            ),
            "TOSTARTOFQUARTER": exp.ToStartOfQuarter.from_arg_list,
            "TOSTARTOFMONTH": exp.ToStartOfMonth.from_arg_list,
            "TOSTARTOFWEEK": exp.ToStartOfWeek.from_arg_list,
            "TOSTARTOFDAY": exp.ToStartOfDay.from_arg_list,
            "TOSTARTOFHOUR": exp.ToStartOfHour.from_arg_list,
            "TOSTARTOFINTERVAL": _build_toStartOf,
            "TOSTARTOFMINUTE": exp.ToStartOfMinute.from_arg_list,
            "TOSTARTOFSECOND": exp.ToStartOfSecond.from_arg_list,
            "TOSTARTOFYEAR": exp.ToStartOfYear.from_arg_list,
            "TOSECOND": exp.Second.from_arg_list,
            "TOUNIXTIMESTAMP": exp.TimeToUnix.from_arg_list,
            "TOYEAR": exp.Year.from_arg_list,
            "TOYYYYMM": exp.ToYyyymm.from_arg_list,
            "TOYYYYMMDD": exp.ToYyyymmdd.from_arg_list,
            "TOYYYYMMDDHHMMSS": exp.ToYyyymmddhhmmss.from_arg_list,
            "TRIMLEFT": lambda args: exp.Trim(this=seq_get(args, 0), position="LEADING"),
            "TRIMRIGHT": lambda args: exp.Trim(this=seq_get(args, 0), position="TRAILING"),
            "TRIMBOTH": lambda args: exp.Trim(this=seq_get(args, 0), position="BOTH"),
            "TUPLE": exp.Struct.from_arg_list,
            "UNIQ": exp.ApproxDistinct.from_arg_list,
            "UNIQCOMBINED": exp.UniqCombined.from_arg_list,
            "UPPERUTF8": exp.Upper.from_arg_list,
            "VARPOP": exp.VariancePop.from_arg_list,
            "VARSAMP": exp.Variance.from_arg_list,
            "XOR": lambda args: exp.Xor(expressions=args),
            "MD5": exp.MD5Digest.from_arg_list,
            "SHA256": lambda args: exp.SHA2(this=seq_get(args, 0), length=exp.Literal.number(256)),
            "SHA512": lambda args: exp.SHA2(this=seq_get(args, 0), length=exp.Literal.number(512)),
            "SHA224": lambda args: exp.SHA2(this=seq_get(args, 0), length=exp.Literal.number(224)),
            "YESTERDAY": exp.YesterDay.from_arg_list,
            "COUNTEQUAL": exp.CountEqual.from_arg_list,
        }

        AGG_FUNCTIONS = {
            "count",
            "min",
            "max",
            "sum",
            "avg",
            "any",
            "stddevPop",
            "stddevSamp",
            "varPop",
            "varSamp",
            "corr",
            "covarPop",
            "covarSamp",
            "entropy",
            "exponentialMovingAverage",
            "intervalLengthSum",
            "kolmogorovSmirnovTest",
            "mannWhitneyUTest",
            "median",
            "rankCorr",
            "sumKahan",
            "studentTTest",
            "welchTTest",
            "anyHeavy",
            "anyLast",
            "boundingRatio",
            "first_value",
            "last_value",
            "argMin",
            "argMax",
            "avgWeighted",
            "topK",
            "topKWeighted",
            "deltaSum",
            "deltaSumTimestamp",
            "groupArray",
            "groupArrayLast",
            "groupUniqArray",
            "groupArrayInsertAt",
            "groupArrayMovingAvg",
            "groupArrayMovingSum",
            "groupArraySample",
            "groupBitAnd",
            "groupBitOr",
            "groupBitXor",
            "groupBitmap",
            "groupBitmapAnd",
            "groupBitmapOr",
            "groupBitmapXor",
            "sumWithOverflow",
            "sumMap",
            "minMap",
            "maxMap",
            "skewSamp",
            "skewPop",
            "kurtSamp",
            "kurtPop",
            "uniq",
            "uniqExact",
            "uniqCombined",
            "uniqCombined64",
            "uniqHLL12",
            "uniqTheta",
            "quantile",
            "quantiles",
            "quantileExact",
            "quantilesExact",
            "quantileExactLow",
            "quantilesExactLow",
            "quantileExactHigh",
            "quantilesExactHigh",
            "quantileExactWeighted",
            "quantilesExactWeighted",
            "quantileTiming",
            "quantilesTiming",
            "quantileTimingWeighted",
            "quantilesTimingWeighted",
            "quantileDeterministic",
            "quantilesDeterministic",
            "quantileTDigest",
            "quantilesTDigest",
            "quantileTDigestWeighted",
            "quantilesTDigestWeighted",
            "quantileBFloat16",
            "quantilesBFloat16",
            "quantileBFloat16Weighted",
            "quantilesBFloat16Weighted",
            "simpleLinearRegression",
            "stochasticLinearRegression",
            "stochasticLogisticRegression",
            "categoricalInformationValue",
            "contingency",
            "cramersV",
            "cramersVBiasCorrected",
            "theilsU",
            "maxIntersections",
            "maxIntersectionsPosition",
            "meanZTest",
            "quantileInterpolatedWeighted",
            "quantilesInterpolatedWeighted",
            "quantileGK",
            "quantilesGK",
            "sparkBar",
            "sumCount",
            "largestTriangleThreeBuckets",
            "histogram",
            "sequenceMatch",
            "sequenceCount",
            "windowFunnel",
            "retention",
            "uniqUpTo",
            "sequenceNextNode",
            "exponentialTimeDecayedAvg",
        }

        AGG_FUNCTIONS_SUFFIXES = [
            "If",
            "Array",
            "ArrayIf",
            "Map",
            "SimpleState",
            "State",
            "Merge",
            "MergeState",
            "ForEach",
            "Distinct",
            "OrDefault",
            "OrNull",
            "Resample",
            "ArgMin",
            "ArgMax",
        ]

        FUNC_TOKENS = {
            *parser.Parser.FUNC_TOKENS,
            TokenType.SET,
        }

        RESERVED_TOKENS = parser.Parser.RESERVED_TOKENS - {TokenType.SELECT}

        ID_VAR_TOKENS = {
            *parser.Parser.ID_VAR_TOKENS,
            TokenType.LIKE,
        }

        AGG_FUNC_MAPPING = (
            lambda functions, suffixes: {
                f"{f}{sfx}": (f, sfx) for sfx in (suffixes + [""]) for f in functions
            }
        )(AGG_FUNCTIONS, AGG_FUNCTIONS_SUFFIXES)

        FUNCTIONS_WITH_ALIASED_ARGS = {*parser.Parser.FUNCTIONS_WITH_ALIASED_ARGS, "TUPLE"}

        FUNCTION_PARSERS = {
            **parser.Parser.FUNCTION_PARSERS,
            "ARRAYJOIN": lambda self: self.expression(exp.Explode, this=self._parse_expression()),
            "QUANTILE": lambda self: self._parse_quantile(),
        }

        FUNCTION_PARSERS.pop("MATCH")

        NO_PAREN_FUNCTION_PARSERS = parser.Parser.NO_PAREN_FUNCTION_PARSERS.copy()
        NO_PAREN_FUNCTION_PARSERS.pop("ANY")

        NO_PAREN_FUNCTIONS = parser.Parser.NO_PAREN_FUNCTIONS.copy()
        NO_PAREN_FUNCTIONS.pop(TokenType.CURRENT_TIMESTAMP)

        RANGE_PARSERS = {
            **parser.Parser.RANGE_PARSERS,
            TokenType.GLOBAL: lambda self, this: self._match(TokenType.IN)
            and self._parse_in(this, is_global=True),
        }

        # The PLACEHOLDER entry is popped because 1) it doesn't affect Clickhouse (it corresponds to
        # the postgres-specific JSONBContains parser) and 2) it makes parsing the ternary op simpler.
        COLUMN_OPERATORS = parser.Parser.COLUMN_OPERATORS.copy()
        COLUMN_OPERATORS.pop(TokenType.PLACEHOLDER)

        JOIN_KINDS = {
            *parser.Parser.JOIN_KINDS,
            TokenType.ANY,
            TokenType.ASOF,
            TokenType.ARRAY,
        }

        TABLE_ALIAS_TOKENS = parser.Parser.TABLE_ALIAS_TOKENS - {
            TokenType.ANY,
            TokenType.ARRAY,
            TokenType.FINAL,
            TokenType.FORMAT,
            TokenType.SETTINGS,
        }

        ALIAS_TOKENS = parser.Parser.ALIAS_TOKENS - {
            TokenType.FORMAT,
        }

        LOG_DEFAULTS_TO_LN = True

        QUERY_MODIFIER_PARSERS = {
            **parser.Parser.QUERY_MODIFIER_PARSERS,
            TokenType.SETTINGS: lambda self: (
                "settings",
                self._advance() or self._parse_csv(self._parse_assignment),
            ),
            TokenType.FORMAT: lambda self: ("format", self._advance() or self._parse_id_var()),
        }

        CONSTRAINT_PARSERS = {
            **parser.Parser.CONSTRAINT_PARSERS,
            "INDEX": lambda self: self._parse_index_constraint(),
            "CODEC": lambda self: self._parse_compress(),
        }

        ALTER_PARSERS = {
            **parser.Parser.ALTER_PARSERS,
            "REPLACE": lambda self: self._parse_alter_table_replace(),
        }

        SCHEMA_UNNAMED_CONSTRAINTS = {
            *parser.Parser.SCHEMA_UNNAMED_CONSTRAINTS,
            "INDEX",
        }

        PLACEHOLDER_PARSERS = {
            **parser.Parser.PLACEHOLDER_PARSERS,
            TokenType.L_BRACE: lambda self: self._parse_query_parameter(),
        }

        def _parse_types(
            self, check_func: bool = False, schema: bool = False, allow_identifiers: bool = True
        ) -> t.Optional[exp.Expression]:
            dtype = super()._parse_types(
                check_func=check_func, schema=schema, allow_identifiers=allow_identifiers
            )
            if isinstance(dtype, exp.DataType) and dtype.args.get("nullable") is not True:
                # Mark every type as non-nullable which is ClickHouse's default, unless it's
                # already marked as nullable. This marker helps us transpile types from other
                # dialects to ClickHouse, so that we can e.g. produce `CAST(x AS Nullable(String))`
                # from `CAST(x AS TEXT)`. If there is a `NULL` value in `x`, the former would
                # fail in ClickHouse without the `Nullable` type constructor.
                dtype.set("nullable", False)

            return dtype

        def _parse_extract(self) -> exp.Extract | exp.Anonymous:
            index = self._index
            this = self._parse_bitwise()
            if self._match(TokenType.FROM):
                self._retreat(index)
                return super()._parse_extract()

            # We return Anonymous here because extract and regexpExtract have different semantics,
            # so parsing extract(foo, bar) into RegexpExtract can potentially break queries. E.g.,
            # `extract('foobar', 'b')` works, but ClickHouse crashes for `regexpExtract('foobar', 'b')`.
            #
            # TODO: can we somehow convert the former into an equivalent `regexpExtract` call?
            self._match(TokenType.COMMA)
            return self.expression(
                exp.Anonymous, this="extract", expressions=[this, self._parse_bitwise()]
            )

        def _parse_assignment(self) -> t.Optional[exp.Expression]:
            this = super()._parse_assignment()

            if self._match(TokenType.PLACEHOLDER):
                return self.expression(
                    exp.If,
                    this=this,
                    true=self._parse_assignment(),
                    false=self._match(TokenType.COLON) and self._parse_assignment(),
                )

            return this

        def _parse_query_parameter(self) -> t.Optional[exp.Expression]:
            """
            Parse a placeholder expression like SELECT {abc: UInt32} or FROM {table: Identifier}
            https://clickhouse.com/docs/en/sql-reference/syntax#defining-and-using-query-parameters
            """
            this = self._parse_id_var()
            self._match(TokenType.COLON)
            kind = self._parse_types(check_func=False, allow_identifiers=False) or (
                self._match_text_seq("IDENTIFIER") and "Identifier"
            )

            if not kind:
                self.raise_error("Expecting a placeholder type or 'Identifier' for tables")
            elif not self._match(TokenType.R_BRACE):
                self.raise_error("Expecting }")

            return self.expression(exp.Placeholder, this=this, kind=kind)

        def _parse_in(self, this: t.Optional[exp.Expression], is_global: bool = False) -> exp.In:
            this = super()._parse_in(this)
            this.set("is_global", is_global)
            return this

        def _parse_table(
            self,
            schema: bool = False,
            joins: bool = False,
            alias_tokens: t.Optional[t.Collection[TokenType]] = None,
            parse_bracket: bool = False,
            is_db_reference: bool = False,
            parse_partition: bool = False,
        ) -> t.Optional[exp.Expression]:
            this = super()._parse_table(
                schema=schema,
                joins=joins,
                alias_tokens=alias_tokens,
                parse_bracket=parse_bracket,
                is_db_reference=is_db_reference,
            )

            if self._match(TokenType.FINAL):
                this = self.expression(exp.Final, this=this)

            return this

        def _parse_position(self, haystack_first: bool = False) -> exp.StrPosition:
            return super()._parse_position(haystack_first=True)

        # https://clickhouse.com/docs/en/sql-reference/statements/select/with/
        def _parse_cte(self) -> exp.CTE:
            # WITH <identifier> AS <subquery expression>
            cte: t.Optional[exp.CTE] = self._try_parse(super()._parse_cte)

            if not cte:
                # WITH <expression> AS <identifier>
                cte = self.expression(
                    exp.CTE,
                    this=self._parse_assignment(),
                    alias=self._parse_table_alias(),
                    scalar=True,
                )

            return cte

        def _parse_join_parts(
            self,
        ) -> t.Tuple[t.Optional[Token], t.Optional[Token], t.Optional[Token]]:
            is_global = self._match(TokenType.GLOBAL) and self._prev
            kind_pre = self._match_set(self.JOIN_KINDS, advance=False) and self._prev

            if kind_pre:
                kind = self._match_set(self.JOIN_KINDS) and self._prev
                side = self._match_set(self.JOIN_SIDES) and self._prev
                return is_global, side, kind

            return (
                is_global,
                self._match_set(self.JOIN_SIDES) and self._prev,
                self._match_set(self.JOIN_KINDS) and self._prev,
            )

        def _parse_join(
            self, skip_join_token: bool = False, parse_bracket: bool = False
        ) -> t.Optional[exp.Join]:
            join = super()._parse_join(skip_join_token=skip_join_token, parse_bracket=True)
            if join:
                join.set("global", join.args.pop("method", None))

            return join

        def _parse_function(
            self,
            functions: t.Optional[t.Dict[str, t.Callable]] = None,
            anonymous: bool = False,
            optional_parens: bool = True,
            any_token: bool = False,
        ) -> t.Optional[exp.Expression]:
            expr = super()._parse_function(
                functions=functions,
                anonymous=anonymous,
                optional_parens=optional_parens,
                any_token=any_token,
            )

            func = expr.this if isinstance(expr, exp.Window) else expr

            # Aggregate functions can be split in 2 parts: <func_name><suffix>
            parts = (
                self.AGG_FUNC_MAPPING.get(func.this) if isinstance(func, exp.Anonymous) else None
            )

            if parts:
                params = self._parse_func_params(func)

                kwargs = {
                    "this": func.this,
                    "expressions": func.expressions,
                }
                if parts[1]:
                    kwargs["parts"] = parts
                    exp_class = exp.CombinedParameterizedAgg if params else exp.CombinedAggFunc
                else:
                    exp_class = exp.ParameterizedAgg if params else exp.AnonymousAggFunc

                kwargs["exp_class"] = exp_class
                if params:
                    kwargs["params"] = params

                func = self.expression(**kwargs)

                if isinstance(expr, exp.Window):
                    # The window's func was parsed as Anonymous in base parser, fix its
                    # type to be ClickHouse style CombinedAnonymousAggFunc / AnonymousAggFunc
                    expr.set("this", func)
                elif params:
                    # Params have blocked super()._parse_function() from parsing the following window
                    # (if that exists) as they're standing between the function call and the window spec
                    expr = self._parse_window(func)
                else:
                    expr = func

            return expr

        def _parse_func_params(
            self, this: t.Optional[exp.Func] = None
        ) -> t.Optional[t.List[exp.Expression]]:
            if self._match_pair(TokenType.R_PAREN, TokenType.L_PAREN):
                return self._parse_csv(self._parse_lambda)

            if self._match(TokenType.L_PAREN):
                params = self._parse_csv(self._parse_lambda)
                self._match_r_paren(this)
                return params

            return None

        def _parse_quantile(self) -> exp.Quantile:
            this = self._parse_lambda()
            params = self._parse_func_params()
            if params:
                return self.expression(exp.Quantile, this=params[0], quantile=this)
            return self.expression(exp.Quantile, this=this, quantile=exp.Literal.number(0.5))

        def _parse_wrapped_id_vars(self, optional: bool = False) -> t.List[exp.Expression]:
            return super()._parse_wrapped_id_vars(optional=True)

        def _parse_primary_key(
            self, wrapped_optional: bool = False, in_props: bool = False
        ) -> exp.PrimaryKeyColumnConstraint | exp.PrimaryKey:
            return super()._parse_primary_key(
                wrapped_optional=wrapped_optional or in_props, in_props=in_props
            )

        def _parse_on_property(self) -> t.Optional[exp.Expression]:
            index = self._index
            if self._match_text_seq("CLUSTER"):
                this = self._parse_id_var()
                if this:
                    return self.expression(exp.OnCluster, this=this)
                else:
                    self._retreat(index)
            return None

        def _parse_index_constraint(
            self, kind: t.Optional[str] = None
        ) -> exp.IndexColumnConstraint:
            # INDEX name1 expr TYPE type1(args) GRANULARITY value
            this = self._parse_id_var()
            expression = self._parse_assignment()

            index_type = self._match_text_seq("TYPE") and (
                self._parse_function() or self._parse_var()
            )

            granularity = self._match_text_seq("GRANULARITY") and self._parse_term()

            return self.expression(
                exp.IndexColumnConstraint,
                this=this,
                expression=expression,
                index_type=index_type,
                granularity=granularity,
            )

        def _parse_partition(self) -> t.Optional[exp.Partition]:
            # https://clickhouse.com/docs/en/sql-reference/statements/alter/partition#how-to-set-partition-expression
            if not self._match(TokenType.PARTITION):
                return None

            if self._match_text_seq("ID"):
                # Corresponds to the PARTITION ID <string_value> syntax
                expressions: t.List[exp.Expression] = [
                    self.expression(exp.PartitionId, this=self._parse_string())
                ]
            else:
                expressions = self._parse_expressions()

            return self.expression(exp.Partition, expressions=expressions)

        def _parse_alter_table_replace(self) -> t.Optional[exp.Expression]:
            partition = self._parse_partition()

            if not partition or not self._match(TokenType.FROM):
                return None

            return self.expression(
                exp.ReplacePartition, expression=partition, source=self._parse_table_parts()
            )

        def _parse_projection_def(self) -> t.Optional[exp.ProjectionDef]:
            if not self._match_text_seq("PROJECTION"):
                return None

            return self.expression(
                exp.ProjectionDef,
                this=self._parse_id_var(),
                expression=self._parse_wrapped(self._parse_statement),
            )

        def _parse_constraint(self) -> t.Optional[exp.Expression]:
            return super()._parse_constraint() or self._parse_projection_def()

    class Generator(generator.Generator):
        QUERY_HINTS = False
        STRUCT_DELIMITER = ("(", ")")
        NVL2_SUPPORTED = False
        TABLESAMPLE_REQUIRES_PARENS = False
        TABLESAMPLE_SIZE_IS_ROWS = False
        TABLESAMPLE_KEYWORDS = "SAMPLE"
        LAST_DAY_SUPPORTS_DATE_PART = False
        CAN_IMPLEMENT_ARRAY_ANY = True
        SUPPORTS_TO_NUMBER = False
        JOIN_HINTS = False
        TABLE_HINTS = False
        GROUPINGS_SEP = ""
        SET_OP_MODIFIERS = False
        SUPPORTS_TABLE_ALIAS_COLUMNS = False
        VALUES_AS_TABLE = False

        STRING_TYPE_MAPPING = {
            exp.DataType.Type.CHAR: "String",
            exp.DataType.Type.LONGBLOB: "String",
            exp.DataType.Type.LONGTEXT: "String",
            exp.DataType.Type.MEDIUMBLOB: "String",
            exp.DataType.Type.MEDIUMTEXT: "String",
            exp.DataType.Type.TINYBLOB: "String",
            exp.DataType.Type.TINYTEXT: "String",
            exp.DataType.Type.TEXT: "String",
            exp.DataType.Type.VARBINARY: "String",
            exp.DataType.Type.VARCHAR: "String",
        }

        SUPPORTED_JSON_PATH_PARTS = {
            exp.JSONPathKey,
            exp.JSONPathRoot,
            exp.JSONPathSubscript,
        }

        TYPE_MAPPING = {
            **generator.Generator.TYPE_MAPPING,
            **STRING_TYPE_MAPPING,
            exp.DataType.Type.ARRAY: "Array",
            exp.DataType.Type.BIGINT: "Int64",
            exp.DataType.Type.DATE32: "Date32",
            exp.DataType.Type.DATETIME: "DateTime",
            exp.DataType.Type.DATETIME64: "DateTime64",
            exp.DataType.Type.TIMESTAMP: "DateTime",
            exp.DataType.Type.TIMESTAMPTZ: "DateTime",
            exp.DataType.Type.DOUBLE: "Float64",
            exp.DataType.Type.ENUM: "Enum",
            exp.DataType.Type.ENUM8: "Enum8",
            exp.DataType.Type.ENUM16: "Enum16",
            exp.DataType.Type.FIXEDSTRING: "FixedString",
            exp.DataType.Type.FLOAT: "Float32",
            exp.DataType.Type.INT: "Int32",
            exp.DataType.Type.MEDIUMINT: "Int32",
            exp.DataType.Type.INT128: "Int128",
            exp.DataType.Type.INT256: "Int256",
            exp.DataType.Type.LOWCARDINALITY: "LowCardinality",
            exp.DataType.Type.MAP: "Map",
            exp.DataType.Type.NESTED: "Nested",
            exp.DataType.Type.SMALLINT: "Int16",
            exp.DataType.Type.STRUCT: "Tuple",
            exp.DataType.Type.TINYINT: "Int8",
            exp.DataType.Type.UBIGINT: "UInt64",
            exp.DataType.Type.UINT: "UInt32",
            exp.DataType.Type.UINT128: "UInt128",
            exp.DataType.Type.UINT256: "UInt256",
            exp.DataType.Type.USMALLINT: "UInt16",
            exp.DataType.Type.UTINYINT: "UInt8",
            exp.DataType.Type.IPV4: "IPv4",
            exp.DataType.Type.IPV6: "IPv6",
            exp.DataType.Type.AGGREGATEFUNCTION: "AggregateFunction",
            exp.DataType.Type.SIMPLEAGGREGATEFUNCTION: "SimpleAggregateFunction",
        }

        TRANSFORMS = {
            **generator.Generator.TRANSFORMS,
            exp.AnyValue: rename_func("any"),
            exp.ApproxDistinct: rename_func("uniq"),
            exp.ArrayFilter: lambda self, e: self.func("arrayFilter", e.expression, e.this),
            exp.ArraySize: rename_func("LENGTH"),
            exp.ArraySum: rename_func("arraySum"),
            exp.ArgMax: arg_max_or_min_no_count("argMax"),
            exp.ArgMin: arg_max_or_min_no_count("argMin"),
            exp.Array: inline_array_sql,
            exp.CastToStrType: rename_func("CAST"),
            exp.CountIf: rename_func("countIf"),
            exp.CompressColumnConstraint: lambda self,
            e: f"CODEC({self.expressions(e, key='this', flat=True)})",
            exp.ComputedColumnConstraint: lambda self,
            e: f"{'MATERIALIZED' if e.args.get('persisted') else 'ALIAS'} {self.sql(e, 'this')}",
            exp.CurrentDate: lambda self, e: self.func("CURRENT_DATE"),
            exp.DateAdd: _datetime_delta_sql("DATE_ADD"),
            exp.DateDiff: _datetime_delta_sql("DATE_DIFF"),
            exp.DateStrToDate: rename_func("toDate"),
            exp.DateSub: _datetime_delta_sql("DATE_SUB"),
            exp.Explode: rename_func("arrayJoin"),
            exp.Final: lambda self, e: f"{self.sql(e, 'this')} FINAL",
            exp.IsNan: rename_func("isNaN"),
            exp.JSONExtract: json_extract_segments("JSONExtractString", quoted_index=False),
            exp.JSONExtractScalar: json_extract_segments("JSONExtractString", quoted_index=False),
            exp.JSONPathKey: json_path_key_only_name,
            exp.JSONPathRoot: lambda *_: "",
            exp.Map: lambda self, e: _lower_func(var_map_sql(self, e)),
            exp.Nullif: rename_func("nullIf"),
            exp.PartitionedByProperty: lambda self, e: f"PARTITION BY {self.sql(e, 'this')}",
            exp.Pivot: no_pivot_sql,
            exp.Quantile: _quantile_sql,
            exp.RegexpLike: lambda self, e: self.func("match", e.this, e.expression),
            exp.Rand: rename_func("randCanonical"),
            exp.StartsWith: rename_func("startsWith"),
            exp.StrPosition: lambda self, e: self.func(
                "position", e.this, e.args.get("substr"), e.args.get("position")
            ),
            exp.TimeToStr: lambda self, e: self.func(
                "formatDateTime", e.this, self.format_time(e), e.args.get("zone")
            ),
            exp.TimeStrToTime: _timestrtotime_sql,
            exp.TimestampAdd: _datetime_delta_sql("TIMESTAMP_ADD"),
            exp.TimestampSub: _datetime_delta_sql("TIMESTAMP_SUB"),
            exp.VarMap: lambda self, e: _lower_func(var_map_sql(self, e)),
            exp.Xor: lambda self, e: self.func("xor", e.this, e.expression, *e.expressions),
            exp.MD5Digest: rename_func("MD5"),
            exp.MD5: lambda self, e: self.func("LOWER", self.func("HEX", self.func("MD5", e.this))),
            exp.SHA: rename_func("SHA1"),
            exp.SHA2: sha256_sql,
            exp.UnixToTime: _unix_to_time_sql,
            exp.TimestampTrunc: timestamptrunc_sql(zone=True),
            exp.Trim: trim_sql,
            exp.Variance: rename_func("varSamp"),
            exp.SchemaCommentProperty: lambda self, e: self.naked_property(e),
            exp.Stddev: rename_func("stddevSamp"),
            exp.Chr: rename_func("CHAR"),
            exp.Lag: lambda self, e: self.func(
                "lagInFrame", e.this, e.args.get("offset"), e.args.get("default")
            ),
            exp.Lead: lambda self, e: self.func(
                "leadInFrame", e.this, e.args.get("offset"), e.args.get("default")
            ),
        }

        PROPERTIES_LOCATION = {
            **generator.Generator.PROPERTIES_LOCATION,
            exp.VolatileProperty: exp.Properties.Location.UNSUPPORTED,
            exp.PartitionedByProperty: exp.Properties.Location.POST_SCHEMA,
            exp.OnCluster: exp.Properties.Location.POST_NAME,
        }

        # There's no list in docs, but it can be found in Clickhouse code
        # see `ClickHouse/src/Parsers/ParserCreate*.cpp`
        ON_CLUSTER_TARGETS = {
            "SCHEMA",  # Transpiled CREATE SCHEMA may have OnCluster property set
            "DATABASE",
            "TABLE",
            "VIEW",
            "DICTIONARY",
            "INDEX",
            "FUNCTION",
            "NAMED COLLECTION",
        }

        # https://clickhouse.com/docs/en/sql-reference/data-types/nullable
        NON_NULLABLE_TYPES = {
            exp.DataType.Type.ARRAY,
            exp.DataType.Type.MAP,
            exp.DataType.Type.STRUCT,
        }

        def strtodate_sql(self, expression: exp.StrToDate) -> str:
            strtodate_sql = self.function_fallback_sql(expression)

            if not isinstance(expression.parent, exp.Cast):
                # StrToDate returns DATEs in other dialects (eg. postgres), so
                # this branch aims to improve the transpilation to clickhouse
                return f"CAST({strtodate_sql} AS DATE)"

            return strtodate_sql

        def cast_sql(self, expression: exp.Cast, safe_prefix: t.Optional[str] = None) -> str:
            this = expression.this

            if isinstance(this, exp.StrToDate) and expression.to == exp.DataType.build("datetime"):
                return self.sql(this)

            return super().cast_sql(expression, safe_prefix=safe_prefix)

        def trycast_sql(self, expression: exp.TryCast) -> str:
            dtype = expression.to
            if not dtype.is_type(*self.NON_NULLABLE_TYPES, check_nullable=True):
                # Casting x into Nullable(T) appears to behave similarly to TRY_CAST(x AS T)
                dtype.set("nullable", True)

            return super().cast_sql(expression)

        def _jsonpathsubscript_sql(self, expression: exp.JSONPathSubscript) -> str:
            this = self.json_path_part(expression.this)
            return str(int(this) + 1) if is_int(this) else this

        def likeproperty_sql(self, expression: exp.LikeProperty) -> str:
            return f"AS {self.sql(expression, 'this')}"

        def _any_to_has(
            self,
            expression: exp.EQ | exp.NEQ,
            default: t.Callable[[t.Any], str],
            prefix: str = "",
        ) -> str:
            if isinstance(expression.left, exp.Any):
                arr = expression.left
                this = expression.right
            elif isinstance(expression.right, exp.Any):
                arr = expression.right
                this = expression.left
            else:
                return default(expression)

            return prefix + self.func("has", arr.this.unnest(), this)

        def eq_sql(self, expression: exp.EQ) -> str:
            return self._any_to_has(expression, super().eq_sql)

        def neq_sql(self, expression: exp.NEQ) -> str:
            return self._any_to_has(expression, super().neq_sql, "NOT ")

        def regexpilike_sql(self, expression: exp.RegexpILike) -> str:
            # Manually add a flag to make the search case-insensitive
            regex = self.func("CONCAT", "'(?i)'", expression.expression)
            return self.func("match", expression.this, regex)

        def datatype_sql(self, expression: exp.DataType) -> str:
            # String is the standard ClickHouse type, every other variant is just an alias.
            # Additionally, any supplied length parameter will be ignored.
            #
            # https://clickhouse.com/docs/en/sql-reference/data-types/string
            if expression.this in self.STRING_TYPE_MAPPING:
                dtype = "String"
            else:
                dtype = super().datatype_sql(expression)

            # This section changes the type to `Nullable(...)` if the following conditions hold:
            # - It's marked as nullable - this ensures we won't wrap ClickHouse types with `Nullable`
            #   and change their semantics
            # - It's not the key type of a `Map`. This is because ClickHouse enforces the following
            #   constraint: "Type of Map key must be a type, that can be represented by integer or
            #   String or FixedString (possibly LowCardinality) or UUID or IPv6"
            # - It's not a composite type, e.g. `Nullable(Array(...))` is not a valid type
            parent = expression.parent
            nullable = expression.args.get("nullable")
            if nullable is True or (
                nullable is None
                and not (
                    isinstance(parent, exp.DataType)
                    and parent.is_type(exp.DataType.Type.MAP, check_nullable=True)
                    and expression.index in (None, 0)
                )
                and not expression.is_type(*self.NON_NULLABLE_TYPES, check_nullable=True)
            ):
                dtype = f"Nullable({dtype})"

            return dtype

        def cte_sql(self, expression: exp.CTE) -> str:
            if expression.args.get("scalar"):
                this = self.sql(expression, "this")
                alias = self.sql(expression, "alias")
                return f"{this} AS {alias}"

            return super().cte_sql(expression)

        def after_limit_modifiers(self, expression: exp.Expression) -> t.List[str]:
            return super().after_limit_modifiers(expression) + [
                (
                    self.seg("SETTINGS ") + self.expressions(expression, key="settings", flat=True)
                    if expression.args.get("settings")
                    else ""
                ),
                (
                    self.seg("FORMAT ") + self.sql(expression, "format")
                    if expression.args.get("format")
                    else ""
                ),
            ]

        def parameterizedagg_sql(self, expression: exp.ParameterizedAgg) -> str:
            params = self.expressions(expression, key="params", flat=True)
            return self.func(expression.name, *expression.expressions) + f"({params})"

        def anonymousaggfunc_sql(self, expression: exp.AnonymousAggFunc) -> str:
            return self.func(expression.name, *expression.expressions)

        def combinedaggfunc_sql(self, expression: exp.CombinedAggFunc) -> str:
            return self.anonymousaggfunc_sql(expression)

        def combinedparameterizedagg_sql(self, expression: exp.CombinedParameterizedAgg) -> str:
            return self.parameterizedagg_sql(expression)

        def placeholder_sql(self, expression: exp.Placeholder) -> str:
            return f"{{{expression.name}: {self.sql(expression, 'kind')}}}"

        def oncluster_sql(self, expression: exp.OnCluster) -> str:
            return f"ON CLUSTER {self.sql(expression, 'this')}"

        def createable_sql(self, expression: exp.Create, locations: t.DefaultDict) -> str:
            if expression.kind in self.ON_CLUSTER_TARGETS and locations.get(
                exp.Properties.Location.POST_NAME
            ):
                this_name = self.sql(
                    expression.this if isinstance(expression.this, exp.Schema) else expression,
                    "this",
                )
                this_properties = " ".join(
                    [self.sql(prop) for prop in locations[exp.Properties.Location.POST_NAME]]
                )
                this_schema = self.schema_columns_sql(expression.this)
                return f"{this_name}{self.sep()}{this_properties}{self.sep()}{this_schema}"

            return super().createable_sql(expression, locations)

        def create_sql(self, expression: exp.Create) -> str:
            # The comment property comes last in CTAS statements, i.e. after the query
            query = expression.expression
            if isinstance(query, exp.Query):
                comment_prop = expression.find(exp.SchemaCommentProperty)
                if comment_prop:
                    comment_prop.pop()
                    query.replace(exp.paren(query))
            else:
                comment_prop = None

            create_sql = super().create_sql(expression)

            comment_sql = self.sql(comment_prop)
            comment_sql = f" {comment_sql}" if comment_sql else ""

            return f"{create_sql}{comment_sql}"

        def prewhere_sql(self, expression: exp.PreWhere) -> str:
            this = self.indent(self.sql(expression, "this"))
            return f"{self.seg('PREWHERE')}{self.sep()}{this}"

        def indexcolumnconstraint_sql(self, expression: exp.IndexColumnConstraint) -> str:
            this = self.sql(expression, "this")
            this = f" {this}" if this else ""
            expr = self.sql(expression, "expression")
            expr = f" {expr}" if expr else ""
            index_type = self.sql(expression, "index_type")
            index_type = f" TYPE {index_type}" if index_type else ""
            granularity = self.sql(expression, "granularity")
            granularity = f" GRANULARITY {granularity}" if granularity else ""

            return f"INDEX{this}{expr}{index_type}{granularity}"

        def partition_sql(self, expression: exp.Partition) -> str:
            return f"PARTITION {self.expressions(expression, flat=True)}"

        def partitionid_sql(self, expression: exp.PartitionId) -> str:
            return f"ID {self.sql(expression.this)}"

        def replacepartition_sql(self, expression: exp.ReplacePartition) -> str:
            return (
                f"REPLACE {self.sql(expression.expression)} FROM {self.sql(expression, 'source')}"
            )

        def projectiondef_sql(self, expression: exp.ProjectionDef) -> str:
            return f"PROJECTION {self.sql(expression.this)} {self.wrap(expression.expression)}"
