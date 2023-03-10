""" Modulo con las funciones para fitear impedancias"""
import iamend_ci.theo as theo
import numpy as np
from scipy import optimize
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

def z1(f,bo,dzucorrnorm,dpatron,sigma,name):
    
    """z1 (frecuencia, bobina, datacorr, n, dpatron,sigma, mur)
    Ajuste del lift-off
    Parameters
    ----------
    f : array_like, vector con las frecuencias
    datacorr : array_like, matriz con las mediciones
    bo: array_like, vector con los parametros geometricos de la bobina
    datacorr: array_like, matrix con las mediciones corregidas y nromalizadas
    n : int, indice de la medicion 
    dpatron: float, espesor muestra
    sigma : float, conductividad muestra
    mur: float, permeabilidad muestra
    """    
    mur=1

    def funz1(x,b):
        r1=bo[0]
        r2=bo[1]
        dh=bo[2]
        N=bo[3]
        z1=b
        bob=[r1,r2,dh,N,z1,1]
        return theo.dzD(x,bob,sigma,dpatron,mur,3000).imag/x0
    #[f,z0,dzucorr,w]
    l0=bo[-1]
    w=2*np.pi*f
    x0=w*l0
      
    xmeas=f
    ymeas=dzucorrnorm.imag   
    fpar, fcov=optimize.curve_fit(funz1, xmeas, ymeas, p0=[1.1e-3], bounds=(0,2e-3))
    

    z1eff=fpar[0]
    r1=bo[0]
    r2=bo[1]
    dh=bo[2]
    N=bo[3]
    boeff=[r1,r2,dh,N,z1eff,l0]
    yteo=theo.dzD(f,boeff,sigma,dpatron,mur,1500)
    yteo=yteo.imag/x0
    
    para_eff={'name' : 'z1', 'value' : z1eff*1000}

    fig=imlogfit(f,[ymeas, yteo],para_eff,name)
    print('z1 =',fpar[0]*1000,'mm')
    return(fpar,fig)


def mu(f,bo_eff,dzucorrnorm,dpatron,sigma, name):
    """mu (frecuencia, bobina, datacorr, dpatron,sigma, name, z1eff)
    Ajuste de la permeabilidad

    Parameters
    ----------
    f : array_like, vector con las frecuencias
    datacorr : array_like, matriz con las mediciones
    bo: array_like, vector con los parametros geometricos de la bobina
    datacorr: array_like, matrix con las mediciones corregidas y nromalizadas
    n : int, indice de la medicion 
    dpatron: float, espesor muestra
    sigma : float, conductividad muestra
    z1eff: float, lift-off efectivo
    """    
    def funmu(x,a):
        return theo.dzD(x,bo_eff,sigma,dpatron,a,1500).imag/x0
    #[f,z0,dzucorr,w]
    l0=bo_eff[-1]    
    w=2*np.pi*f
    x0=w*l0    
    xmeas=f
    ymeas=dzucorrnorm.imag   
    fpar, fcov=optimize.curve_fit(funmu, xmeas, ymeas, p0=[1], bounds=(0,150))
    mur=fpar[0]
    yteo=theo.dzD(f,bo_eff,sigma,dpatron,mur,1500)
    yteo=yteo.imag/x0
    para_eff={'name' : 'mu_r', 'value' : mur}
    fig=imlogfit(f,[ymeas, yteo],para_eff,name)
    print('mu_r_eff =',fpar[0])
    return(fpar,fig)


def fmu(f,coil,n,dzcorrnorm,sigma,name,dpatron=1):
    bo=coil
    mues=list()
    yts=list()
    fs=np.array_split(f,n)
    ys=np.array_split(dzcorrnorm.imag,n)
    l0=bo[-1]
    boeff=coil[:]
    def funmu(x,a):
        return theo.dzD(x,boeff,sigma,dpatron,a,1500).imag/x0    
    for i,frec in enumerate(fs):
        w=2*np.pi*frec
        x0=w*l0
        xmeas=frec
        ymeas=ys[i]
        fpar, fcov=optimize.curve_fit(funmu, xmeas, ymeas, p0=5, bounds=(1, 200))    
        yt=theo.dzD(frec,boeff,sigma,dpatron,fpar[0],1500).imag/x0     
        yts.append(yt)    
        mues.append(fpar[0])

    datafmu={
        'mues' : mues ,
        'fs'   : fs ,
        'ymeas'   : ys,
        'yteos'   :yts,
        'name'  : name
    }          
    return datafmu

def imlogfit(f,data,para_eff,name,savefile=0):
    """ agarra data procesada por fit.mu y guarda png """
    ymeas=data[0]
    yteo=data[1]
    label=para_eff['name']
    p_eff=para_eff['value']
    fig=plt.figure(figsize=(8,6))
    plt.semilogx(f,ymeas,'ok',markersize=4,markerfacecolor='none')
    plt.semilogx(f,yteo,'k',label=label +'_eff = ' + str(np.round(p_eff,2)) )
    plt.ylabel('$Im(\Delta Z)/X_0$',fontsize=12)
    plt.xlabel('Frecuencia [Hz]',fontsize=12)
    plt.legend(loc='lower left', prop={'size': 13})
    plt.title(name)
    plt.grid(True, which="both")
    if savefile==1:
        g=name.split(' ')
        fname=''.join(g)
        plt.savefig(fname)   
    return fig



# plotly
def pxlogfit(x,Y,titulo):
    """ fiteo y plot (plotly) varias muestras """
    
    fig =make_subplots(rows=1, cols=1 ,print_grid=False)
    for b,a in enumerate(Y):
        if b==0:
            trace0 = go.Scatter(
            x = x,
            y = a,
            name='exp',
            mode = 'markers')
            fig.append_trace(trace0, 1, 1)

        else:
            trace0 = go.Scatter(
            x = x,
            y = a,
            mode='lines',
            name=titulo)
            fig.append_trace(trace0, 1, 1)
    fig["layout"]["xaxis"].update( type='log',zeroline=False , autorange=True   )
    fig["layout"]["yaxis"].update( type='linear',zeroline=False , autorange=True   )
    return(fig)