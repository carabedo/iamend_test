""" Modulo con funciones para graficar en matplotlib o plotly"""	
import iamend_ci.theo as theo												
import numpy as np
import matplotlib.pyplot as plt
# plt.ion()
# import mpld3
# mpld3.enable_notebook()
# from mpld3 import plugins
# import plotly.graph_objs as go
# import plotly
# plotly.offline.init_notebook_mode(connected=True)
# import tkinter as tk
# from tkinter import filedialog






## matplotlib

def im(dzcorrnorm,f,name,figsize=[8,6]):
    """im( frecuencia, datacorr, n)
    Grafica la parte imaginaria de la impedancia corregida y normalizada.
    Parameters
    ----------
    f : array_like, vector con las frecuencias
    datacorr : array_like, matriz con las mediciones
    n : int, indice de la medicion 
    """    
    plt.figure(figsize=figsize)
    plt.semilogx(f,dzcorrnorm.imag,'ok',markersize=3,markerfacecolor='none')
    plt.ylabel('$Im(\Delta Z)/X_0$')
    plt.xlabel('Frecuencia [Hz]')
    plt.title(name)
    plt.grid(True, which="both")
    
    
def re(dzcorrnorm,f,name,figsize=[8,6]):
    """im( frecuencia, datacorr, n)
    Grafica la parte imaginaria de la impedancia corregida y normalizada.
    Parameters
    ----------
    f : array_like, vector con las frecuencias
    datacorr : array_like, matriz con las mediciones
    n : int, indice de la medicion 
    """    
    plt.figure(figsize=figsize)
    plt.semilogx(f,dzcorrnorm.real,'ok',markersize=3,markerfacecolor='none')
    plt.ylabel('$Im(\Delta Z)/X_0$')
    plt.xlabel('Frecuencia [Hz]')
    plt.title(name)
    plt.grid(True, which="both")

# ploteo de fiteos        

def mu(data,acero,savefile=0):
    """ agarra data procesada por fit.mu y guarda png """
    f=data[1]
    ymeas=data[2]
    mu=data[5]
    rsqr=data[6]
    yteo=data[-2]
    name=data[-1]
    plt.figure(figsize=(7,5))
    plt.semilogx(f,ymeas.imag,'ok',markersize=4,markerfacecolor='none')
    plt.semilogx(f,yteo,'k',label='$\mu_r$ = '+ str(np.round(mu,2)) + '   $r^2$ = ' + str(np.round(rsqr,3)  ))
    plt.ylabel('$Im(\Delta Z)/X_0$',fontsize=12)
    plt.xlabel('Frecuencia [Hz]',fontsize=12)
    plt.legend(loc='lower left', prop={'size': 13})
    plt.title(acero)
    plt.grid(True, which="both")
    if savefile==1:
        g=name.split(' ')
        fname=''.join(g)
        plt.savefig(fname)       
        
        
def sigma(data,savefile=0):
    """ agarra data procesada por fit.sigma y guarda png """
    f=data[0]
    ymeas=data[1]
    mu=data[3]
    rsqr=data[4]
    yteo=data[2]
    plt.figure()
    plt.semilogx(f,ymeas,'ok',markersize=4,markerfacecolor='none')
    plt.semilogx(f,yteo,'k',label='$\sigma$ = '+ str(np.round(mu,2)) + '   $r^2$ = ' + str(np.round(rsqr,3)  ))
    plt.ylabel('$Im(\Delta Z)/X_0$')
    plt.xlabel('Frecuencia [Hz]')
    plt.legend(loc='lower left')
   
     

# ploteo de fiteo por frecuencias

def ffit(fdata,save=0,fit='par',figsize=[8,6]):
    """ agarra data procesada por fit.ffmu guarda png """
    mrks=['o','s','^','*','X']
    plt.figure(figsize=figsize)
    for i,mu in enumerate(fdata['mues']):
        f=fdata['fs'][i]
        ymeas=fdata['ymeas'][i]
        yteo=fdata['yteos'][i]
        plt.semilogx(f,ymeas,mrks[i]+'k',markersize=7,markerfacecolor='none',label=fit+' = '+ str(np.round(mu,3)) )
        plt.semilogx(f,yteo,'-k')
    plt.ylabel('$Im(\Delta Z)/X_0$')
    plt.xlabel('Frecuencia [Hz]')
    plt.legend(loc='lower left')
    plt.title(fdata['name'])
    plt.grid(True, which="both")

    if save==1:
        g=fdata[-1].split(' ')
        fname=''.join(g)
        plt.savefig('fmu_'+fname)



        

