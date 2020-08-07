from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pyodbc
import urllib
import pymysql
import sys
import json
import pandas

app = Flask(__name__)

server = 'tcp:or1010050154084'
database = 'HostedTesting'
username = 'user'
password = 'password'

try:
    con = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                         server+';DATABASE='+database+';UID='+username+';PWD=' + password)
    print('+=========================+')
    print('|  CONNECTED TO DATABASE  |')
    print('+=========================+')
except Exception as e:
    sys.exit(e)
cur = con.cursor()


@app.route('/')
def index():
    return render_template('index.html')

rows = ""


def parse(query_output):
    result = ""
    # print(query_output)
    for i in query_output:
        if len(i) > 0:
            result += i[0]
    result = json.loads(result)
    # result = json.dumps(result)
    print("I am here")
    print(type(result))
    return result


@app.route('/query', methods=['GET', 'POST'])
def get_query():
    table_data = []
    query_data = ""
    temp = ""
    df = ""
    if request.method == 'POST':
        sql_query = request.form['sqlquery']
        print(sql_query)
        sql_query = sql_query + ' FOR JSON AUTO'
        print(sql_query)
        df = pandas.read_sql_query(sql_query, con)
        df_new = pandas.DataFrame(df)
        print(df_new)
        print(type(df_new))
        cur.execute(sql_query)
        rows = cur.fetchall()
        table_data = []
        for row in rows:
            table_data.append(list(row))
        query_data = json.dumps(table_data)
        print(type(query_data))
        query_output = json.loads(query_data)
        print(type(query_output))

        temp = parse(query_output)
        # print(F"{temp}")
    # cur.close()
    # dict([d for i in temp for d in i.items()])

    # return render_template('query.html', query_data=temp)
    return render_template('query.html', tables=[df_new.to_html(classes='data', header="true")])
    cur.close()


if __name__ == "__main__":
    app.run(debug=True)

# Below are the links to be referred
# https://www.encodedna.com/javascript/practice-ground/default.htm?pg=convert_json_to_table_javascript
