""" Modulo con funciones para graficar en matplotlin o plotly"""	
import iamend_ci.theo as theo															
import os
import csv
import numpy
import numpy as np
import cmath
# import plotly.graph_objs as go
# import plotly
# plotly.offline.init_notebook_mode(connected=True)
# import tkinter as tk
# from tkinter import filedialog
import random
import matplotlib.pyplot as plt
# plt.ion()
# import mpld3
# mpld3.enable_notebook()
# from mpld3 import plugins






## matplotlib






def im(exp,n,figsize=[8,6]):
    """im( frecuencia, datacorr, n)
    Grafica la parte imaginaria de la impedancia corregida y normalizada.
    Parameters
    ----------
    f : array_like, vector con las frecuencias
    datacorr : array_like, matriz con las mediciones
    n : int, indice de la medicion 
    """    
    dz=exp[n]['dzcorrnorm']
    f=exp[n]['f']
    name=exp[n]['name']
    plt.figure(figsize=figsize)
    plt.semilogx(f,dz.imag,'ok',markersize=3,markerfacecolor='none')
    plt.ylabel('$Im(\Delta Z)/X_0$')
    plt.xlabel('Frecuencia [Hz]')
    plt.title(name)
    plt.grid(True, which="both")
    
    
def re(exp,n,figsize=[8,6]):
    """re(frecuencia, datacorr, n)
    Grafica la parte real de la impedancia corregida y normalizada.
    Parameters
    ----------
    f : array_like, vector con las frecuencias
    datacorr : array_like, matriz con las mediciones
    n : int, indice de la medicion 
    """    
    dz=exp[n]['dzcorrnorm']
    f=exp[n]['f']
    name=exp[n]['name']
    plt.figure(figsize=figsize)
    plt.semilogx(f,dz.real,'ok',markersize=3,markerfacecolor='none')
    plt.ylabel('$Re(\Delta Z)/X_0$')
    plt.xlabel('Frecuencia [Hz]')
    plt.title(name)
    plt.grid(True, which="both")
        


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
    #plt.title(acero+name[4:])
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
   
     


def fmu(fdata,save=0,name='default'):
    """ agarra data procesada por fit.fmu y guarda png """
    mrks=['o','s','p','^','*','X']
    plt.figure(figsize=(7,5))
    for i,x in enumerate(fdata[0]):
        f=fdata[1][i]
        ymeas=fdata[2][i]
        yteo=fdata[3][i]
        plt.semilogx(f,ymeas,mrks[i]+'k',markersize=5,markerfacecolor='none',label='mu = '+ str(np.round(fdata[0][i],3)) )
        plt.semilogx(f,yteo,'-k')
    plt.ylabel('$Im(\Delta Z)/X_0$',fontsize=12)
    plt.xlabel('Frecuencia [Hz]',fontsize=12)
    plt.legend(loc='lower left', prop={'size': 13})
    plt.grid(True, which="both")
    if name=='default':
        plt.title(fdata[-1])
    else:
        plt.title(name)
    if save==1:
        g=fdata[-1].split(' ')
        fname=''.join(g)
        plt.savefig('fmu_'+fname)


        
def ffit(fdata,save=0,fit='par',name=''):
    """ agarra data procesada por fit.ffmu guarda png """
    mrks=['o','s','p','^','*','X']
    plt.figure()
    for i,x in enumerate(fdata[0]):
        f=fdata[1][i]
        ymeas=fdata[2][i]
        yteo=fdata[3][i]
        plt.semilogx(f,ymeas,mrks[i]+'k',markersize=5,markerfacecolor='none',label=fit+' = '+ str(np.round(fdata[0][i],3)) )
        plt.semilogx(f,yteo,'-k')
    plt.ylabel('$Im(\Delta Z)/X_0$')
    plt.xlabel('Frecuencia [Hz]')
    plt.legend(loc='lower left')
    plt.title(name)
    if save==1:
        g=fdata[-1].split(' ')
        fname=''.join(g)
        plt.savefig('fmu_'+fname)
        

        




## plotly

def semilog(x,datacorr,titulo='',mode='lines'):
    Y=datacorr[0].imag
    data=[]
    for b,a in enumerate(Y):
        trace0 = go.Scatter(
        x = x,
        y = a,
        name=datacorr[1][b],
        mode = mode)
        data.append(trace0)

    layout = go.Layout(
        xaxis=dict(        type='log',zeroline=False , autorange=True   ),
        yaxis=dict(        type='linear',zeroline=False,autorange=True  ),
        title=titulo
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.iplot(fig)
    return(fig)




def ims(x,datacorr,titulo='',mode='lines'):
    data=[]
    Y=datacorr[0].imag
    datas=datacorr[1]
    for b,a in enumerate(Y):
        trace0 = go.Scatter(
        x = x,
        y = a,
        name=datas[b],    
        mode = mode)
        data.append(trace0)

    layout = go.Layout(
        xaxis=dict(        type='log',zeroline=False , autorange=True   ),
        yaxis=dict(        type='linear',zeroline=False,autorange=True  ),
        title=titulo
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.iplot(fig)



def res(x,datacorr,titulo='',mode='lines'):
    data=[]
    Y=datacorr[0].real
    datas=datacorr[1]
    for b,a in enumerate(Y):
        trace0 = go.Scatter(
        x = x,
        y = a,
        name=datas[b],    
        mode = mode)
        data.append(trace0)

    layout = go.Layout(
        xaxis=dict(        type='log',zeroline=False , autorange=True   ),
        yaxis=dict(        type='linear',zeroline=False,autorange=True  ),
        title=titulo
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.iplot(fig)




def rawplot(dataraw,m):
    data=dataraw[0][m]
    i=int(data[1][-1])
    n=int(len(data[3])/i)
    x=data[2][0:n]
    reY=np.reshape(data[3],(i,n))
    imY=np.reshape(data[4]/data[5],(i,n))
    nms=list()
    for j in np.arange(0,i): nms.append(str(j))
    res(x,list([reY,nms]),titulo='Re(z)'+dataraw[1][m])
    res(x,list([imY,nms]),titulo='Im(z)'+dataraw[1][m])
    



#def Y(data,f='null',mode='lines',type='linear'):
#    """ agarra matriz"""
#    if f=='null':
#        x=np.arange(1,data.shape[0]+1)
#    else:        
#        x=f 
#    Y=data
#    dataplots=list()
#    for i in range(0,Y.shape[1]):
#        trace = go.Scatter(
#        x = x,
#        y = Y[:,i],
#        mode = mode)
#        dataplots.append(trace)
#
#    layout = go.Layout(
#        xaxis=dict(        type=type,zeroline=False , autorange=True   ),
#        yaxis=dict(        type='linear',zeroline=False,autorange=True  )
#            )
#
#    figs = go.Figure(data=dataplots, layout=layout)
#    return(figs)       												
#
#def gety(fig,err=0):
#    if err==0:
#        ys=list()
#        for x in fig.data:
#            ys.append(x['y'])
#    else:
#        ys=list()
#        
#        for i,x in enumerate(fig.data):
#            ys.append(fig.data[i*3+3]['y'])    
#        
#    return(np.array(ys))    
#
#def u(*args,mode='lines',type='linear'):
#    X=args[0::2]
#    Y=args[1::2]
#    dataplots=list()
#    for i,x in enumerate(X):
#        trace = go.Scatter(
#        x = x,
#        y = Y[i],
#        mode = mode)
#        dataplots.append(trace)
#
#    layout = go.Layout(
#        xaxis=dict(        type=type,zeroline=False , autorange=True   ),
#        yaxis=dict(        type=type,zeroline=False,autorange=True  )
#            )
#
#    figs = go.Figure(data=dataplots, layout=layout)
#    return(figs)	
#
#def v(*args,mode='lines',type='linear'):
#    X=args[0::2]
#    Y=args[1::2]
#    dataplots=list()
#    for i,x in enumerate(X):
#        trace = go.Scatter(
#        x = x,
#        y = Y[i],
#        mode = mode)
#        dataplots.append(trace)
#
#    layout = go.Layout(
#        xaxis=dict(        type=type,zeroline=False , autorange=True   ),
#        yaxis=dict(        type=type,zeroline=False,autorange=True  )
#            )
#
#    figs = go.Figure(data=dataplots, layout=layout)
#    plotly.offline.iplot(figs)
#    return(figs)    
#
#
#
#
#
#def logx(*args):
#    X=args[0::2]
#    Y=args[1::2]
#    dataplots=list()
#    for i,x in enumerate(X):
#        trace = go.Scatter(
#        x = x,
#        y = Y[i],
#        mode = 'lines')
#        dataplots.append(trace)
#
#    layout = go.Layout(
#        xaxis=dict(        type='log',zeroline=False , autorange=True   ),
#        yaxis=dict(        type='linear',zeroline=False,autorange=True  )
#            )
#
#    figs = go.Figure(data=dataplots, layout=layout)
#    plotly.offline.iplot(figs)
#    return(figs)
#
#
#
#def vs(X,Y,tipo='log'):
#    dataplots=[]
#    for i,x in enumerate(X):
#        trace0 = go.Scatter(
#                x = x,
#                y = Y[i],
#                mode = 'lines')
#        dataplots.append(trace0)
#    layout = go.Layout(
#                xaxis=dict(        type=tipo,zeroline=False , autorange=True   ),
#                yaxis=dict(        type='linear',zeroline=False,autorange=True  )            )
#    
#    fig = go.Figure(data=dataplots, layout=layout)
#    plotly.offline.iplot(fig)
#    return(fig)
#
#def cat(*args):
#    Fig=getfig(tipo='linear')
#    if len(args)==1:
#        figs=args[0]
#        for i in range(0,len(figs)):
#            Fig.add_traces(figs[i].data[:])
#        ret=Fig    
#    else:
#        
#        for i in range(0,len(args)):
#            Fig.add_traces(args[i].data[:])
#        ret=Fig   
#    return(ret)    
#
#
#def getfig(tipo='log'):
#    layout = go.Layout(
#        xaxis=dict(        type=tipo,zeroline=False , autorange=True   ),
#        yaxis=dict(        type='linear',zeroline=False,autorange=True  )
#    )
#    fig = go.Figure(layout=layout)
#    return(fig)
#    
#
#
#
#    
#    
#def semilogn(x,Y):
#    data=[]
#    for b,a in enumerate(Y):
#        trace0 = go.Scatter(
#        x = x,
#        y = a/(2*np.pi*x),
#        mode = 'markers')
#        data.append(trace0)
#
#    layout = go.Layout(
#        xaxis=dict(        type='log',zeroline=False , autorange=True   ),
#        yaxis=dict(        type='linear',zeroline=False,autorange=True  )
#    )
#
#    fig = go.Figure(data=data, layout=layout)
#    plotly.offline.iplot(fig)
#    return(fig)
#
#
#
#def semilogm(x,Y,titulo=''):
#    data=[]
#    for b,a in enumerate(Y):
#        trace0 = go.Scatter(
#        x = x,
#        y = a,
#        mode = 'markers')
#        data.append(trace0)
#    Ymean=numpy.mean(Y,0)
#    trace0 = go.Scatter(
#    x = x,
#    y = Ymean)
#    data.append(trace0)
#
#    layout = go.Layout(
#        xaxis=dict(        type='log',zeroline=False , autorange=True   ),
#        yaxis=dict(        type='linear',zeroline=False,autorange=True  ),
#        title=titulo
#    )
#
#
#    plotly.offline.iplot(fig)  
#
#
#
    

#### solartron



#
#
#def irawplot(datax,p):
#    data=datax[0][p]
#    i=data[1][-1]
#    n=int(len(data[3])/i)
#    x=data[2][0:n]
#    imY=np.reshape(data[4]/data[5],(i,n))
#    fig=semilog(x,imY,datax[1][p]+'  Im(Z)')
#    return(fig)
#
#
#def iallraw(DATA):
#    figs=list()
#    for p,x in enumerate(DATA[0]):
#        data=x
#        i=int(data[1][-1])
#        n=int(len(data[3])/i)
#        x=data[2][0:n]
#        imY=np.reshape(data[4]/data[5],(i,n))
#        fig=semilog(x,imY,DATA[1][p]+'  Im(Z)')
#        figs.append(fig)
#    return(figs)
#    
#def solarplots(file):
#    """ procesa un archivo, solo arma la matriz """
#    data1=read(file,';')
#    #  return(n,i,f, rez,imz, w )
#    N=len(data1[0])
#    print('N='+str(len(data1[0])))
#    r=data1[1][N-1]
#    print('#iteraciones='+str(data1[1][N-1]))
#    n=int(N/data1[1][N-1])
#    print('#frecuencias='+str(n))
#    semilogm(data1[2][0:n-1],(data1[4]/data1[5]).reshape((r,n)),file)
#    #promedia las N mediciones
#    #datam1=solartron.mean(data1)
#    # rertunr ([fs,rezum,imzum,ws])
#    #semilog(datam1[0],[datam1[2]/datam1[3]],'Promedio de las N iteraciones de una medicion')
#    
#    
#
#    
#def meanplot(data,title):
#    i=data[1][-1]
#    n=int(len(data[3])/i)
#    x=data[2][0:n]
#    reY=np.reshape(data[3],(i,n))
#    imY=np.reshape(data[4]/data[5],(i,n))
#    semilogm(x,reY,title+'  Re(Z)')
#    semilogm(x,imY,title+'  Im(Z)')

###### plots    



def errorplotvR(data,v):
    data2=np.array(data)
    dataz3=data2[0][v]
    DATA=[]
    for n,x in enumerate(dataz3):
        ni=x[1][-1]
        nf=int(int(x[0][-1])/ni)
        f=np.reshape(x[2],(ni,nf))
        fm=np.mean(f,0)
        X=np.reshape(x[3],(ni,nf))
        X=np.array(X)
        X=np.array(X[1:,:]) #saco la primer iteracion
        xm=np.mean(X,0)
        err=list()
        for i in range(0,len(X[0,:])):
            y=X[:,i]
            err.append((max(y)-min(y))/2)
        err=np.array(err)
        upper_bound = go.Scatter(
            name='Upper Bound',
            x=fm,
            y=xm+err/2,
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False,
            legendgroup=data2[1][v[n]])
        
        trace = go.Scatter(
            name=data2[1][v[n]],
            x=fm,
            y=xm,
            mode='lines',
            #line=dict(color='rgb(31, 119, 180)'),
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            legendgroup=data2[1][v[n]])

        lower_bound = go.Scatter(
            name='Lower Bound',
            x=fm,
            y=xm-err/2,
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            showlegend=False,
            legendgroup=data2[1][v[n]])

        # Trace order can be important
        # with continuous error bars
        data = [lower_bound, trace, upper_bound]

        #layout = go.Layout(
        #    yaxis=dict(title='Wind speed (m/s)'),
        #    showlegend = False)

        DATA.extend(data)

    layout = go.Layout(
            xaxis=dict(        type='log',zeroline=False , autorange=True   ),
            yaxis=dict(        type='linear',zeroline=False,autorange=True  ),
            )    
    fig = go.Figure(data=DATA, layout=layout)
    plotly.offline.iplot(fig)
	
def imag(data,m):
    dataz=data[0][m]
    ni=dataz[1][-1]
    nf=int(int(dataz[0][-1])/ni)
    f=np.reshape(dataz[2],(ni,nf))
    fm=np.mean(f,0)
    X=np.reshape(dataz[4]/dataz[5],(ni,nf))
    X=np.array(X)
    xm=np.mean(X,0)
    err=list()
    for i in range(0,len(X[0,:])):
        y=X[:,i]
        err.append((max(y)-min(y))/2)
    err=np.array(err)

    upper_bound = go.Scatter(
        name='Upper Bound',
        x=fm,
        y=xm+err/2,
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False,
        legendgroup=data[1][m])

    trace = go.Scatter(
        x=fm,
        y=xm,
        mode='lines',
        name=data[1][m],
        legendgroup=data[1][m],
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty')

    lower_bound = go.Scatter(
        name='Lower Bound',
        x=fm,
        y=xm-err/2,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        showlegend=False,
        legendgroup=data[1][m])

    # Trace order can be important
    # with continuous error bars
    data = [lower_bound, trace, upper_bound]

    #layout = go.Layout(
    #    yaxis=dict(title='Wind speed (m/s)'),
    #    showlegend = False)
    layout = go.Layout(
            xaxis=dict(        type='log',zeroline=False , autorange=True   ),
            yaxis=dict(        type='linear',zeroline=False,autorange=True  ) )


    fig = go.Figure(data=data, layout=layout)
      
    return(fig)


def errorplotvL(data,v):
    data2=np.array(data)
    dataz3=data2[0][v]
    DATA=[]
    for n,x in enumerate(dataz3):
        ni=x[1][-1]
        nf=int(int(x[0][-1])/ni)
        f=np.reshape(x[2],(ni,nf))
        fm=np.mean(f,0)
        X=np.reshape(x[4]/x[5],(ni,nf))
        X=np.array(X)
        X=np.array(X[1:,:]) #saco la primer iteracion
        xm=np.mean(X,0)
        err=list()
        for i in range(0,len(X[0,:])):
            y=X[:,i]
            err.append((max(y)-min(y))/2)
        err=np.array(err)
        upper_bound = go.Scatter(
            name='Upper Bound',
            x=fm,
            y=xm+err/2,
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False,
            legendgroup=data2[1][v[n]])
        
        trace = go.Scatter(
            name=data2[1][v[n]],
            x=fm,
            y=xm,
            mode='lines',
            #line=dict(color='rgb(31, 119, 180)'),
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            legendgroup=data2[1][v[n]])

        lower_bound = go.Scatter(
            name='Lower Bound',
            x=fm,
            y=xm-err/2,
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            showlegend=False,
            legendgroup=data2[1][v[n]])

      
    fig = plotly.tools.make_subplots(rows=1, cols=1 ,print_grid=False)
    fig.append_trace(lower_bound, 1, 1)
    fig.append_trace(trace, 1, 1)
    fig.append_trace(upper_bound, 1, 1)
    fig["layout"]["xaxis"].update( type='log',zeroline=False , autorange=True   )
    fig["layout"]["yaxis"].update( type='linear',zeroline=False , autorange=True   )

    
    return(fig)    	


def errplot(data,n):
    rr=random.randint(0,12)
    ns=2
    x=data[0][n][2][0:35]
    zim=data[0][n][4].reshape(11,35)
    y=np.mean(zim,0)/(2*np.pi*x)
    y_up=(np.mean(zim,0)+ns*np.std(zim,0))/(2*np.pi*x)
    y_lw=(np.mean(zim,0)-ns*np.std(zim,0))/(2*np.pi*x)

    upper_bound = go.Scatter(
        name='Upper Bound',
        x=x,
        y=y_up,
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor=lrgb2a[rr],
            showlegend=False,
        legendgroup=data[1][n])

    trace = go.Scatter(
        
        x=x,
        y=y,
        mode='markers+lines',
        
        line=dict(width=0.9),
        marker={'symbol':'x','color':lrgb2[rr]},  
        fill='tonexty',
        fillcolor=lrgb2a[rr],
        name=data[1][n],
        showlegend=True,
        legendgroup=data[1][n])


    lower_bound = go.Scatter(
        name='Lower Bound',
        x=x,
        y=y_lw,      
        line=dict(width=0),
        mode='lines',
            showlegend=False,
        legendgroup=data[1][n])


    # Trace order can be important
    # with continuous error bars
    dataplot = [lower_bound, trace, upper_bound]

    #layout = go.Layout(
    #    yaxis=dict(title='Wind speed (m/s)'),
    #    showlegend = False)
    layout = go.Layout(
            xaxis=dict(        type='log',zeroline=False , autorange=True   ),
            yaxis=dict(        type='linear',zeroline=False,autorange=True  ),
    
        )

    fig = go.Figure(data=dataplot, layout=layout)
    return(fig)




def errplotall(dataraw,corr=0,Z0=0):
    if corr==1:
        figs=list()
        data=[datamean(dataraw),dataraw[1]]
        datas=data[1]
        data=np.array(data[0])
        za=data[0][1]
        
        datacorr=[]
        lwerr=[]
        uperr=[]
        for i,x in enumerate(data):
                    rr=random.randint(0,11)
                    f=x[0].real
                    zu=x[1]
                    w=x[2].real
                    xraw=dataraw[0][i][4].reshape(int(dataraw[0][i][4].shape[0]/f.shape[0]),f.shape[0])
                    x0=w*Z0.imag
                    z0=Z0.real+1j*x0

                    ns=2    
                    dzucorr=((1/(1/zu - 1/za + 1/z0))-z0  )
                    yupcorr=((1/(1/(zu+1j*ns*np.std(xraw,0)) - 1/za + 1/z0))-z0  )
                    ylwcorr=((1/(1/(zu-1j*ns*np.std(xraw,0)) - 1/za + 1/z0))-z0  )


                    y = (np.imag(dzucorr)/x0).real
                    y_upcorr=(np.imag(yupcorr)/x0).real
                    y_lwcorr=(np.imag(ylwcorr)/x0).real
                    
                           
                    trace0 = go.Scatter(
                    x =f ,
                    y = y,
                    mode = 'markers+lines',
                    line=dict(width=0.9),
                    marker={'symbol':'x','color':lrgb2[rr]},  
                    fill='tonexty',
                    fillcolor=lrgb2a[rr],
                    name=datas[i],
                    showlegend=True,
                    legendgroup=datas[i])
                    
                    upper_bound = go.Scatter(
                        name='Upper Bound',
                        x=f,
                        y=y_upcorr,
                        mode='lines',
                        line=dict(width=0),
                        fill='tonexty',
                        fillcolor=lrgb2a[rr],
                            showlegend=False,
                        legendgroup=datas[i])                    

                    lower_bound = go.Scatter(
                        name='Lower Bound',
                        x=f,
                        y=y_lwcorr,      
                        line=dict(width=0),
                        mode='lines',
                            showlegend=False,
                        legendgroup=datas[i])
                   
                    
                    datacorr.append(dzucorr/x0)    
                    lwerr.append(ylwcorr/x0)           
                    uperr.append(yupcorr/x0) 
                    
                    
                    layout = go.Layout(
                    xaxis=dict(        type='log',zeroline=False , autorange=True   ),
                    yaxis=dict(        type='linear',zeroline=False,autorange=True  ))
                    figs.append(go.Figure(data=[lower_bound, trace0, upper_bound], layout=layout))

        for i in range(1,len(figs)):
            figs[0].add_traces(figs[i].data)
            
        ret=[np.array(datacorr[1:]),np.array(lwerr[1:]),np.array(uperr[1:]),figs[0]]
        
    else:
        figs=list()
        data=dataraw
        for n,datax in enumerate(data[0]):
            rr=random.randint(0,11)
            ni=data[0][n][1][-1]
            nf=int(int(data[0][n][0][-1])/ni)

            ns=2
            x=data[0][n][2][0:nf]
            zim=data[0][n][4].reshape(ni,nf)
            y=np.mean(zim,0)/(2*np.pi*x)
            y_up=(np.mean(zim,0)+ns*np.std(zim,0))/(2*np.pi*x)
            y_lw=(np.mean(zim,0)-ns*np.std(zim,0))/(2*np.pi*x)

            upper_bound = go.Scatter(
                name='Upper Bound',
                x=x,
                y=y_up,
                mode='lines',
                line=dict(width=0),
                fill='tonexty',
                fillcolor=lrgb2a[rr],
                    showlegend=False,
                legendgroup=data[1][n])

            trace = go.Scatter(

                x=x,
                y=y,
                mode='markers+lines',

                line=dict(width=0.9),
                marker={'symbol':'x','color':lrgb2[rr]},  
                fill='tonexty',
                fillcolor=lrgb2a[rr],
                name=data[1][n],
                showlegend=True,
                legendgroup=data[1][n])


            lower_bound = go.Scatter(
                name='Lower Bound',
                x=x,
                y=y_lw,      
                line=dict(width=0),
                mode='lines',
                    showlegend=False,
                legendgroup=data[1][n])


            # Trace order can be important
            # with continuous error bars
            dataplot = [lower_bound, trace, upper_bound]

            #layout = go.Layout(
            #    yaxis=dict(title='Wind speed (m/s)'),
            #    showlegend = False)
            layout = go.Layout(
                    xaxis=dict(        type='log',zeroline=False , autorange=True   ),
                    yaxis=dict(        type='linear',zeroline=False,autorange=True  ),

                )

            figs.append(go.Figure(data=dataplot, layout=layout))

        for i in range(1,len(figs)):
            figs[0].add_traces(figs[i].data)
        ret=figs[0]    
    return(ret)

def errplotre(dataz):
    ni=dataz[1][-1]
    nf=int(int(dataz[0][-1])/ni)
    f=np.reshape(dataz[2],(ni,nf))
    fm=np.mean(f,0)
    X=np.reshape(dataz[3],(ni,nf))
    X=np.array(X)
    xm=np.mean(X,0)
    err=list()
    for i in range(0,len(X[0,:])):
        y=X[:,i]
        err.append((max(y)-min(y))/2)
    err=np.array(err)
    
    
    
    upper_bound = go.Scatter(
        name='Upper Bound',
        x=fm,
        y=xm+err/2,
        mode='lines',
        line=dict(width=0),
        fillcolor=lrgb2a[rr],
                showlegend=False,
        fill='tonexty')

    trace = go.Scatter(
        name='Measurement',
        x=fm,
        y=xm,
        mode='lines',
        line=dict(color='rgb(31, 119, 180)'),
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty')

    lower_bound = go.Scatter(
        name='Lower Bound',
        x=fm,
        y=xm-err/2,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines')

    # Trace order can be important
    # with continuous error bars
    data = [lower_bound, trace, upper_bound]

    #layout = go.Layout(
    #    yaxis=dict(title='Wind speed (m/s)'),
    #    showlegend = False)
    layout = go.Layout(
            xaxis=dict(        type='log',zeroline=False , autorange=True   ),
            yaxis=dict(        type='linear',zeroline=False,autorange=True  ),
            showlegend = False,
        )
    fig = go.Figure(data=data, layout=layout)
    
    return(fig)
	
def imags(*args):
    figs=list()
    DATA=args[0::2]
    M=args[1::2]
    for i,data in enumerate(DATA):
        m=M[i]
        dataz=data[0][m]
        ni=dataz[1][-1]
        nf=int(int(dataz[0][-1])/ni)
        f=np.reshape(dataz[2],(ni,nf))
        fm=np.mean(f,0)
        X=np.reshape(dataz[4]/dataz[5],(ni,nf))
        X=np.array(X)
        xm=np.mean(X,0)
        err=list()
        for i in range(0,len(X[0,:])):
            y=X[:,i]
            err.append((max(y)-min(y))/2)
        err=np.array(err)

        upper_bound = go.Scatter(
            name='Upper Bound',
            x=fm,
            y=xm+err/2,
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False,
            legendgroup=data[1][m])

        trace = go.Scatter(
            x=fm,
            y=xm,
            mode='lines',
            name=data[1][m],
            legendgroup=data[1][m],
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty')

        lower_bound = go.Scatter(
            name='Lower Bound',
            x=fm,
            y=xm-err/2,
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            showlegend=False,
            legendgroup=data[1][m])

        # Trace order can be important
        # with continuous error bars
        data = [lower_bound, trace, upper_bound]

        #layout = go.Layout(
        #    yaxis=dict(title='Wind speed (m/s)'),
        #    showlegend = False)
        layout = go.Layout(
                xaxis=dict(        type='log',zeroline=False , autorange=True   ),
                yaxis=dict(        type='linear',zeroline=False,autorange=True  ) )


        fig = go.Figure(data=data, layout=layout)
        figs.append(fig)
      
    return(figs)







        
defaultsa=['rgba(31, 119, 180,0.5)',
 'rgba(255, 127, 14,0.5)',
 'rgba(44, 160, 44,0.5)',
 'rgba(214, 39, 40,0.5)',
 'rgba(148, 103, 189,0.5)',
 'rgba(140, 86, 75,0.5)',
 'rgba(227, 119, 194,0.5)',
 'rgba(127, 127, 127,0.5)',
 'rgba(188, 189, 34,0.5)',
 'rgba(23, 190, 207,0.5)']


lrgb=['rgb(141,211,199)',
 'rgb(255,255,179)',
 'rgb(190,186,218)',
 'rgb(251,128,114)',
 'rgb(128,177,211)',
 'rgb(253,180,98)',
 'rgb(179,222,105)',
 'rgb(252,205,229)',
 'rgb(217,217,217)',
 'rgb(188,128,189)',
 'rgb(204,235,197)']

lrgb2=['rgb(166,206,227)','rgb(31,120,180)','rgb(178,223,138)','rgb(51,160,44)','rgb(251,154,153)','rgb(227,26,28)','rgb(253,191,111)','rgb(255,127,0)','rgb(202,178,214)','rgb(106,61,154)','rgb(255,255,153)','rgb(177,89,40)']

lrgb2a=['rgba(166,206,227,0.5)',
 'rgba(31,120,180,0.5)',
 'rgba(178,223,138,0.5)',
 'rgba(51,160,44,0.5)',
 'rgba(251,154,153,0.5)',
 'rgba(227,26,28,0.5)',
 'rgba(253,191,111,0.5)',
 'rgba(255,127,0,0.5)',
 'rgba(202,178,214,0.5)',
 'rgba(106,61,154,0.5)',
 'rgba(255,255,153,0.5)',
 'rgba(177,89,40,0.5)']

lrgba=['rgba(141,211,199,0.5)',
 'rgba(255,255,179,0.5)',
 'rgba(190,186,218,0.5)',
 'rgba(251,128,114,0.5)',
 'rgba(128,177,211,0.5)',
 'rgba(253,180,98,0.5)',
 'rgba(179,222,105,0.5)',
 'rgba(252,205,229,0.5)',
 'rgba(217,217,217,0.5)',
 'rgba(188,128,189,0.5)',
 'rgba(204,235,197,0.5)']	


