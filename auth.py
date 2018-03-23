import dash_auth
import os
from textwrap import dedent
import urllib3

import config

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file provides an interface to the `plotly_auth` library
# You do not need to edit this file
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def auth(app):
    # Print info for debugging
    if 'DYNO' in os.environ:
        print(dedent('''
            DASH_APP_NAME: {DASH_APP_NAME}
            DASH_APP_PRIVACY: {DASH_APP_PRIVACY}
            PATH_BASED_ROUTING: {PATH_BASED_ROUTING}
            PLOTLY_USERNAME: {PLOTLY_USERNAME}
            PLOTLY_DOMAIN: {PLOTLY_DOMAIN}
            PLOTLY_API_DOMAIN: {PLOTLY_API_DOMAIN}
            PLOTLY_DASH_DOMAIN: {PLOTLY_DASH_DOMAIN}
            PLOTLY_SSL_VERIFICATION: {PLOTLY_SSL_VERIFICATION}
        '''.format(
            DASH_APP_NAME=config.DASH_APP_NAME,
            DASH_APP_PRIVACY=config.DASH_APP_PRIVACY,
            PATH_BASED_ROUTING=config.PATH_BASED_ROUTING,
            PLOTLY_USERNAME=os.environ['PLOTLY_USERNAME'],
            PLOTLY_DOMAIN=os.environ['PLOTLY_DOMAIN'],
            PLOTLY_API_DOMAIN=os.environ['PLOTLY_API_DOMAIN'],
            PLOTLY_DASH_DOMAIN=config.PLOTLY_DASH_DOMAIN,
            PLOTLY_SSL_VERIFICATION=os.environ['PLOTLY_SSL_VERIFICATION']
        )))
    if config.DASH_APP_PRIVACY == 'private':
        # Checks if running inside Plotly On-Premise environment
        if 'DYNO' in os.environ:
            if config.PATH_BASED_ROUTING:
                if config.DASH_APP_NAME == 'name-of-your-dash-app':
                     raise Exception(
                        'Please enter the name of your' +
                        ' dash app inside config.py')
                app.config.requests_pathname_prefix = '/{}/'.format(
                    config.DASH_APP_NAME
                )

        if os.environ['PLOTLY_API_KEY'] == 'your-plotly-api-key':
             raise Exception(
                'Please enter the your Plotly API key inside config.py')

        if os.environ['PLOTLY_USERNAME'] == 'your-plotly-username':
             raise Exception(
                'Please enter the your Plotly username inside config.py')

        if os.environ['PLOTLY_DOMAIN'] == 'https://your-plotly-domain.com':
             raise Exception(
                'Please enter the your Plotly domain inside config.py')

        if os.environ['PLOTLY_SSL_VERIFICATION'] == 'False':
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if config.PATH_BASED_ROUTING:
            APP_URL = '{}/{}'.format(
                config.PLOTLY_DASH_DOMAIN.strip('/'),
                config.DASH_APP_NAME,
            )
        else:
            APP_URL = '{}://{}.{}'.format(
                config.PLOTLY_DASH_DOMAIN.split('://')[0],
                config.DASH_APP_NAME,
                config.PLOTLY_DASH_DOMAIN.split('://')[1].strip('/')
            )

        dash_auth.PlotlyAuth(
            app,
            config.DASH_APP_NAME,
            config.DASH_APP_PRIVACY,
            APP_URL
        )
