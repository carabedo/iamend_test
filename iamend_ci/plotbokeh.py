from bokeh.io import output_notebook # output_file
from bokeh.plotting import figure, show
from bokeh.layouts import  gridplot
import numpy as np
import iamend_ci.theo as theo	
from iamend_ci.so import corrnorm
import logging
from bokeh.palettes import Category20

output_notebook()


tool_list = ['box_zoom', 'reset','pan']



def implots(exp,altura=500,ancho=900):
    x=exp.f
    plot1 = figure( x_axis_label='f[Hz]',y_axis_label='im(dz)/x0',height=altura, width=ancho,
                        tools=tool_list,x_axis_type="log")
    for i,m in enumerate(exp.dznorm.muestra.unique()):
        ymeas=exp.dznorm[exp.dznorm.muestra == m].imag.values
        plot1.line(x, ymeas,line_width=2,line_color=Category20[len(exp.dznorm.muestra.unique())][i],legend_label=m)
    plot1.legend.click_policy="hide"
    show(plot1)


def replots(exp,altura=500,ancho=900):
    x=exp.f
    plot1 = figure( x_axis_label='f[Hz]',y_axis_label='im(dz)/x0',height=altura, width=ancho,
                        tools=tool_list,x_axis_type="log")
    for i,m in enumerate(exp.dznorm.muestra.unique()):
        ymeas=exp.dznorm[exp.dznorm.muestra == m].real.values
        plot1.line(x, ymeas,line_width=2,line_color=Category20[len(exp.dznorm.muestra.unique())][i],legend_label=m)
    plot1.legend.click_policy="hide"
    show(plot1)

def plot_im(exp,indice_muestra):
    altura=500
    ancho=600
    x=exp.f
    muestra_filename=exp.info.iloc[indice_muestra].archivo
    fig = figure( title=muestra_filename, x_axis_label='f[Hz]',y_axis_label='im(dz)/x0',height=altura, width=ancho,
                        tools=tool_list,x_axis_type="log")
    df_ci=exp.data[indice_muestra]
    
    for i in df_ci.repeticion.unique():
        
        ymeas=corrnorm(exp,muestra_filename,i).imag
        fig.circle(x, ymeas,fill_color="white",fill_alpha=0,alpha=0.3)
    show(fig)
    

def plot_re(exp,indice_muestra):
    altura=500
    ancho=600
    x=exp.f
    muestra_filename=exp.info.iloc[indice_muestra].archivo
    fig = figure( title=muestra_filename, x_axis_label='f[Hz]',y_axis_label='im(dz)/x0',height=altura, width=ancho,
                        tools=tool_list,x_axis_type="log")
    df_ci=exp.data[indice_muestra]
    
    for i in df_ci.repeticion.unique():
        
        ymeas=corrnorm(exp,muestra_filename,i).real
        fig.circle(x, ymeas,fill_color="white",fill_alpha=0,alpha=0.3)
    show(fig)
    



def plot_fit_patron(exp,param_geo,indice_patron):
    altura=500
    ancho=600
    x=exp.f
    bobina_effectiva=exp.coil
    l0=bobina_effectiva[-1]
    w=2*np.pi*x
    x0=w*l0
    try:
        patron_filename=exp.info.iloc[indice_patron].archivo
        ymeas=exp.dznorm[exp.dznorm.muestra == patron_filename].imag.values
        espesorpatron=exp.info.espesor.iloc[indice_patron]
        sigmapatron=exp.info.conductividad.iloc[indice_patron]
        yteo=theo.dzD(exp.f,bobina_effectiva,sigmapatron,espesorpatron,1,3000).imag/x0
        plot1 = figure(title=patron_filename, x_axis_label='f[Hz]',y_axis_label='im(dz)/x0',height=altura, width=ancho,
                         tools=tool_list,x_axis_type="log")
        #scatter ymeas
        plot1.circle(x, ymeas)
        #linea ajuste yteo
        plot1.line(x=x, y=yteo,
                    line_color="#f46d43", line_width=2, 
                    line_alpha=0.6)
        show(plot1)
    except Exception as e:
        logging.exception('Error')   





def plot_fit_mues(exp):
    plots=[]
    for muestra in exp.dznorm.muestra.unique():
        if 'M' in muestra:
            x=exp.f
            dzucorrnorm_test=exp.dznorm_test[exp.dznorm_test.muestra == muestra].dzcorrnorm.values

            y=dzucorrnorm_test.imag
            yteo=exp.ypreds[muestra].imag

            mur=exp.info[exp.info.muestras.str.contains(muestra)].mueff.values[0]
            plot1 = figure( title=muestra+' mueff = '+ str(mur.round(2)),x_axis_label='f[Hz]',
                           y_axis_label='im(dz)/x0',height=250, width=300, tools=tool_list,x_axis_type="log")
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


def plot_fit_mu(exp,indice_muestra,altura=500,ancho=600):
    x=exp.f
    archivo_muestra=exp.info.iloc[indice_muestra].archivo
    y=exp.dznorm.query('muestra=="'+archivo_muestra+'"').imag.values
    yteo=exp.ypreds[archivo_muestra].imag
    mur=exp.info.iloc[indice_muestra].mueff
    fig = figure( title=archivo_muestra+' mueff = '+ str(mur.round(2)),x_axis_label='f[Hz]',y_axis_label='im(dz)/x0',height=altura, width=ancho, tools=tool_list,x_axis_type="log")
    fig.circle(x, y)
    fig.line(x=x, y=yteo, line_color="#f46d43", line_width=2, line_alpha=0.6)
    show(fig)


def plot_fit_sigma(exp,indice_muestra,yteo,altura=500,ancho=600):
    x=exp.f
    archivo_muestra=exp.info.iloc[indice_muestra].archivo
    y=exp.dznorm.query('muestra=="'+archivo_muestra+'"').imag.values
    sigma_eff=exp.info.iloc[indice_muestra].sigma_eff
    fig = figure( title=archivo_muestra+' sigma_eff = '+ str(sigma_eff/1e6),x_axis_label='f[Hz]',y_axis_label='im(dz)/x0',height=altura, width=ancho, tools=tool_list,x_axis_type="log")
    fig.circle(x, y)
    fig.line(x=x, y=yteo, line_color="#f46d43", line_width=2, line_alpha=0.6)
    show(fig)



def plot_fit_fmu(exp,indice_muestra,altura=500,ancho=600):

    markers=["square",'triangle','circle','inverted_triangle']
    try:

        muestra_name=exp.info.iloc[indice_muestra].archivo
        fmu=exp.fmues[muestra_name]
        plot1 = figure(x_axis_label='f[Hz]',y_axis_label='im(dz)/x0',height=altura,
                    width=ancho, tools=tool_list,x_axis_type="log")
        for n,fn in enumerate(fmu['fs']):
            x=fn
            ymeas=fmu['ymeas'][n]
            yteo=fmu['yteos'][n]
            plot1.scatter(x, ymeas,marker=markers[n],size=6,fill_alpha = 0)
            plot1.line(x=x, y=yteo, line_color="#f46d43", line_width=2, line_alpha=0.6)
        show(plot1)
    except:
        print('No existe la muestra, revise .info')