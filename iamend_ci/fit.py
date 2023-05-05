""" Modulo con las funciones para fitear impedancias"""
import iamend_ci.theo as theo
import numpy as np
from scipy import optimize
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots


def z1(f,bo,dzucorrnorm,dpatron,sigma,mur=1):
    
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

    fpar, fcov=optimize.curve_fit(funz1, xmeas, ymeas, p0=[1.1e-3], bounds=(0,5e-3))
    print('z1 =',fpar[0]*1000,'mm')
    return fpar,np.sqrt(fcov[0][0])



def r2(f,bo,dzucorrnorm,dpatron,sigma,rango):
    
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

    def fun_r2(x,b):
        r1=bo[0]
        r2=b
        dh=bo[2]
        N=bo[3]
        z1=bo[4]
        bob=[r1,r2,dh,N,z1,1]
        return theo.dzD(x,bob,sigma,dpatron,mur,3000).imag/x0

    l0=bo[-1]
    w=2*np.pi*f
    x0=w*l0
      
    xmeas=f
    ymeas=dzucorrnorm.imag   
    if rango:
        bound_min=rango[0]
        bound_max=rango[1]
        p0=(bound_max+bound_min)/2
        fpar, fcov=optimize.curve_fit(fun_r2, xmeas, ymeas, p0=[p0], bounds=(bound_min,bound_max))
    else:
        bound_min=bo[0]
        bound_max=10e-3
        p0=(bound_max+bound_min)/2
        fpar, fcov=optimize.curve_fit(fun_r2, xmeas, ymeas, p0=[p0], bounds=(bound_min,bound_max))

    print('r2 =',fpar[0]*1000,'mm')
    return(fpar)


def N(f,bo,dzucorrnorm,espesorpatron,sigmapatron,rango):
    mupatron=1

    def fun_N(x,b):
        r1=bo[0]
        r2=bo[1]
        dh=bo[2]
        N=b
        z1=bo[4]
        bob_eff=[r1,r2,dh,N,z1,bo[5]]
        return theo.dzD(x,bob_eff,sigmapatron,espesorpatron,mupatron,3000).imag/x0
    l0=bo[-1]
    w=2*np.pi*f
    x0=w*l0
      
    xmeas=f
    ymeas=dzucorrnorm.imag   

    if rango:
        bound_min=rango[0]
        bound_max=rango[1]
        p0=(bound_max+bound_min)/2
        fpar, fcov=optimize.curve_fit(fun_N, xmeas, ymeas, p0=[p0], bounds=(bound_min,bound_max))
    else:
        fpar, fcov=optimize.curve_fit(fun_N, xmeas, ymeas, p0=[500], bounds=(0,1000))

    print('N =',fpar[0])
    return(fpar)


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
    return(fpar, np.sqrt(fcov[0][0]))

def muSigma(f,bo_eff,dzucorrnorm,dpatron):

    def funmu(x,mu,sigma):
        return theo.dzD(x,bo_eff,sigma,dpatron,mu,1500).imag/x0

    l0=bo_eff[-1]    
    w=2*np.pi*f
    x0=w*l0    
    xmeas=f
    ymeas=dzucorrnorm.imag   
    fpar, fcov=optimize.curve_fit(funmu, xmeas, ymeas, p0=[5,1e6], bounds=[[1,0.1e6],[10,2e6]])
    return(fpar, fcov)

def fmu(f,coil_eff,n_splits_f,dzcorrnorm,sigma,espesor,name):
    """fmu (frecuencia, bobina, n_splits_f,datacorr,sigma,dpatron, name)
    Ajuste de la permeabilidad

    Parameters
    ----------
    f : array_like, vector con las frecuencias
    datacorr : array_like, matriz con las mediciones
    bo: array_like, vector con los parametros geometricos de la bobina
    datacorr: array_like, matrix con las mediciones corregidas y nromalizadas
    n : int, indice de la medicion 
    espesor: float, espesor muestra
    sigma : float, conductividad muestra
    """  
    n=n_splits_f
    bo=coil_eff
    mues=list()
    yts=list()
    fs=np.array_split(f,n)
    ys=np.array_split(dzcorrnorm.imag,n)
    l0=bo[-1]
    def funmu(x,a):
        return theo.dzD(x,coil_eff,sigma,espesor,a,1500).imag/x0    
    for i,frec in enumerate(fs):
        w=2*np.pi*frec
        x0=w*l0
        xmeas=frec
        ymeas=ys[i]
        fpar, fcov=optimize.curve_fit(funmu, xmeas, ymeas, p0=5, bounds=(1, 200))    
        yt=theo.dzD(frec,coil_eff,sigma,espesor,fpar[0],1500).imag/x0     
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

def mu2layers(exp,layer1,layer2):
    pass


# matplotlib

def imlogfit(f,data,para_eff,name,savefile=0):
    """ agarra data procesada por fit.mu y guarda png """
    ymeas=data[0]
    yteo=data[1]
    label=para_eff['name']
    p_eff=para_eff['value']
    fig=plt.figure(figsize=(6,4))
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

# 

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