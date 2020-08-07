from flask import Flask, render_template, request, redirect, session, url_for, jsonify, flash, session
from flask_ldap3_login import LDAP3LoginManager
from flask_login import login_user, logout_user, login_manager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pyodbc
import pymysql
import yaml
import sys
import json
import pandas
from models import authenticate
from database.dbhost import *

app = Flask(__name__)

app.secret_key = 'asdsdfsdfs13sdf_df%&'

server_uri="ldaps://ldap.loc.adobe.net:636"
domain = "adobe.com"
attributes = ['*']

cluster_list = ['apac1', 'na1', 'na2', 'na3', 'na4', 'na5', 'na6', 'na7', 'na8', 'na9', 'na10', 'na11', 'na12', 'na13', 'emea1', 'emea2', 'emea3',
                'emea4', 'emea5', 'emea6']


@ app.route("/", methods=['POST'])
def login():
    # context = {}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            auth = authenticate(server_uri, domain, username, password)
            print(username)
            display_name = auth
            session['logged_in'] = True
            session['display_name'] = display_name
            session['username'] = username
            return redirect(url_for('query_output'))
        except ValueError as err:
            print(err)

    return render_template("login.html")


@app.route('/query')
def query_output():
    if session.get('logged_in'):
        display_name = session.get('display_name')
        username = session.get('username')
        return render_template('query.html', display_name=display_name, username=username, cluster_list=cluster_list)
    return redirect(url_for('index'))


@ app.route('/logout')
def logout():
    session['logged_in'] = False
    # logout_user()
    return redirect(url_for('index'))


@ app.route('/')
def index():
    login = False
    if 'username' in session:
        login = True
    return render_template('login.html', login=login)


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


@ app.route('/query', methods=['GET'])
def get_query():
    return render_template('query.html')


@ app.route('/query1', methods=['POST'])
def run_query():
    table_data = []
    query_data = ""
    temp = ""
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    # pandas.set_option('colheader_justify', 'center')
    # df = pandas.DataFrame()
    # df_new = pandas.DataFrame()
    if request.method == 'POST':
        clid = request.form.get("cluster")
        print(F"Selected cluster is: {clid}")
        db_value = db_host(clid)
        print(db_value)
        print(F"DB Host is: {db_value[0]}")
        print(F"DB Name is: {db_value[1]}")
        cur = db_value[2]
        try:
            sql_query = request.form['sqlquery']
            sql_query = sql_query + ' FOR JSON AUTO, INCLUDE_NULL_VALUES'
            print(sql_query)
            cur.execute(sql_query)
        except pyodbc.Error as ex:
            err = ex.args[0]
            print(type(err))
            print(
                F"There is an error processing your request. Please check your query >> {err}")
            # sys.exit(1)
            return render_template("query.html", err=err)
        rows = cur.fetchall()
        for row in rows:
            table_data.append(list(row))
        query_data = json.dumps(table_data)
        query_output = json.loads(query_data)
        temp = parse(query_output)
        print((temp))
        # tables = pandas.DataFrame.from_records(temp).to_html(
        #     classes='table table-striped table-hover table-sm table-responsive')
        cur.close()
    return jsonify(temp)


# @app.route('/query', methods=['GET', 'POST'])
# def get_query():
#     table_data = []
#     query_data = ""
#     temp = ""
#     pandas.set_option('colheader_justify', 'center')
#     df = pandas.DataFrame()
#     df_new = pandas.DataFrame()
#     if request.method == 'POST':
#         clid = request.form.get("cluster")
#         print(F"Selected cluster is: {clid}")
#         db_value = db_host(clid)
#         print(db_value)
#         print(F"DB Host is: {db_value[0]}")
#         print(F"DB Name is: {db_value[1]}")
#         cur = db_value[2]
#         sql_query = request.form['sqlquery']
#         sql_query = sql_query + ' FOR JSON AUTO, INCLUDE_NULL_VALUES'
#         print(sql_query)
#         cur.execute(sql_query)
#         rows = cur.fetchall()
#         for row in rows:
#             table_data.append(list(row))
#         query_data = json.dumps(table_data)
#         query_output = json.loads(query_data)
#         temp = parse(query_output)
#         print((temp))
#         tables = pandas.DataFrame.from_records(temp).to_html(
#             classes='table table-striped table-hover table-sm table-responsive')
#     return render_template('query.html', tables=tables)
#     # return render_template('query.html', temp=temp)
#     cur.close()
if __name__ == "__main__":
    app.run(debug=True)
