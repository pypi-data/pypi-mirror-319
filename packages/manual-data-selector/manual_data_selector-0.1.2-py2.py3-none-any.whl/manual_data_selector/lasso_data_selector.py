""" LassoDataSelector class for interactive selection of data points in a plotly scatter plot. 
    The selected data points are stored in a pandas DataFrame.
    The confrimed data points are stored in a pandas DataFrame.
    The confirmed data points can be accessed via the all_confirmed_data dictionnary.

    Inspiration from: https://plotly.com/python/v3/selection-events/?_gl=1*1mrgxu1*_ga*MTg2MDIwODQ1Ny4xNzAwNjYwNzI0*_ga_6G7EE0JNSC*MTcwMDY2NTk1Ni4yLjEuMTcwMDY2NjExOS42MC4wLjA.
"""

import pandas as pd
import plotly.graph_objs as go
from ipywidgets import Button, HBox, Output, VBox, interactive


class LassoDataSelector:
    def __init__(self, df, fig_size=(800, 600), marker_size=10):
        self.df = df
        self.fig_size = fig_size
        self.marker_size = marker_size
        self.selected_data = pd.DataFrame()
        self.confirmed_data = pd.DataFrame()
        self.all_confirmed_data = {}
        self.confirmation_nr = 1
        self.output = Output()


    def _update_axes(self, xaxis, yaxis):
        self.scatter.x = self.df[xaxis]
        self.scatter.y = self.df[yaxis]
        with self.fig.batch_update():
            self.fig.layout.xaxis.title = xaxis
            self.fig.layout.yaxis.title = yaxis

    def _selection_fn(self, trace, points, selector):
        if points.point_inds:
            self.selected_data = self.df.iloc[points.point_inds]

    def select_data(self):
        self.fig = go.FigureWidget(
            data=[go.Scatter(y=self.df.iloc[:, 1], x=self.df.iloc[:, 0], mode='markers', marker=dict(size=self.marker_size))],
            layout=go.Layout(width=self.fig_size[0], height=self.fig_size[1])
        )
        self.scatter = self.fig.data[0]
        self.scatter.on_selection(self._selection_fn)

        axis_dropdowns = interactive(self._update_axes, yaxis=self.df.columns, xaxis=self.df.columns)
        confirm_button = Button(description="Confirm Selection")

        def on_button_clicked(b):
            with self.output:
                print("Selection confirmed.")
                self.confirmed_data = self.selected_data.copy()
                self.all_confirmed_data[self.confirmation_nr] = self.confirmed_data
                self.confirmation_nr += 1
                print(self.confirmed_data)


        confirm_button.on_click(on_button_clicked)
        self.plot_and_controls = VBox((HBox(axis_dropdowns.children), self.fig))

        return VBox([self.plot_and_controls, confirm_button, self.output])