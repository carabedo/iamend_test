from bokeh.io import output_notebook, curdoc  # output_file
from bokeh.plotting import figure, show
from bokeh.layouts import row, column, gridplot
import numpy as np

output_notebook()



def plot_fit_mues(exp):
    tool_list = ['box_zoom', 'reset']
    plots=[]
    for muestra in exp.dznorm.muestra.unique():
        if 'M' in muestra:
            x=exp.f
            y=exp.dznorm_test[muestra].values.imag
            yteo=exp.ypreds[muestra].imag
            mur=exp.info[exp.info.muestras.str.contains(muestra)].mueff.values[0]
            plot1 = figure( title=muestra+' mueff = '+ str(mur.round(2)),x_axis_label='f[Hz]',y_axis_label='im(dz)/x0',height=250, width=300, tools=tool_list,x_axis_type="log")
            plot1.circle(x, y)
            plot1.line(x=x, y=yteo, line_color="#f46d43", line_width=2, line_alpha=0.6)
            plots.append(plot1)
        

    if len(plots) >= 6:
        original_list = plots
        size_of_sublist = 3
        list_of_lists = []

        for i in range(0, len(original_list), size_of_sublist):
            sublist = original_list[i:i+size_of_sublist]
            list_of_lists.append(sublist)
        layout = gridplot(list_of_lists)
        show(layout)
    else:
        original_list = plots
        size_of_sublist = 2
        list_of_lists = []

        for i in range(0, len(original_list), size_of_sublist):
            sublist = original_list[i:i+size_of_sublist]
            list_of_lists.append(sublist)
        layout = gridplot(list_of_lists)
        show(layout)


def plot_fit_mu(exp,muestra,altura=500,ancho=600):
    tool_list = ['box_zoom', 'reset']
    x=exp.f
    try:
        muestra_name=exp.dznorm[exp.dznorm.muestra.str.contains(muestra.upper())].muestra.values[0]
        y=exp.dznorm[exp.dznorm.muestra == muestra_name].imag.values
        yteo=exp.ypreds[muestra_name].imag
        mur=exp.info[exp.info.muestras.str.contains(muestra.upper())].mueff.values[0]
        plot1 = figure( title=muestra+' mueff = '+ str(mur.round(2)),x_axis_label='f[Hz]',y_axis_label='im(dz)/x0',height=altura, width=ancho, tools=tool_list,x_axis_type="log")
        plot1.circle(x, y)
        plot1.line(x=x, y=yteo, line_color="#f46d43", line_width=2, line_alpha=0.6)
        show(plot1)
    except:
        print('No existe la muestra, revise .info')