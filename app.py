import os
import tempfile
from contextlib import contextmanager

from impala.dbapi import connect

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from components import Column, Header, Row
import config
from auth import auth
from utils import StaticUrlPath


app = dash.Dash(
    __name__,
)
dash_auth = auth(app)

server = app.server  # Expose the server variable for deployments

# Standard Dash app code below
app.layout = html.Div(className='container', children=[

    Header('Sample App'),

    dash_auth.create_logout_button(
        id='logout-btn',
        label='Logout'),

    Row([
        Column(width=4, children=[
            dcc.Dropdown(
                id='dropdown',
                options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
                value='LA'
            )
        ]),
        Column(width=8, children=[
            dcc.Graph(id='graph')
        ])
    ])
])


@contextmanager
def kerberos_auth():
    ticket_cache = dash_auth.get_kerberos_ticket_cache()

    # Remove group and other permissions for the ccache file:
    os.umask(0o077)

    with tempfile.NamedTemporaryFile() as ccache:
        ccache.write(ticket_cache)
        ccache.flush()

        # Use the temporary file as our ccache. This avoids having a global
        # ccache file. If the Kerberos library you're using requires you to
        # use a global ccache file (i.e. if KRB5CCNAME does not work),
        # be sure to configure the app to only accept one request at a time
        # per container.

        # Also note that modifying the process environment is not thread safe,
        # so avoid running multiple gunicorn threads. (This is the default.)
        os.environ['KRB5CCNAME'] = 'FILE:{}'.format(ccache.name)

        yield

    # The temporary ccache file is automatically deleted by
    # NamedTemporaryFile(). If you need to use a global ccache file,
    # remove it here. We also recommend removing it at the start of every
    # request for added safety.


@app.callback(Output('graph', 'figure'),
              [Input('dropdown', 'value')])
def update_graph(value):
    # This context manager must be used with any function/method calls that use
    # Kerberos. If there's more than one, we recommend enclosing all of them
    # in the same "with" statement to avoid duplicate ccache retrievals.
    with kerberos_auth():
        conn = connect(host='quickstart.cloudera', port=21050,
                       auth_mechanism='GSSAPI', kerberos_service_name='impala',
                       database='poc')

    cursor = conn.cursor()
    cursor.execute('SELECT x, y FROM t3;')

    print(cursor.description)  # prints the result set's schema

    x = []
    y = []

    for row in cursor.fetchall():
        x.append(row[0])
        y.append(row[1])

    return {
        'data': [{
            'x': x,
            'y': y,
        }],
        'layout': {
            'title': value,
            'margin': {
                'l': 60,
                'r': 10,
                't': 40,
                'b': 60
            }
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)
