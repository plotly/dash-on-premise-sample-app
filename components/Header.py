import dash_html_components as html
from .Column import Column
from utils import StaticUrlPath

def Header(title):
    height = 60
    return html.Div(
        style={
            'borderBottom': 'thin lightgrey solid',
            'marginRight': 20,
            'marginBottom': 20,
            'height': height
        },
        children=[
            Column(
                width=6,
                children=title,
                style={
                    'fontSize': 35,
                }
            ),
            Column(
                width=6,
                children=html.Img(
                    src=StaticUrlPath('dash-logo.png'),
                    style={
                        'float': 'right',
                        'height': height,
                    }
                )
            )
        ]
    )
