import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output

# https://bootswatch.com/solar/
'''dbc.DropdownMenu(
                 className="navbar-brand",
                 nav=True,
                 in_navbar=True,
                 label="Menu",
                 children=[
                    dbc.DropdownMenuItem("Entry 1"),
                    dbc.DropdownMenuItem("Entry 2"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Help")
                          ],
                      ),'''
def Navbar():
    navbar = dbc.Nav([
              dbc.NavItem(dbc.NavLink("Home", href="/home",className="navbar-brand")),
              dbc.NavItem(dbc.NavLink("Room Type Analysis", href="/room_type",className="navbar-brand")),
            ],
          pills=True,
          className="navbar navbar-expand-lg navbar-dark bg-primary",
        )
    return navbar