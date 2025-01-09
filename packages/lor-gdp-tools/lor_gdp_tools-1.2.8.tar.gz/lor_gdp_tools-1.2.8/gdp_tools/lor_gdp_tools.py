# from dotenv import load_dotenv
import subprocess
import getpass
from io import StringIO
from pathlib import Path
import pandas as pd
import pyodbc

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azureml.core import Dataset

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

# from tests import test_deffined_connection

class GlobalDataPlatformTools:
    """
    This package will support you in accessing, and working with data from the GDP.
    It's functional requirements are:
    - Accessing data on GDP Base/CIM/Warehouse
    - Accessing data in temp storage (LAB)
    - Querying that data in SQL
    - utlising that data as a Python/PySpark DataFrame
    - Storing processed data to the temp storage space (LAB)

    Note on publishing the package on PyPI:
    - pip install twine
    - rm -r build/ dist/
    - python setup.py sdist bdist_wheel
    - twine upload -u __token__ -p [PYPI API KEY - in ENV file] dist/*
    """

    def __init__(self, SERVER: str, DATABASE: str, USERNAME: str, PASSWORD: str):
        """
        Initialise the module with key credentials and locations.
        Comtact the LOR Data Science Team to get hold of these
        """

        # Access the variables
        self.SERVER = SERVER
        self.DATABASE = DATABASE  # Location of Synapse
        self.USERNAME = USERNAME  # user entry
        self.PASSWORD = PASSWORD  # user entry
        self.AUTH = "ActiveDirectoryInteractive"  # aka Azure Active Directory - Universal with MFA

        print(f"using credentials of {self.USERNAME}")

        # deffine connectors
        self.validate_odbc_drivers()
        self.setup_odbc_connection()

        # storage container details
        self.blob_account_url = "https://azstgdpdlpreproduks.blob.core.windows.net"
        self.container = "data-lake"

    def validate_odbc_drivers(self,):
        """
        Check if the ODBC Driver 18 for SQL Server is installed, if not install it
        """
        if not self.check_odbc_driver():
            self.install_odbc_driver()

    def check_odbc_driver(self,):
        """
        # Check if the ODBC Driver 18 for SQL Server is installed
        """
        try:
            
            result = subprocess.run(
                ["odbcinst", "-q", "-d"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if "ODBC Driver 18 for SQL Server" in result.stdout:
                print("ODBC Driver 18 for SQL Server is already installed.")
                return True
            else:
                print("ODBC Driver 18 for SQL Server is not installed.")
                return False
        except FileNotFoundError:
            print("odbcinst command not found. Please install unixODBC.")
            return False

    def install_odbc_driver(self,):
        """
        # Install the ODBC driver
        """
        try:
            # Add the Microsoft repository key
            subprocess.run(
                "curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -",
                shell=True,
                check=True,
            )

            # Add the Microsoft repository
            subprocess.run(
                "sudo sh -c 'curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list -o /etc/apt/sources.list.d/mssql-release.list'",
                shell=True,
                check=True,
            )

            # Update package list
            # subprocess.run("sudo apt-get update",shell=True, check=True)

            # Install the ODBC driver
            subprocess.run(
                "sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18",
                shell=True,
                check=True,
            )

            print("ODBC Driver 18 for SQL Server has been installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while installing the ODBC driver: {e}")

    def setup_odbc_connection(self,):
        """
        # https://learn.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver16
        # https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module#connect
        # https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-connect-overview

        # Setup connection using ODBC Driver
        """
        connectionString = f"""
                             DRIVER={{ODBC Driver 18 for SQL Server}};
                             SERVER=tcp:{self.SERVER};
                             DATABASE={self.DATABASE};
                             UID={self.USERNAME};
                             PWD={self.PASSWORD};
                             Encrypt=yes;
                             TrustServerCertificate=no;
                             Connection Timeout=30;
                            """

        # SQL Server Native Client 11.0
        try:
            self.conn = pyodbc.connect(connectionString)
            print("Connected Successfully")
        except Exception as e:
            print("Connection failed: ", e)

    def query_gdp_to_pd(self, sql_query: str):
        """
        Input: user enters a SQL query as a string
        Output: returns a python dataframe
        """
        # test if connection is deffined
        # test_deffined_connection(self.conn)

        return pd.read_sql(sql_query, self.conn)

    def list_schema(self):
        """
        Output:
        - df - list of schema within the database
        """

        sql_query = f"""
        SELECT distinct table_schema
        FROM information_schema.tables
        """
        return pd.read_sql(sql_query, self.conn)

    def search_tables(self, **kwargs):
        """
        table_schema = 'BASE', table_type = 'BASE TABLE',

        Input:
        - database: str - take 'BASE' as a default (as opposed to CIM)
        - Kwargs:
            - source_system = str - deffine a source system to reffine the search to certain term
        Output:
        - df - list of tables within the database
        """

        source_system = kwargs.get("source_system", None)
        if source_system:
            source_system_condition = f"table_name like '%{source_system}%'"
            print(f"Searching for tables like {source_system}")
        else:
            source_system_condition = ""

        sql_query = f"""
        SELECT 
        table_type as 'table_type',
        table_schema as 'table_schema',
        table_name
        FROM information_schema.tables
        WHERE 1=1 
        -- AND table_type = 'BASE TABLE' 
        -- AND table_schema = 'BASE' 
        AND {source_system_condition};
        """

        print(sql_query)
        return pd.read_sql(sql_query, self.conn)

    def save_df_to_lab_storage(self,
                                df,
                                user_dir: str,
                                project_dir: str,
                                file_name: str,
                                raw_bool: bool):
        """
        upload a pandas dataframe into Azure Blob Storage

        input:
        - df - pandas data frame
        - user_dir - of the form 'DRumble'
        - project_dir - any string
        - file_name - must include '.csv'
        - raw_bool - if True the data will be stored as 'raw' else 'processed'
        """
        if raw_bool is True:
            data_stage = "raw"
        else:
            data_stage = "processed"

        # convert the pandas dataframe into a .csv and store locally
        local_filepath = Path(f"data/{data_stage}/{file_name}")
        df.to_csv(local_filepath, index=False)

        # Azure credentials, this will automatically work in a compute
        credential = DefaultAzureCredential()

        lab_filename = f"LAB/{user_dir}/{project_dir}/data/{data_stage}/{file_name}"

        blob_client = (
            BlobServiceClient(account_url=self.blob_account_url, credential=credential)
            .get_container_client(container=self.container)
            .get_blob_client(blob=lab_filename)
        )

        # Read in the local file to upload it
        with open(local_filepath, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"data stored in lab location: {lab_filename}")

    def load_df_from_lab(self,
                         user_dir: str,
                         project_dir: str,
                         file_name: str,
                         raw_bool: bool):
        """
        read data from blob storage and load it as a pandas dataframe

        input
        - user_dir - of the form 'DRumble'
        - project_dir - any string
        - file_name - must include '.csv'
        - raw_bool - if True the data will be stored as 'raw' else in 'processed'
        """
        if raw_bool is True:
            data_stage = "raw"
        else:
            data_stage = "processed"

        lab_filename = f"LAB/{user_dir}/{project_dir}/data/{data_stage}/{file_name}"
        web_filepath = f"{self.blob_account_url}/{self.container}/{lab_filename}"
        print(web_filepath)
        data = Dataset.Tabular.from_delimited_files(path=web_filepath)
        return data.to_pandas_dataframe()

    def load_df_from_sharepoint(self,
                                sharepoint_url: str):
        """
        read data from MSO365 Sharepoint and load it as a pandas dataframe.

        Currently restrcited by AD Group

        Input:
        - sharepoint_url - string, copied directly from sharepoint

        """
        # capture credentials manually
        username = getpass.getpass("Enter your Email: ")
        password = getpass.getpass("Enter your password: ")

        # Authentication
        ctx_auth = AuthenticationContext(sharepoint_url)
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(sharepoint_url, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()
            print("Authenticated into SharePoint site:", web.properties["Title"])
        else:
            print("Authentication failed")

        # Download the file
        response = ctx.web.get_file_by_server_relative_url(sharepoint_url).download()
        ctx.execute_query()

        # Load the file content into a pandas DataFrame
        file_content = StringIO(response.content.decode("utf-8"))
        return pd.read_csv(file_content)
