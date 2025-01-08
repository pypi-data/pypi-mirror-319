from __future__ import annotations

import typing as t

from sqlglot import exp
from sqlglot.dialects.dialect import (
    approx_count_distinct_sql,
    arrow_json_extract_sql,
    binary_from_function,
    build_timestamp_trunc,
    rename_func,
    unit_to_str,
    inline_array_sql,
    property_sql,
)
from sqlglot.dialects.mysql import MySQL
from sqlglot.helper import seq_get


def _parse_time_slice(args: t.List) -> exp.DateCeil | exp.DateFloor:
    if len(args) < 3:
        return exp.DateFloor(this=seq_get(args, 0), expression=seq_get(args, 1))
    pos = str(seq_get(args, 2)).upper()
    if pos == "FLOOR":
        return exp.DateFloor(this=seq_get(args, 0), expression=seq_get(args, 1))
    else:
        return exp.DateCeil(this=seq_get(args, 0), expression=seq_get(args, 1))


def _parse_retention(args: t.List) -> exp.Retention:
    expr = args[0].expressions
    return exp.Retention(expressions=expr)


class StarRocks(MySQL):
    STRICT_JSON_PATH_SYNTAX = False

    # [+doris]
    def to_json_path(self, path: t.Optional[exp.Expression]) -> t.Optional[exp.Expression]:
        if isinstance(path, exp.Literal):
            path_text = path.name
            if not path_text.startswith("$") or "$" not in path_text:
                path_text = "$." + path_text
                return path.replace(exp.Literal.string(path_text))

        return super().to_json_path(path)

    class Parser(MySQL.Parser):
        FUNCTIONS = {
            **MySQL.Parser.FUNCTIONS,
            "ADDDATE": exp.DateAdd.from_arg_list,
            "ARRAY_APPEND": exp.ArrayPushback.from_arg_list,
            "ARRAY_TO_BITMAP": exp.BitmapFromArray.from_arg_list,
            "COT": exp.Cot.from_arg_list,
            "DATE_TRUNC": build_timestamp_trunc,
            "DATEDIFF": lambda args: exp.DateDiff(
                this=seq_get(args, 0), expression=seq_get(args, 1), unit=exp.Literal.string("DAY")
            ),
            "DATE_DIFF": lambda args: exp.DateDiff(
                this=seq_get(args, 1), expression=seq_get(args, 2), unit=seq_get(args, 0)
            ),
            "DIVIDE": binary_from_function(exp.Div),
            "JSON_EXISTS": exp.JsonExists.from_arg_list,
            "JSON_QUERY": exp.JSONExtract.from_arg_list,
            "JSON_STRING": lambda args: exp.CastToStrType(
                this=seq_get(args, 0),
                to="JSON",
            ),
            "LEAST": exp.Min.from_arg_list,
            "MULTIPLY": binary_from_function(exp.Mul),
            "MULTI_DISTINCT_COUNT": exp.CountDistinct.from_arg_list,
            "REGEXP": exp.RegexpLike.from_arg_list,
            "RETENTION": _parse_retention,
            "PARSE_JSON": lambda args: exp.ParseJSON(this=seq_get(args, 0), safe=True),
            "PERCENTILE_APPROX_RAW": exp.ApproxQuantile.from_arg_list,
            "SQUARE": lambda args: exp.Pow(this=seq_get(args, 0), expression=exp.Literal.number(2)),
            "STD": exp.Stddev.from_arg_list,
            "STR2DATE": exp.StrToDate.from_arg_list,
            "TIME_SLICE": _parse_time_slice,
        }

        PROPERTY_PARSERS = {
            **MySQL.Parser.PROPERTY_PARSERS,
            "PROPERTIES": lambda self: self._parse_wrapped_properties(),
        }

        def _parse_create(self) -> exp.Create | exp.Command:
            create = super()._parse_create()

            # Starrocks' primary key is defined outside of the schema, so we need to move it there
            # https://docs.starrocks.io/docs/table_design/table_types/primary_key_table/#usage
            if isinstance(create, exp.Create) and isinstance(create.this, exp.Schema):
                props = create.args.get("properties")
                if props:
                    primary_key = props.find(exp.PrimaryKey)
                    if primary_key:
                        create.this.append("expressions", primary_key.pop())

            return create

        def _parse_unnest(self, with_alias: bool = True) -> t.Optional[exp.Unnest]:
            unnest = super()._parse_unnest(with_alias=with_alias)

            if unnest:
                alias = unnest.args.get("alias")

                if not alias:
                    # Starrocks defaults to naming the table alias as "unnest"
                    alias = exp.TableAlias(
                        this=exp.to_identifier("unnest"), columns=[exp.to_identifier("unnest")]
                    )
                    unnest.set("alias", alias)
                elif not alias.args.get("columns"):
                    # Starrocks defaults to naming the UNNEST column as "unnest"
                    # if it's not otherwise specified
                    alias.set("columns", [exp.to_identifier("unnest")])

            return unnest

    class Generator(MySQL.Generator):
        EXCEPT_INTERSECT_SUPPORT_ALL_CLAUSE = False
        JSON_TYPE_REQUIRED_FOR_EXTRACTION = False
        VARCHAR_REQUIRES_SIZE = False
        PARSE_JSON_NAME: t.Optional[str] = "PARSE_JSON"
        WITH_PROPERTIES_PREFIX = "PROPERTIES"

        CAST_MAPPING = {}

        TYPE_MAPPING = {
            **MySQL.Generator.TYPE_MAPPING,
            exp.DataType.Type.TEXT: "STRING",
            exp.DataType.Type.TIMESTAMP: "DATETIME",
            exp.DataType.Type.TIMESTAMPTZ: "DATETIME",
        }

        PROPERTIES_LOCATION = {
            **MySQL.Generator.PROPERTIES_LOCATION,
            exp.PrimaryKey: exp.Properties.Location.POST_SCHEMA,
        }

        TRANSFORMS = {
            **MySQL.Generator.TRANSFORMS,
            exp.Array: inline_array_sql,
            exp.ApproxDistinct: approx_count_distinct_sql,
            exp.DateDiff: lambda self, e: self.func(
                "DATE_DIFF", unit_to_str(e), e.this, e.expression
            ),
            exp.JSONExtractScalar: arrow_json_extract_sql,
            exp.JSONExtract: arrow_json_extract_sql,
            exp.Property: property_sql,
            exp.RegexpLike: rename_func("REGEXP"),
            exp.StrToUnix: lambda self, e: self.func("UNIX_TIMESTAMP", e.this, self.format_time(e)),
            exp.TimestampTrunc: lambda self, e: self.func("DATE_TRUNC", unit_to_str(e), e.this),
            exp.TimeStrToDate: rename_func("TO_DATE"),
            exp.UnixToStr: lambda self, e: self.func("FROM_UNIXTIME", e.this, self.format_time(e)),
            exp.UnixToTime: rename_func("FROM_UNIXTIME"),
            exp.ArrayFilter: rename_func("ARRAY_FILTER"),
        }

        TRANSFORMS.pop(exp.DateTrunc)

        def create_sql(self, expression: exp.Create) -> str:
            # Starrocks' primary key is defined outside of the schema, so we need to move it there
            schema = expression.this
            if isinstance(schema, exp.Schema):
                primary_key = schema.find(exp.PrimaryKey)

                if primary_key:
                    props = expression.args.get("properties")

                    if not props:
                        props = exp.Properties(expressions=[])
                        expression.set("properties", props)

                    # Verify if the first one is an engine property. Is true then insert it after the engine,
                    # otherwise insert it at the beginning
                    engine = props.find(exp.EngineProperty)
                    engine_index = (engine.index or 0) if engine else -1
                    props.set("expressions", primary_key.pop(), engine_index + 1, overwrite=False)

            return super().create_sql(expression)
