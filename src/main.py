import os

from dash import Dash

from src.framework.ui import create_layout
from src.framework.utilities import add_callback

app = Dash(__name__,
           external_stylesheets=[
               os.path.join(".", "assets", "bootstrap.css"),
               os.path.join(".", "assets", "custom.css")
           ],
           meta_tags=[
               {
                   'name': 'viewport',
                   'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'
               }
           ],
           title="Textzeichen"
           )

server = app.server

create_layout(app)

add_callback(app)

if __name__ == '__main__':
    app.run_server(host="127.0.0.1")
