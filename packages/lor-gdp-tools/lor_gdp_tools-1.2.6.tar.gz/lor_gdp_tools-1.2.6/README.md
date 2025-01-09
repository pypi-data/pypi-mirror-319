# Gdp Tools Package

[![Code Checks](https://github.com/laingorourke/gdp-tools/actions/workflows/code-checks.yml/badge.svg)](https://github.com/laingorourke/gdp-tools/actions/workflows/code-checks.yml)
[![Code Style](https://img.shields.io/badge/Code%20Style-flake8-blue)](https://flake8.pycqa.org/)

This is a utility package designed to enable data scientists and analysts to easily access GDP data within a python environment

Requirements:
- The data professional should be able to clone the package at the start of new project and when in production
- The package will contain a number of support functions serving the following objectives:
-- Accessing data on GDP Base/CIM/Warehouse 
-- Accessing data in temp storage (LAB)
-- Querying that data in SQL
-- utlising that data as a Python/PySpark DataFrame
-- Storing processed data to the temp storage space (LAB)
- any data access configs should available to be used 


## Credentials

Contact a member of the Laing O'Rourke Data Science team to set up up your credentials.

SERVER, DATABASE, USERNAME and PASSWORD need to be entered in as arguments when initailising the tool, for example '''gdp_tools = GlobalDataPlatformTools(SERVER, DATABASE, USERNAME,PWD)'''

The designation of SERVER and DATABASE will determining if you are accessing PROD or PREPROD data. It is strongly advised to PREPROD to avoid interfering with PROD systems. 

## Functionality

Should be used in Azure ML Studio. NO access to GDP locally. Generally functionality covers:

v0
- check/install drivers
- search GDP by table name
- query GDP with SQL

v1
- load/test a LLM
- access to CIM and Warehouse data
- store data
- access data from share point


### GDP Tools

This module contains tools for accessing and storing data in the GDP.

The module will likely break if you use some of these functions successively. When changing between functionality, re-initialise the module with '''gdp_tools = GlobalDataPlatformTools(SERVER, DATABASE, USERNAME,PWD)'''

**validate_odbc_drivers** - check if the correct ODBC connectors are installed, install them as necessary automatically [**check_odbc_driver**, **install_odbc_driver**] 

**setup_odbc_connection** - set up the ODBC with your credentials. Happens when class is initalised

**query_gdp_to_pd** - enter a SQL query as a string, return the data as a pandas dataframe

**search_tables** - will return a list of all table in the GDP. give it the argument 'source_system' = '[COINS]' to narrow your search for any table with the term 'COINS' in it (for example). Will also return the corresponding schema name and table type. 

**list_schema** - list all available schema. This typically will include BASE, CIM and WAREHOUSE and variants on those.


### LLM Tools

This module contains tools for access LOR LLM API end points

These methods require the following credentials, to be entered manually as arguments when initailised, for example '''llm = LORLargeLanguageModels(api_key,azure_endpoint)'''. Contact a member of the Data Science team to obtain these seperately. 

**tell_me_about_the_models_that_are_available** -  This function returns a pandas table with information about the models available. It covers cost, performance and accuracy. The numbers here were pulled from Chat GPT and checked, but may not be 100% accurate. 

**llm_architecture** - the default architecture for using a chat gpt model. Takes guidence, prompt and the name of the model as strings.

**test_llm** - testing function, works for the pre-deffined list of models and a simple UAT prompt 'What is 2+2?'

