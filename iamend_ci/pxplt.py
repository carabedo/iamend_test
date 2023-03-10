""" Modulo con funciones para graficar en plotly"""	
import iamend_ci.theo as theo												
import numpy as np
import plotly.express as px
import pandas as pd


def ims(dfci):
    dfm = dfci.imdz.melt('f', var_name='muestra', value_name='imdzcorrnorm')
    return px.line(dfm, x='f',y='imdzcorrnorm',color='muestra',log_x=True)
