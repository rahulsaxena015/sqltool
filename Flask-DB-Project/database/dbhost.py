import yaml
import pyodbc
import sys

username = 'user'
password = 'password!'

filename = "database/db.yaml"
with open(filename, "r") as f:
    file_db = yaml.safe_load(f)


def db_host(cluster):
    db_host = str(file_db[cluster]['dbhost'])
    db_name = str(file_db[cluster]['dbname'])
    try:
        # con = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server}; Server=' + db_host +
        #         '; Database=master; uid=ssrs; pwd=' + password + '')
        con = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                             db_host+';DATABASE='+db_name+';UID='+username+';PWD=' + password)
        print('+=========================+')
        print('|  CONNECTED TO DATABASE  |')
        print('+=========================+')
    except Exception as e:
        sys.exit(e)
    cur = con.cursor()
    print(db_host, db_name)
    return db_host, db_name, cur


# if __name__ == "__main__":
#     cluster = "na2"
#     db_host(cluster)
