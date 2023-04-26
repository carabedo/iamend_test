""" Modulo con funciones para graficar en matplotlib o plotly"""	
import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show
from bokeh.palettes import Spectral4

class Fig:
    def __init__(self,altura=500,ancho=600):
        self.tool_list = ['box_zoom', 'reset']
        self.altura=altura
        self.ancho=ancho
        self.fig= figure( x_axis_label='f[Hz]',y_axis_label='im(dz)/x0',height=self.altura, width=self.ancho,tools=self.tool_list,x_axis_type="log")
        self.color=0
    def add(self,exp,indice_archivo,tipo):
        x=exp.f
        bobina_effectiva=exp.coil
        l0=bobina_effectiva[-1]
        w=exp.w
        x0=w*l0
        if tipo == 'raw':
            df=exp.data[indice_archivo]
            grouped = df.groupby('repeticion')
            for name, repeticion in grouped:
                ymeas=repeticion.imag
                #scatter ymeas
                self.fig.circle(x, ymeas/x0 ,fill_color=None,color=Spectral4[self.color],alpha=0.8,)      
            self.fig.line(x,df.groupby('f').mean().imag/x0,legend_label=df.filename,color=Spectral4[self.color])
            self.fig.legend.click_policy="hide"
            self.color+=1
        elif tipo == 'corr':
            archivo_muestra=exp.info.iloc[indice_archivo].archivo
            df=exp.dznorm.query('muestra=="'+archivo_muestra+'"')
            ymeas=df.dzcorrnorm.values.imag
            self.fig.line(x, ymeas ,legend_label=archivo_muestra,color=Spectral4[self.color], alpha=0.8)
            self.fig.legend.click_policy="hide"
            self.color+=1
    def show(self):
        show(self.fig)


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



        

