import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output

# https://bootswatch.com/solar/

def Navbar():
    navbar = dbc.Nav([
              dbc.NavItem(dbc.NavLink("Home", href="/home",className="navbar-brand")),
              dbc.NavItem(dbc.NavLink("Room Type Analysis", href="/room_type",className="navbar-brand")),
            ],
          pills=True,
          className="navbar navbar-expand-lg navbar-light bg-light",
        )
    return navbar