general_functions = [
    "BLAKE3",
    "CAST",
    "CHARACTER_LENGTH",
    "CHAR_LENGTH",
    "CRC32",
    "CRC32IEEE",
    "CRC64",
    "DATABASE",
    "DATE",
    "DATE_DIFF",
    "DATE_FORMAT",
    "DATE_TRUNC",
    "DAY",
    "DAYOFMONTH",
    "DAYOFWEEK",
    "DAYOFYEAR",
    "FORMAT_BYTES",
    "FQDN",
    "FROM_BASE64",
    "FROM_DAYS",
    "FROM_UNIXTIME",
    "HOUR",
    "INET6_ATON",
    "INET6_NTOA",
    "INET_ATON",
    "INET_NTOA",
    "IPv4CIDRToRange",
    "IPv4NumToString",
    "IPv4NumToStringClassC",
    "IPv4StringToNum",
    "IPv4StringToNumOrDefault",
    "IPv4StringToNumOrNull",
    "IPv4ToIPv6",
    "IPv6CIDRToRange",
    "IPv6NumToString",
    "IPv6StringToNum",
    "IPv6StringToNumOrDefault",
    "IPv6StringToNumOrNull",
    "JSONArrayLength",
    "JSONExtract",
    "JSONExtractArrayRaw",
    "JSONExtractBool",
    "JSONExtractFloat",
    "JSONExtractInt",
    "JSONExtractKeys",
    "JSONExtractKeysAndValues",
    "JSONExtractKeysAndValuesRaw",
    "JSONExtractRaw",
    "JSONExtractString",
    "JSONExtractUInt",
    "JSONHas",
    "JSONKey",
    "JSONLength",
    "JSONRemoveDynamoDBAnnotations",
    "JSONType",
    "JSON_ARRAY_LENGTH",
    "JSON_EXISTS",
    "JSON_QUERY",
    "JSON_VALUE",
    "L1Distance",
    "L1Norm",
    "L1Normalize",
    "L2Distance",
    "L2Norm",
    "L2Normalize",
    "L2SquaredDistance",
    "L2SquaredNorm",
    "LAST_DAY",
    "LinfDistance",
    "LinfNorm",
    "LinfNormalize",
    "LpDistance",
    "LpNorm",
    "LpNormalize",
    "MACNumToString",
    "MACStringToNum",
    "MACStringToOUI",
    "MAP_FROM_ARRAYS",
    "MD4",
    "MD5",
    "MILLISECOND",
    "MINUTE",
    "MONTH",
    "OCTET_LENGTH",
    "QUARTER",
    "REGEXP_EXTRACT",
    "REGEXP_MATCHES",
    "REGEXP_REPLACE",
    "SCHEMA",
    "SECOND",
    "SHA1",
    "SHA224",
    "SHA256",
    "SHA384",
    "SHA512",
    "SHA512_256",
    "SUBSTRING_INDEX",
    "SVG",
    "TIMESTAMP_DIFF",
    "TO_BASE64",
    "TO_DAYS",
    "TO_UNIXTIME",
    "ULIDStringToDateTime",
    "URLHash",
    "URLHierarchy",
    "URLPathHierarchy",
    "UTCTimestamp",
    "UTC_timestamp",
    "UUIDNumToString",
    "UUIDStringToNum",
    "UUIDToNum",
    "UUIDv7ToDateTime",
    "YEAR",
    "YYYYMMDDToDate",
    "YYYYMMDDToDate32",
    "YYYYMMDDhhmmssToDateTime",
    "YYYYMMDDhhmmssToDateTime64",
]

general_functions_insensitive = [
    "cast",
    "character_length",
    "char_length",
    "crc32",
    "crc32ieee",
    "crc64",
    "database",
    "date",
    "date_format",
    "date_trunc",
    "day",
    "dayofmonth",
    "dayofweek",
    "dayofyear",
    "format_bytes",
    "fqdn",
    "from_base64",
    "from_days",
    "from_unixtime",
    "hour",
    "inet6_aton",
    "inet6_ntoa",
    "inet_aton",
    "inet_ntoa",
    "json_array_length",
    "last_day",
    "millisecond",
    "minute",
    "month",
    "octet_length",
    "quarter",
    "regexp_extract",
    "regexp_matches",
    "regexp_replace",
    "schema",
    "second",
    "substring_index",
    "to_base64",
    "to_days",
    "to_unixtime",
    "utctimestamp",
    "utc_timestamp",
    "year",
]

aggregate_functions = [
    "BIT_AND",
    "BIT_OR",
    "BIT_XOR",
    "COVAR_POP",
    "COVAR_SAMP",
    "STD",
    "STDDEV_POP",
    "STDDEV_SAMP",
    "VAR_POP",
    "VAR_SAMP",
    "aggThrow",
    "analysisOfVariance",
    "anova",
    "any",
    "anyHeavy",
    "anyLast",
    "anyLast_respect_nulls",
    "any_respect_nulls",
    "any_value",
    "any_value_respect_nulls",
    "approx_top_count",
    "approx_top_k",
    "approx_top_sum",
    "argMax",
    "argMin",
    "array_agg",
    "array_concat_agg",
    "avg",
    "avgWeighted",
    "boundingRatio",
    "categoricalInformationValue",
    "contingency",
    "corr",
    "corrMatrix",
    "corrStable",
    "count",
    "covarPop",
    "covarPopMatrix",
    "covarPopStable",
    "covarSamp",
    "covarSampMatrix",
    "covarSampStable",
    "cramersV",
    "cramersVBiasCorrected",
    "deltaSum",
    "deltaSumTimestamp",
    "dense_rank",
    "entropy",
    "exponentialMovingAverage",
    "exponentialTimeDecayedAvg",
    "exponentialTimeDecayedCount",
    "exponentialTimeDecayedMax",
    "exponentialTimeDecayedSum",
    "first_value",
    "first_value_respect_nulls",
    "flameGraph",
    "groupArray",
    "groupArrayInsertAt",
    "groupArrayIntersect",
    "groupArrayLast",
    "groupArrayMovingAvg",
    "groupArrayMovingSum",
    "groupArraySample",
    "groupArraySorted",
    "groupBitAnd",
    "groupBitOr",
    "groupBitXor",
    "groupBitmap",
    "groupBitmapAnd",
    "groupBitmapOr",
    "groupBitmapXor",
    "groupUniqArray",
    "histogram",
    "intervalLengthSum",
    "kolmogorovSmirnovTest",
    "kurtPop",
    "kurtSamp",
    "lagInFrame",
    "largestTriangleThreeBuckets",
    "last_value",
    "last_value_respect_nulls",
    "leadInFrame",
    "lttb",
    "mannWhitneyUTest",
    "max",
    "maxIntersections",
    "maxIntersectionsPosition",
    "maxMappedArrays",
    "meanZTest",
    "median",
    "medianBFloat16",
    "medianBFloat16Weighted",
    "medianDD",
    "medianDeterministic",
    "medianExact",
    "medianExactHigh",
    "medianExactLow",
    "medianExactWeighted",
    "medianGK",
    "medianInterpolatedWeighted",
    "medianTDigest",
    "medianTDigestWeighted",
    "medianTiming",
    "medianTimingWeighted",
    "min",
    "minMappedArrays",
    "nonNegativeDerivative",
    "nothing",
    "nothingNull",
    "nothingUInt64",
    "nth_value",
    "ntile",
    "quantile",
    "quantileBFloat16",
    "quantileBFloat16Weighted",
    "quantileDD",
    "quantileDeterministic",
    "quantileExact",
    "quantileExactExclusive",
    "quantileExactHigh",
    "quantileExactInclusive",
    "quantileExactLow",
    "quantileExactWeighted",
    "quantileGK",
    "quantileInterpolatedWeighted",
    "quantileTDigest",
    "quantileTDigestWeighted",
    "quantileTiming",
    "quantileTimingWeighted",
    "quantiles",
    "quantilesBFloat16",
    "quantilesBFloat16Weighted",
    "quantilesDD",
    "quantilesDeterministic",
    "quantilesExact",
    "quantilesExactExclusive",
    "quantilesExactHigh",
    "quantilesExactInclusive",
    "quantilesExactLow",
    "quantilesExactWeighted",
    "quantilesGK",
    "quantilesInterpolatedWeighted",
    "quantilesTDigest",
    "quantilesTDigestWeighted",
    "quantilesTiming",
    "quantilesTimingWeighted",
    "rank",
    "rankCorr",
    "retention",
    "row_number",
    "sequenceCount",
    "sequenceMatch",
    "sequenceNextNode",
    "simpleLinearRegression",
    "singleValueOrNull",
    "skewPop",
    "skewSamp",
    "sparkBar",
    "sparkbar",
    "stddevPop",
    "stddevPopStable",
    "stddevSamp",
    "stddevSampStable",
    "stochasticLinearRegression",
    "stochasticLogisticRegression",
    "studentTTest",
    "sum",
    "sumCount",
    "sumKahan",
    "sumMapFiltered",
    "sumMapFilteredWithOverflow",
    "sumMapWithOverflow",
    "sumMappedArrays",
    "sumWithOverflow",
    "theilsU",
    "topK",
    "topKWeighted",
    "uniq",
    "uniqCombined",
    "uniqCombined64",
    "uniqExact",
    "uniqHLL12",
    "uniqTheta",
    "uniqUpTo",
    "varPop",
    "varPopStable",
    "varSamp",
    "varSampStable",
    "welchTTest",
    "windowFunnel",
]


create_project_prompt = """
You are a Tinybird expert. You will be given a prompt describing a data project and you will generate all the associated datasources and pipes.
<datasource>
    name: The name of the datasource.
    content: The content of the datasource datafile in the following format:

    ```
DESCRIPTION >
    Some meaningful description of the datasource

SCHEMA >
    `<column_name_1>` <clickhouse_tinybird_compatible_data_type> `json:$.<column_name_1>`,
    `<column_name_2>` <clickhouse_tinybird_compatible_data_type> `json:$.<column_name_2>`,
    ...
    `<column_name_n>` <clickhouse_tinybird_compatible_data_type> `json:$.<column_name_n>`

ENGINE "MergeTree"
ENGINE_PARTITION_KEY "<partition_key>"
ENGINE_SORTING_KEY "<sorting_key_1, sorting_key_2, ...>"
    ```
</datasource>
<pipe>
    name: The name of the pipe.
    content: The content of the pipe datafile in the following format:
    ```
DESCRIPTION >
    Some meaningful description of the pipe

NODE node_1
SQL >
    <sql_query_using_clickhouse_syntax_and_tinybird_templating_syntax>

...

NODE node_n
SQL >
    <sql_query_using_clickhouse_syntax_and_tinybird_templating_syntax>
    ```
</pipe>
<instructions>
    - The datasource name must be unique.
    - The pipe name must be unique.
    - The datasource will be the landing table for the data.
    - Create multiple pipes to show different use cases over the same datasource.
    - The SQL query must be a valid ClickHouse SQL query that mixes ClickHouse syntax and Tinybird templating syntax.
    - If you use dynamic parameters you MUST start ALWAYS the whole sql query with "%" symbol on top. e.g: SQL >\n    %\n SELECT * FROM <table> WHERE <condition> LIMIT 10
    - The Parameter functions like this one {{String(my_param_name,default_value)}} can be one of the following: String, DateTime, Date, Float32, Float64, Int, Integer, UInt8, UInt16, UInt32, UInt64, UInt128, UInt256, Int8, Int16, Int32, Int64, Int128, Int256
    - Parameter names must be different from column names. Pass always the param name and a default value to the function.
    - Code inside the template {{code}} is python code but no module is allowed to be imported. So for example you can't use now() as default value for a DateTime parameter. You need an if else block like this:
    ```
    (...)
    AND timestamp BETWEEN {{DateTime(start_date, now() - interval 30 day)}} AND {{DateTime(end_date, now())}} --this is not valid

    {%if not defined(start_date)%}
    timestamp BETWEEN now() - interval 30 day
    {%else%}
    timestamp BETWEEN {{DateTime(start_date)}} 
    {%end%}
    {%if not defined(end_date)%}
    AND now()
    {%else%}
    AND {{DateTime(end_date)}} 
    {%end%} --this is valid
    ```
    - Nodes can't have the same exact name as the Pipe they belong to.
    - Endpoints can export Prometehus format, Node sql must have name two columns: 
        name (String): The name of the metric 
        value (Number): The numeric value for the metric. 
      and then some optional columns:
        help (String): A description of the metric.
        timestamp (Number): A Unix timestamp for the metric.
        type (String): Defines the metric type (counter, gauge, histogram, summary, untyped, or empty).
        labels (Map(String, String)): A set of key-value pairs providing metric dimensions.
    - Use prometheus format when you are asked to monitor something
    - Nodes do NOT use the same name as the Pipe they belong to. So if the pipe name is "my_pipe", the nodes must be named "my_pipe_node_1", "my_pipe_node_2", etc.
</instructions>
"""

generate_sql_mock_data_prompt = """
Given the schema for a Tinybird datasource, return a can you create a clickhouse sql query to generate some random data that matches that schema.

Response format MUST be just a valid clickhouse sql query.

# Example input:

SCHEMA >
    experience_gained Int16 `json:$.experience_gained`,
    level Int16 `json:$.level`,
    monster_kills Int16 `json:$.monster_kills`,
    player_id String `json:$.player_id`,
    pvp_kills Int16 `json:$.pvp_kills`,
    quest_completions Int16 `json:$.quest_completions`,
    timestamp DateTime `json:$.timestamp`


# Example output:

SELECT
    rand() % 1000 AS experience_gained, -- Random experience gained between 0 and 999
    1 + rand() % 100 AS level,          -- Random level between 1 and 100
    rand() % 500 AS monster_kills,      -- Random monster kills between 0 and 499
    concat('player_', toString(rand() % 10000)) AS player_id, -- Random player IDs like "player_1234"
    rand() % 50 AS pvp_kills,           -- Random PvP kills between 0 and 49
    rand() % 200 AS quest_completions,  -- Random quest completions between 0 and 199
    now() - rand() % 86400 AS timestamp -- Random timestamp within the last day
FROM numbers({rows})

# Instructions:

- The query MUST return a random sample of data that matches the schema.
- The query MUST return a valid clickhouse sql query.
- The query MUST return a sample of EXACTLY {rows} rows.
- The query MUST be valid for clickhouse and Tinybird.
- Return JUST the sql query, without any other text or symbols. 
- Do NOT include ```clickhouse or ```sql or any other wrapping text.
- Do NOT use any of these functions: elementAt
- Do NOT add a semicolon at the end of the query
- Do NOT add any FORMAT at the end of the query, because it will be added later by Tinybird.

# Examples with different schemas, like an array field or a nested JSON field:

## Example schema with an array field:

### Schema:

SCHEMA >
    `order_id` UInt64 `json:$.order_id`,
    `customer_id` UInt64 `json:$.customer_id`,
    `order_date` DateTime `json:$.order_date`,
    `total_amount` Float64 `json:$.total_amount`,
    `items` Array(String) `json:$.items[:]` // This is an array field 

### Desired final output of the query:
{
  "order_id": 123456,
  "customer_id": 7890,
  "order_date": "2024-11-30T10:30:00.000Z",
  "total_amount": 150.0,
  "items": ["item1", "item2", "item3"]
}

### Example SQL output with an array field:

SELECT
  concat('ord_', toString(rand() % 10000)) AS order_id,
  concat('cust_', toString(rand() % 10000)) AS customer_id,
  now() - rand() % 86400 AS order_date,
  rand() % 1000 AS total_amount,
  arrayMap(x -> concat('item_', toString(x)), range(1, rand() % 5 + 1)) AS items
FROM numbers(ROWS)

## Example schema with a nested JSON field:

### Schema:

SCHEMA >
    `request_id` String `json:$.request_id`,
    `timestamp` DateTime `json:$.timestamp`,
    `model` String `json:$.request.model`,
    `temperature` Float32 `json:$.request.options.temperature`,
    `max_tokens` UInt32 `json:$.request.options.max_tokens`,
    `stream` UInt8 `json:$.request.options.stream`

### Desired final output of the query:

Note that the important part is generating the nested fields:
json:$.request.options.max_tokens > this means that the max_tokens field is nested inside the options field inside the request field.

{
  "request_id": "req_abc123",
  "timestamp": "2024-11-30T10:30:00.000Z",
  "request": {
    "model": "gpt-4",
    "options": {
      "temperature": 0.7,
      "max_tokens": 1000,
      "stream": false
    }
  }
}

### Example SQL output with nested fields:

SELECT
    request_id,
    timestamp,
    CAST(concat('{
        "model": "', model, '",
        "options": {
            "temperature": ', temperature, ',
            "max_tokens": ', max_tokens, ',
            "stream": ', IF(stream = 1, 'true', 'false'), '
        }
    }'), 'JSON') AS request
FROM
(
    SELECT
        concat('req_', lower(hex(randomString(6)))) AS request_id,
        (now() - toIntervalDay(rand() % 30)) + toIntervalSecond(rand() % 86400) AS timestamp,
        ['gpt-4', 'gpt-3.5-turbo', 'gpt-4-turbo'][(rand() % 3) + 1] AS model,
        round(rand() / 10, 2) AS temperature,
        500 + (rand() % 2500) AS max_tokens,
        rand() % 2 AS stream
    FROM numbers(ROWS)
)

# Extra context:
{context}

"""

create_test_prompt = """
You are a Tinybird expert. You will be given a pipe endpoint containing different nodes with SQL and Tinybird templating syntax. You will generate URLs to test it with different parameters combinations.

<test>
    <test_1>:
        name: <test_name_1>
        description: <description_1>
        parameters: <url_encoded_parameters_1>
    <test_2>:
        name: <test_name_2>
        description: <description_2>
        parameters: <url_encoded_parameters_2>
</test>
<instructions>
    - The test name must be unique.
    - The test command must be a valid Tinybird command that can be run in the terminal.
    - The test command can have as many parameters as are needed to test the pipe.
    - The parameter within Tinybird templating syntax looks like this one {{String(my_param_name, default_value)}}.
    - If there are no parameters in the , you can omit parametrs and generate a single test command.
    - Extra context: {prompt}
</instructions>
"""

test_create_prompt = """
You are a Tinybird expert. You will be given a pipe containing different nodes with SQL and Tinybird templating syntax. You will generate URLs to test it with different parameters combinations.
<pipe>
    <name>{name}</name>
    <content>{content}</content>
    <parameters>{parameters}</parameters>
</pipe>

<instructions>
    - Every test name must be unique.
    - The test command must be a valid Tinybird command that can be run in the terminal.
    - The test command can have as many parameters as are needed to test the pipe.
    - The parameter within Tinybird templating syntax looks like this one {{String(my_param_name, default_value)}}.
    - If there are no parameters, you can omit parameters and generate a single test command.
    - The format of the parameters is the following: ?param1=value1&param2=value2&param3=value3
</instructions>

Follow the instructions and generate the following response with no additional text:

<response>
    <test>
        <name>[test name here]</name>
        <description>[test description here]</description>
        <parameters>[parameters here]</parameters>
    </test>
</response>
"""


def create_prompt(existing_resources: str) -> str:
    return """
You are a Tinybird expert. You will be given a prompt to generate Tinybird resources: datasources and/or pipes.
<existing_resources>
{existing_resources}
</existing_resources>
<datasource_file_instructions>
    - The datasource names must be unique.
    - No indentation is allowed for property names: DESCRIPTION, SCHEMA, ENGINE, ENGINE_PARTITION_KEY, ENGINE_SORTING_KEY, etc.
</datasource_file_instructions>
<pipe_file_instructions>
    - The pipe names must be unique.
    - Nodes do NOT use the same name as the Pipe they belong to. So if the pipe name is "my_pipe", the nodes must be named different like "my_pipe_node_1", "my_pipe_node_2", etc.
    - Nodes can't have the same exact name as the Pipe they belong to.
    - Avoid more than one node per pipe unless it is really necessary or requested by the user.
    - No indentation is allowed for property names: DESCRIPTION, NODE, SQL, TYPE, etc.
    - Endpoints can export Prometehus format, Node sql must have name two columns: 
        - name (String): The name of the metric 
        - value (Number): The numeric value for the metric. 
    - and then some optional columns:
        - help (String): A description of the metric.
        - timestamp (Number): A Unix timestamp for the metric.
        - type (String): Defines the metric type (counter, gauge, histogram, summary, untyped, or empty).
        - labels (Map(String, String)): A set of key-value pairs providing metric dimensions.
    - Use prometheus format when you are asked to monitor something
</pipe_file_instructions>
<sql_instructions>
    - The SQL query must be a valid ClickHouse SQL query that mixes ClickHouse syntax and Tinybird templating syntax (Tornado templating language under the hood).
    - SQL queries with parameters must start with "%" character and a newline on top of every query to be able to use the parameters. Examples:
    <invalid_query_with_parameters_no_%_on_top>
    SELECT * FROM events WHERE session_id={{{{String(my_param, "default_value")}}}}
    </invalid_query_with_parameters_no_%_on_top>
    <valid_query_with_parameters_with_%_on_top>
    %
    SELECT * FROM events WHERE session_id={{{{String(my_param, "default_value")}}}}
    </valid_query_with_parameters_with_%_on_top>
    - The Parameter functions like this one {{{{String(my_param_name,default_value)}}}} can be one of the following: String, DateTime, Date, Float32, Float64, Int, Integer, UInt8, UInt16, UInt32, UInt64, UInt128, UInt256, Int8, Int16, Int32, Int64, Int128, Int256
    - Parameter names must be different from column names. Pass always the param name and a default value to the function.
    - Code inside the template {{{{template_expression}}}} follows the rules of Tornado templating language so no module is allowed to be imported. So for example you can't use now() as default value for a DateTime parameter. You need an if else block like this:
    <invalid_condition_with_now>
    AND timestamp BETWEEN {{DateTime(start_date, now() - interval 30 day)}} AND {{DateTime(end_date, now())}}
    </invalid_condition_with_now>
    <valid_condition_without_now>
    {{%if not defined(start_date)%}}
    timestamp BETWEEN now() - interval 30 day
    {{%else%}}
    timestamp BETWEEN {{{{DateTime(start_date)}}}}
    {{%end%}}
    {{%if not defined(end_date)%}}
    AND now()
    {{%else%}}
    AND {{{{DateTime(end_date)}}}} 
    {{%end%}}
    </valid_condition_without_now>
    - Use datasource names as table names when doing SELECT statements.
    - Do not use pipe names as table names.
    - The available datasource names to use in the SQL are the ones present in the existing_resources section or the ones you will create.
    - Use node names as table names only when nodes are present in the same file.
    - Do not reference the current node name in the SQL.
    - SQL queries only accept SELECT statements with conditions, aggregations, joins, etc.
    - Do NOT use CREATE TABLE, INSERT INTO, CREATE DATABASE, etc.
    - Use ONLY SELECT statements in the SQL section.
    - INSERT INTO is not supported in SQL section.
    - General functions supported are: {general_functions}
    - Character insensitive functions supported are: {general_functions_insensitive}
    - Aggregate functions supported are: {aggregate_functions}
    - Do not use any function that is not present in the list of general functions, character insensitive functions and aggregate functions.
    - If the function is not present in the list, the sql query will fail, so avoid at all costs to use any function that is not present in the list.
    - When aliasing a column, use first the column name and then the alias.
    - General functions and aggregate functions are case sensitive.
    - Character insensitive functions are case insensitive.
</sql_instructions>

<datasource_content>
DESCRIPTION >
    Some meaningful description of the datasource

SCHEMA >
    `column_name_1` clickhouse_tinybird_compatible_data_type `json:$.column_name_1`,
    `column_name_2` clickhouse_tinybird_compatible_data_type `json:$.column_name_2`,
    ...
    `column_name_n` clickhouse_tinybird_compatible_data_type `json:$.column_name_n`

ENGINE "MergeTree"
ENGINE_PARTITION_KEY "partition_key"
ENGINE_SORTING_KEY "sorting_key_1, sorting_key_2, ..."
</datasource_content>
<pipe_content>
DESCRIPTION >
    Some meaningful description of the pipe

NODE node_1
SQL >
    [sql query using clickhouse syntax and tinybird templating syntax and starting always with SELECT or %\nSELECT]

</pipe_content>

Use the following format to generate the response and do not wrap it in any other text, including the <response> tag.

<response>
    <resource>
        <type>[datasource or pipe]</type>
        <name>[resource name here]</name>
        <content>[resource content here]</content>
    </resource>
</response>

""".format(
        existing_resources=existing_resources,
        general_functions=general_functions,
        general_functions_insensitive=general_functions_insensitive,
        aggregate_functions=aggregate_functions,
    )


def mock_prompt(rows: int) -> str:
    return f"""
Given the schema for a Tinybird datasource, return a can you create a clickhouse sql query to generate some random data that matches that schema.

Response format MUST be just a valid clickhouse sql query.

<example>
    <example_datasource_schema>
SCHEMA >
    experience_gained Int16 `json:$.experience_gained`,
    level Int16 `json:$.level`,
    monster_kills Int16 `json:$.monster_kills`,
    player_id String `json:$.player_id`,
    pvp_kills Int16 `json:$.pvp_kills`,
    quest_completions Int16 `json:$.quest_completions`,
    timestamp DateTime `json:$.timestamp`
    </example_datasource_schema>
    <example_output>

SELECT
    rand() % 1000 AS experience_gained, -- Random experience gained between 0 and 999
    1 + rand() % 100 AS level,          -- Random level between 1 and 100
    rand() % 500 AS monster_kills,      -- Random monster kills between 0 and 499
    concat('player_', toString(rand() % 10000)) AS player_id, -- Random player IDs like "player_1234"
    rand() % 50 AS pvp_kills,           -- Random PvP kills between 0 and 49
    rand() % 200 AS quest_completions,  -- Random quest completions between 0 and 199
    now() - rand() % 86400 AS timestamp -- Random timestamp within the last day
FROM numbers({rows})
    </example_output>
</example>

<instructions>
- The query MUST return a random sample of data that matches the schema.
- The query MUST return a valid clickhouse sql query.
- The query MUST return a sample of EXACTLY {rows} rows.
- The query MUST be valid for clickhouse and Tinybird.
- FROM numbers({rows}) part is mandatory.
- Do NOT include ```clickhouse or ```sql or any other wrapping text to the sql query.
- Do NOT use any of these functions: elementAt
- Do NOT add a semicolon at the end of the query
- Do NOT add any FORMAT at the end of the query, because it will be added later by Tinybird.
- General functions supported are: {general_functions}
- Character insensitive functions supported are: {general_functions_insensitive}
- Aggregate functions supported are: {aggregate_functions}
- Do not use any function that is not present in the list of general functions, character insensitive functions and aggregate functions.
- If the function is not present in the list, the sql query will fail, so avoid at all costs to use any function that is not present in the list.
</instructions>

<more_examples>
# Examples with different schemas, like an array field or a nested JSON field:

## Example schema with an array field:

### Schema:

SCHEMA >
    `order_id` UInt64 `json:$.order_id`,
    `customer_id` UInt64 `json:$.customer_id`,
    `order_date` DateTime `json:$.order_date`,
    `total_amount` Float64 `json:$.total_amount`,
    `items` Array(String) `json:$.items[:]` // This is an array field 

### Desired final output of the query:
{{
  "order_id": 123456,
  "customer_id": 7890,
  "order_date": "2024-11-30T10:30:00.000Z",
  "total_amount": 150.0,
  "items": ["item1", "item2", "item3"]
}}

### Example SQL output with an array field:

SELECT
  concat('ord_', toString(rand() % 10000)) AS order_id,
  concat('cust_', toString(rand() % 10000)) AS customer_id,
  now() - rand() % 86400 AS order_date,
  rand() % 1000 AS total_amount,
  arrayMap(x -> concat('item_', toString(x)), range(1, rand() % 5 + 1)) AS items
FROM numbers(ROWS)

## Example schema with a nested JSON field:

### Schema:

SCHEMA >
    `request_id` String `json:$.request_id`,
    `timestamp` DateTime `json:$.timestamp`,
    `model` String `json:$.request.model`,
    `temperature` Float32 `json:$.request.options.temperature`,
    `max_tokens` UInt32 `json:$.request.options.max_tokens`,
    `stream` UInt8 `json:$.request.options.stream`

### Desired final output of the query:

Note that the important part is generating the nested fields:
json:$.request.options.max_tokens > this means that the max_tokens field is nested inside the options field inside the request field.

{{
  "request_id": "req_abc123",
  "timestamp": "2024-11-30T10:30:00.000Z",
  "request": {{
    "model": "gpt-4",
    "options": {{
      "temperature": 0.7,
      "max_tokens": 1000,
      "stream": false
    }}
  }}
}}

### Example SQL output with nested fields:

SELECT
    request_id,
    timestamp,
    CAST(concat('{{
        "model": "', model, '",
        "options": {{
            "temperature": ', temperature, ',
            "max_tokens": ', max_tokens, ',
            "stream": ', IF(stream = 1, 'true', 'false'), '
        }}
    }}'), 'JSON') AS request
FROM
(
    SELECT
        concat('req_', lower(hex(randomString(6)))) AS request_id,
        (now() - toIntervalDay(rand() % 30)) + toIntervalSecond(rand() % 86400) AS timestamp,
        ['gpt-4', 'gpt-3.5-turbo', 'gpt-4-turbo'][(rand() % 3) + 1] AS model,
        round(rand() / 10, 2) AS temperature,
        500 + (rand() % 2500) AS max_tokens,
        rand() % 2 AS stream
    FROM numbers(ROWS)
)
</more_examples>

Follow the instructions and generate the following response with no additional text in the following format:
<response>
    <sql>[raw sql query here]</sql>
</response>
"""
