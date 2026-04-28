{% macro generate_schema_name(custom_schema_name, node) -%}
    {#- 
        Jika kita letak +schema dalam dbt_project.yml, 
        kod ni akan paksa dbt guna nama tu SAHAJA (tanpa 'silver_')
    -#}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}