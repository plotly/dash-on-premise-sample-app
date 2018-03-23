import os
from textwrap import dedent

import config

def StaticUrlPath(resource):
    if not os.path.exists(os.path.join('static', resource)):
        raise Exception(dedent('''
            The file "{}" does not exist in the "static" folder.
        '''.format(resource, resource)))
    if 'DYNO' in os.environ and config.PATH_BASED_ROUTING:
        return '/{}/static/{}'.format(config.DASH_APP_NAME, resource)
    else:
        return '/static/{}'.format(resource)
