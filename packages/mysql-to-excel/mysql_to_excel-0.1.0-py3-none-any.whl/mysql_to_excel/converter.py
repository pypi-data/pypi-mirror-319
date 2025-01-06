from dataclasses import dataclass
import mysql.connector
import pandas as pd

@dataclass
class MySQLConfig:
    host: str
    user: str
    password: str
    database: str

def convert_to_excel(config: MySQLConfig, table: str = None, output_file: str = None, columns: list = None):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )

        # Determine output file name
        if not output_file:
            output_file = f'{table if table else config.database}.xlsx'

        # Create Excel writer
        with pd.ExcelWriter(output_file) as writer:
            if table:
                # Fetch data from specified table
                columns_str = ', '.join(columns) if columns else '*'
                query = f'SELECT {columns_str} FROM {table}'
                data = pd.read_sql(query, conn)
                data.to_excel(writer, index=False)
            else:
                # Fetch data from all tables
                cursor = conn.cursor()
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                for (tbl_name,) in tables:
                    query = f'SELECT * FROM {tbl_name}'
                    data = pd.read_sql(query, conn)
                    data.to_excel(writer, sheet_name=tbl_name, index=False)
                
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    except ValueError as ve:
        print(f"Value Error: {ve}")
    except IOError as ioe:
        print(f"I/O Error: {ioe}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()