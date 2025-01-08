from __future__ import annotations

import re
import typing as t
from sqlglot import exp, generator, transforms, tokens
from sqlglot.dialects.dialect import (
    approx_count_distinct_sql,
    count_if_to_sum,
    rename_func,
    time_format,
    Dialect,
    NormalizationStrategy,
)
from sqlglot.helper import seq_get, csv
from sqlglot.dialects.mysql import MySQL
from sqlglot.parser import binary_range_parser
from sqlglot.tokens import TokenType
from sqlglot.dialects.mysql import _remove_ts_or_ds_to_date

if t.TYPE_CHECKING:
    from sqlglot._typing import E

DATE_DELTA_INTERVAL = {
    "year": "year",
    "yyyy": "year",
    "yy": "year",
    "y": "year",
    "quarter": "quarter",
    "qq": "quarter",
    "q": "quarter",
    "month": "month",
    "mm": "month",
    "m": "month",
    "rm": "month",
    "mon": "month",
    "week": "week",
    "ww": "week",
    "wk": "week",
    "day": "day",
    "dd": "day",
    "d": "day",
    "dy": "day",
    "hour": "hour",
    "minute": "minute",
    "second": "second",
    "hh": "hour",
    "hh12": "hour",
    "hh24": "hour",
    "mi": "minute",
}


def no_paren_current_date_sql(self, expression: exp.CurrentDate) -> str:
    zone = self.sql(expression, "this")
    return f"CURRENT_DATE() AT TIME ZONE {zone}" if zone else "CURRENT_DATE()"


def handle_array_concat(self, expression: exp.ArrayStringConcat) -> str:
    this = self.sql(expression, "this")
    expr = self.sql(expression, "expressions")
    if expr == "":
        return f"CONCAT_WS('',{this})"
    return f"CONCAT_WS({expr}, {this})"


def handle_array_to_string(self, expression: exp.ArrayToString) -> str:
    this = self.sql(expression, "this")
    sep = self.sql(expression, "expression")
    null_replace = self.sql(expression, "null")
    result = f"ARRAY_JOIN({this},{sep}"
    if null_replace:
        result += f",{null_replace}"
    result += ")"
    return result


def handle_concat_ws(self, expression: exp.ConcatWs) -> str:
    delim, *rest_args = expression.expressions
    rest_args_sql = ", ".join(self.sql(arg) for arg in rest_args)
    return f"CONCAT_WS({self.sql(delim)}, {rest_args_sql})"


def handle_date_diff(self, expression: exp.DateDiff) -> str:
    unit_to_function = {
        "microsecond": "MICROSECONDS_DIFF",
        "millisecond": "MILLISECONDS_DIFF",
        "second": "SECONDS_DIFF",
        "minute": "MINUTES_DIFF",
        "hour": "HOURS_DIFF",
        "day": "DAYS_DIFF",
        "month": "MONTHS_DIFF",
        "year": "YEARS_DIFF",
    }
    unit = self.sql(expression, "unit").lower()
    expressions = self.sql(expression, "expression")
    this = self.sql(expression, "this")
    sql_function = unit_to_function.get(unit, "DATEDIFF")
    return f"{sql_function}({this}, {expressions})"


def handle_date_trunc(self, expression: exp.DateTrunc) -> str:
    unit = self.sql(expression, "unit").strip("\"'").lower()
    this = self.sql(expression, "this")
    if unit.isalpha():
        mapped_unit = DATE_DELTA_INTERVAL.get(unit) or unit
        return f"DATE_TRUNC({this}, '{mapped_unit}')"
    if unit.isdigit() or unit.lstrip("-").isdigit() or this.isdigit():
        if this.isdigit():
            return f"TRUNCATE({this})"
        return f"TRUNCATE({this}, {unit})"
    return f"DATE({this})"


def handle_geography(
    self, expression: exp.StAstext
) -> str:  # Realize the identification of geography
    this = self.sql(expression, "this").upper()
    match = re.search(r"POINT\(([-\d.]+) ([-\d.]+)\)", this)
    if match is None:
        return f"ST_ASTEXT(ST_GEOMETRYFROMWKB({this}))"
    x = float(match.group(1))
    y = float(match.group(2))
    return f"ST_ASTEXT(ST_POINT{x, y})"


def handle_log(self, expression: exp.Log) -> str:
    this = self.sql(expression, "this")
    expression = self.sql(expression, "expression")

    if expression == "":
        return self.func("LOG10", this)
    return self.func("LOG", this, expression)


def presto_codepoint_doris_ascii(self, expression: exp.Codepoint) -> str:
    value = self.sql(expression.this, "this")
    if len(value) > 1:
        jutai_value = self.sql(expression.this, "this")
        zhpattern = re.compile("[\u4e00-\u9fa5]+").search(jutai_value)
        if zhpattern:
            raise ValueError("Chinese characters not allowed")
        return f"ASCII({jutai_value})"
    else:
        if value is not None and "\u4e00" <= value <= "\u9fff":
            raise ValueError("Chinese characters not allowed")
        return f"ASCII('{value}')"


def handle_filter(self, expr: exp.Filter) -> str:
    expression = expr.copy()
    self.sql(expr, "this")
    expr = expression.expression.args["this"]
    agg = expression.this.key
    spec = expression.this.args["this"]
    case = (
        exp.Case()
        .when(
            expr,
            spec,
        )
        .else_("0")
    )
    return f"{agg}({self.sql(case)})"


def _string_agg_sql(self: Doris.Generator, expression: exp.GroupConcat) -> str:
    expression = expression.copy()
    separator = expression.args.get("separator") or exp.Literal.string(",")

    order = ""
    this = expression.this
    if isinstance(this, exp.Order):
        if this.this:
            this = this.this.pop()
        order = self.sql(expression.this)  # Order has a leading space
    if isinstance(separator, exp.Chr):
        separator = "\n"
        return f"GROUP_CONCAT({self.format_args(this)}{order},'{separator}')"
    return f"GROUP_CONCAT({self.format_args(this, separator)}{order})"


def handle_range(self, expression: exp.GenerateSeries) -> str:
    start = expression.args.get("start")
    end = self.sql(expression, "end")
    step = expression.args.get("step")

    if step is None:
        end = str(int(end) + 1)
        return self.func("Array_Range", start, end)
    elif isinstance(step, exp.Interval):
        return self.func("Array_Range", start, end, step)

    end = str(int(end) + 1)
    return self.func("Array_Range", start, end, step)


def handle_regexp_extract(self, expr: exp.RegexpExtract | exp.RegexpExtractAll) -> str:
    this = self.sql(expr, "this")
    expression = self.sql(expr, "expression")
    group = self.sql(expr, "group")
    if isinstance(expr, exp.RegexpExtract):
        if self.sql(expr, "dialects") == "presto":
            return (
                f"REGEXP_EXTRACT_OR_NULL({this}, '{expression[1:-1]}', {group if group else '0'})"
            )
        return f"REGEXP_EXTRACT({this}, '{expression[1:-1]}', {group if group else '0'})"
    else:
        assert group == "", "doris's REGEXP_EXTRACT_ALL function does not support three parameters"
        return f"REGEXP_EXTRACT_ALL({this}, '({expression[1:-1]})')"


def build_time_format(time_format: str) -> str:
    # Replace "mi" with "%i"
    time_format = re.sub("mi", "%i", time_format, flags=re.IGNORECASE)
    # Replace "mm" with "%i"
    time_format = time_format.replace("mm", "%i")
    # postgres %M->%i
    time_format = time_format.replace("%M", "%i")
    # Replace both "hh24" and "HH24" with "%H", case-insensitively
    time_format = re.sub("hh24", "%H", time_format, flags=re.IGNORECASE)
    # Replace both "sYYYY" and "YYYY" with "%Y", case-insensitively
    time_format = re.sub(r"s?YYYY", "%Y", time_format, flags=re.IGNORECASE)
    # time_format = re.sub(r"s{0,1}%y", "%Y", time_format, flags=re.IGNORECASE)
    # Remove all digits from the time_format
    time_format = re.sub(r"\d", "", time_format)
    # treadata format to doris
    time_format = re.sub("MONTH", "%M", time_format, flags=re.IGNORECASE)
    time_format = re.sub("MM", "%M", time_format, flags=re.IGNORECASE)
    time_format = re.sub("SS", "%s", time_format, flags=re.IGNORECASE)
    time_format = re.sub("DAY", "%W", time_format, flags=re.IGNORECASE)

    return time_format


def handle_to_date(
    self: Doris.Generator,
    expression: exp.TsOrDsToDate | exp.StrToTime | exp.ToChar | exp.TimeToStr | exp.StrToDate,
) -> str:
    this = self.sql(expression, "this")
    if expression.find(exp.UnicodeString):
        time_format = self.sql(expression, "format")
    else:
        tmp_format = self.format_time(expression)
        time_format = build_time_format(tmp_format) if tmp_format is not None else ""

    if time_format and time_format not in (Doris.TIME_FORMAT, Doris.DATE_FORMAT):
        if isinstance(expression, exp.StrToDate) or isinstance(expression, exp.StrToTime):
            return f"STR_TO_DATE({this}, {time_format})"
        return f"DATE_FORMAT({this}, {time_format})"
    if isinstance(expression.this, exp.TsOrDsToDate):
        return this
    return f"TO_DATE({this})"


def presto_doris_extract_url_parameter(self, expression: exp.ExtractUrlParameter):
    x = self.sql(expression.this, "this")
    y = getattr(expression.expressions, "this", None)
    if x is None or y is None:
        raise ValueError("Both parameters 'name' and 'this' are required.")
    return f"EXTRACT_URL_PARAMETER{x, y}"


def json_exists_to_doris(self, expression: exp.JsonExists):
    json_value = self.sql(expression, "this")
    search_value = self.sql(expression, "expression")
    if json_value is None or search_value is None:
        raise ValueError("json and search values cannot be null values.")
    if isinstance(expression.this, exp.ParseJSON):
        return self.func("JSON_EXISTS_PATH", json_value, search_value)
    match = re.search(r"\$\.[\w\[\]*]+", search_value)
    if match:
        return f"JSON_EXISTS_PATH({json_value},'{match.group()}')"


def clickhouse_countequal_to_doris(self, expression: exp.CountEqual):
    array = self.sql(expression, "this")
    vaule = self.sql(expression, "expression")
    if array is None or vaule is None:
        raise ValueError(
            "The value of the statistics to be parsed cannot be null and must be an array."
        )
    if re.search(r"ARRAY\(.*?\)", array):
        array = f"[{array[6:-1]}]"
    if vaule == "NULL":
        return f"ARRAY_COUNT(x -> x is {vaule},{array})"
    else:
        return f"ARRAY_COUNT(x -> x = {vaule},{array})"


def handle_to_char(self: Doris.Generator, expression: exp.ToChar | exp.TimeToStr) -> str:
    this = self.sql(expression, "this")
    time_format = self.format_time(expression)
    time_format = build_time_format(time_format) if time_format is not None else time_format
    if isinstance(expression.this, exp.Interval):
        raise ValueError(
            "eg. Postgres:to_char(interval '15h 2m 12s', 'HH24:MI:SS') → 15:02:12 not support transform"
        )
    if time_format and time_format not in (Doris.TIME_FORMAT, Doris.DATE_FORMAT):
        return f"DATE_FORMAT({this}, {time_format})"
    if isinstance(expression.this, exp.TsOrDsToDate):
        return this
    return f"CAST({this} AS STRING)"


def handle_replace(self, expression: exp.Replace | exp.ReplaceEmpty | exp.OrReplace) -> str:
    this = self.sql(expression, "this")
    old = self.sql(expression, "old")
    new = self.sql(expression, "new")
    if new == "":
        if isinstance(expression, exp.ReplaceEmpty):
            return f"REPLACE_EMPTY({this},{old},'')"
        return f"REPLACE({this},{old},'')"
    else:
        if isinstance(expression, exp.ReplaceEmpty):
            return f"REPLACE_EMPTY({this},{old},{new})"
        return f"REPLACE({this},{old},{new})"


def handle_rand(self, expr: exp.Rand) -> str:
    min = self.sql(expr, "this")
    max = self.sql(expr, "expression")
    if min == "" and max == "":
        return "RANDOM()"
    elif max == "":
        return f"FLOOR(RANDOM()*{min}.0)"
    else:
        temp = int(max) - int(min)
        return f"FLOOR(RANDOM()*{temp}.0+{min}.0)"


def _str_to_unix_sql(self: generator.Generator, expression: exp.StrToUnix) -> str:
    return self.func("UNIX_TIMESTAMP", expression.this, time_format("doris")(self, expression))


def _json_extract_sql(
    self: Doris.Generator,
    expression: exp.JSONExtract | exp.JSONExtractScalar | exp.JSONBExtract | exp.JSONBExtractScalar,
) -> str:
    dialect = self.sql(expression, "dialect")
    # The string returned by doris using json_extract will contain double quotes, but presto will not.
    # The content returned by json_extract_string is consistent with that of presto.
    if dialect == "'trino'" or dialect == "'presto'":
        return self.func(
            "JSON_EXTRACT_STRING",
            expression.this,
            expression.expression,
            # *json_path_segments(self, expression.expression),
            expression.args.get("null_if_invalid"),
        )
    if isinstance(expression, exp.JSONExtractScalar) or isinstance(
        expression, exp.JSONBExtractScalar
    ):
        return self.func(
            "JSON_EXTRACT",
            expression.this,
            expression.expression,
            # *json_path_segments(self, expression.expression),
            expression.args.get("null_if_invalid"),
        )
    else:
        return self.func(
            "JSONB_EXTRACT",
            expression.this,
            expression.expression,
            # *json_path_segments(self, expression.expression),
            expression.args.get("null_if_invalid"),
        )


def _trim_sql(self: Doris.Generator, expression: exp.Trim) -> str:
    target = self.sql(expression, "this")
    trim_type = self.sql(expression, "position")
    remove_chars = self.sql(expression, "expression")
    collation = self.sql(expression, "collation")
    dialect = self.sql(expression, "dialect")

    # Use TRIM/LTRIM/RTRIM syntax if the expression isn't mysql-specific
    if not remove_chars and not collation:
        return self.trim_sql(expression)
    if dialect == "MYSQL":
        return self.trim_sql(expression)
    if trim_type == "LEADING":
        # doris add trim_in function, https://github.com/apache/doris/pull/41681
        return self.func("LTRIM_IN", target, remove_chars)
    elif trim_type == "TRAILING":
        return self.func("RTRIM_IN", target, remove_chars)
    else:
        return self.func("TRIM_IN", target, remove_chars)


def timestamptrunc_sql(self: Doris.Generator, expression: exp.TimestampTrunc) -> str:
    this = self.sql(expression, "this")
    unit = self.sql(expression, "unit").strip("\"'").lower()
    mapped_unit = DATE_DELTA_INTERVAL.get(unit)
    if mapped_unit is None:
        raise ValueError(
            "date_trunc function second param only support argument is year|quarter|month|week|day|hour|minute|second"
        )
    return f"DATE_TRUNC({this}, '{mapped_unit}')"


def attimezone_sql(self: Doris.Generator, expression: exp.AtTimeZone) -> str:
    this = self.sql(expression, "this")
    timezone = self.sql(expression, "zone")
    return f"CONVERT_TZ({this},'UTC',{timezone})"


def toStartOfInterval(self: Doris.Generator, expression: exp.TimeRound) -> str:
    this = self.sql(expression, "this")
    period = self.sql(expression, "period")
    unit = self.sql(expression, "unit")
    return f"{unit}_FLOOR({this},{period})"


def dayofweeksql(self: Doris.Generator, expression: exp.DayOfWeek) -> str:
    this = self.sql(expression, "this")
    dialect = self.sql(expression, "dialect")
    if dialect == "presto":
        return f"(DAYOFWEEK({this}) + 5) % 7 + 1"
    return f"DAYOFWEEK({this})"


def handle_array_filter(self: Doris.Generator, expression: exp.ArrayFilter) -> str:
    this = self.sql(expression, "this")
    expression_list = []
    if isinstance(expression.this, exp.Lambda):
        for i in range(0, len(expression.expression)):
            expression_list.append(self.sql(expression.expression[i]))
        expressions_str = ", ".join(map(str, expression_list))
        return f"ARRAY_FILTER({this}, {expressions_str})"
    else:
        return f"ARRAY_FILTER({self.sql(expression.expression[0])}, {this})"


def _parse_doris_key(
    self: Doris.Parser, key_type: str, wrapped_optional: bool = False
) -> exp.UniqueKey | exp.DuplicateKey:
    expressions = self._parse_wrapped_csv(self._parse_id_var, optional=wrapped_optional)
    options = self._parse_key_constraint_options()
    if key_type == "UNIQUE":
        return self.expression(exp.UniqueKey, expressions=expressions, options=options)
    elif key_type == "DUPLICATE":
        return self.expression(exp.DuplicateKey, expressions=expressions, options=options)

    return self.expression(exp.DuplicateKey, expressions=expressions, options=options)


def _parse_distributed_by_hash(
    self: Doris.Parser, wrapped_optional: bool = False
) -> exp.DistributedByHash:
    expressions = self._parse_wrapped_csv(self._parse_id_var, optional=wrapped_optional)

    options = []
    while True:
        if not self._curr:
            break
        if self._match_text_seq("BUCKETS", "AUTO"):
            options.append("BUCKETS AUTO")
        else:
            break

    return self.expression(exp.DistributedByHash, expressions=expressions, options=options)


def replace_column_type(self: Doris.Generator, column: exp.ColumnDef):
    # If is NULLABLE type, remove the NULLABLE keyword
    if column.kind and column.kind.is_type(exp.DataType.Type.LOWCARDINALITY):
        column.set("kind", column.kind.expressions[0])

    if column.kind and column.kind.this in (
        exp.DataType.Type.FLOAT,
        exp.DataType.Type.DOUBLE,
    ):
        column.set("kind", exp.DataType.build("decimal"))
    elif (
        column.kind and self.STRING_TYPE_MAPPING.get(column.kind.this, column.kind.this) == "STRING"
    ):
        column.set("kind", exp.DataType.build("varchar"))


def _lag_lead_sql(self, expression: exp.Lag | exp.Lead) -> str:
    if expression.args.get("dialect") == "clickhouse":
        return (
            f"{'LAG' if isinstance(expression, exp.Lag) else 'LEAD'}"
            f"({expression.this},{expression.args.get('offset') or exp.Literal.number(1)},"
            f"{expression.args.get('default') or exp.null()}) OVER ()"
        )
    else:
        return self.func(
            "LAG" if isinstance(expression, exp.Lag) else "LEAD",
            expression.this,
            expression.args.get("offset") or exp.Literal.number(1),
            expression.args.get("default") or exp.null(),
        )


def date_add_sql(kind: str) -> t.Callable[[MySQL.Generator, exp.Expression], str]:
    def func(self: MySQL.Generator, expression: exp.Expression) -> str:
        this = self.sql(expression, "this")
        unit = (expression.text("unit") or "DAY").upper()
        interval_expr = expression.expression

        # Function generation
        def generate_date(kind: str, this: str, interval: t.Union[exp.Interval, str]) -> str:
            return f"DATE_{kind}({this}, {interval})"

        # Handling the QUARTER special case
        if unit == "QUARTER":
            if isinstance(interval_expr, exp.Interval):
                return generate_date(kind, this, interval_expr)
            return generate_date(
                kind, this, self.sql(exp.Interval(this=interval_expr * 3, unit="MONTH"))
            )

        # Handling other units
        if isinstance(interval_expr, exp.Interval):
            return generate_date(kind, this, interval_expr)
        return generate_date(kind, this, self.sql(exp.Interval(this=interval_expr, unit=unit)))

    return func


def unnest_sql(self, expression: exp.Unnest) -> str:
    alias = expression.args.get("alias")
    if isinstance(expression.parent, exp.Join):
        if alias:
            table_sql = alias.args.get("this").alias_or_name if alias.args.get("this") else None
            columns = alias.args.get("columns")
            alias_sql = columns[0].alias_or_name if columns else None
        else:
            table_sql = None
            alias_sql = None
        return f"EXPLODE({self.sql(expression.expressions[0])}) {table_sql} as {alias_sql}"
    else:
        # Retrieve alias and columns information
        columns = alias.args.get("columns") if alias else None
        # Check validity of columns
        if not columns or not columns[0]:
            raise ValueError("alias or columns is None or empty")
        # https://prestodb.io/docs/current/sql/select.html#unnest
        # UNNEST is normally used with a JOIN and can reference columns from relations on the left side of the join.
        alias_dict = {}
        # Check if expression.parent and expression.parent.parent are None
        if expression.parent and expression.parent.parent:
            parent_this = expression.parent.parent.this
            if parent_this:
                # Get expressions, make sure parent_this has an args attribute
                expressions = parent_this.args.get("expressions", [])

                for column_alias in expressions:
                    # Check if column_alias has alias and this attributes
                    if column_alias and column_alias.alias and column_alias.this:
                        alias_dict[column_alias.alias] = column_alias.this

            for column in expression.find_all(exp.Column):
                # Use alias_or_name to get the character to replace
                replace_char = column.this.alias_or_name
                # Check if alias_dict contains replace_char
                if replace_char in alias_dict:
                    column.this.replace(alias_dict[replace_char])

        # Generate SQL
        explode_sql = exp.Explode(this=expression.expressions).sql()
        lateral_sql = f"{exp.Literal(this=explode_sql, view=True, is_string=False).sql()} tmp1"
        alias_sql = exp.TableAlias(this=exp.Identifier(this=columns[0].this, quoted=False)).sql()
        select_sql = (
            exp.Select()
            .select(columns[0].this)
            .lateral(lateral_sql)
            .from_("(select 1 as c1) as t")
            .as_(alias_sql)
            .sql("doris")
        )
        # Return the subquery SQL
        # If the parent has an alias, return the subquery SQL without alias
        if expression.parent and expression.parent.args.get("alias"):
            return exp.Subquery(this=select_sql).sql("doris")
        return exp.Subquery(this=select_sql, alias=expression.alias).sql("doris")


def presto_cte_table_alias_rewrite(expression: exp.Expression) -> exp.Expression:
    if (
        isinstance(expression, exp.Select)
        and "dialect" in expression.args.keys()
        and expression.args["dialect"] == "PRESTO"
        and expression.ctes
    ):
        table_aliases = []
        for cte in expression.ctes:
            table_aliases.append(cte.alias.lower())
            cte.args["alias"].this.args["this"] = cte.alias.lower()

        for tbl in expression.find_all(exp.TableAlias, exp.Table):
            if tbl.this.this.lower() in table_aliases:
                tbl.this.args["this"] = tbl.this.this.lower()

        for column in expression.find_all(exp.Column):
            if column.table.lower() in table_aliases:
                column.args["table"].args["this"] = column.args["table"].this.lower()

    return expression


class Doris(MySQL):
    INDEX_OFFSET = 1
    DATE_FORMAT = "'yyyy-MM-dd'"
    DATEINT_FORMAT = "'yyyyMMdd'"
    TIME_FORMAT = "'yyyy-MM-dd HH:mm:ss'"
    NULL_ORDERING = "nulls_are_small"
    DPIPE_IS_STRING_CONCAT = True
    TIME_MAPPING = {
        **MySQL.TIME_MAPPING,
        "%Y": "yyyy",
        "%m": "MM",
        "%d": "dd",
        "%s": "ss",
        "%H": "HH",
    }
    NORMALIZATION_STRATEGY = NormalizationStrategy.LOWERCASE

    def normalize_identifier(self, expression: E) -> E:
        if (
            isinstance(expression, exp.Identifier)
            and self.normalization_strategy is not NormalizationStrategy.CASE_SENSITIVE
            and (
                not expression.quoted
                or self.normalization_strategy is NormalizationStrategy.CASE_INSENSITIVE
            )
            and not isinstance(expression.parent, exp.Table)
        ):
            if (
                expression.parent
                and hasattr(expression.parent, "this")
                and expression.parent.this.alias_or_name != expression.args.get("this")
                or isinstance(expression.parent, exp.TableAlias)
            ):
                expression.set(
                    "this",
                    (
                        expression.this.upper()
                        if self.normalization_strategy is NormalizationStrategy.UPPERCASE
                        else expression.this.lower()
                    ),
                )

        return expression

    def quote_identifier(self, expression: E, identify: bool = True):
        # Add quote_identifier to doris keywords
        if (
            isinstance(expression, exp.Identifier)
            and not isinstance(expression.parent, exp.Func)
            and expression.name.upper() in Doris.KeyWords
        ):
            return Dialect.get_or_raise(Dialect).quote_identifier(
                expression=expression, identify=identify
            )

        return expression

    class Parser(MySQL.Parser):
        RANGE_PARSERS = {
            **MySQL.Parser.RANGE_PARSERS,
            TokenType.MATCH_ANY: binary_range_parser(exp.MatchAny),
            TokenType.MATCH_ALL: binary_range_parser(exp.MatchAll),
            TokenType.MATCH_PHRASE: binary_range_parser(exp.MatchPhrase),
        }

        PROPERTY_PARSERS = {
            **MySQL.Parser.PROPERTY_PARSERS,
            "UNIQUE KEY": lambda self: _parse_doris_key(self, "UNIQUE"),
            "DUPLICATE KEY": lambda self: _parse_doris_key(self, "DUPLICATE"),
            "DISTRIBUTED BY HASH": _parse_distributed_by_hash,
            "PROPERTIES": lambda self: self._parse_wrapped_csv(self._parse_property),
        }

        FUNCTIONS = {
            **MySQL.Parser.FUNCTIONS,
            "ARRAY_SHUFFLE": exp.Shuffle.from_arg_list,
            "ARRAY_RANGE": exp.GenerateSeries.from_arg_list,
            "ARRAY_SORT": exp.SortArray.from_arg_list,
            "COLLECT_LIST": exp.ArrayAgg.from_arg_list,
            "COLLECT_SET": exp.ArrayUniqueAgg.from_arg_list,
            "DATE_TRUNC": lambda args: exp.TimestampTrunc(
                this=seq_get(args, 0), unit=seq_get(args, 1)
            ),
            "DATE_ADD": exp.DateAdd.from_arg_list,
            "DATE_SUB": exp.DateSub.from_arg_list,
            "DATEDIFF": exp.DateDiff.from_arg_list,
            "FROM_UNIXTIME": exp.StrToUnix.from_arg_list,
            "GROUP_ARRAY": exp.ArrayAgg.from_arg_list,
            "GROUP_CONCAT": exp.GroupConcat.from_arg_list,
            "MONTHS_ADD": exp.AddMonths.from_arg_list,
            "NOW": exp.CurrentTimestamp.from_arg_list,
            "REGEXP": exp.RegexpLike.from_arg_list,
            "SIZE": exp.ArraySize.from_arg_list,
            "TO_DATE": exp.TsOrDsToDate.from_arg_list,
            "TRUNCATE": exp.Truncate.from_arg_list,
        }

        FUNCTION_PARSERS = {
            **MySQL.Parser.FUNCTION_PARSERS,
        }
        # Since it is incompatible with the implementation of mysql, we will pop it out here.
        FUNCTION_PARSERS.pop("GROUP_CONCAT")

        def _parse_explain(self) -> exp.Explain:
            this = "explain"
            comments = self._prev_comments
            return self.expression(
                exp.Explain,
                comments=comments,
                **{  # type: ignore
                    "this": this,
                    "expressions": self._parse_select(nested=True),
                },
            )

    class Tokenizer(MySQL.Tokenizer):
        KEYWORDS = {
            **MySQL.Tokenizer.KEYWORDS,
            "MATCH_ANY": TokenType.MATCH_ANY,
            "MATCH_ALL": TokenType.MATCH_ALL,
            "MATCH_PHRASE": TokenType.MATCH_PHRASE,
            "UNIQUE KEY": TokenType.UNIQUE,
            "DUPLICATE KEY": TokenType.DUPLICATE_KEY,
            "DISTRIBUTED BY HASH": TokenType.DISTRIBUTE_BY,
            "JSONB": TokenType.JSONB,
            "IPV4": TokenType.IPV4,
            "IPV6": TokenType.IPV6,
        }

        UNICODE_STRINGS = [
            (prefix + q, q)
            for q in t.cast(t.List[str], tokens.Tokenizer.QUOTES)
            for prefix in ("U&", "u&")
        ]

        FUNCTION_PARSERS = MySQL.Parser.FUNCTION_PARSERS.copy()
        FUNCTION_PARSERS.pop("GROUP_CONCAT")

    class Generator(MySQL.Generator):
        CAST_MAPPING = {}
        INTERVAL_ALLOWS_PLURAL_FORM = False
        LAST_DAY_SUPPORTS_DATE_PART = False
        SET_OP_MODIFIERS = False
        NULL_ORDERING_SUPPORTED = True

        STRING_TYPE_MAPPING = {
            exp.DataType.Type.TEXT: "STRING",
            exp.DataType.Type.TINYTEXT: "STRING",
            exp.DataType.Type.MEDIUMTEXT: "STRING",
            exp.DataType.Type.LONGTEXT: "STRING",
            exp.DataType.Type.TINYBLOB: "STRING",
            exp.DataType.Type.MEDIUMBLOB: "STRING",
            exp.DataType.Type.LONGBLOB: "STRING",
            exp.DataType.Type.SET: "STRING",
            exp.DataType.Type.BINARY: "STRING",
            exp.DataType.Type.VARBINARY: "STRING",
            exp.DataType.Type.ENUM: "STRING",
            exp.DataType.Type.ENUM8: "STRING",
            exp.DataType.Type.ENUM16: "STRING",
            exp.DataType.Type.INT256: "STRING",
            exp.DataType.Type.UINT128: "STRING",
            exp.DataType.Type.UINT256: "STRING",
            exp.DataType.Type.TIMETZ: "STRING",
            exp.DataType.Type.INTERVAL: "STRING",
            exp.DataType.Type.UUID: "STRING",
            exp.DataType.Type.IPADDRESS: "STRING",
            exp.DataType.Type.GEOMETRY: "STRING",
            exp.DataType.Type.FIXEDDECIMAL: "DECIMAL",
            exp.DataType.Type.MONEY: "STRING",
            exp.DataType.Type.USERDEFINED: "STRING",
            exp.DataType.Type.INET: "STRING",
            exp.DataType.Type.IPPREFIX: "STRING",
        }

        TYPE_MAPPING = {
            **MySQL.Generator.TYPE_MAPPING,
            **STRING_TYPE_MAPPING,
            exp.DataType.Type.TIMESTAMP: "DATETIME",
            exp.DataType.Type.TIMESTAMPTZ: "DATETIME",
            # https://github.com/apache/doris/pull/41008
            exp.DataType.Type.TIME: "TIME",
            exp.DataType.Type.BIT: "BOOLEAN",
            exp.DataType.Type.UTINYINT: "SMALLINT",
            exp.DataType.Type.USMALLINT: "INT",
            exp.DataType.Type.UMEDIUMINT: "INT",
            exp.DataType.Type.UINT: "BIGINT",
            exp.DataType.Type.UBIGINT: "LARGEINT",
            exp.DataType.Type.MEDIUMINT: "INT",
            exp.DataType.Type.YEAR: "SMALLINT",
            exp.DataType.Type.DATE32: "DATE",
            exp.DataType.Type.INT128: "LARGEINT",
            exp.DataType.Type.DATE: "DATE",
            exp.DataType.Type.UNKNOWN: "STRING",
            exp.DataType.Type.TINYINT: "TINYINT",
            exp.DataType.Type.SMALLINT: "SMALLINT",
            exp.DataType.Type.INT: "INT",
            exp.DataType.Type.BIGINT: "BIGINT",
            exp.DataType.Type.JSON: "JSON",
            exp.DataType.Type.BOOLEAN: "BOOLEAN",
            exp.DataType.Type.FLOAT: "FLOAT",
            exp.DataType.Type.DOUBLE: "DOUBLE",
            exp.DataType.Type.SERIAL: "INT",
            exp.DataType.Type.BIGSERIAL: "BIGINT",
            exp.DataType.Type.MULTI_DIMENSIONAL_ARRAY: "ARRAY",
            exp.DataType.Type.INTERVAL_DATETIME: "BIGINT",
        }

        # Type correspondence between clickhouse and doris, used for STRUCT type adaptation
        CLICKHOUSE_TYPE_MAPPING = {
            "int8": "TINYINT",
            "int16": "SMALLINT",
            "int32": "INT",
            "int64": "BIGINT",
            "int128": "LARGEINT",
            "int256": "STRING",
            "uint8": "SMALLINT",
            "uint16": "INT",
            "uint32": "BIGINT",
            "uint64": "LARGEINT",
            "uint128": "STRING",
            "uint256": "STRING",
            "date32": "DATE",
            "datetime64": "DATETIME",
            "float32": "FLOAT",
            "float64": "DOUBLE",
            "enum": "STRING",
            "enum8": "STRING",
            "enum16": "STRING",
            "ipv4": "STRING",
            "ipv6": "STRING",
        }

        CLICKHOUSE_NOT_SUPPORT_TYPE = [
            exp.DataType.Type.AGGREGATEFUNCTION,
            exp.DataType.Type.SIMPLEAGGREGATEFUNCTION,
            # exp.DataType.Type.LOWCARDINALITY,
            # exp.DataType.Type.FIXEDSTRING,
            exp.DataType.Type.NESTED,
        ]

        DORIS_SURROPT_PROPERTIES = [
            "dynamic_partition.enable",
            "dynamic_partition.time_unit",
            "dynamic_partition.prefix",
            "dynamic_partition.end",
            "replication_allocation",
        ]

        LIST_PARTITION_TYPE = [
            exp.DataType.Type.TIMESTAMP,
            exp.DataType.Type.TIMESTAMPTZ,
            exp.DataType.Type.BIT,
            exp.DataType.Type.UTINYINT,
            exp.DataType.Type.USMALLINT,
            exp.DataType.Type.UMEDIUMINT,
            exp.DataType.Type.UINT,
            exp.DataType.Type.UBIGINT,
            exp.DataType.Type.MEDIUMINT,
            exp.DataType.Type.YEAR,
            exp.DataType.Type.DATE32,
            exp.DataType.Type.INT128,
            exp.DataType.Type.DATE,
            exp.DataType.Type.UNKNOWN,
            exp.DataType.Type.TINYINT,
            exp.DataType.Type.SMALLINT,
            exp.DataType.Type.INT,
            exp.DataType.Type.BIGINT,
            exp.DataType.Type.SERIAL,
            exp.DataType.Type.BIGSERIAL,
            exp.DataType.Type.BOOLEAN,
            exp.DataType.Type.CHAR,
            exp.DataType.Type.TEXT,
            exp.DataType.Type.VARCHAR,
        ]

        POSTGRES_NOT_SUPPORT_TYPE = [
            exp.DataType.Type.NUMRANGE,
            exp.DataType.Type.TSRANGE,
            exp.DataType.Type.TSTZRANGE,
            exp.DataType.Type.DATERANGE,
            exp.DataType.Type.INT4RANGE,
            exp.DataType.Type.INT8RANGE,
        ]
        CAST_MAPPING = {}
        TIMESTAMP_FUNC_TYPES = set()

        PROPERTIES_LOCATION = {
            **MySQL.Generator.PROPERTIES_LOCATION,
            exp.PartitionedByProperty: exp.Properties.Location.UNSUPPORTED,
            exp.WithDataProperty: exp.Properties.Location.UNSUPPORTED,
            exp.EngineProperty: exp.Properties.Location.UNSUPPORTED,
            exp.AutoIncrementProperty: exp.Properties.Location.UNSUPPORTED,
            exp.CharacterSetProperty: exp.Properties.Location.UNSUPPORTED,
            exp.CollateProperty: exp.Properties.Location.UNSUPPORTED,
            exp.SchemaCommentProperty: exp.Properties.Location.UNSUPPORTED,
            exp.Order: exp.Properties.Location.UNSUPPORTED,
            exp.MergeTreeTTL: exp.Properties.Location.UNSUPPORTED,
            exp.SettingsProperty: exp.Properties.Location.UNSUPPORTED,
            exp.FileFormatProperty: exp.Properties.Location.UNSUPPORTED,
            exp.RowFormatDelimitedProperty: exp.Properties.Location.UNSUPPORTED,
            exp.ClusteredByProperty: exp.Properties.Location.UNSUPPORTED,
            exp.PrimaryKey: exp.Properties.Location.UNSUPPORTED,
            exp.UniqueKey: exp.Properties.Location.POST_SCHEMA,
            exp.DuplicateKey: exp.Properties.Location.POST_SCHEMA,
            exp.DistributedByHash: exp.Properties.Location.POST_SCHEMA,
            exp.LocationProperty: exp.Properties.Location.UNSUPPORTED,
            exp.RowFormatSerdeProperty: exp.Properties.Location.UNSUPPORTED,
            exp.SerdeProperties: exp.Properties.Location.UNSUPPORTED,
            exp.SetProperty: exp.Properties.Location.UNSUPPORTED,
            exp.NoPrimaryIndexProperty: exp.Properties.Location.UNSUPPORTED,
            exp.SegmentCreation: exp.Properties.Location.UNSUPPORTED,
            exp.Pctfree: exp.Properties.Location.UNSUPPORTED,
            exp.Pctused: exp.Properties.Location.UNSUPPORTED,
            exp.Initrans: exp.Properties.Location.UNSUPPORTED,
            exp.Maxtrans: exp.Properties.Location.UNSUPPORTED,
            exp.NoCompress: exp.Properties.Location.UNSUPPORTED,
            exp.Logging: exp.Properties.Location.UNSUPPORTED,
            exp.Storage: exp.Properties.Location.UNSUPPORTED,
            exp.Tablespace: exp.Properties.Location.UNSUPPORTED,
            exp.EnableRowMovement: exp.Properties.Location.UNSUPPORTED,
            exp.DisableRowMovement: exp.Properties.Location.UNSUPPORTED,
        }

        TRANSFORMS = {
            **MySQL.Generator.TRANSFORMS,
            exp.AddMonths: rename_func("MONTHS_ADD"),
            exp.AtTimeZone: attimezone_sql,
            exp.ApproxDistinct: approx_count_distinct_sql,
            exp.ApproxQuantile: rename_func("PERCENTILE_APPROX"),
            exp.ArgMax: rename_func("MAX_BY"),
            exp.ArgMin: rename_func("MIN_BY"),
            exp.ArrayAgg: rename_func("COLLECT_LIST"),
            exp.ArrayFilter: handle_array_filter,
            exp.ArrayUniq: lambda self, e: f"SIZE(ARRAY_DISTINCT({self.sql(e, 'this')}))",
            exp.ArrayOverlaps: rename_func("ARRAYS_OVERLAP"),
            exp.ArrayPosition: rename_func("ARRAY_POSITION"),
            exp.ArrayElement: rename_func("ELEMENT_AT"),
            exp.ArrayReverse: rename_func("ARRAY_REVERSE_SORT"),
            exp.ArrayStringConcat: handle_array_concat,
            exp.ArrayToString: handle_array_to_string,
            exp.ArrayUniqueAgg: rename_func("COLLECT_SET"),
            exp.AssertTrue: lambda self, e: self.func("IF", self.sql(e, "this"), "True", "Null"),
            exp.BitwiseAnd: rename_func("BITAND"),
            exp.BitwiseAndAgg: rename_func("GROUP_BIT_AND"),
            exp.BitwiseLeftShift: rename_func("BIT_SHIFT_LEFT"),
            exp.BitwiseRightShift: rename_func("BIT_SHIFT_RIGHT"),
            exp.BitwiseNot: rename_func("BITNOT"),
            exp.BitwiseOr: rename_func("BITOR"),
            exp.BitwiseOrAgg: rename_func("GROUP_BIT_OR"),
            exp.BitwiseXor: rename_func("BITXOR"),
            exp.BitmapXOrCount: rename_func("BITMAP_XOR_COUNT"),
            exp.CastToStrType: lambda self,
            e: f"CAST({self.sql(e, 'this')} AS {self.sql(e, 'to')})",
            exp.ConcatWs: handle_concat_ws,
            exp.CountDistinct: lambda self, e: f"COUNT(DISTINCT({self.sql(e, 'this')}))",
            exp.CountIf: count_if_to_sum,
            exp.CurrentDate: no_paren_current_date_sql,
            exp.CurrentTimestamp: lambda self, e: f"NOW({self.sql(e, 'this')})",
            exp.ConvertTz: lambda self,
            e: f"TO_DATE(CONVERT_TZ({self.sql(e, 'this')},'Asia/Shanghai',{self.sql(e, 'to_tz')}))",
            exp.Cot: lambda self, e: f"COS({self.sql(e, 'this')})/SIN({self.sql(e, 'this')})",
            exp.Decrypt: lambda self,
            e: f"AES_DECRYPT({self.sql(e, 'expression')},{self.sql(e, 'key')},{self.sql(e, 'iv')})",
            exp.DateDiff: handle_date_diff,
            exp.DPipe: lambda self, e: f"CONCAT({self.sql(e, 'this')},{self.sql(e, 'expression')})",
            exp.DateTrunc: handle_date_trunc,
            exp.DayOfWeek: dayofweeksql,
            exp.DateAdd: _remove_ts_or_ds_to_date(date_add_sql("ADD")),
            exp.DateSub: _remove_ts_or_ds_to_date(date_add_sql("SUB")),
            exp.Empty: rename_func("NULL_OR_EMPTY"),
            exp.Encrypt: lambda self,
            e: f"AES_ENCRYPT({self.sql(e, 'expression')},{self.sql(e, 'key')},{self.sql(e, 'iv')})",
            exp.Final: lambda self, e: f"{self.sql(e, 'this')}",
            exp.Filter: handle_filter,
            exp.GenerateSeries: handle_range,
            exp.GroupConcat: _string_agg_sql,
            exp.GroupBitMap: lambda self, e: f"BITMAP_COUNT(TO_BITMAP({self.sql(e, 'this')}))",
            exp.GroupBitMapState: lambda self, e: f"BITMAP_UNION(TO_BITMAP({self.sql(e, 'this')}))",
            exp.GroupBitMapOrState: rename_func("BITMAP_UNION"),
            exp.GroupBitMapOrStateOrDefault: lambda self,
            e: f"IFNULL(BITMAP_UNION({self.sql(e, 'this')}), BITMAP_EMPTY())",
            exp.HasAny: rename_func("ARRAYS_OVERLAP"),
            exp.Hex: lambda self, e: f"LOWER(HEX({self.sql(e, 'this')}))",
            exp.IsNotNull: rename_func("NOT_NULL_OR_EMPTY"),
            exp.JSONArrayAgg: rename_func("COLLECT_LIST"),
            exp.JSONExtractScalar: _json_extract_sql,
            exp.JSONExtract: _json_extract_sql,
            exp.JSONBExtract: _json_extract_sql,
            exp.JSONBExtractScalar: _json_extract_sql,
            exp.JSONArrayContains: rename_func("JSON_CONTAINS"),
            exp.ParseJSON: lambda self, e: self.func(
                "JSON_PARSE_ERROR_TO_NULL" if e.args.get("safe") else "JSON_PARSE", e.this
            ),
            exp.JsonArrayLength: rename_func("JSON_LENGTH"),
            exp.Log: handle_log,
            exp.LTrim: rename_func("LTRIM_IN"),
            exp.Length: rename_func("CHAR_LENGTH"),
            exp.LengthB: rename_func("LENGTH"),
            exp.Lead: _lag_lead_sql,
            exp.Lag: _lag_lead_sql,
            exp.Map: rename_func("ARRAY_MAP"),
            exp.Min: rename_func("MIN"),
            exp.MonthsBetween: rename_func("MONTHS_DIFF"),
            exp.MD5Digest: rename_func("MD5"),
            exp.NotEmpty: rename_func("NOT_NULL_OR_EMPTY"),
            exp.NumbersTable: lambda self,
            e: f"NUMBERS('{self.sql('number')}' = '{self.sql(e, 'this')}')",
            exp.QuartersAdd: lambda self,
            e: f"MONTHS_ADD({self.sql(e, 'this')},{3 * int(self.sql(e, 'expression'))})",
            exp.QuartersSub: lambda self,
            e: f"MONTHS_SUB({self.sql(e, 'this')},{3 * int(self.sql(e, 'expression'))})",
            exp.Rand: handle_rand,
            exp.RegexpLike: rename_func("REGEXP"),
            exp.RegexpExtract: handle_regexp_extract,
            exp.RegexpExtractAll: handle_regexp_extract,
            exp.RegexpSplit: rename_func("SPLIT_BY_STRING"),
            exp.Replace: handle_replace,
            exp.ReplaceEmpty: handle_replace,
            exp.RTrim: rename_func("RTRIM_IN"),
            exp.StringToArray: rename_func("SPLIT_BY_STRING"),
            exp.SchemaCommentProperty: lambda self, e: self.naked_property(e),
            exp.SHA2: lambda self, e: f"SHA2({self.sql(e, 'this')},{self.sql(e, 'length')})",
            exp.Shuffle: rename_func("ARRAY_SHUFFLE"),
            exp.Slice: rename_func("ARRAY_SLICE"),
            exp.SortArray: rename_func("ARRAY_SORT"),
            exp.Split: rename_func("SPLIT_BY_STRING"),
            exp.StAstext: handle_geography,
            exp.StrPosition: lambda self, e: (
                f"LOCATE({self.sql(e, 'substr')}, {self.sql(e, 'this')}, {self.sql(e, 'position')})"
                if self.sql(e, "position")
                else f"LOCATE({self.sql(e, 'substr')}, {self.sql(e, 'this')})"
            ),
            exp.StrToUnix: _str_to_unix_sql,
            exp.StrToDate: handle_to_date,
            exp.StrToTime: handle_to_date,
            exp.TimeRound: toStartOfInterval,
            exp.TimestampTrunc: timestamptrunc_sql,
            exp.TimeStrToDate: rename_func("TO_DATE"),
            exp.TimeStrToUnix: rename_func("UNIX_TIMESTAMP"),
            exp.TimeToUnix: rename_func("UNIX_TIMESTAMP"),
            exp.TimeToStr: handle_to_date,
            exp.Trim: _trim_sql,
            exp.ToChar: handle_to_char,
            exp.Today: lambda self, e: "TO_DATE(NOW())",
            exp.ToStartOfDay: lambda self, e: f"DATE_TRUNC({self.sql(e, 'this')}, 'Day')",
            exp.ToStartOfHour: lambda self, e: f"DATE_TRUNC({self.sql(e, 'this')}, 'Hour')",
            exp.ToStartOfMinute: lambda self, e: f"DATE_TRUNC({self.sql(e, 'this')}, 'Minute')",
            exp.ToStartOfMonth: lambda self, e: f"DATE_TRUNC({self.sql(e, 'this')}, 'Month')",
            exp.ToStartOfQuarter: lambda self, e: f"DATE_TRUNC({self.sql(e, 'this')}, 'Quarter')",
            exp.ToStartOfSecond: lambda self, e: f"DATE_TRUNC({self.sql(e, 'this')}, 'Second')",
            exp.ToStartOfWeek: lambda self, e: f"DATE_TRUNC({self.sql(e, 'this')}, 'Week')",
            exp.ToStartOfYear: lambda self, e: f"DATE_TRUNC({self.sql(e, 'this')}, 'Year')",
            exp.ToYyyymm: lambda self, e: f"DATE_FORMAT({self.sql(e, 'this')}, '%Y%m')",
            exp.ToYyyymmdd: lambda self, e: f"DATE_FORMAT({self.sql(e, 'this')}, '%Y%m%d')",
            exp.ToYyyymmddhhmmss: lambda self,
            e: f"DATE_FORMAT({self.sql(e, 'this')}, '%Y%m%d%H%i%s')",
            # Only for day level
            exp.TsOrDsAdd: lambda self,
            e: f"DATE_ADD({self.sql(e, 'this')}, {self.sql(e, 'expression')})",
            exp.TsOrDsToDate: handle_to_date,
            exp.UniqCombined: lambda self, e: f"HLL_CARDINALITY(HLL_HASH({self.sql(e, 'this')}))",
            exp.UnixToStr: lambda self, e: self.func(
                "FROM_UNIXTIME", e.this, time_format("doris")(self, e)
            ),
            exp.UnixToTime: rename_func("FROM_UNIXTIME"),
            exp.Unnest: unnest_sql,
            exp.Variance: rename_func("VAR_SAMP"),
            exp.Select: transforms.preprocess(
                [
                    presto_cte_table_alias_rewrite,
                    transforms.presto_join_rewrite,
                    transforms.subquery_alias,
                    transforms.replace_with_aliases,
                    transforms.eliminate_distinct_on,
                    transforms.eliminate_semi_and_anti_joins,
                    transforms.replace_column_clickhouse,
                    transforms.array_join_rewrite,
                ]
            ),
            exp.ExtractUrlParameter: presto_doris_extract_url_parameter,
            exp.Codepoint: presto_codepoint_doris_ascii,
            exp.YesterDay: lambda self, e: "DATE_SUB(TO_DATE(NOW()) ,INTERVAL 1 DAY)",
            exp.CountEqual: clickhouse_countequal_to_doris,
            exp.JsonExists: json_exists_to_doris,
            exp.Left: rename_func("STRLEFT"),
            exp.OrReplace: handle_replace,
            exp.Median: lambda self, e: "The value cannot be empty."
            if self.sql(e, "this") is None
            else f"PERCENTILE({self.sql(e, 'this')},0.5)",
        }

        def join_sql(self, expression: exp.Join) -> str:
            if isinstance(expression.this, exp.Unnest):
                return f" LATERAL VIEW {self.sql(expression.this)}"
            return super().join_sql(expression)

        def ordered_sql(self, expression: exp.Ordered) -> str:
            desc = expression.args.get("desc")
            asc = not desc

            nulls_first = expression.args.get("nulls_first")
            nulls_last = not nulls_first
            nulls_are_large = self.dialect.NULL_ORDERING == "nulls_are_large"
            nulls_are_small = self.dialect.NULL_ORDERING == "nulls_are_small"
            nulls_are_last = self.dialect.NULL_ORDERING == "nulls_are_last"

            this = self.sql(expression, "this")

            sort_order = " DESC" if desc else (" ASC" if desc is False else "")
            nulls_sort_change = " NULLS FIRST" if nulls_first else " NULLS LAST"
            if nulls_first and (
                (asc and nulls_are_large) or (desc and nulls_are_small) or nulls_are_last
            ):
                nulls_sort_change = " NULLS FIRST"
            elif (
                nulls_last
                and ((asc and nulls_are_small) or (desc and nulls_are_large))
                and not nulls_are_last
            ):
                nulls_sort_change = " NULLS LAST"
            with_fill = self.sql(expression, "with_fill")
            with_fill = f" {with_fill}" if with_fill else ""

            return f"{this}{sort_order}{nulls_sort_change}{with_fill}"

        def anonymousaggfunc_sql(self, expression: exp.AnonymousAggFunc) -> str:
            return self.func(expression.name, *expression.expressions)

        def combinedaggfunc_sql(self, expression: exp.CombinedAggFunc) -> str:
            part = expression.args.get("parts")
            function_name = "_".join(part).lower() if part is not None else []
            return f"{function_name}({self.sql(expression.expressions[0], 'this')})"

        def parameter_sql(self, expression: exp.Parameter) -> str:
            this = self.sql(expression, "this")
            expression_sql = self.sql(expression, "expression")

            parent = expression.parent
            this = f"{this}:{expression_sql}" if expression_sql else this

            if isinstance(parent, exp.EQ) and isinstance(parent.parent, exp.SetItem):
                # We need to produce SET key = value instead of SET ${key} = value
                return this

            return f"${{{this}}}"

        def if_sql(self, expression: exp.If) -> str:
            this = self.sql(expression, "this")
            true = self.sql(expression, "true")
            false = self.sql(expression, "false") or "NULL"
            return f"IF({this}, {true}, {false})"

        def explain_sql(self, expression: exp.Explain) -> str:
            this = self.sql(expression, "this")
            expr = self.sql(expression, "expressions")
            return f"{this} {expr}"

        def matchany_sql(self, expression: exp.MatchAny) -> str:
            return self.binary(expression, "MATCH_ANY")

        def matchall_sql(self, expression: exp.MatchAll) -> str:
            return self.binary(expression, "MATCH_ALL")

        def matchphrase_sql(self, expression: exp.MatchPhrase) -> str:
            return self.binary(expression, "MATCH_PHRASE")

        def uniquekey_sql(self, expression: exp.UniqueKey):
            expressions = self.expressions(expression, flat=True)
            options = self.expressions(expression, key="options", flat=True, sep=" ")
            options = f" {options}" if options else ""
            return f"UNIQUE KEY ({expressions}){options}"

        def duplicatekey_sql(self, expression: exp.DuplicateKey):
            expressions = self.expressions(expression, flat=True)
            options = self.expressions(expression, key="options", flat=True, sep=" ")
            options = f" {options}" if options else ""
            return f"DUPLICATE KEY ({expressions}){options}"

        def distributedbyhash_sql(self, expression: exp.DistributedByHash):
            expressions = self.expressions(expression, flat=True)
            options = self.expressions(expression, key="options", flat=True, sep=" ")
            options = f" {options}" if options else ""
            return f"DISTRIBUTED BY HASH ({expressions}){options}"

        def property_name(self, expression: exp.Property, string_key: bool = False) -> str:
            return super().property_name(expression, True)

        def with_properties(self, properties: exp.Properties) -> str:
            return self.properties(properties, prefix=self.seg("PROPERTIES", sep=""))

        def properties(
            self,
            properties: exp.Properties,
            prefix: str = "",
            sep: str = ", ",
            suffix: str = "",
            wrapped: bool = True,
        ) -> str:
            remove_prop = []
            for prop in properties.expressions:
                if (
                    prop.this
                    and prop.this.this
                    and str(prop.this.this).lower() not in self.DORIS_SURROPT_PROPERTIES
                ):
                    remove_prop.append(prop)
            for prop in remove_prop:
                properties.expressions.remove(prop)
            return super().properties(properties, prefix, sep, suffix, wrapped)

        def in_sql(self, expression: exp.In) -> str:
            query = expression.args.get("query")
            unnest = expression.args.get("unnest")
            field = expression.args.get("field")
            # doris does not support global in
            # is_global = " GLOBAL" if expression.args.get("is_global") else ""

            if query:
                in_sql = self.wrap(self.sql(query))
            elif unnest:
                in_sql = self.in_unnest_op(unnest)
            elif field:
                in_sql = self.sql(field)
            else:
                in_sql = f"({self.expressions(expression, flat=True)})"

            return f"{self.sql(expression, 'this')} IN {in_sql}"

        def withingroup_sql(self, expression):
            this = self.sql(expression, "this")
            if isinstance(expression.this, exp.ListAgg):
                expr = self.sql(expression, "expression")[1:]
                return f"GROUP_CONCAT({expression.args['this'].this},{expression.args['this'].expression} {expr})"
            if isinstance(expression.this, exp.PercentileCont):
                pvaluete = self.sql(expression.this, "this")
                if expression.args.get("expression").find(exp.Order):  # have you found the order by
                    epvalues = expression.args.get("expression").find(exp.Column).alias_or_name
                    return f"PERCENTILE({epvalues},{pvaluete})"
            expression = self.sql(expression, "expression")[1:]  # order has a leading space
            return f"{this} WITHIN GROUP ({expression})"

        def group_sql(self, expression: exp.Group) -> str:
            group_by_all = expression.args.get("all")
            if group_by_all is True:
                modifier = " ALL"
            elif group_by_all is False:
                modifier = " DISTINCT"
            else:
                modifier = ""

            group_by = self.op_expressions(f"GROUP BY{modifier}", expression)

            grouping_sets = self.expressions(expression, key="grouping_sets")
            cube = self.expressions(expression, key="cube")
            rollup = self.expressions(expression, key="rollup")
            # Currently, Doris does not support the syntax of group by k1, rollup(k1,k2).
            # replaced by group by grouping sets((k1),(k1,k1),(k1,k1,k2)).
            # Doris will support it in the future and cancel this conversion.
            if expression.args.get("rollup") and expression.args.get("expressions"):
                # Extract rollup expressions and group expressions
                rollup_expr = expression.args.get("rollup")
                rollup_set = (
                    [i.alias_or_name for i in rollup_expr[0].expressions]
                    if rollup_expr
                    and isinstance(rollup_expr, list)
                    and rollup_expr
                    and hasattr(rollup_expr[0], "expressions")
                    else []
                )
                group_expr = expression.args.get("expressions")
                group_set = (
                    [i.alias_or_name for i in group_expr]
                    if group_expr and isinstance(group_expr, list)
                    else []
                )
                # Generate prefix subsets of the rollup set
                subsets = [rollup_set[:i] for i in range(len(rollup_set) + 1)]
                # Combine group set with each prefix subset of the rollup set
                grouping_set = [group_set + subset for subset in subsets]
                # Generate the final GROUPING SETS string, removing quotes
                grouping_str = ", ".join(f'({", ".join(subset)})' for subset in grouping_set)
                return f" GROUP BY GROUPING SETS ({grouping_str})"

            groupings = csv(
                self.seg(grouping_sets) if grouping_sets else "",
                self.seg(cube) if cube else "",
                self.seg(rollup) if rollup else "",
                self.seg("WITH TOTALS") if expression.args.get("totals") else "",
                sep=self.GROUPINGS_SEP,
            )

            if (
                expression.expressions
                and groupings
                and groupings.strip() not in ("WITH CUBE", "WITH ROLLUP")
            ):
                group_by = f"{group_by}{self.GROUPINGS_SEP}"

            return f"{group_by}{groupings}"

        def from_sql(self, expression: exp.From) -> str:
            if expression.this.this == "dual":
                return ""
            return f"{self.seg('FROM')} {self.sql(expression, 'this')}"

        def datatype_sql(self, expression: exp.DataType) -> str:
            root_expression: exp.Expression = expression
            while root_expression.parent is not None:
                root_expression = root_expression.parent

            # Only perform type conversion on create table statements
            if (
                not isinstance(root_expression, exp.Create)
                or not root_expression.args["kind"] == "TABLE"
            ):
                return generator.Generator.datatype_sql(self, expression)

            if expression.this in self.STRING_TYPE_MAPPING:
                return "STRING"
            elif expression.is_type(exp.DataType.Type.TIME):
                return "STRING"
            elif expression.is_type(exp.DataType.Type.UDECIMAL):
                precision_expression = expression.find(exp.DataTypeParam)
                if precision_expression:
                    # If p + 1 > 38, type STRING will be used
                    precision = int(precision_expression.name) + 1
                    if precision <= 38:
                        precision_expression.this.set("this", precision)
                    else:
                        return "STRING"
            elif expression.is_type(exp.DataType.Type.CHAR):
                size_expression = expression.find(exp.DataTypeParam)
                if size_expression:
                    size = int(size_expression.name)
                    return "STRING" if size * 3 > 255 else f"CHAR({size * 3})"
            elif expression.is_type(exp.DataType.Type.VARCHAR):
                size_expression = expression.find(exp.DataTypeParam)
                if size_expression:
                    size = int(size_expression.name)
                    return "STRING" if size * 3 > 65533 else f"VARCHAR({size * 3})"
            elif expression.is_type(exp.DataType.Type.BIT):
                size_expression = expression.find(exp.DataTypeParam)
                if size_expression:
                    size = int(size_expression.name)
                    return "BOOLEAN" if size == 1 else "STRING"
            elif expression.is_type(
                exp.DataType.Type.DATETIME,
                exp.DataType.Type.TIMESTAMP,
                exp.DataType.Type.DATETIME64,
            ):
                size_expression = expression.find(exp.DataTypeParam)
                if size_expression:
                    size = int(size_expression.name)
                    precision = 6 if size > 6 else size
                    return f"DATETIME({precision})"
                else:
                    return "DATETIME"

            dialect = root_expression.args["dialect"]
            if dialect in ("HIVE", "SPARK"):
                return self.hive_type_to_doris(expression)
            elif dialect == "CLICKHOUSE":
                return self.clickhouse_type_to_doris(expression)
            elif dialect in ("PRESTO", "TRINO"):
                return self.presto_or_trino_type_to_doris(expression)
            elif dialect == "ORACLE":
                return self.oracle_type_to_doris(expression)
            elif dialect in ("POSTGRES", "TERADATA"):
                return self.postgres_or_teradate_type_to_doris(expression)

            return generator.Generator.datatype_sql(self, expression)

        def create_sql(self, expression: exp.Create) -> str:
            root_expression: exp.Expression = expression
            # Only process create table
            if not expression.args["kind"] == "TABLE":
                return generator.Generator.create_sql(self, expression)

            # Convertor of [EXTERNAL TABLE] is not supported
            if expression.find(exp.ExternalProperty):
                raise SyntaxError("Convertor of [EXTERNAL TABLE] is not supported")

            # The 'create xxx like xxx' and 'create xxx as select xxx' statements is not processed
            if (
                expression.find(exp.LikeProperty, exp.Select)
                and root_expression.args["dialect"] != "TERADATA"
                and root_expression.args["dialect"] != "PRESTO"
            ):
                return generator.Generator.create_sql(self, expression)

            # todo Only default value for character types are supported.
            for e in expression.this.expressions:
                if isinstance(e, exp.ColumnDef) and e.kind:
                    if e.kind.is_type(
                        exp.DataType.Type.VARCHAR, exp.DataType.Type.TEXT, exp.DataType.Type.CHAR
                    ):
                        for constraint in e.constraints:
                            if isinstance(constraint.kind, exp.DefaultColumnConstraint):
                                constraint.kind.this.set("is_string", True)
                                break
                    else:
                        default = None
                        computed_constraint = None
                        for constraint in e.constraints:
                            if isinstance(constraint, exp.ComputedColumnConstraint):
                                computed_constraint = constraint
                            elif constraint and isinstance(
                                constraint.kind, exp.DefaultColumnConstraint
                            ):
                                default = constraint
                        if computed_constraint:
                            e.constraints.remove(computed_constraint)
                        if default:
                            e.constraints.remove(default)

            # If only one column and it is map, struct, or array type, need to add an auto-increment column
            if len(expression.this.expressions) == 1:
                col = expression.this.expressions[0]
                if (
                    isinstance(col, exp.ColumnDef)
                    and col.kind
                    and col.kind.is_type(
                        exp.DataType.Type.STRUCT,
                        exp.DataType.Type.ARRAY,
                        exp.DataType.Type.MAP,
                        exp.DataType.Type.JSON,
                        exp.DataType.Type.JSONB,
                        exp.DataType.Type.VARIANT,
                    )
                ):
                    this = exp.Identifier(this="doris_col_1", quoted=False)
                    kind = exp.DataType(this=exp.DataType.Type.BIGINT, nested=False)
                    constraints = [
                        exp.ColumnConstraint(kind=exp.NotNullColumnConstraint()),
                        exp.ColumnConstraint(kind=exp.AutoIncrementColumnConstraint()),
                    ]
                    expression.this.expressions.insert(
                        0, exp.ColumnDef(this=this, kind=kind, constraints=constraints)
                    )

            dialect = expression.args["dialect"]
            if dialect in ("MYSQL", "ORACLE"):
                return self.create_mysql_or_oracle_sql(expression)
            elif dialect == "CLICKHOUSE":
                return self.create_clickhouse_sql(expression)
            elif dialect in ("HIVE", "PRESTO", "SPARK", "TRINO"):
                return self.create_hive_or_presto_or_trino_or_spark_sql(expression)
            elif dialect in ("POSTGRES", "TERADATA"):
                return self.create_postgres_or_teradata_sql(expression)
            return generator.Generator.create_sql(self, expression)

        def createable_sql(self, expression: exp.Create, locations: t.DefaultDict) -> str:
            # Remove table-level constraints that doris does not support

            remove_list = []
            expressions = expression.this.expressions
            expression_index = expression.args.get("indexes")
            for e in expressions:
                if (
                    isinstance(e, exp.PrimaryKey)
                    or isinstance(e, exp.IndexColumnConstraint)
                    or isinstance(e, exp.UniqueColumnConstraint)
                    or isinstance(e, exp.ForeignKey)
                    or isinstance(e, exp.Constraint)
                    or isinstance(e, exp.SupplementalLogConstraint)
                ):
                    remove_list.append(e)
            for e in remove_list:
                expressions.remove(e)
            if expression_index:
                expression_index.clear()

            createable_sql = super().createable_sql(expression, locations)

            return createable_sql

        def oracle_type_to_doris(self, expression: exp.DataType) -> str:
            if expression.is_type(exp.DataType.Type.DATE):
                size_expression = expression.find(exp.DataTypeParam)
                if size_expression:
                    size = int(size_expression.name)
                    precision = 6 if size > 6 else size
                    return f"DATETIME({precision})"
                else:
                    return "DATETIME"
            elif expression.is_type(exp.DataType.Type.FLOAT):
                expression.set("this", exp.DataType.Type.DOUBLE)
            elif expression.this == exp.DataType.Type.USERDEFINED and expression.parent:
                raise TypeError(
                    f"UNSUPPORTED TYPE: {expression.parent.name} {expression.args['kind']}"
                )

            return generator.Generator.datatype_sql(self, expression)

        def clickhouse_type_to_doris(self, expression: exp.DataType) -> str:
            if expression.this in self.CLICKHOUSE_NOT_SUPPORT_TYPE and expression.parent:
                raise TypeError(
                    f"UNSUPPORTED TYPE: {expression.parent.name} {expression.this.name}"
                )
            elif expression.is_type(exp.DataType.Type.LOWCARDINALITY):
                # clickhouse has Nullable(xxx) type, doris takes xxx as the type
                return self.datatype_sql(expression.expressions[0])
            elif expression.is_type(exp.DataType.Type.STRUCT):
                # The STRUCT type of clickhouse is STRUCT<String, String, Int>, while doris needs to be STRUCT<cnt_1:String,cnt_2:String,cnt_3:Int>, which needs to be converted.
                col_list = []
                for index, col in enumerate(expression.expressions, start=1):
                    st_type = self.datatype_sql(col)
                    col_list.append(f"col_{index}: {st_type}")
                cols = ", ".join(col_list)
                return f"STRUCT<{cols}>"
            elif expression.is_type(exp.DataType.Type.FIXEDSTRING):
                size_expression = expression.find(exp.DataTypeParam)
                if size_expression:
                    size = int(size_expression.name)
                    if size > 255 or size < 1:
                        raise TypeError(
                            f"[FIXEDSTRING] will be converted to [CHAR], but [{expression.parent.__str__()}] size: {size} not in [1, 255]"
                        )
                    return f"CHAR({size})"

            return generator.Generator.datatype_sql(self, expression)

        def hive_type_to_doris(self, expression: exp.DataType) -> str:
            if expression.is_type(expression.Type.STRUCT):
                # The STRUCT type of hive is STRUCT<tet1 STRING, test2 INT>, while the one read by doris is STRUCT<tet1:STRING, test2:INT>, which needs to be converted.
                col_list = []
                for col in expression.expressions:
                    st_type = self.datatype_sql(col.args["kind"])
                    col_list.append(f"{col.name}:{st_type}")
                cols = ", ".join(col_list)
                return f"STRUCT<{cols}>"

            return generator.Generator.datatype_sql(self, expression)

        def presto_or_trino_type_to_doris(self, expression: exp.DataType) -> str:
            if expression.is_type(expression.Type.STRUCT):
                # The STRUCT type of presto is STRUCT(tet1 STRING, test2 INT), while the type of doris is STRUCT<tet1:STRING, test2:INT>, which needs to be converted.
                col_list = []
                for col in expression.expressions:
                    st_type = self.datatype_sql(col.args["kind"])
                    col_list.append(f"{col.name}:{st_type}")
                cols = ", ".join(col_list)
                return f"STRUCT<{cols}>"
            elif isinstance(expression.this, exp.Interval):
                return "STRING"

            return generator.Generator.datatype_sql(self, expression)

        def postgres_or_teradate_type_to_doris(self, expression: exp.DataType) -> str:
            if expression.this in self.POSTGRES_NOT_SUPPORT_TYPE:
                raise TypeError(f"UNSUPPORTED TYPE: {expression.this.name}")
            elif expression.is_type(expression.Type.SMALLSERIAL):
                return "BIGINT NOT NULL AUTO_INCREMENT"
            elif expression.is_type(expression.Type.PERIOD):
                se_datetime = self.datatype_sql(expression.expressions[0])
                if se_datetime is None:
                    raise TypeError(f"{se_datetime}：The data type cannot be empty")
                return f"{se_datetime}"
            return generator.Generator.datatype_sql(self, expression)

        def create_mysql_or_oracle_sql(self, expression: exp.Create) -> str:
            notnull = exp.ColumnConstraint(kind=exp.NotNullColumnConstraint())
            key_list = []
            col_def_list = []
            expressions = expression.this.expressions
            for e in expressions:
                if isinstance(e, exp.ColumnDef):
                    col_def_list.append(e)

            # Remove unnecessary constraints information
            for column in col_def_list:
                primary_key = None
                unique = None
                check_constraint = None
                enable = None
                disable = None
                auto = None
                zero_fill = None
                for constraint in column.constraints:
                    if isinstance(constraint.kind, exp.PrimaryKeyColumnConstraint):
                        primary_key = constraint
                    elif (
                        isinstance(constraint.kind, exp.NotNullColumnConstraint) and constraint.this
                    ):
                        constraint.set("this", None)
                    elif isinstance(constraint.kind, exp.UniqueColumnConstraint):
                        unique = constraint
                    elif isinstance(constraint.kind, exp.CheckColumnConstraint):
                        check_constraint = constraint
                    elif isinstance(constraint.kind, exp.EnableConstraint):
                        enable = constraint
                    elif isinstance(constraint.kind, exp.DisableColumnConstraint):
                        disable = constraint
                    elif isinstance(constraint.kind, exp.AutoIncrementColumnConstraint):
                        auto = constraint
                    elif isinstance(constraint.kind, exp.ZeroFillConstraint):
                        zero_fill = constraint

                if primary_key:
                    if f"`{column.name}`" not in key_list:
                        key_list.append(f"`{column.name}`")
                    column.constraints.remove(primary_key)
                if unique:
                    if f"`{column.name}`" not in key_list:
                        key_list.append(f"`{column.name}`")
                    column.constraints.remove(unique)
                if check_constraint:
                    column.constraints.remove(check_constraint)
                if enable:
                    column.constraints.remove(enable)
                if disable:
                    column.set("constraints", [])
                if auto:
                    column.set("kind", exp.DataType.build("bigint"))
                    if notnull not in column.constraints:
                        column.args["constraints"].insert(0, notnull)
                if zero_fill:
                    column.constraints.remove(zero_fill)

            for pk in expression.find_all(exp.PrimaryKey):
                for e in pk:
                    if f"`{e.name}`" not in key_list:
                        key_list.append(f"`{e.name}`")
            for uni in expression.find_all(exp.UniqueColumnConstraint):
                for e in uni.this:
                    if f"`{e.name}`" not in key_list:
                        key_list.append(f"`{e.name}`")

            # Key columns should be a ordered prefix of the schema.
            for index, key in enumerate(key_list, start=0):
                for col in col_def_list:
                    if key == f"`{col.name}`":
                        expressions.remove(col)
                        expressions.insert(index, col)
                        # Replace float and double with decimal, and replace text with varchar.
                        replace_column_type(self, col)
                        break

            # Add notnull to the primary key model
            for e in expressions:
                if isinstance(e, exp.ColumnDef) and f"`{e.name}`" in key_list:
                    if notnull not in e.constraints:
                        e.args["constraints"].insert(0, notnull)

            if key_list:  # UNIQUE model
                pk_name = ", ".join(key_list)
                expression_sql = super().create_sql(expression).strip()
                return (
                    f"{expression_sql}\n"
                    f"UNIQUE KEY({pk_name})\n"
                    f"DISTRIBUTED BY HASH({pk_name}) BUCKETS AUTO\n"
                    f"PROPERTIES (\n"
                    f'    "replication_allocation" = "tag.location.default: 3"\n'
                    f")"
                )
            else:  # DUPLICATE model
                first_field_name = ""
                col_def = expression.find(exp.ColumnDef)
                if col_def:
                    # Replace float and double with decimal, and replace text with varchar.
                    replace_column_type(self, col_def)
                    first_field_name = col_def.name
                expression_sql = super().create_sql(expression).strip()
                return (
                    f"{expression_sql}\n"
                    f"DUPLICATE KEY(`{first_field_name}`)\n"
                    f"DISTRIBUTED BY HASH(`{first_field_name}`) BUCKETS AUTO\n"
                    f"PROPERTIES (\n"
                    f'    "replication_allocation" = "tag.location.default: 3"\n'
                    f")"
                )

        def create_clickhouse_sql(self, expression: exp.Create) -> str:
            col_def_list = []
            expressions = expression.this.expressions
            for e in expressions:
                if isinstance(e, exp.ColumnDef):
                    col_def_list.append(e)

            # Remove unnecessary constraints information
            for column in col_def_list:
                computed_column = None
                for constraint in column.constraints:
                    if isinstance(constraint.kind, exp.ComputedColumnConstraint):
                        computed_column = constraint
                if computed_column:
                    column.constraints.remove(computed_column)

            # process partition by
            partition_by = ""
            partition_by_property = expression.find(exp.PartitionedByProperty)
            if partition_by_property:
                partition_unit = "day"
                partition_col = partition_by_property.find(exp.Identifier)
                if isinstance(partition_by_property.this, exp.ToYyyymm):
                    partition_unit = "month"
                for col in col_def_list:
                    if (
                        partition_col
                        and col.name == partition_col.this
                        and col.kind
                        and col.kind.is_type(exp.DataType.Type.DATETIME, exp.DataType.Type.DATE)
                    ):
                        partition_by = f"AUTO PARTITION BY RANGE (date_trunc(`{col.name}`, '{partition_unit}')) ()\n"
                        if (
                            exp.ColumnConstraint(kind=exp.NotNullColumnConstraint())
                            not in col.args["constraints"]
                        ):
                            col.args["constraints"].insert(
                                0, exp.ColumnConstraint(kind=exp.NotNullColumnConstraint())
                            )
                        break

            # process order by
            dup_key_list = []
            for order in expression.find_all(exp.Order):
                order_cols = []
                for ordered in order.expressions:
                    if isinstance(ordered.this, exp.Column):
                        order_cols.append(ordered.this)
                    elif isinstance(ordered.this, exp.Tuple):
                        for e in ordered.this.expressions:
                            order_cols.append(e)
                    elif isinstance(ordered.this, exp.Paren):
                        order_cols.append(ordered.this.this)
                for index, order_col in enumerate(order_cols, start=0):
                    for col in col_def_list:
                        if order_col.name == col.name:
                            dup_key_list.append(f"`{col.name}`")
                            expressions.remove(col)
                            expressions.insert(index, col)
                            # Replace float and double with decimal, and replace text with varchar.
                            replace_column_type(self, col)
                            break

            first_field_name = ""
            col_def = expression.find(exp.ColumnDef)
            if col_def:
                # Replace float and double with decimal, and replace text with varchar.
                replace_column_type(self, col_def)
                first_field_name = col_def.name

            # process Engine Property
            distributed_by = f"DISTRIBUTED BY HASH(`{first_field_name}`) BUCKETS AUTO\n"
            for engine in expression.find_all(exp.EngineProperty):
                if engine.this.this == "Distributed" and engine.find(exp.Rand):
                    distributed_by = "DISTRIBUTED BY RANDOM BUCKETS AUTO\n"

            expression_sql = super().create_sql(expression).strip()
            dup_key = ", ".join(dup_key_list) if dup_key_list else f"`{first_field_name}`"
            return (
                f"{expression_sql}\n"
                f"DUPLICATE KEY({dup_key})\n"
                f"{partition_by}"
                f"{distributed_by}"
                f"PROPERTIES (\n"
                f'    "replication_allocation" = "tag.location.default: 3"\n'
                f")"
            )

        def create_hive_or_presto_or_trino_or_spark_sql(self, expression: exp.Create) -> str:
            dialect = expression.args["dialect"]
            # Add the columns in the hive partition to the corresponding schema
            parti_range_column = None
            partion_list_column = []
            disted_by_hash = None
            partition_by_property = expression.find(exp.PartitionedByProperty)
            if dialect == "HIVE":
                if partition_by_property:
                    # Attempt to find a DATE or DATETIME column that lacks a NOT NULL constraint and apply the constraint
                    date_or_datetime_col = next(
                        (
                            col
                            for col in partition_by_property.this.expressions
                            if self.TYPE_MAPPING.get(col.args["kind"].this) in ("DATE", "DATETIME")
                            and exp.ColumnConstraint(kind=exp.NotNullColumnConstraint())
                            not in col.args["constraints"]
                        ),
                        None,
                    )
                    if date_or_datetime_col:
                        date_or_datetime_col.args["constraints"].insert(
                            0, exp.ColumnConstraint(kind=exp.NotNullColumnConstraint())
                        )
                        parti_range_column = date_or_datetime_col.name
                    else:
                        for col in partition_by_property.this.expressions:
                            if (
                                col
                                and isinstance(col, exp.ColumnDef)
                                and col.kind
                                and col.kind.this in self.LIST_PARTITION_TYPE
                            ):
                                partion_list_column.append(f"`{col.name}`")
                                if col.kind.is_type(exp.DataType.Type.TEXT):
                                    col.kind.set("this", exp.DataType.Type.VARCHAR)
                                if (
                                    exp.ColumnConstraint(kind=exp.NotNullColumnConstraint())
                                    not in col.args["constraints"]
                                ):
                                    col.args["constraints"].insert(
                                        0, exp.ColumnConstraint(kind=exp.NotNullColumnConstraint())
                                    )
                    expression.this.expressions.extend(partition_by_property.this.expressions)
                # Simplified clustered by logic, ensure it only applies under HIVE dialect
                cluster_by_property = expression.find(exp.ClusteredByProperty)
                disted_by_hash = (
                    ", ".join(f"`{col.name}`" for col in cluster_by_property.expressions)
                    if cluster_by_property
                    else ""
                )
            if dialect in ("PRESTO", "SPARK", "TRINO"):
                # support presto ctas with properties
                if expression.find(exp.Select):
                    properties = expression.args.get("properties")
                    if properties:
                        properties_list = []
                        if properties and hasattr(properties, "expressions"):
                            for expr in properties.expressions:
                                this = expr.args["this"].this
                                value = expr.args["value"].this
                                properties_list.append(f"'{this}'='{value}'")

                        properties_sql = "PROPERTIES (\n" + ",\n".join(properties_list) + "\n)"
                        select_sql = expression.expression.sql("doris")

                        create_table_sql = f"CREATE TABLE {self.sql(expression.this)}"
                        return f"{create_table_sql}\n" f"{properties_sql}\n" f"AS {select_sql}"
                    else:
                        return generator.Generator.create_sql(self, expression)

                if partition_by_property:
                    expression_expressions = {col.name: col for col in expression.this.expressions}
                    not_null_constraint = exp.ColumnConstraint(kind=exp.NotNullColumnConstraint())
                    parti_range_column = None
                    for col in partition_by_property.this.expressions:
                        column_test = expression_expressions.get(col.this)
                        if (
                            column_test
                            and self.TYPE_MAPPING.get(
                                column_test.args["kind"].this, column_test.args["kind"].this
                            )
                            in ("DATE", "DATETIME")
                            and not_null_constraint not in column_test.args["constraints"]
                        ):
                            parti_range_column = column_test.name
                            break
                    # If a valid column has been identified, apply the NOT NULL constraint
                    if parti_range_column:
                        expression_expressions[parti_range_column].args["constraints"].insert(
                            0, not_null_constraint
                        )
                    # Add list partition
                    for col in partition_by_property.this.expressions:
                        column_test = expression_expressions.get(col.this)
                        if (
                            column_test
                            and isinstance(column_test, exp.ColumnDef)
                            and column_test.kind
                            and column_test.kind.this in self.LIST_PARTITION_TYPE
                        ):
                            partion_list_column.append(f"`{column_test.name}`")
                            if column_test.kind.is_type(exp.DataType.Type.TEXT):
                                column_test.kind.set("this", exp.DataType.Type.VARCHAR)
                            if (
                                exp.ColumnConstraint(kind=exp.NotNullColumnConstraint())
                                not in column_test.args["constraints"]
                            ):
                                column_test.args["constraints"].insert(
                                    0, exp.ColumnConstraint(kind=exp.NotNullColumnConstraint())
                                )
                disted_by_hash = ", ".join(
                    "`{}`".format(bukec_inr.this)
                    for porc in expression.find_all(exp.Property)
                    if porc.name.lower() == "bucketed_by"
                    for bukec_inr in porc.args["value"].expressions
                )

            col_def = expression.find(exp.ColumnDef)
            first_field_name = f"`{col_def.name}`" if col_def else ""
            replace_column_type(self, col_def) if col_def else None
            properties = 'PROPERTIES (\n    "replication_allocation" = "tag.location.default: 3"\n)'
            partition_str = ""
            if parti_range_column:
                partition_str = (
                    f"AUTO PARTITION BY RANGE (date_trunc(`{parti_range_column}`, 'day')) ()\n"
                )
            elif partion_list_column:
                part_str = ",".join(partion_list_column)
                partition_str = f"AUTO PARTITION BY LIST ({part_str}) ()\n"

            expression_sql = super().create_sql(expression).strip()
            return (
                f"{expression_sql}\n"
                f"DUPLICATE KEY({first_field_name})\n"
                f"{partition_str}"
                f"DISTRIBUTED BY HASH({disted_by_hash if disted_by_hash else first_field_name}) BUCKETS AUTO\n"
                f"{properties}"
            )

        def create_postgres_or_teradata_sql(self, expression: exp.Create) -> str:
            # Obtain the corresponding partition columns according to the situation
            dialect = expression.args["dialect"]
            notnull = exp.ColumnConstraint(kind=exp.NotNullColumnConstraint())
            parti_range_column = None
            parti_range_granularity = None
            model_selection = None
            parti_range_parse = None
            partion_list_column = []
            col_range = []
            col_list = []
            if dialect == "TERADATA":
                if expression.find(exp.SetProperty):
                    set_property_obj = expression.find(exp.SetProperty)
                    if isinstance(set_property_obj, exp.SetProperty):
                        model_selection = f'{set_property_obj.args.get("multi", None)}'
                if expression.find(exp.AsProperty):
                    as_property_obj = expression.find(exp.AsProperty)
                    if isinstance(as_property_obj, exp.AsProperty) and not as_property_obj.find(
                        exp.Select
                    ):
                        as_property_obj.replace(exp.LikeProperty(this=as_property_obj.this))
                        return generator.Generator.create_sql(self, expression)
                    else:
                        return generator.Generator.create_sql(self, expression)
                if expression.find(exp.RangeN):
                    range_n_obj = expression.find(exp.RangeN)
                    if isinstance(range_n_obj, exp.RangeN):
                        parti_range_parse = range_n_obj.args.get("this", None).this
                        each_arg = range_n_obj.args.get("each", None)
                    if each_arg and each_arg.unit and "this" in each_arg.unit.args:
                        parti_range_granularity = each_arg.unit.args.get("this")
                if parti_range_parse:
                    partitioned_names = parti_range_parse
                    col = next(
                        (
                            col
                            for col in expression.this.expressions
                            if col.name == partitioned_names
                            and self.TYPE_MAPPING.get(col.args["kind"].this, col.args["kind"].this)
                            in ("DATE", "DATETIME")
                        ),
                        None,
                    )
                    if col:
                        if notnull not in col.args["constraints"]:
                            col.args["constraints"].insert(0, notnull)
                        parti_range_column = col.name
                        col_range.append(col)
            if dialect == "POSTGRES":
                partitioned_by_property_result = expression.find(exp.PartitionedByProperty)
                if partitioned_by_property_result:
                    partitioned_names = [
                        col.name for col in partitioned_by_property_result.this.expressions
                    ]
                    col = next(
                        (
                            col
                            for col in expression.this.expressions
                            if col.name in partitioned_names
                            and self.TYPE_MAPPING.get(col.args["kind"].this, col.args["kind"].this)
                            in ("DATE", "DATETIME")
                        ),
                        None,
                    )
                    if col:
                        if notnull not in col.args["constraints"]:
                            col.args["constraints"].insert(0, notnull)
                        parti_range_column = col.name
                        col_range.append(col)
                    for col in expression.this.expressions:
                        if (
                            col
                            and isinstance(col, exp.ColumnDef)
                            and col.name in partitioned_names
                            and col.kind
                            and col.kind.this in self.LIST_PARTITION_TYPE
                        ):
                            partion_list_column.append(f"`{col.name}`")
                            col_list.append(col)
                            if col.kind.is_type(exp.DataType.Type.TEXT):
                                col.kind.set("this", exp.DataType.Type.VARCHAR)
                            if notnull not in col.args["constraints"]:
                                col.args["constraints"].insert(0, notnull)
            expressions = expression.this.expressions
            pg_key: list[str] = []
            col_pg_list = []
            for e in expressions:
                if isinstance(e, exp.ColumnDef):
                    if (
                        f'{e.args["kind"].this}' in ("Type.SMALLSERIAL")
                        and notnull in e.args["constraints"]
                    ):
                        e.constraints.remove(notnull)
                    col_pg_list.append(e)

            # Remove primary_key,  unique information
            def process_constraints(column, constraints_to_check, pg_key):
                constraints = [
                    constraint
                    for constraint in column.constraints
                    if isinstance(constraint.kind, constraints_to_check)
                ]
                if constraints:
                    pg_key_name = f"`{column.name}`"
                    if pg_key_name not in pg_key:
                        pg_key.append(pg_key_name)
                    replace_column_type(self, column)
                    for constraint in constraints:
                        column.constraints.remove(constraint)

            def format_constraints(column, constraints_to_check):
                constraints_df = [
                    constraint
                    for constraint in column.constraints
                    if isinstance(constraint.kind, constraints_to_check)
                ]
                if constraints_df:
                    for constraint in constraints_df:
                        column.constraints.remove(constraint)

            # Processed separately according to constraint type
            constraints_to_process = [
                (exp.PrimaryKeyColumnConstraint, pg_key),
                (exp.UniqueColumnConstraint, pg_key),
                (exp.DateFormatColumnConstraint, pg_key),
            ]
            for column in col_pg_list:
                # Remove unnecessary constraints
                remove_constraint = []
                for constraint in column.constraints:
                    if isinstance(constraint.kind, exp.CharacterSetColumnConstraint) or isinstance(
                        constraint.kind, exp.CaseSpecificColumnConstraint
                    ):
                        remove_constraint.append(constraint)
                for constraint in remove_constraint:
                    column.constraints.remove(constraint)

                for constraint_type, keys in constraints_to_process:
                    if constraint_type in (
                        exp.PrimaryKeyColumnConstraint,
                        exp.UniqueColumnConstraint,
                    ):
                        process_constraints(column, constraint_type, keys)
                    else:
                        format_constraints(column, constraint_type)
            pg_key_list = pg_key
            primary_keys = [f"`{e.name}`" for pk in expression.find_all(exp.PrimaryKey) for e in pk]
            pg_key_list.extend(x for x in primary_keys if x not in pg_key_list)
            unique_constraints = [
                f"`{e.name}`"
                for uni in expression.find_all(exp.UniqueColumnConstraint)
                for e in uni.this
            ]
            pg_key_list.extend(x for x in unique_constraints if x not in pg_key_list)

            # Output the primary key with the not null attribute
            for i in expression.this.expressions:
                if dialect == "POSTGRES":
                    if f"`{i.name}`" in pg_key_list and f'{i.args["kind"].this}' not in (
                        "Type.SMALLSERIAL"
                    ):
                        if notnull not in i.args["constraints"]:
                            i.args["constraints"].insert(0, notnull)
                elif dialect == "TERADATA":
                    if (
                        pg_key_list
                        and (model_selection == "False" or not model_selection)
                        and f"`{i.name}`" in pg_key_list
                    ):
                        if notnull not in i.args["constraints"]:
                            i.args["constraints"].insert(0, notnull)

            # If col_range exists, reverse it and merge it; if it does not exist, check col_list
            if col_range and pg_key:
                col_range_reversed = [f"`{i.name}`" for i in col_range]
                pg_key_list.extend(x for x in col_range_reversed if x not in pg_key_list)
            elif col_list and pg_key:
                col_list_reversed = [f"`{o.name}`" for o in col_list]
                pg_key_list.extend(x for x in col_list_reversed if x not in pg_key_list)
            # If you need to sort the pg_key_list in the order in the original pg_key (assuming the elements in pg_key are unique
            pg_key_ordered = sorted(
                pg_key_list, key=lambda x: pg_key.index(x) if x in pg_key else float("inf")
            )
            # A dictionary mapping column names to column objects
            col_mapping = {f"`{col.name}`": col for col in col_pg_list}
            if (
                dialect == "POSTGRES"
                or (pg_key and model_selection == "False")
                or (pg_key and dialect == "TERADATA")
            ):
                for index, key in enumerate(pg_key_ordered):
                    col = col_mapping.get(key)
                    if col:
                        expressions.remove(col)
                        expressions.insert(index, col)
                        replace_column_type(self, col)
            if not pg_key and model_selection == "False" and col_range:
                for index, key in enumerate(f"`{i.name}`" for i in col_range):
                    col = col_mapping.get(key)
                    if col:
                        expressions.remove(col)
                        expressions.insert(index + 1, col)
                        replace_column_type(self, col)

            properties = 'PROPERTIES (\n    "replication_allocation" = "tag.location.default: 3"\n)'
            partition_str = ""
            if parti_range_column:
                if parti_range_granularity:
                    partition_str = f"AUTO PARTITION BY RANGE (date_trunc(`{parti_range_column}`, '{parti_range_granularity}')) ()\n"
                else:
                    partition_str = (
                        f"AUTO PARTITION BY RANGE (date_trunc(`{parti_range_column}`, 'day')) ()\n"
                    )
            elif partion_list_column:
                part_str = ",".join(partion_list_column)
                partition_str = f"AUTO PARTITION BY LIST ({part_str}) ()\n"

            def get_and_replace_column_def(expression):
                col_def = expression.find(exp.ColumnDef) if "find" in dir(expression) else None
                replace_column_type(self, col_def) if col_def else None
                return col_def

            col_def = get_and_replace_column_def(expression)
            first_field_name = f"`{col_def.name}`" if col_def else ""
            if pg_key:
                if model_selection == "True":
                    key_str = f"DUPLICATE KEY({first_field_name})\n"
                else:
                    key_name = ", ".join(pg_key_ordered)
                    key_str = f"UNIQUE KEY({key_name})\n"
            else:
                if model_selection == "False":
                    if col_range:
                        set_cloumn = []
                        for i in range(2):
                            replace_column_type(self, expressions[i])
                            if notnull not in expressions[i].args["constraints"]:
                                expressions[i].args["constraints"].insert(0, notnull)
                            set_cloumn.append(f"`{expressions[i].name}`")
                        if not first_field_name:
                            first_field_name = set_cloumn[0]
                        set_field = ", ".join(set_cloumn)
                        key_str = f"UNIQUE KEY({set_field})\n"
                    else:
                        key_str = f"UNIQUE KEY({first_field_name})\n"
                else:
                    key_str = f"DUPLICATE KEY({first_field_name})\n"
            expression_sql = super().create_sql(expression).strip()
            # Return the final SQL string
            return (
                f"{expression_sql}\n"
                f"{key_str}"
                f"{partition_str}"
                f"DISTRIBUTED BY HASH({first_field_name}) BUCKETS AUTO\n"
                f"{properties}"
            )
            # todo bucket table、partition bucket table、ordinary table still need to be processed

    KeyWords = [
        "ACCOUNT_LOCK",
        "ACCOUNT_UNLOCK",
        "ADD",
        "ADDDATE",
        "ADMIN",
        "AFTER",
        "AGG_STATE",
        "AGGREGATE",
        "ALIAS",
        "ALL",
        "ALTER",
        "ANALYZE",
        "ANALYZED",
        "AND",
        "ANTI",
        "APPEND",
        "ARRAY",
        "AS",
        "ASC",
        "AT",
        "AUTHORS",
        "AUTO",
        "AUTO_INCREMENT",
        "BACKEND",
        "BACKENDS",
        "BACKUP",
        "BEGIN",
        "BETWEEN",
        "BIGINT",
        "BIN",
        "BINARY",
        "BINLOG",
        "BITAND",
        "BITMAP",
        "BITMAP_UNION",
        "BITOR",
        "BITXOR",
        "BLOB",
        "BOOLEAN",
        "BRIEF",
        "BROKER",
        "BUCKETS",
        "BUILD",
        "BUILTIN",
        "BY",
        "CACHED",
        "CALL",
        "CANCEL",
        "CASE",
        "CAST",
        "CATALOG",
        "CATALOGS",
        "CHAIN",
        "CHAR",
        "CHARACTER",
        "CHARSET",
        "CHECK",
        "CLEAN",
        "CLUSTER",
        "CLUSTERS",
        "COLLATE",
        "COLLATION",
        "COLUMN",
        "COLUMNS",
        "COMMENT",
        "COMMIT",
        "COMMITTED",
        "COMPACT",
        "COMPLETE",
        "CONFIG",
        "CONNECTION",
        "CONNECTION_ID",
        "CONSISTENT",
        "CONSTRAINT",
        "CONSTRAINTS",
        "CONVERT",
        "COPY",
        "COUNT",
        "CREATE",
        "CREATION",
        "CRON",
        "CROSS",
        "CUBE",
        "CURRENT",
        "CURRENT_CATALOG",
        "CURRENT_DATE",
        "CURRENT_TIME",
        "CURRENT_TIMESTAMP",
        "CURRENT_USER",
        "DATA",
        "DATABASE",
        "DATABASES",
        "DATE",
        "DATE_ADD",
        "DATE_CEIL",
        "DATE_DIFF",
        "DATE_FLOOR",
        "DATE_SUB",
        "DATEADD",
        "DATEDIFF",
        "DATETIME",
        "DATETIMEV2",
        "DATEV2",
        "DATETIMEV1",
        "DATEV1",
        "DAY",
        "DAYS_ADD",
        "DAYS_SUB",
        "DECIMAL",
        "DECIMALV2",
        "DECIMALV3",
        "DECOMMISSION",
        "DEFAULT",
        "DEFERRED",
        "DELETE",
        "DEMAND",
        "DESC",
        "DESCRIBE",
        "DIAGNOSE",
        "DISK",
        "DISTINCT",
        "DISTINCTPC",
        "DISTINCTPCSA",
        "DISTRIBUTED",
        "DISTRIBUTION",
        "DIV",
        "DO",
        "DORIS_INTERNAL_TABLE_ID",
        "DOUBLE",
        "DROP",
        "DROPP",
        "DUPLICATE",
        "DYNAMIC",
        "ELSE",
        "ENABLE",
        "ENCRYPTKEY",
        "ENCRYPTKEYS",
        "END",
        "ENDS",
        "ENGINE",
        "ENGINES",
        "ENTER",
        "ERRORS",
        "EVENTS",
        "EVERY",
        "EXCEPT",
        "EXCLUDE",
        "EXECUTE",
        "EXISTS",
        "EXPIRED",
        "EXPLAIN",
        "EXPORT",
        "EXTENDED",
        "EXTERNAL",
        "EXTRACT",
        "FAILED_LOGIN_ATTEMPTS",
        "FALSE",
        "FAST",
        "FEATURE",
        "FIELDS",
        "FILE",
        "FILTER",
        "FIRST",
        "FLOAT",
        "FOLLOWER",
        "FOLLOWING",
        "FOR",
        "FOREIGN",
        "FORCE",
        "FORMAT",
        "FREE",
        "FROM",
        "FRONTEND",
        "FRONTENDS",
        "FULL",
        "FUNCTION",
        "FUNCTIONS",
        "GLOBAL",
        "GRANT",
        "GRANTS",
        "GRAPH",
        "GROUP",
        "GROUPING",
        "GROUPS",
        "HASH",
        "HAVING",
        "HDFS",
        "HELP",
        "HISTOGRAM",
        "HLL",
        "HLL_UNION",
        "HOSTNAME",
        "HOUR",
        "HUB",
        "IDENTIFIED",
        "IF",
        "IGNORE",
        "IMMEDIATE",
        "IN",
        "INCREMENTAL",
        "INDEX",
        "INDEXES",
        "INFILE",
        "INNER",
        "INSERT",
        "INSTALL",
        "INT",
        "INTEGER",
        "INTERMEDIATE",
        "INTERSECT",
        "INTERVAL",
        "INTO",
        "INVERTED",
        "IPV4",
        "IPV6",
        "IS",
        "IS_NOT_NULL_PRED",
        "IS_NULL_PRED",
        "ISNULL",
        "ISOLATION",
        "JOB",
        "JOBS",
        "JOIN",
        "JSON",
        "JSONB",
        "KEY",
        "KEYS",
        "KILL",
        "LABEL",
        "LARGEINT",
        "LAST",
        "LATERAL",
        "LDAP",
        "LDAP_ADMIN_PASSWORD",
        "LEFT",
        "LESS",
        "LEVEL",
        "LIKE",
        "LIMIT",
        "LINES",
        "LINK",
        "LIST",
        "LOAD",
        "LOCAL",
        "LOCALTIME",
        "LOCALTIMESTAMP",
        "LOCATION",
        "LOCK",
        "LOGICAL",
        "LOW_PRIORITY",
        "MANUAL",
        "MAP",
        "MATCH",
        "MATCH_ALL",
        "MATCH_ANY",
        "MATCH_ELEMENT_EQ",
        "MATCH_ELEMENT_GE",
        "MATCH_ELEMENT_GT",
        "MATCH_ELEMENT_LE",
        "MATCH_ELEMENT_LT",
        "MATCH_PHRASE",
        "MATCH_PHRASE_PREFIX",
        "MATCH_REGEXP",
        "MATERIALIZED",
        "MAX",
        "MAXVALUE",
        "MEMO",
        "MERGE",
        "MIGRATE",
        "MIGRATIONS",
        "MIN",
        "MINUS",
        "MINUTE",
        "MODIFY",
        "MONTH",
        "MTMV",
        "NAME",
        "NAMES",
        "NATURAL",
        "NEGATIVE",
        "NEVER",
        "NEXT",
        "NGRAM_BF",
        "NO",
        "NON_NULLABLE",
        "NOT",
        "NULL",
        "NULLS",
        "OBSERVER",
        "OF",
        "OFFSET",
        "ON",
        "ONLY",
        "OPEN",
        "OPTIMIZED",
        "OR",
        "ORDER",
        "OUTER",
        "OUTFILE",
        "OVER",
        "OVERWRITE",
        "PARAMETER",
        "PARSED",
        "PARTITION",
        "PARTITIONS",
        "PASSWORD",
        "PASSWORD_EXPIRE",
        "PASSWORD_HISTORY",
        "PASSWORD_LOCK_TIME",
        "PASSWORD_REUSE",
        "PATH",
        "PAUSE",
        "PERCENT",
        "PERIOD",
        "PERMISSIVE",
        "PHYSICAL",
        "PLAN",
        "PLUGIN",
        "PLUGINS",
        "POLICY",
        "PRECEDING",
        "PREPARE",
        "PRIMARY",
        "PROC",
        "PROCEDURE",
        "PROCESSLIST",
        "PROFILE",
        "PROPERTIES",
        "PROPERTY",
        "QUANTILE_STATE",
        "QUANTILE_UNION",
        "QUERY",
        "QUOTA",
        "RANDOM",
        "RANGE",
        "READ",
        "REAL",
        "REBALANCE",
        "RECOVER",
        "RECYCLE",
        "REFRESH",
        "REFERENCES",
        "REGEXP",
        "RELEASE",
        "RENAME",
        "REPAIR",
        "REPEATABLE",
        "REPLACE",
        "REPLACE_IF_NOT_NULL",
        "REPLICA",
        "REPOSITORIES",
        "REPOSITORY",
        "RESOURCE",
        "RESOURCES",
        "RESTORE",
        "RESTRICTIVE",
        "RESUME",
        "RETURNS",
        "REVOKE",
        "REWRITTEN",
        "RIGHT",
        "RLIKE",
        "ROLE",
        "ROLES",
        "ROLLBACK",
        "ROLLUP",
        "ROUTINE",
        "ROW",
        "ROWS",
        "S3",
        "SAMPLE",
        "SCHEDULE",
        "SCHEDULER",
        "SCHEMA",
        "SCHEMAS",
        "SECOND",
        "SELECT",
        "SEMI",
        "SERIALIZABLE",
        "SESSION",
        "SET",
        "SETS",
        "SHAPE",
        "SHOW",
        "SIGNED",
        "SKEW",
        "SMALLINT",
        "SNAPSHOT",
        "SONAME",
        "SPLIT",
        "SQL_BLOCK_RULE",
        "START",
        "STARTS",
        "STATS",
        "STATUS",
        "STOP",
        "STORAGE",
        "STREAM",
        "STREAMING",
        "STRING",
        "STRUCT",
        "SUBDATE",
        "SUM",
        "SUPERUSER",
        "SWITCH",
        "SYNC",
        "SYSTEM",
        "TABLE",
        "TABLES",
        "TABLESAMPLE",
        "TABLET",
        "TABLETS",
        "TASK",
        "TASKS",
        "TEMPORARY",
        "TERMINATED",
        "TEXT",
        "THAN",
        "THEN",
        "TIME",
        "TIMESTAMP",
        "TIMESTAMPADD",
        "TIMESTAMPDIFF",
        "TINYINT",
        "TO",
        "TRANSACTION",
        "TRASH",
        "TREE",
        "TRIGGERS",
        "TRIM",
        "TRUE",
        "TRUNCATE",
        "TYPE",
        "TYPECAST",
        "TYPES",
        "UNBOUNDED",
        "UNCOMMITTED",
        "UNINSTALL",
        "UNION",
        "UNIQUE",
        "UNLOCK",
        "UNSIGNED",
        "UPDATE",
        "USE",
        "USER",
        "USING",
        "VALUE",
        "VALUES",
        "VARCHAR",
        "VARIABLES",
        "VERBOSE",
        "VERSION",
        "VIEW",
        "WARNINGS",
        "WEEK",
        "WHEN",
        "WHERE",
        "WHITELIST",
        "WITH",
        "WORK",
        "WORKLOAD",
        "WRITE",
        "YEAR",
    ]
