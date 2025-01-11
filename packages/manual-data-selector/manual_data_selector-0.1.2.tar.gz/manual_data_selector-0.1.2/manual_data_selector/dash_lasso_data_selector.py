import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd


class DashLassoDataSelector:
    def __init__(self, df, app, fig_size=(800, 600), marker_size=10, port=8050):
        self.df = df
        self.fig_size = fig_size
        self.marker_size = marker_size
        self.selected_data = pd.DataFrame()
        self.confirmed_data = pd.DataFrame()
        self.all_confirmed_data = {}
        self.confirmation_nr = 1
        self.app = app
        self.port = port

        # Define the layout
        self.app.layout = html.Div([
            dcc.Graph(id='scatter-plot'),
            dcc.Dropdown(
                id='x-axis-dropdown',
                options=[{'label': col, 'value': col} for col in self.df.columns],
                value=self.df.columns[0]
            ),
            dcc.Dropdown(
                id='y-axis-dropdown',
                options=[{'label': col, 'value': col} for col in self.df.columns],
                value=self.df.columns[1]
            ),
            html.Button('Confirm Selection', id='confirm-button'),
            html.Div(id='confirmed-data-output')
        ])

        # Define callbacks
        self.app.callback(
            Output('scatter-plot', 'figure'),
            [Input('x-axis-dropdown', 'value'),
             Input('y-axis-dropdown', 'value')]
        )(self.update_scatter_plot)

        self.app.callback(
            Output('confirmed-data-output', 'children'),
            [Input('confirm-button', 'n_clicks')],
            [State('scatter-plot', 'selectedData')]
        )(self.confirm_selection)

    def run(self):
        self.app.run_server(port=self.port, debug=True)

    def update_scatter_plot(self, x_axis, y_axis):
        fig = px.scatter(self.df, x=x_axis, y=y_axis,
                         width=self.fig_size[0], 
                         height=self.fig_size[1])

        fig.update_traces(marker=dict(size=self.marker_size))
        return fig

    def confirm_selection(self, n_clicks, selected_data):
        if n_clicks is None:
            return "Select data points and click 'Confirm Selection'."

        if selected_data and 'points' in selected_data:
            indices = [point['pointIndex'] for point in selected_data['points']]
            self.selected_data = self.df.iloc[indices]
            self.confirmed_data = self.selected_data.copy()
            self.all_confirmed_data[self.confirmation_nr] = self.confirmed_data
            self.confirmation_nr += 1
            return f"Selection {self.confirmation_nr - 1} confirmed."

        return "No data selected. Select data points first."

if __name__ == '__main__':
    dash_app = DashLassoDataSelector(df, fig_size=(1600, 600), marker_size=5)
    dash_app.run()
