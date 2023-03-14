from bokeh.io import output_notebook, curdoc  # output_file
from bokeh.plotting import figure, show
from bokeh.sampledata.iris import flowers
from bokeh.sampledata.iris import flowers as iris_df
from bokeh.models import ColumnDataSource, HoverTool, CategoricalColorMapper, Slider, Column, Select
from bokeh.models import CheckboxGroup, RadioGroup, Toggle, Button
from bokeh.layouts import row, column, gridplot
from bokeh.palettes import Spectral6
from bokeh.themes import Theme
import yaml

output_notebook()

tool_list = ['box_zoom', 'reset']

plots=[]
for muestra in exp3.dznorm.muestra.unique():
    x=exp3.f
    y=exp3.dznorm.query('muestra == '+'"'+muestra+'"').imag
    plot1 = figure( height=250, width=300, tools=tool_list,x_axis_type="log")
    plot1.circle(x, y)
    plots.append(plot1)
    

row1=[plots[0], plots[1]]
row2=[plots[2], plots[3]]
layout = gridplot([row1, row2])
show(layout)