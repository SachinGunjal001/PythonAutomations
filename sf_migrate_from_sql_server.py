import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pyodbc as pyo
import pandas as pd

print('opening sql server..')

cnn_sql = (
    r"Driver={SQL Server};"
    r"Server=SACHIN\SQLEXPRESS;"
    r"Database=bankDB;"
    r"Trusted_Connection=yes;"
)

cnn = pyo.connect(cnn_sql)
print('opened..')

sql = "SELECT * from Dim_customer ;"
df = pd.read_sql(sql, cnn)

print(df.head(10))
print(df.tail(10))

cnn.close()
print('sql server closed..')


print('create snowflake table..')

sql = """
CREATE TABLE Dim_customer (
    customer_id Number,
    customer_type nvarchar(100),
    segment nvarchar(100),
    risk_category nvarchar(100),
    branch_id NUMBER,
    city nvarchar(50),
    state nvarchar(50),
    region nvarchar(50),    
    branch_type nvarchar(50)
   
);
"""
scnn = snowflake.connector.connect(
    user='GUNJAL',
    password='SachinGunjal@123',
    account='KYJZBXP-SD79035',
    warehouse='COMPUTE_WH',
    database='BANKDB',
    schema='project_schema'
)

cs = scnn.cursor()
cs.execute(sql) 

print('writing to snowflake table..')

success, nchunks, nrows, _ = write_pandas(
    scnn,
    df,
    'Dim_customer',
    quote_identifiers=False
)

print('get some data..')

sql = "SELECT * FROM Dim_customer LIMIT 10;"
cs.execute(sql)

df_result = cs.fetch_pandas_all()

scnn.close()

print(df_result)
print('operation complete.')