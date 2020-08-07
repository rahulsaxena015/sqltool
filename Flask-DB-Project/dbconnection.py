import pyodbc
import json
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:or1010050154084'
database = 'HostedTesting'
username = 'hornet'
password = 'hornet'


class DBConnection():
    def __init__(self, query):
        self.query = query

    def db_query(self):
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                              server+';DATABASE='+database+';UID='+username+';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute(self.query)
        rows = cursor.fetchall()
        table_data = []
        for row in rows:
            table_data.append(list(row))
        query_data = json.dumps(table_data)
        print(type(query_data))
        print(query_data)
        cursor.close()
        return query_data


        # print(row)
if __name__ == "__main__":
    query = "SELECT top 20 * from pps_scos where name like '%template%' FOR JSON AUTO;"
    result = DBConnection(query)
    print(F"{result.db_query()}")
