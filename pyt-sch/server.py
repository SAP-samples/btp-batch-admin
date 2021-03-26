"""
CF/XSA Python buildpack app example
Author: Andrew Lunde
"""
from flask import Flask
from flask import request
from flask import Response

from flask import send_from_directory
#   
import os
#import pyhdb
# Downloading pyhdb-0.3.3.tar.gz
import json
import datetime
#import Crypto.PublicKey.RSA as RSA
#import jws.utils
#import python_jwt as jwt
#https://help.sap.com/viewer/4505d0bdaf4948449b7f7379d24d0f0d/2.0.03/en-US/8732609bd5314b51a17d6a3cc09110c3.html#loio8732609bd5314b51a17d6a3cc09110c3__section_atx_2vt_vt
from sap import xssec
from cfenv import AppEnv
#
#from sap.cf_logging import flask_logging
#
#https://help.sap.com/viewer/0eec0d68141541d1b07893a39944924e/2.0.03/en-US/d12c86af7cb442d1b9f8520e2aba7758.html
from hdbcli import dbapi

import platform

app = Flask(__name__)
env = AppEnv()

# Get port from environment variable or choose 9099 as local default
# If you are testing locally (i.e. not with xs or cf deployments,
# Be sure to pull all the python modules locally 
#   with pip using XS_PYTHON unzipped to /tmp
# mkdir -p local
# pip install -t local -r requirements.txt -f /tmp
port = int(os.getenv("PORT", 9099))
hana = env.get_service(label='hana')

def attach(port, host):
    try:
        print("pydevd attached.")
        import pydevd
        pydevd.stoptrace() #I.e.: disconnect if already connected
        # pydevd.DebugInfoHolder.DEBUG_RECORD_SOCKET_READS = True
        # pydevd.DebugInfoHolder.DEBUG_TRACE_BREAKPOINTS = 3
        # pydevd.DebugInfoHolder.DEBUG_TRACE_LEVEL = 3
        pydevd.settrace(
            port=port,
            host=host,
            stdoutToServer=True,
            stderrToServer=True,
            overwrite_prev_trace=True,
            suspend=False,
            trace_only_current_thread=False,
            patch_multiprocessing=False,
        )
    except:
        import traceback;traceback.print_exc() 
        
        
# This module's Flask webserver will respond to these three routes (URL paths)
# If there is no path then just return Hello World and this module's instance number
# Requests passed through the app-router will never hit this route.
@app.route('/')
@app.route('/pyt-sch/')
def hello_world():
    output = '<strong>Hello World! I am instance ' + str(os.getenv("CF_INSTANCE_INDEX", 0)) + '</strong> Try these links.</br>\n'
    output += '<a href="/pyt-sch/env">/pyt-sch/env</a><br />\n'
    output += '<a href="/pyt-sch/test">/pyt-sch/test</a><br />\n'
    output += '<a href="/pyt-sch/create_table">/pyt-sch/create_table</a><br />\n'
    output += '<a href="/pyt-sch/insert_data">/pyt-sch/insert_data</a><br />\n'
    output += '<a href="/pyt-sch/select_data">/pyt-sch/select_data</a><br />\n'
    output += '<a href="/pyt-sch/delete_data">/pyt-sch/delete_data</a><br />\n'
    output += '<a href="/pyt-sch/drop_table">/pyt-sch/drop_table</a><br />\n'

    return output
    
# Satisfy browser requests for favicon.ico so that don't return 404
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/env')
@app.route('/pyt-sch/env')
def dump_env():
    output = '\n Key Environment variables... \n'
    output += 'PYTHONHOME: ' + str(os.getenv("PYTHONHOME", 0)) + '\n'
    output += 'PYTHONPATH: ' + str(os.getenv("PYTHONPATH", 0)) + '\n'
    output += 'VCAP_SERVICES: ' + str(os.getenv("VCAP_SERVICES", 0)) + '\n'
    output += 'host: ' + hana.credentials['host'] + '\n'
    output += 'port: ' + hana.credentials['port'] + '\n'
    output += 'user: ' + hana.credentials['user'] + '\n'
    output += 'pass: ' + hana.credentials['password'] + '\n'
    output += '\n'
    return output

# If there is a request for a python/test, return Testing message and module's instance number
@app.route('/pyt-sch/test')
def unauth_test():
    return 'Python UnAuthorized Test, Hey! <br />\nI am instance ' + str(os.getenv("CF_INSTANCE_INDEX", 0))

@app.route('/pyt-sch/post', methods=['POST'])
def unauth_post():
    output = 'Python Post to DB (Dangerous!). \n'
    output += '\n'
    output += 'Receiving module should check that it came from our approuter and verify or abort if otherwise.\n'
    output += '\n'

    content = request.json

    output += content

    return Response(output, mimetype='application/json' , status=201,)

@app.route('/pyt-sch/set_env')
def set_pyenv():
    output = 'Set Environment variable... <br />\n'
    if request.args.get('PATHS_FROM_ECLIPSE_TO_PYTHON'):
        output += request.args.get('PATHS_FROM_ECLIPSE_TO_PYTHON')
        os.environ["PATHS_FROM_ECLIPSE_TO_PYTHON"] = request.args.get('PATHS_FROM_ECLIPSE_TO_PYTHON')
        output += '<br />\n'
        output += 'Eclipse paths set for debugging.<br />\n'
        output += '<br />\n'
        output += 'Check that this process has the correct environment.<br />\n'
        output += '<a href="/pyt-sch/env">/pyt-sch/env</a><br />\n'
        output += '<br />\n'
    output += '\n'
    #return Response(output, mimetype='text/plain' , status=200,)
    return output

@app.route('/pyt-sch/env')
def dump_pyenv():
    output = '<pre>Key Environment variables... \n'
    print('env with ' + platform.python_version())
    output += 'PYTHONVERSION: ' + platform.python_version() + '\n'
    output += 'PYTHONHOME: ' + str(os.getenv("PYTHONHOME", 0)) + '\n'
    output += 'PYTHONPATH: ' + str(os.getenv("PYTHONPATH", 0)) + '\n'
    output += 'PATHS_FROM_ECLIPSE_TO_PYTHON: ' + str(os.getenv("PATHS_FROM_ECLIPSE_TO_PYTHON", 0)) + '\n'
    output += '\n'
    intnum = 5
    output += 'intnum = ' + str(intnum) + '\n'
    output += '\n'
    jsonok = json.loads(os.environ.get('PATHS_FROM_ECLIPSE_TO_PYTHON', '[]'))
    if jsonok:
        output += "JSON is OK" + '\n'
        tuples = [tuple(x) for x in jsonok]
        output += '<a href="/pyt-sch/attach">/pyt-sch/attach</a>\n'
    else:
        output += "JSON is NOT OK" + '\n'
        output += '<a href="/pyt-sch/links">/pyt-sch/links</a>\n'
        output += '<a href="/pyt-sch/set_env?PATHS_FROM_ECLIPSE_TO_PYTHON=[[%22/Users/i830671/git/mta_cfs_boost/python%22,%22/home/vcap/app%22]]">/pyt-sch/set_env</a>\n'
    output += 'VCAP_SERVICES: ' + str(os.getenv("VCAP_SERVICES", 0)) + '\n'
    output += 'host: ' + hana.credentials['host'] + '\n'
    output += 'port: ' + hana.credentials['port'] + '\n'
    output += 'user: ' + hana.credentials['user'] + '\n'
    output += 'pass: ' + hana.credentials['password'] + '\n'
    output += '</pre>\n'
    return output

@app.route('/pyt-sch/attach')
def do_attach():
    output = '<pre>\n Attaching to debugger... \n'
    output = '\n Double check that you Eclipse Debug Server is listening on port 5678 and the tunnel is connected. \n'
    attach(5678,"localhost")
    output += '\n Set some breakpoints...\n'
    output += '<a href="/pyt-sch/env">/pyt-sch/env</a> + test breakpoints<br />\n'
    output += '\n</pre>\n'
    return output

@app.route('/pyt-sch/create_table')
def create_table():
    output = 'Python Authorized DB Validated Request. \n'
    output += '\n'
    output += 'Receiving module should check that it came from our approuter and verify or abort if otherwise.\n'
    output += '\n'
    svcs_json = str(os.getenv("VCAP_SERVICES", 0))
    svcs = json.loads(svcs_json)

    # Verify the JWT before proceeding. or refuse to process the request.
    # https://jwt.io/ JWT Debugger Tool and libs for all languages
    # https://github.com/jpadilla/pyjwt/
    # https://github.com/davedoesdev/python-jwt

    uaa_service = env.get_service(label='xsuaa').credentials
    access_token = request.headers.get('authorization')[7:]

    security_context = xssec.create_security_context(access_token, uaa_service)
    isAuthorized = security_context.check_scope('openid')
    if not isAuthorized:
        abort(403)

    output += 'get_logon_name: ' + security_context.get_logon_name() + '\n'
    output += 'get_email: ' + security_context.get_email() + '\n'
    output += 'get_identity_zone: ' + security_context.get_identity_zone() + '\n'

    schema = hana.credentials['schema']
    host = hana.credentials['host']
    port = hana.credentials['port']
    user = hana.credentials['user']
    password = hana.credentials['password']


    output += 'schema: ' + schema + '\n'
    output += 'host: ' + host + '\n'
    output += 'port: ' + port + '\n'
    output += 'user: ' + user + '\n'
    output += 'pass: ' + password + '\n'

    # The certificate will available for HANA service instances that require an encrypted connection
    # Note: This was tested to work with python hdbcli-2.3.112 tar.gz package not hdbcli-2.3.14 provided in XS_PYTHON00_0-70003433.ZIP  
    if 'certificate' in hana.credentials:
        haascert = hana.credentials['certificate']
    
    # Connect to the python HANA DB driver using the connection info
# User for HANA as a Service instances
    if 'certificate' in hana.credentials:
        connection = dbapi.connect(
            address=host,
            port=int(port),
            user=user,
            password=password,
            currentSchema=schema,
            encrypt="true",
            sslValidateCertificate="true",
            sslCryptoProvider="openssl",
            sslTrustStore=haascert
        )
    else:
        connection = dbapi.connect(
            address=host,
            port=int(port),
            user=user,
            password=password,
            currentSchema=schema
        )

    cursor = connection.cursor()
    cursor.execute('CREATE COLUMN TABLE city (zip CHAR(5) PRIMARY KEY, name CHAR (30) NOT NULL, state CHAR(2) NOT NULL)')
    connection.close()
    
    output += 'TABLE city CREATED.\n'

    # Return the results
    return output

@app.route('/pyt-sch/drop_table')
def drop_table():
    output = 'Python Authorized DB Validated Request. \n'
    output += '\n'
    output += 'Receiving module should check that it came from our approuter and verify or abort if otherwise.\n'
    output += '\n'
    svcs_json = str(os.getenv("VCAP_SERVICES", 0))
    svcs = json.loads(svcs_json)

    # Verify the JWT before proceeding. or refuse to process the request.
    # https://jwt.io/ JWT Debugger Tool and libs for all languages
    # https://github.com/jpadilla/pyjwt/
    # https://github.com/davedoesdev/python-jwt

    uaa_service = env.get_service(label='xsuaa').credentials
    access_token = request.headers.get('authorization')[7:]

    security_context = xssec.create_security_context(access_token, uaa_service)
    isAuthorized = security_context.check_scope('openid')
    if not isAuthorized:
        abort(403)

    output += 'get_logon_name: ' + security_context.get_logon_name() + '\n'
    output += 'get_email: ' + security_context.get_email() + '\n'
    output += 'get_identity_zone: ' + security_context.get_identity_zone() + '\n'

    schema = hana.credentials['schema']
    host = hana.credentials['host']
    port = hana.credentials['port']
    user = hana.credentials['user']
    password = hana.credentials['password']


    output += 'schema: ' + schema + '\n'
    output += 'host: ' + host + '\n'
    output += 'port: ' + port + '\n'
    output += 'user: ' + user + '\n'
    output += 'pass: ' + password + '\n'

    # The certificate will available for HANA service instances that require an encrypted connection
    # Note: This was tested to work with python hdbcli-2.3.112 tar.gz package not hdbcli-2.3.14 provided in XS_PYTHON00_0-70003433.ZIP  
    if 'certificate' in hana.credentials:
        haascert = hana.credentials['certificate']
    
    # Connect to the python HANA DB driver using the connection info
# User for HANA as a Service instances
    if 'certificate' in hana.credentials:
        connection = dbapi.connect(
            address=host,
            port=int(port),
            user=user,
            password=password,
            currentSchema=schema,
            encrypt="true",
            sslValidateCertificate="true",
            sslCryptoProvider="openssl",
            sslTrustStore=haascert
        )
    else:
        connection = dbapi.connect(
            address=host,
            port=int(port),
            user=user,
            password=password,
            currentSchema=schema
        )

    cursor = connection.cursor()
    cursor.execute('DROP TABLE city')
    connection.close()

    output += 'TABLE city DROPPED.\n'

    # Return the results
    return output

@app.route('/pyt-sch/insert_data')
def insert_data():
    output = 'Python Authorized DB Validated Request. \n'
    output += '\n'
    output += 'Receiving module should check that it came from our approuter and verify or abort if otherwise.\n'
    output += '\n'
    svcs_json = str(os.getenv("VCAP_SERVICES", 0))
    svcs = json.loads(svcs_json)

    # Verify the JWT before proceeding. or refuse to process the request.
    # https://jwt.io/ JWT Debugger Tool and libs for all languages
    # https://github.com/jpadilla/pyjwt/
    # https://github.com/davedoesdev/python-jwt

    uaa_service = env.get_service(label='xsuaa').credentials
    access_token = request.headers.get('authorization')[7:]

    security_context = xssec.create_security_context(access_token, uaa_service)
    isAuthorized = security_context.check_scope('openid')
    if not isAuthorized:
        abort(403)

    output += 'get_logon_name: ' + security_context.get_logon_name() + '\n'
    output += 'get_email: ' + security_context.get_email() + '\n'
    output += 'get_identity_zone: ' + security_context.get_identity_zone() + '\n'

    schema = hana.credentials['schema']
    host = hana.credentials['host']
    port = hana.credentials['port']
    user = hana.credentials['user']
    password = hana.credentials['password']


    output += 'schema: ' + schema + '\n'
    output += 'host: ' + host + '\n'
    output += 'port: ' + port + '\n'
    output += 'user: ' + user + '\n'
    output += 'pass: ' + password + '\n'

    # The certificate will available for HANA service instances that require an encrypted connection
    # Note: This was tested to work with python hdbcli-2.3.112 tar.gz package not hdbcli-2.3.14 provided in XS_PYTHON00_0-70003433.ZIP  
    if 'certificate' in hana.credentials:
        haascert = hana.credentials['certificate']
    
    # Connect to the python HANA DB driver using the connection info
# User for HANA as a Service instances
    if 'certificate' in hana.credentials:
        connection = dbapi.connect(
            address=host,
            port=int(port),
            user=user,
            password=password,
            currentSchema=schema,
            encrypt="true",
            sslValidateCertificate="true",
            sslCryptoProvider="openssl",
            sslTrustStore=haascert
        )
    else:
        connection = dbapi.connect(
            address=host,
            port=int(port),
            user=user,
            password=password,
            currentSchema=schema
        )

    cursor = connection.cursor()
    cursor.execute("INSERT INTO city VALUES ('12203','Albany','NY')")
    cursor.execute("INSERT INTO city VALUES ('60601','Chicago','IL')")
    cursor.execute("INSERT INTO city VALUES ('60615','Chicago','IL')")
    connection.close()

    output += '3 rows of data inserted into TABLE city.\n'

    # Return the results
    return output

@app.route('/pyt-sch/select_data')
def select_data():
    output = 'Python Authorized DB Validated Request. \n'
    output += '\n'
    output += 'Receiving module should check that it came from our approuter and verify or abort if otherwise.\n'
    output += '\n'
    svcs_json = str(os.getenv("VCAP_SERVICES", 0))
    svcs = json.loads(svcs_json)

    # Verify the JWT before proceeding. or refuse to process the request.
    # https://jwt.io/ JWT Debugger Tool and libs for all languages
    # https://github.com/jpadilla/pyjwt/
    # https://github.com/davedoesdev/python-jwt

    uaa_service = env.get_service(label='xsuaa').credentials
    access_token = request.headers.get('authorization')[7:]

    security_context = xssec.create_security_context(access_token, uaa_service)
    isAuthorized = security_context.check_scope('openid')
    if not isAuthorized:
        abort(403)

    output += 'get_logon_name: ' + security_context.get_logon_name() + '\n'
    output += 'get_email: ' + security_context.get_email() + '\n'
    output += 'get_identity_zone: ' + security_context.get_identity_zone() + '\n'

    schema = hana.credentials['schema']
    host = hana.credentials['host']
    port = hana.credentials['port']
    user = hana.credentials['user']
    password = hana.credentials['password']


    output += 'schema: ' + schema + '\n'
    output += 'host: ' + host + '\n'
    output += 'port: ' + port + '\n'
    output += 'user: ' + user + '\n'
    output += 'pass: ' + password + '\n'

    # The certificate will available for HANA service instances that require an encrypted connection
    # Note: This was tested to work with python hdbcli-2.3.112 tar.gz package not hdbcli-2.3.14 provided in XS_PYTHON00_0-70003433.ZIP  
    if 'certificate' in hana.credentials:
        haascert = hana.credentials['certificate']
    
    # Connect to the python HANA DB driver using the connection info
# User for HANA as a Service instances
    if 'certificate' in hana.credentials:
        connection = dbapi.connect(
            address=host,
            port=int(port),
            user=user,
            password=password,
            currentSchema=schema,
            encrypt="true",
            sslValidateCertificate="true",
            sslCryptoProvider="openssl",
            sslTrustStore=haascert
        )
    else:
        connection = dbapi.connect(
            address=host,
            port=int(port),
            user=user,
            password=password,
            currentSchema=schema
        )

    cursor = connection.cursor()

    # Form an SQL statement to retrieve some data
    cursor.execute('SELECT * FROM city')

    # Execute the SQL and capture the result set
    city_vals = cursor.fetchall()

    # Loop through the result set and output
    for city_val in city_vals:
        output += 'zip: ' + str(city_val[0]) + ' name: ' + str(city_val[1]) + ' state: ' + str(city_val[2]) + '\n'

    # Close the DB connection
    connection.close()

    output += 'All data selected from TABLE city.\n'

    # Return the results
    return output

@app.route('/pyt-sch/delete_data')
def delete_data():
    output = 'Python Authorized DB Validated Request. \n'
    output += '\n'
    output += 'Receiving module should check that it came from our approuter and verify or abort if otherwise.\n'
    output += '\n'
    svcs_json = str(os.getenv("VCAP_SERVICES", 0))
    svcs = json.loads(svcs_json)

    # Verify the JWT before proceeding. or refuse to process the request.
    # https://jwt.io/ JWT Debugger Tool and libs for all languages
    # https://github.com/jpadilla/pyjwt/
    # https://github.com/davedoesdev/python-jwt

    uaa_service = env.get_service(label='xsuaa').credentials
    access_token = request.headers.get('authorization')[7:]

    security_context = xssec.create_security_context(access_token, uaa_service)
    isAuthorized = security_context.check_scope('openid')
    if not isAuthorized:
        abort(403)

    output += 'get_logon_name: ' + security_context.get_logon_name() + '\n'
    output += 'get_email: ' + security_context.get_email() + '\n'
    output += 'get_identity_zone: ' + security_context.get_identity_zone() + '\n'

    schema = hana.credentials['schema']
    host = hana.credentials['host']
    port = hana.credentials['port']
    user = hana.credentials['user']
    password = hana.credentials['password']


    output += 'schema: ' + schema + '\n'
    output += 'host: ' + host + '\n'
    output += 'port: ' + port + '\n'
    output += 'user: ' + user + '\n'
    output += 'pass: ' + password + '\n'

    # The certificate will available for HANA service instances that require an encrypted connection
    # Note: This was tested to work with python hdbcli-2.3.112 tar.gz package not hdbcli-2.3.14 provided in XS_PYTHON00_0-70003433.ZIP  
    if 'certificate' in hana.credentials:
        haascert = hana.credentials['certificate']
    
    # Connect to the python HANA DB driver using the connection info
# User for HANA as a Service instances
    if 'certificate' in hana.credentials:
        connection = dbapi.connect(
            address=host,
            port=int(port),
            user=user,
            password=password,
            currentSchema=schema,
            encrypt="true",
            sslValidateCertificate="true",
            sslCryptoProvider="openssl",
            sslTrustStore=haascert
        )
    else:
        connection = dbapi.connect(
            address=host,
            port=int(port),
            user=user,
            password=password,
            currentSchema=schema
        )

    cursor = connection.cursor()
    cursor.execute("DELETE FROM city")
    connection.close()

    output += 'All rows of data in TABLE city deleted.\n'

    # Return the results
    return output


if __name__ == '__main__':
    print(platform.python_version())
    # Run the app, listening on all IPs with our chosen port number
    # Use this for production 
    #app.run(host='0.0.0.0', port=port)
    # Use this for debugging 
    app.run(debug=True, host='0.0.0.0', port=port)

