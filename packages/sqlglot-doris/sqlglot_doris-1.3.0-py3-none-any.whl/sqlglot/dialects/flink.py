from __future__ import annotations

import typing as t

from sqlglot import exp, generator, parser, tokens, transforms
from sqlglot.dialects.dialect import (
    Dialect,
    max_or_greatest,
    min_or_least,
    rename_func,
    to_number_with_nls_param,
)
from sqlglot.helper import seq_get
from sqlglot.tokens import TokenType


class Flink(Dialect):
    SUPPORTS_SEMI_ANTI_JOIN = False
    TYPED_DIVISION = True

    class Tokenizer(tokens.Tokenizer):
        QUOTES = ["'", '"']
        IDENTIFIERS = ["`"]
        STRING_ESCAPES = ["\\"]

        KEYWORDS = {
            **tokens.Tokenizer.KEYWORDS,
            "**": TokenType.DSTAR,
            "^=": TokenType.NEQ,
            "BYTEINT": TokenType.SMALLINT,
            "COLLECT": TokenType.COMMAND,
            "DEL": TokenType.DELETE,
            "EQ": TokenType.EQ,
            "GE": TokenType.GTE,
            "GT": TokenType.GT,
            "HELP": TokenType.COMMAND,
            "INS": TokenType.INSERT,
            "LE": TokenType.LTE,
            "LT": TokenType.LT,
            "MINUS": TokenType.EXCEPT,
            "MOD": TokenType.MOD,
            "NE": TokenType.NEQ,
            "NOT=": TokenType.NEQ,
            "SAMPLE": TokenType.TABLE_SAMPLE,
            "SEL": TokenType.SELECT,
            "ST_GEOMETRY": TokenType.GEOMETRY,
            "TOP": TokenType.TOP,
            "UPD": TokenType.UPDATE,
            "$": TokenType.PARAMETER,
            "PLACING": TokenType.PLACING,
            "FOR": TokenType.PARAMETER,
            "WATERMARK FOR": TokenType.WATERMARK_FOR,
        }
        SINGLE_TOKENS = {
            **tokens.Tokenizer.SINGLE_TOKENS,
            "$": TokenType.PARAMETER,
        }
        NUMERIC_LITERALS = {
            "L": "BIGINT",
            "S": "SMALLINT",
            "Y": "TINYINT",
            "D": "DOUBLE",
            "F": "FLOAT",
            "BD": "DECIMAL",
        }

    class Parser(parser.Parser):
        TABLESAMPLE_CSV = True
        VALUES_FOLLOWED_BY_PAREN = False

        FUNC_TOKENS = {*parser.Parser.FUNC_TOKENS}

        STATEMENT_PARSERS = {
            **parser.Parser.STATEMENT_PARSERS,
            TokenType.DATABASE: lambda self: self.expression(
                exp.Use, this=self._parse_table(schema=False)
            ),
            TokenType.REPLACE: lambda self: self._parse_create(),
        }

        FUNCTIONS = {
            **parser.Parser.FUNCTIONS,
            "DATE_ADD": lambda args: exp.TsOrDsAdd(
                this=seq_get(args, 0), expression=seq_get(args, 1), unit=exp.Literal.string("DAY")
            ),
            "REPLACE": exp.Replace.from_arg_list,
            "OVERLAY": exp.Overlay.from_arg_list,
            "LOCATE": exp.Locate.from_arg_list,
            "PARSE_URL": exp.ParseUrl.from_arg_list,
            "REGEXP": exp.Regexp.from_arg_list,
            "REVERSE": exp.ArrayReverse.from_arg_list,
            "SPLIT_INDEX": exp.SplitIndex.from_arg_list,
            "SUBSTR": exp.Substr.from_arg_list,
            "BIN": exp.Bin.from_arg_list,
            "LOCALTIMESTAMP": exp.LocalTimestamp.from_arg_list,
            "LOCALTIME": exp.LocalTime.from_arg_list,
            "TO_DATE": exp.ToDate.from_arg_list,
            "HOUR": exp.Hour.from_arg_list,
            "NOW": exp.Now.from_arg_list,
            "UNIX_TIMESTAMP": exp.UnixTimestamp.from_arg_list,
            "TO_TIMESTAMP": exp.ToTimestamp.from_arg_list,
            "FROM_UNIXTIME": exp.FromUnixTime.from_arg_list,
            "TABLE_FUNC": exp.TableFunc.from_arg_list,
            "TUMBLE": exp.Tumble.from_arg_list,
            "DESCRIPTOR": exp.Descriptor.from_arg_list,
        }

        FUNCTION_PARSERS = {
            **parser.Parser.FUNCTION_PARSERS,
            "SUBSTR": lambda self: self._parse_substr(),
        }

        PROPERTY_PARSERS: t.Dict[str, t.Callable] = {
            **parser.Parser.PROPERTY_PARSERS,
            "AS": lambda self: self._parse_create_as(),
        }

        EXPONENT = {
            TokenType.DSTAR: exp.Pow,
        }

        def _parse_substr(self) -> exp.Substr:
            args = t.cast(t.List[t.Optional[exp.Expression]], self._parse_csv(self._parse_bitwise))

            if self._match(TokenType.FROM):
                args.append(self._parse_bitwise())
            if self._match(TokenType.FOR):
                if len(args) == 1:
                    args.append(exp.Literal.number(1))
                args.append(self._parse_bitwise())

            return self.validate_expression(exp.Substr.from_arg_list(args), args)

        def _parse_position(self, haystack_first: bool = False) -> exp.StrPosition:
            return super()._parse_position(haystack_first=True)

        def _parse_create_as(self) -> t.Optional[exp.AsProperty]:
            table = self._parse_table(schema=True)

            options = []
            while self._match_texts(("INCLUDING", "EXCLUDING")):
                this = self._prev.text.upper()

                id_var = self._parse_id_var()
                if not id_var:
                    return None

                options.append(
                    self.expression(exp.Property, this=this, value=exp.var(id_var.this.upper()))
                )

            return self.expression(exp.AsProperty, this=table, expressions=options)

        def _parse_update(self) -> exp.Update:
            return self.expression(
                exp.Update,
                **{  # type: ignore
                    "this": self._parse_table(alias_tokens=self.UPDATE_ALIAS_TOKENS),
                    "from": self._parse_from(joins=True),
                    "expressions": self._match(TokenType.SET)
                    and self._parse_csv(self._parse_equality),
                    "where": self._parse_where(),
                },
            )

        def _parse_rangen(self):
            this = self._parse_id_var()
            self._match(TokenType.BETWEEN)

            expressions = self._parse_csv(self._parse_conjunction)
            each = self._match_text_seq("EACH") and self._parse_conjunction()
            # [+doris]Initialize no_range and unknown as False
            no_range = False
            unknown = False
            self._match(TokenType.COMMA)
            # Check for the presence of NO RANGE or UNKNOWN
            if self._match_text_seq("NO", "RANGE"):
                no_range = True
            self._match(TokenType.OR)
            if self._match_text_seq("UNKNOWN"):
                unknown = True
            return self.expression(
                exp.RangeN,
                this=this,
                expressions=expressions,
                each=each,
                no_range=no_range,
                unknown=unknown,
            )

        def _parse_index_params(self) -> exp.IndexParameters:
            this = super()._parse_index_params()

            if this.args.get("on"):
                this.set("on", None)
                self._retreat(self._index - 2)
            return this

    class Generator(generator.Generator):
        LIMIT_IS_TOP = True
        JOIN_HINTS = False
        TABLE_HINTS = False
        QUERY_HINTS = False
        TABLESAMPLE_KEYWORDS = "SAMPLE"
        LAST_DAY_SUPPORTS_DATE_PART = False
        CAN_IMPLEMENT_ARRAY_ANY = True
        TZ_TO_WITH_TIME_ZONE = True

        TYPE_MAPPING = {
            **generator.Generator.TYPE_MAPPING,
            exp.DataType.Type.GEOMETRY: "ST_GEOMETRY",
            exp.DataType.Type.DOUBLE: "DOUBLE",
            exp.DataType.Type.TIMESTAMPTZ: "TIMESTAMP",
            exp.DataType.Type.TEXT: "STRING",
            # exp.DataType.Type.
        }

        PROPERTIES_LOCATION = {
            **generator.Generator.PROPERTIES_LOCATION,
            exp.OnCommitProperty: exp.Properties.Location.POST_INDEX,
            exp.PartitionedByProperty: exp.Properties.Location.POST_SCHEMA,
            exp.StabilityProperty: exp.Properties.Location.POST_CREATE,
        }

        TRANSFORMS = {
            **generator.Generator.TRANSFORMS,
            exp.ArgMax: rename_func("MAX_BY"),
            exp.ArgMin: rename_func("MIN_BY"),
            exp.ArraySize: rename_func("CARDINALITY"),
            exp.Max: max_or_greatest,
            exp.Min: min_or_least,
            exp.Rand: lambda self, e: self.func("RANDOM", e.args.get("lower"), e.args.get("upper")),
            exp.Select: transforms.preprocess(
                [transforms.eliminate_distinct_on, transforms.eliminate_semi_and_anti_joins]
            ),
            exp.StrToDate: lambda self,
            e: f"CAST({self.sql(e, 'this')} AS DATE FORMAT {self.format_time(e)})",
            exp.ToChar: lambda self, e: self.function_fallback_sql(e),
            exp.ToNumber: to_number_with_nls_param,
            exp.Use: lambda self, e: f"DATABASE {self.sql(e, 'this')}",
            # exp.Quarter: lambda self, e: self.sql(exp.Extract(this="QUARTER", expression=e.this)),
            exp.StrPosition: lambda self,
            e: f"POSITION({self.sql(e,'substr')} in {self.sql(e,'this')})",
            exp.ArrayReverse: rename_func("REVERSE"),
            exp.LocalTimestamp: rename_func("LOCALTIMESTAMP"),
            exp.LocalTime: rename_func("LOCALTIME"),
            exp.DayOfYear: rename_func("DAYOFYEAR"),
            exp.DayOfMonth: rename_func("DAYOFMONTH"),
            exp.DayOfWeek: rename_func("DAYOFWEEK"),
            exp.TsOrDsToTimestamp: lambda self, e: self.sql(e, "this"),
            exp.FromUnixTime: rename_func("FROM_UNIXTIME"),
            exp.PartitionedByProperty: lambda self, e: f"PARTITIONED BY {self.sql(e, 'this')}",
        }

        def currenttimestamp_sql(self, expression: exp.CurrentTimestamp) -> str:
            prefix, suffix = ("(", ")") if expression.this else ("", "")
            return self.func("CURRENT_TIMESTAMP", expression.this, prefix=prefix, suffix=suffix)

        def cast_sql(self, expression: exp.Cast, safe_prefix: t.Optional[str] = None) -> str:
            if expression.to.this == exp.DataType.Type.UNKNOWN and expression.args.get("format"):
                expression.to.pop()

            return super().cast_sql(expression, safe_prefix=safe_prefix)

        def trycast_sql(self, expression: exp.TryCast) -> str:
            return self.cast_sql(expression, safe_prefix="TRY")

        def tablesample_sql(
            self,
            expression: exp.TableSample,
            tablesample_keyword: t.Optional[str] = None,
        ) -> str:
            return f"{self.sql(expression, 'this')} SAMPLE {self.expressions(expression)}"

        def placing_sql(self, expression: exp.Placing) -> str:
            return self.binary(expression, "PLACING")

        def LPAD_sql(self, expression: exp.Placing) -> str:
            return self.binary(expression, "PLACING")

        def partitionedbyproperty_sql(self, expression: exp.PartitionedByProperty) -> str:
            return f"PARTITION BY {self.sql(expression, 'this')}"

        def update_sql(self, expression: exp.Update) -> str:
            this = self.sql(expression, "this")
            from_sql = self.sql(expression, "from")
            set_sql = self.expressions(expression, flat=True)
            where_sql = self.sql(expression, "where")
            sql = f"UPDATE {this}{from_sql} SET {set_sql}{where_sql}"
            return self.prepend_ctes(expression, sql)

        def mod_sql(self, expression: exp.Mod) -> str:
            return self.binary(expression, "MOD")

        def datatype_sql(self, expression: exp.DataType) -> str:
            type_sql = super().datatype_sql(expression)
            prefix_sql = expression.args.get("prefix")
            return f"SYSUDTLIB.{type_sql}" if prefix_sql else type_sql

        def rangen_sql(self, expression: exp.RangeN) -> str:
            this = self.sql(expression, "this")
            expressions_sql = self.expressions(expression)
            each_sql = self.sql(expression, "each")
            each_sql = f" EACH {each_sql}" if each_sql else ""

            return f"RANGE_N({this} BETWEEN {expressions_sql}{each_sql})"

        def createable_sql(self, expression: exp.Create, locations: t.DefaultDict) -> str:
            kind = self.sql(expression, "kind").upper()
            if kind == "TABLE" and locations.get(exp.Properties.Location.POST_NAME):
                this_name = self.sql(expression.this, "this")
                this_properties = self.properties(
                    exp.Properties(expressions=locations[exp.Properties.Location.POST_NAME]),
                    wrapped=False,
                    prefix=",",
                )
                this_schema = self.schema_columns_sql(expression.this)
                return f"{this_name}{this_properties}{self.sep()}{this_schema}"

            return super().createable_sql(expression, locations)

        def interval_sql(self, expression: exp.Interval) -> str:
            multiplier = 0
            unit = expression.text("unit")

            if unit.startswith("WEEK"):
                multiplier = 7
            elif unit.startswith("QUARTER"):
                multiplier = 90

            if multiplier:
                return f"({multiplier} * {super().interval_sql(exp.Interval(this=expression.this, unit=exp.var('DAY')))})"

            return super().interval_sql(expression)

        def property_name(self, expression: exp.Property, string_key: bool = False) -> str:
            return super().property_name(expression, True)

        def with_properties(self, properties: exp.Properties) -> str:
            return self.properties(properties, prefix=self.seg("WITH", sep=""))
