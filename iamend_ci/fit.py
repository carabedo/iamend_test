""" Modulo con las funciones para fitear impedancias"""
import iamend_ci.theo as theo
import numpy as np
from scipy import optimize
import plotly.graph_objs as go
import matplotlib.pyplot as plt

from plotly.subplots import make_subplots

def z1(exp,n):
    
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

    f=exp[n]['f']
    bo=exp[n]['bo']
    dzucorrnorm=exp[n]['dzcorrnorm']
    dpatron=exp[n]['espesor']
    sigma=exp[n]['sigma']
    name=exp[n]['name']
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
    #plt.title(acero+name[4:])
    plt.title(name)
    plt.grid(True, which="both")
    if savefile==1:
        g=name.split(' ')
        fname=''.join(g)
        plt.savefig(fname)   
    return fig











def mu(exp,n, z1eff):
    """mu (frecuencia, bobina, datacorr, n, dpatron,sigma, mur)
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
    f=exp[n]['f']
    bo=exp[n]['bo']
    dzucorrnorm=exp[n]['dzcorrnorm']
    dpatron=exp[n]['espesor']
    sigma=exp[n]['sigma']
    name=exp[n]['name']
    def funmu(x,a):
        bob=bo[:]
        bob[4]=z1eff
        return theo.dzD(x,bob,sigma,dpatron,a,1500).imag/x0
    #[f,z0,dzucorr,w]
    l0=bo[-1]    
    w=2*np.pi*f
    x0=w*l0
      
    xmeas=f
    ymeas=dzucorrnorm.imag   
    fpar, fcov=optimize.curve_fit(funmu, xmeas, ymeas, p0=[1], bounds=(0,150))
    

    mur=fpar[0]

    yteo=theo.dzD(f,bo,sigma,dpatron,mur,1500)
    yteo=yteo.imag/x0
    

    # fig=semilogfit(f,[ymeas, yteo],'curve_fit{mu} '+datacorr[1][n])
    # print('mu =',fpar[0])
    # return(fpar,fig)

    
    para_eff={'name' : 'mu_r', 'value' : mur}

    fig=imlogfit(f,[ymeas, yteo],para_eff,name)
    print('mu_r_eff =',fpar[0])
    return(fpar,fig)





# plotly
def semilogfit(x,Y,titulo):
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




#####################


#
#
#def mu(f,bo,dzcorrnorm,sigma,z1eff,dpatron=1,silent=1, lims=(1, 100),name='noname'):
#    def funmu(x,a):
#        bob=bo[:]
#        bob[4]=z1eff
#        return theo.dzD(x,bob,sigma,dpatron,a,1500).imag/x0
#    
#    l0=bo[-1]
#    w=2*np.pi*f
#    x0=w*l0
#    
#    xmeas=f
#    ymeas=dzcorrnorm.imag
#    fpar, fcov=optimize.curve_fit(funmu, xmeas, ymeas, p0=5, bounds=lims)
#    yteo=funmu(f,fpar[0])
#    res = ymeas-yteo
#    ss_res=np.sum(res**2)
#    ss_tot = np.sum((ymeas-np.mean(ymeas))**2)
#    rsqr=1-(ss_res/ss_tot)
#    if silent==0:    
#        print('mu =',fpar, '  perr =',perr)
#            
#    return([bo,f,dzcorrnorm,sigma,dpatron,fpar[0],rsqr,yteo,name])

#
#
#
#def semilog():
#    """ plot plotly semilog """
#    fig = go.Figure()
#    fig["layout"]["xaxis"].update( type='log',zeroline=False , autorange=True   )
#    fig["layout"]["yaxis"].update( type='linear',zeroline=False , autorange=True   )
#    return(fig)
#
#def z1r2(bo,aire,muestra,sep,dpatron,sigma,mur):
#    """ fiteo z1 r2 """
#    def funz1r2(x,a,b):
#        r1=bo[0]
#        r2=a
#        dh=bo[2]
#        N=bo[3]
#        z1=b
#        bob=[r1,r2,dh,N,z1,1]
#        return dztheo.dzHF(x,bob,sigma,mur,3000).imag/x0
#    dzucorr=solartron.dzcorr(aire,muestra,sep)
#    za=solartron.mean(solartron.read(aire,sep))    
#    z0=dzucorr[1]
#    x0=dzucorr[1].imag
#    r0=dzucorr[1].real
#    w=za[3]
#    f=za[0]
#    l0=dzucorr[1].imag/w
#    xmeas=f
#    ymeas=dzucorr[2].imag/x0    
#    fpar, fcov=optimize.curve_fit(funz1r2, xmeas, ymeas, p0=[bo[1],bo[4]], bounds=(0,5e-3))
#    r2eff=fpar[0]
#    z1eff=fpar[1]
#    r1=bo[0]
#    dh=bo[2]
#    N=bo[3]
#    boeff=[r1,r2eff,dh,N,z1eff,l0]
#    yteo=dztheo.dzD(f,boeff,sigma,dpatron,mur,3000)
#    yteo=yteo.imag/x0
#    semilogfit(f,[ymeas, yteo],'im(dzucorr vs dzteo) curve_fit{z1,r2}')
#    print('r2 =',fpar[0]*1000,'  z1 =',fpar[1]*1000)
#    return(fpar)
#
#def sigma(bo,aire,muestra,sep,dpatron,z1,mur):
#    """ fiteo sigma """
#    def funz1r2(x,b):
#        r1=bo[0]
#        r2=bo[1]
#        dh=bo[2]
#        N=bo[3]
#        bob=[r1,r2,dh,N,z1,1]
#        return dztheo.dzHF(x,bob,b,mur,3000).imag/x0    
#    dzucorr=solartron.dzcorr(aire,muestra,sep)
#    za=solartron.mean(solartron.read(aire,sep))
#    z0=dzucorr[1]
#    x0=dzucorr[1].imag
#    r0=dzucorr[1].real
#    w=za[3]
#    f=za[0]
#    l0=dzucorr[1].imag/w
#    xmeas=f
#    ymeas=dzucorr[2].imag/x0
#    fpar, fcov=optimize.curve_fit(funz1r2, xmeas, ymeas, p0=[1e6], bounds=((1e6,1e8)))
#    r1=bo[0]
#    r2=bo[1]
#    dh=bo[2]
#    N=bo[3]
#    boeff=[r1,r2,dh,N,z1,l0]
#    sigmaeff=fpar[0]
#    yteo=dztheo.dzD(f,boeff,sigmaeff,dpatron,mur,3000)
#    yteo=yteo.imag/x0
#    semilogfit(f,[ymeas, yteo],'im(dzucorr vs dzteo) curve_fit{z1}')
#    print( 'sigma =',fpar[0])
#    return(fpar)
#
#def sigmaz1(bo,aire,muestra,sep,dpatron,mur):
#    """ fiteo sigma z1 """
#    def funz1r2(x,a,b):
#        r1=bo[0]
#        r2=bo[1]
#        dh=bo[2]
#        N=bo[3]
#        z1=a
#        bob=[r1,r2,dh,N,z1,1]
#        return dztheo.dzHF(x,bob,b,mur,3000).imag/x0
#    
#    dzucorr=solartron.dzcorr(aire,muestra,sep)
#    za=solartron.mean(solartron.read(aire,sep))
#    z0=dzucorr[1]
#    x0=dzucorr[1].imag
#    r0=dzucorr[1].real
#    w=za[3]
#    f=za[0]
#    l0=dzucorr[1].imag/w
#    xmeas=f
#    ymeas=dzucorr[2].imag/x0
#    r1=bo[0]
#    r2=bo[1]
#    dh=bo[2]
#    N=bo[3]
#    fpar, fcov=optimize.curve_fit(funz1r2, xmeas, ymeas, p0=[bo[4],1e6], bounds=((0,5e-3),(1e6,1e8)))
#    fpar
#    r2eff=r2
#    z1eff=fpar[0]
#    boeff=[r1,r2eff,dh,N,z1eff,l0]
#    sigmaeff=fpar[1]
#    yteo=dztheo.dzD(f,boeff,sigmaeff,dpatron,mur,3000)
#    yteo=yteo.imag/x0
#    semilogfit(f,[ymeas, yteo],'im(dzucorr vs dzteo) curve_fit{z1,sigma}')
#    print('z1 =',fpar[0]*1000,'  sigma =',fpar[1]/1e6)
#    return(fpar)
#
#def muz1(bo,aire,muestra,sep,dpatron,sigma):
#    """ fiteo mu z1 """
#    def funmuz1(x,a,b):
#        r1=bo[0]
#        r2=bo[1]
#        dh=bo[2]
#        N=bo[3]
#        z1=a
#        bob=[r1,r2,dh,N,z1,1]
#        return dztheo.dzHF(x,bob,sigma,b,3000).imag/x0
#    
#    dzucorr=solartron.dzcorr(aire,muestra,sep)
#    za=solartron.mean(solartron.read(aire,sep))
#    z0=dzucorr[1]
#    x0=dzucorr[1].imag
#    r0=dzucorr[1].real
#    w=za[3]
#    f=za[0]
#    l0=dzucorr[1].imag/w
#    xmeas=f
#    ymeas=dzucorr[2].imag/x0
#    fpar, fcov=optimize.curve_fit(funmuz1, xmeas, ymeas, p0=[bo[4],1], bounds=((0,3e-3),(1,150)))
#    z1eff=fpar[0]
#    r1=bo[0]
#    r2=bo[1]
#    dh=bo[2]
#    N=bo[3]
#    boeff=[r1,r2,dh,N,z1eff,l0]
#    mueff=fpar[1]
#    yteo=dztheo.dzD(f,boeff,sigma,dpatron,mueff,3000)
#    yteo=yteo.imag/x0
#    #semilogfit(f,[ymeas, yteo],'im(dzucorr vs dzteo) curve_fit{z1,mu}')
#    print('z1 =',fpar[0]*1000,'  mu =',fpar[1])
#    return(fpar,f,ymeas,yteo)
#
#def mu2(bo,aire,muestra,sep,dpatron,sigma):
#    """ fiteo mu 2"""
#    def funmuz1(x,a):
#        return dztheo.dzHF(x,bo,sigma,a,3000).imag/x0    
#    dzucorr=solartron.dzcorr(aire,muestra,sep)
#    za=solartron.mean(solartron.read(aire,sep))
#    z0=dzucorr[1]
#    x0=dzucorr[1].imag
#    r0=dzucorr[1].real
#    w=za[3]
#    f=za[0]
#    l0=dzucorr[1].imag/w
#    xmeas=f
#    ymeas=dzucorr[2].imag/x0
#    fpar, fcov=optimize.curve_fit(funmuz1, xmeas, ymeas, p0=[1], bounds=(1,150))
#    mueff=fpar[0]
#    yteo=dztheo.dzD(f,bo,sigma,dpatron,mueff,3000)
#    yteo=yteo.imag/x0
#    semilogfit(f,[ymeas, yteo],'im(dzucorr vs dzteo) curve_fit{z1,mu}')
#    print('  mu =',fpar[0])
#    return(fpar)
# 
#def sigma2(aire,muestra,sep,dpatron,r2,mur):
#    """ definido para mediciones de GCC sin header en el CSV """
#    def funz1r2(x,a,b):
#        bo=bobina.bo
#        r1=bo[0]
#        dh=bo[2]
#        N=bo[3]
#        z1=a
#        bob=[r1,r2,dh,N,z1,1]
#        return dztheo.dzHF(x,bob,b,mur,3000).imag/x0    
#    dzucorr=solartron.dzcorr2(aire,muestra,sep)
#    za=solartron.mean2(solartron.read2(aire,sep))
#    z0=dzucorr[1]
#    x0=dzucorr[1].imag
#    r0=dzucorr[1].real
#    w=za[3]
#    f=za[0]
#    l0=dzucorr[1].imag/w
#    xmeas=f
#    ymeas=dzucorr[2].imag/x0
#    bo=bobina.bo
#    r1=bo[0]
#    dh=bo[2]
#    N=bo[3]
#    fpar, fcov=optimize.curve_fit(funz1r2, xmeas, ymeas, p0=[bo[1],1e6], bounds=((0,5e-3),1e6,1e8))
#    fpar
#    r2eff=r2
#    z1eff=fpar[0]
#    boeff=[r1,r2eff,dh,N,z1eff,l0]
#    sigmaeff=fpar[1]
#    yteo=dztheo.dzD(f,boeff,sigmaeff,dpatron,mur,3000)
#    yteo=yteo.imag/x0
#    semilogfit(f,[ymeas, yteo],'im(dzucorr vs dzteo) curve_fit{z1,r2}')
#    print('z1 =',fpar[0],'  sigma =',fpar[1])
#    
######### nuevo 22.02.19
#
#
#
#
#
#
#def z1r1(bo,datacorr,dpatron,sigma,mur):
#    """ fiteo z1 y r1 """
#    def funz1r1(x,b,a):
#        r1=a
#        r2=bo[1]
#        dh=bo[2]
#        N=bo[3]
#        z1=b
#        bob=[r1,r2,dh,N,z1,1]
#        return dztheo.dzD(x,bob,sigma,dpatron,mur,3000).imag/x0
#  #[f,z0,dzucorr,w]
#    f=datacorr[0]
#    l0=datacorr[1]
#    dzucorrnorm=datacorr[2]
#    w=2*np.pi*f
#    x0=w*l0
#      
#    xmeas=f
#    ymeas=dzucorrnorm.imag   
#    fpar, fcov=optimize.curve_fit(funz1r1, xmeas, ymeas, p0=[1.1e-3, bo[0]], bounds=(0,5e-3))
#    
#
#    z1eff=fpar[0]
#    r2=bo[1]
#    r1eff=fpar[1]
#    dh=bo[2]
#    N=bo[3]
#    boeff=[r1eff,r2,dh,N,z1eff,l0]
#    yteo=dztheo.dzD(f,boeff,sigma,dpatron,mur,3000)
#    yteo=yteo.imag/x0
#    
#    fig=semilogfit(f,[ymeas, yteo],'curve_fit{z1 r1}')
#    print('z1 =',fpar[0]*1000,'mm')
#    print('r1 =',fpar[1]*1000,'mm')
#
#    return([fpar,fig])
#
#def z1r2(bo,datacorr,dpatron,sigma,mur):
#    """ fiteo z1 y r2 """
#    def funz1r2(x,b,a):
#        r1=bo[0]
#        r2=a
#        dh=bo[2]
#        N=bo[3]
#        z1=b
#        bob=[r1,r2,dh,N,z1,1]
#        return dztheo.dzD(x,bob,sigma,dpatron,mur,3000).imag/x0
#    #[f,z0,dzucorr,w]
#    f=datacorr[0]
#    l0=datacorr[1]
#    dzucorrnorm=datacorr[2]
#    w=2*np.pi*f
#    x0=w*l0
#    
#    xmeas=f
#    ymeas=dzucorrnorm.imag   
#    fpar, fcov=optimize.curve_fit(funz1r2, xmeas, ymeas, p0=[1.1e-3, bo[0]], bounds=((0,3e-3),(2e-3,8e-3)))
#    
#
#    z1eff=fpar[0]
#    r1=bo[0]
#    r2eff=fpar[1]
#    dh=bo[2]
#    N=bo[3]
#    boeff=[r1,r2eff,dh,N,z1eff,l0]
#    yteo=dztheo.dzD(f,boeff,sigma,dpatron,mur,3000)
#    yteo=yteo.imag/x0
#    
#    fig=semilogfit(f,[ymeas, yteo],'curve_fit{z1 r2}')
#    print('z1 =',fpar[0]*1000,'mm')
#    print('r2 =',fpar[1]*1000,'mm')
#
#    return([fpar,fig])
#
#def z1N(bo,datacorr,dpatron,sigma,mur):
#    """" fiteo z1 y N """
#    def funz1N(x,b,a):
#        r1=bo[0]
#        r2=bo[1]
#        dh=bo[2]
#        N=a
#        z1=b
#        bob=[r1,r2,dh,N,z1,1]
#        return dztheo.dzD(x,bob,sigma,dpatron,mur,3000).imag/x0
#    #[f,z0,dzucorr,w]
#    f=datacorr[0]
#    l0=datacorr[1]
#    dzucorrnorm=datacorr[2]
#    w=2*np.pi*f
#    x0=w*l0
#    
#    xmeas=f
#    ymeas=dzucorrnorm.imag   
#    fpar, fcov=optimize.curve_fit(funz1N, xmeas, ymeas, p0=[1.1e-3, bo[3]], bounds=((0,200), (2e-3, 400)))
#    
#
#    z1eff=fpar[0]
#    r2=bo[1]
#    r1=bo[0]
#    dh=bo[2]
#    Neff=fpar[1]
#    boeff=[r1,r2,dh,Neff,z1eff,l0]
#    yteo=dztheo.dzD(f,boeff,sigma,dpatron,mur,3000)
#    yteo=yteo.imag/x0
#    
#    fig=semilogfit(f,[ymeas, yteo],'curve_fit{z1 N}')
#    print('z1 =',fpar[0]*1000,'mm')
#    print('N =',fpar[1],'vueltas')
#    return([fpar,fig])
#
#
#def bob(bo,datacorr,dpatron,sigma,mur):
#    def funz1(x,a,b,c):
#        r1=bo[0]
#        r2=a
#        dh=bo[2]
#        N=b
#        z1=c
#        bob=[r1,r2,dh,N,z1,1]
#        return dztheo.dzD(x,bob,sigma,dpatron,mur,3000).imag/x0
#    #[f,z0,dzucorr,w]
#    f=datacorr[0]
#    l0=datacorr[1]
#    dzucorrnorm=datacorr[2]
#    w=2*np.pi*f
#    x0=w*l0
#      
#    xmeas=f
#    ymeas=dzucorrnorm.imag   
#    fpar, fcov=optimize.curve_fit(funz1, xmeas, ymeas, p0=[bo[1],bo[3],bo[4]], bounds=((bo[0],240,1e-3),(5e-3,260,1.3e-3)),method='trf')
#    
#
#    z1eff=fpar[2]
#    r1=bo[0]
#    r2=fpar[0]
#    dh=bo[2]
#    N=fpar[1]
#    boeff=[r1,r2,dh,N,z1eff,l0]
#    yteo=dztheo.dzD(f,boeff,sigma,dpatron,mur,3000)
#    yteo=yteo.imag/x0
#    fig=semilogfit(f,[ymeas, yteo],'curve_fit{r2 N z1} ')
#    print(fpar)
#    return([fpar, fig])
#
### 02-19
#
#def z1mu(f,bo,datacorr,dpatron,sigma):
#    """ fiteo de z1 y mu """    
#    def funz1mu(x,a,b):
#        r1=bo[0]
#        r2=bo[1]
#        dh=bo[2]
#        N=bo[3]
#        z1=a
#        bob=[r1,r2,dh,N,z1,1]
#        return theo.dzD(x,bob,sigma,dpatron,b,3000).imag/x0
#    #[f,z0,dzucorr,w]
#    l0=bo[-1]
#    dzucorrnorm=datacorr
#    w=2*np.pi*f
#    x0=w*l0
#    
#    xmeas=f
#    ymeas=dzucorrnorm.imag   
#    fpar, fcov=optimize.curve_fit(funz1mu, xmeas, ymeas, p0=[1.1e-3, 5], bounds=((0,1), (3.5e-3, 100)))
#    
#
#    z1eff=fpar[0]
#    r2=bo[1]
#    r1=bo[0]
#    dh=bo[2]
#    Neff=bo[3]
#    boeff=[r1,r2,dh,Neff,z1eff,l0]
#    yteo=theo.dzD(f,boeff,sigma,dpatron,fpar[1],3000)
#    yteo=yteo.imag/x0
#    
#    fig=semilogfit(f,[ymeas, yteo],str(np.round(fpar[1]))+'   '+str(np.round(fpar[0]*1e3,2))+'mm')
#    print('z1 =',fpar[0]*1000,'mm')
#    print('mu =',fpar[1])
#    return([fpar,fig])
#
##### 
#def mu3(bo,datacorr,sigmas,mur2,z1,title):    
#    """propongo una region de espesor 'd' con permeablidad relativa 'mu1'"""
#    def fun(x,a,b):
#        r1=bo[0]
#        r2=bo[1]
#        dh=bo[2]
#        N=bo[3]
#        bob=[r1,r2,dh,N,z1,1]
#        return dztheo.dz2(x,bob,sigmas,a,b,mur2,3000).imag/x0      
#    #[f,z0,dzucorr,w]
#    f=datacorr[0]
#    l0=datacorr[1]
#    dzucorrnorm=datacorr[2]
#    w=2*np.pi*f
#    x0=w*l0
#      
#    xmeas=f
#    ymeas=dzucorrnorm.imag   
#    fpar, fcov=optimize.curve_fit(fun, xmeas, ymeas, p0=[0.1e-3,mur2], bounds=((0,2e-3),(1,200)))
#    
#
#    r1=bo[0]
#    r2=bo[1]
#    dh=bo[2]
#    N=bo[3]
#    boeff=[r1,r2,dh,N,z1,l0]
#    yteo=dztheo.dz2(f,boeff,sigmas,fpar[0],fpar[1],mur2,3000)
#    yteo=yteo.imag/x0
#    
#    fig=mufit.semilogfit(f,[ymeas, yteo],'curve_fit{z1} '+title)
#    print('d =',fpar[0]*1000,'mm')
#    print('mu1 =',fpar[1])
#    return(fpar,fig)
