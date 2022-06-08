""" Modulo para el procesamiento de los archivos CVS del solartron"""
import iamend_ci.theo as theo

import os
# import tkinter as tk
# from tkinter import filedialog
import csv
import numpy
import numpy as np
import cmath
# import plotly.graph_objs as go
# import plotly
# plotly.offline.init_notebook_mode(connected=True)
import random



###### OLD
	
def zload(): 
    root = tk.Tk()
    root.lift()
    root.attributes('-topmost',True)
    root.after_idle(root.attributes,'-topmost',False)
    folder_path = filedialog.askdirectory()
    files=list()
    print(folder_path)
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        
        for i,j in enumerate(filenames):
            files.extend([dirpath + '\\'+j])
            print(i,j)
        break
    
    root.withdraw()
    return (files,filenames)

def csv2data(files,separador):
    
    
    data=list()
    for file in files[0]:
        data.append(read(file,separador))
    return(data,files[1])



def read2(file, separador):
    z=list()
    with open(file, 'r') as csvfile:
        spam = csv.reader(csvfile, delimiter=separador)
        for row in spam:
            z.append(row)

    f=list()
    rez=list()
    imz=list()
    n=list()
    i=list()
    for x in range(len(z)):
        f.append(float(z[x][4]))
        rez.append(float(z[x][7]))
        imz.append(float(z[x][8]))
        n.append(int(z[x][0]))
        i.append(int(z[x][1]))
    f = numpy.asarray(f)
    w=2*numpy.pi*f
    rez=numpy.asarray(rez)
    imz=numpy.asarray(imz)
    n=numpy.asarray(n)
    i=numpy.asarray(i)
    return(n,i,f, rez,imz, w )

def mean(zs):
    zs=numpy.array(zs)
    # numero de iteraciones
    ni=int(zs[1][len(zs[0])-1])
    # numero total de mediciones
    n=len(zs[1])
    # numero de puntos de cada medicion
    nm=int(n/ni)
    zsmean=list()
    f=zs[2]
    rezu=zs[3]
    imzu=zs[4]
    w=zs[5]
    rezu2=numpy.reshape(rezu,(ni,nm))
    imzu2=numpy.reshape(imzu,(ni,nm))
    # tiro la primera
    rezum=numpy.mean(rezu2[1:11],0)
    imzum=numpy.mean(imzu2[1:11],0)
    fs=numpy.reshape(f,(ni,nm))
    fs=numpy.mean(fs,0)
    ws=2*numpy.pi*fs
    zsmean=numpy.array([fs,rezum,imzum,ws])
    return(zsmean)

def mean2(zs):
    zs=numpy.array(zs)
    # numero de iteraciones
    ni=int(zs[1][len(zs[0])-1])
    # numero total de mediciones
    n=len(zs[1])
    # numero de puntos de cada medicion
    nm=int(n/ni)
    zsmean=list()
    f=zs[2]
    rezu=zs[3]
    imzu=zs[4]
    w=zs[5]
    rezu2=numpy.reshape(rezu,(ni,nm))
    imzu2=numpy.reshape(imzu,(ni,nm))
    # tiro la primera
    rezum=numpy.mean(rezu2[1:11],0)
    imzum=numpy.mean(imzu2[1:11],0)
    fs=numpy.reshape(f,(ni,nm))
    fs=numpy.mean(fs,0)
    ws=2*numpy.pi*fs
    zsmean=numpy.array([fs,rezum,imzum,ws])
    return(zsmean)

def zcorr_vf(w,za,zu,r0,l0):
    z0=r0+1j*w*l0
    return (((1/(1/zu - 1/za + 1/z0))-z0))

def z0(aire):
    data1=read(aire,';')
    data1=mean(data1)
    #  return[fs,rezum,imzum,ws]
    ws=data1[3]
    l0=(data1[2]/ws)[0]
    r0=data1[1][0]
    za=data1[1]+1j*data1[2]
    f=data1[0]
    z0=r0+1j*ws*l0
    return([f,za,z0,w])


# cargo datos del aire
def dzcorr(aire,file,sep):
    data1=read(aire,sep)
    data1=mean(data1)
    #  return[fs,rezum,imzum,ws]
    ws=data1[3]
    l0=(data1[2]/ws)[0]
    r0=data1[1][0]
    za=data1[1]+1j*data1[2]
    f=data1[0]
    z0=r0+1j*ws*l0

    ##cargo datos a corregir
    data2=read(file,sep)
    data2=mean(data2)
    zu=data2[1]+1j*data2[2]
    dzucorr=((1/(1/zu - 1/za + 1/z0))-z0)
    return([f,z0,dzucorr])


def dzcorr2(aire,file,sep):
    """ cargo datos del aire """
    data1=read2(aire,sep)
    data1=mean2(data1)
    #  return[fs,rezum,imzum,ws]
    ws=data1[3]
    l0=(data1[2]/ws)[0]
    r0=data1[1][0]
    za=data1[1]+1j*data1[2]
    f=data1[0]
    z0=r0+1j*ws*l0

    ##cargo datos a corregir
    data2=read2(file,sep)
    data2=mean2(data2)
    zu=data2[1]+1j*data2[2]
    dzucorr=((1/(1/zu - 1/za + 1/z0))-z0)
    return([f,z0,dzucorr])
        
def findnear(A,x):
    idx=numpy.argmin(numpy.abs(A - x))
    return(idx)

    


    

def meanz0(data,v):
    """ le saca la primera iteracion """
    data2=np.array(data)
    dataz3=data2[0][v]
    DATA=[]
    for n,x in enumerate(dataz3):
        ni=x[1][-1]
        nf=int(int(x[0][-1])/ni)
        X=np.reshape(x[4]/x[5],(ni,nf))
        Y=np.reshape(x[3],(ni,nf))
        Y=np.array(Y[1:,:])
        X=np.array(X[1:,:])
        xm=np.mean(np.mean(X,0))
        ym=np.mean(np.mean(Y,0))
        DATA.append(ym+1j*xm)
    return(np.array(DATA))

def datamean(data):
    dataz3=data[0]
    DATA=[]
    for n,x in enumerate(dataz3):
        ni=x[1][-1]
        nf=int(int(x[0][-1])/ni)
        X=np.reshape(x[4],(ni,nf))
        R=np.reshape(x[3],(ni,nf))
        f=np.reshape(x[2],(ni,nf))
        R=np.array(R[1:,:])
        X=np.array(X[1:,:])
        Xm=np.mean(X,0)
        Xsd=np.std(X,0)
        Rm=np.mean(R,0)
        Rsd=np.std(R,0)
        f=np.mean(f,0)
        DATA.append([f,Rm+1j*Xm,2*np.pi*f,Rsd+1j*Xsd])
        
    return(DATA)      


def fitz0(bob,parametro,val,data):
    par=['r1', 'r2', 'dh','N'].index(parametro)
    bob=np.array(bob)
    xv=np.linspace(val[0],val[1],100)
    z0v=list()
    for x in xv:
        bobf=np.append(bob[0:par],x)
        bobf=np.append(bobf,bob[par+1:])
        z0v.append((data-theo.l0(bobf,3000))**2)
    z0v = [item for sublist in z0v for item in sublist]
    data=[]
    trace0 = go.Scatter(
    x = xv,
    y = np.real(z0v),
    mode = 'markers')
    data.append(trace0)
    fig = go.Figure(data=data)
    plotly.offline.iplot(fig)
    bobf=np.append(bob[0:par],xv[np.argmin(z0v)])
    bobf=np.append(bobf,bob[par+1:])
    return([xv[np.argmin(z0v)],bobf,theo.l0(bobf,3000).real])    




################ nuevo


def dzcorrnorm(dataraw,Vzu,Z0):
    datams=datamean(dataraw)
    datams=[datams,dataraw[1]]
    data=np.array(datams[0])
    datas=datams[1]
    
    if Vzu=='all':
        #[0] primer archivo 0[0] f 0[1]z   0[2]w 
        za=data[0][1]
        dataplot=[]
        datacorr=[]
        for i,x in enumerate(data):
            f=x[0].real
            zu=x[1]
            w=x[2]
            x0=w*Z0.imag
            z0=Z0.real+1j*x0
            dzucorr=((1/(1/zu - 1/za + 1/z0))-z0  )
            trace0 = go.Scatter(
            x =f ,
            y = (np.imag(dzucorr)/x0).real,
            mode = 'lines',
            name=datas[i],
            legendgroup=datas[i])
            dataplot.append(trace0)
            trace1 = go.Scatter(
            x = f,
            y = (np.imag(zu-za)/x0).real,
            mode = 'markers', showlegend=False,
            legendgroup=datas[i])
            #dataplot.append(trace1)
            datacorr.append(dzucorr/x0)    
          
        layout = go.Layout(
        xaxis=dict(        type='log',zeroline=False , autorange=True   ),
        yaxis=dict(        type='linear',zeroline=False,autorange=True  ))
        fig = go.Figure(data=dataplot[1:], layout=layout)
        plotly.offline.iplot(fig)

    else:
        
        za=data[0][1]
        data=data[Vzu]
        dataplot=[]
        datacorr=[]
        for i,x in enumerate(data):
            f=x[0].real
            zu=x[1]
            w=x[2]
            x0=w*Z0.imag
            z0=Z0.real+1j*x0
            dzucorr=((1/(1/zu - 1/za + 1/z0))-z0  )
            trace0 = go.Scatter(
            x = f,
            y = (np.imag(dzucorr)/x0).real,
            mode = 'lines',
            name=datas[i+1],
            legendgroup=datas[i+1])
            dataplot.append(trace0)
            trace1 = go.Scatter(
            x = f,
            y = (np.imag(zu-za)/x0).real,
            mode = 'markers',
            showlegend=False,
            legendgroup=datas[i+1])
            dataplot.append(trace1)
            datacorr.append([f,Z0.imag,dzucorr/x0])

        layout = go.Layout(
                xaxis=dict(        type='log',zeroline=False , autorange=True   ),
                yaxis=dict(        type='linear',zeroline=False,autorange=True  ))
        fig = go.Figure(data=dataplot, layout=layout)
        plotly.offline.iplot(fig)
    
    return(fig,datacorr[1:])



def z0mean(data,v): 
    """ le saca la primera iteracion """
    data2=np.array(data)
    x=data2[0]
    ni=int(x[1][-1])
    nf=int(int(x[0][-1])/ni)
    X=np.reshape(x[4]/x[5],(ni,nf))
    Y=np.reshape(x[3],(ni,nf))
    Y=np.array(Y[1:,:])
    X=np.array(X[1:,:])
    xm=np.mean(np.mean(X[:,v[0]:v[1]],0))
    ym=np.mean(np.mean(Y[:,v[0]:v[1]],0))
    z0m=(ym+1j*xm)
    return(z0m)

def l0fit(bob,parametro,val,data):
    par=['r1', 'r2', 'dh','N'].index(parametro)
    bob=np.array(bob)
    xv=np.linspace(val[0],val[1],200)
    z0v=list()
    for x in xv:
        bobf=np.append(bob[0:par],x)
        bobf=np.append(bobf,bob[par+1:])
        z0v.append((data-theo.l0(bobf,3000))**2)
    
    data=[]
    trace0 = go.Scatter(
    x = xv,
    y = np.real(z0v),
    mode = 'markers')
    data.append(trace0)
    fig = go.Figure(data=data)
    plotly.offline.iplot(fig)
    bobf=np.append(bob[0:par],xv[np.argmin(z0v)])
    bobf=np.append(bobf,bob[par+1:])
    return([xv[np.argmin(z0v)],bobf,theo.l0(bobf,3000).real])    

def znorm(datams,Vzu):
    data=np.array(datams[0])
    datas=datams[1]
    
    if Vzu=='all':
        
        za=data[0][1]
        dataplot=[]
        datacorr=[]
        for i,x in enumerate(data):
            f=x[0].real
            zu=x[1]
            w=x[2]
            x0=w*Z0.imag
            z0=Z0.real+1j*x0
            dzucorr=((1/(1/zu - 1/za + 1/z0))-z0  )
            trace0 = go.Scatter(
            x =f ,
            y = (np.imag(dzucorr)/x0).real,
            mode = 'lines',
            name=datas[i],
            legendgroup=datas[i])
            dataplot.append(trace0)
            trace1 = go.Scatter(
            x = f,
            y = (np.imag(zu-za)/x0).real,
            mode = 'markers', showlegend=False,
            legendgroup=datas[i])
            dataplot.append(trace1)
            datacorr.append([f,Z0.imag,dzucorr/x0])    
          
        layout = go.Layout(
        xaxis=dict(        type='log',zeroline=False , autorange=True   ),
        yaxis=dict(        type='linear',zeroline=False,autorange=True  ))
        fig = go.Figure(data=dataplot[2:], layout=layout)
        plotly.offline.iplot(fig)

    else:
        
        za=data[0][1]
        data=data[Vzu]
        dataplot=[]
        datacorr=[]
        for i,x in enumerate(data):
            f=x[0].real
            zu=x[1]
            w=x[2]
            x0=w*Z0.imag
            z0=Z0.real+1j*x0
            dzucorr=((1/(1/zu - 1/za + 1/z0))-z0  )
            trace0 = go.Scatter(
            x = f,
            y = (np.imag(dzucorr)/x0).real,
            mode = 'lines',
            name=datas[i+1],
            legendgroup=datas[i+1])
            dataplot.append(trace0)
            trace1 = go.Scatter(
            x = f,
            y = (np.imag(zu-za)/x0).real,
            mode = 'markers',
            showlegend=False,
            legendgroup=datas[i+1])
            dataplot.append(trace1)
            datacorr.append([f,Z0.imag,dzucorr/x0])

        layout = go.Layout(
                xaxis=dict(        type='log',zeroline=False , autorange=True   ),
                yaxis=dict(        type='linear',zeroline=False,autorange=True  ))
        fig = go.Figure(data=dataplot, layout=layout)
        plotly.offline.iplot(fig)
    
    return(fig,datacorr[1:])

def iamp(data,vrms):
    """ calculo """
    z=np.abs(data[3]+1j*data[4])
    v=vrms*np.sqrt(2)
    iamp=v/z
    return(iamp*1000)





#### nuevo








### nuevo 2




def read(file, separador):

    z=list()
    with open(file, 'r') as csvfile:
        spam = csv.reader(csvfile, delimiter=separador)

        next(spam)
        next(spam)
        next(spam)
        next(spam)

        for row in spam:
            z.append(row)

    f=list()
    rez=list()
    imz=list()
    n=list()
    i=list()

    for x in range(len(z)):
        f.append(float(z[x][4]))
        rez.append(float(z[x][12]))
        imz.append(float(z[x][13]))
        n.append(int(z[x][0]))
        i.append(int(z[x][1]))

    f = numpy.asarray(f)
    w=2*numpy.pi*f
    rez=numpy.asarray(rez)
    imz=numpy.asarray(imz)
    n=numpy.asarray(n)
    i=numpy.asarray(i)
    out=list([n,i,f, rez,imz, w])
    out=numpy.array(out)
    return(out)

def load(path):
    """ carga archivos en la carpeta actual, todos deben pertenecer a un mismo experimento, mismas frecuencias y misma cantidad de repeticiones, se le puede asginar la direccion en disco de la carpeta a la variable path (tener cuidado con los //), si path=0 abre una ventana de windows para elegirla manualmente
    --------------------------------------------------------------------------------------
    devuelve una lista: 
        data[0] lista de los datos de cada archivo, cada indice es una matriz con los datos crudos de cada archivo
        
        data[1] lista con los nombres de los archivos        
    """    
    
    folder_path = path
    files=list()
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        filenames.sort()
        for i,j in enumerate(filenames):
            files.extend([dirpath + '/'+j])
        break

    files=[files,filenames]
    data=list()
    for file in files[0]:
        if 'info' not in file:
            data.append(read(file,';')) 
     
    return data  




def pack(path,bobina,sigmas,espesores):
    dataraw=load(path)
    f=getf(dataraw)
    dcorr=corr(f,bobina,dataraw)
    exp=[]
    for i,x in enumerate(dcorr[0]):

        muestra={
            'bo' : bobina,
            'f' : f,
            'dzcorrnorm' : x,
            'sigma' : sigmas[i],
            'espesor' : espesores[i],
            'name' : dcorr[1][i]
        }

        exp.append(muestra)
    return exp

def getf(data):
    """ obtiene el vector de frecuencias de los datos"""
    return(data[0][2][:int(data[0][0][-1]/data[0][1][-1])])
	



def corr(f,bo,dataraw,Vzu='all'):
    """ corrige y normaliza los datos, toma como input el vector de frecuencias, la info de la bobina y los datos
        devuelve una lista de arrays, cada array es la impedancia compleja corregida y normalizada para cada frecuencia, parte real y parte imaginaria
        para recuperar la parte real  (.real) e imaginaria (.imag)
    """
    datams=stats(dataraw)
    w=np.pi*2*f
    Z0=bo[-2]
    x0=w*Z0.imag              
   
    x0=f*2*np.pi*bo[-1]
    z0=np.real(bo[-2])+1j*x0
    if Vzu=='all':
        #[0] primer archivo 0[0] f 0[1]z   0[2]w 
        za=datams[0][0]
        dataplot=[]
        datacorr=[]
        data=datams[1:]
        for i,x in enumerate(data):
            zu=x[0]
            dzucorr=((1/(1/zu - 1/za + 1/z0))-z0  )				
            datacorr.append(dzucorr/x0)    
    else:
        za=data[0][0]
        data=data[Vzu]
        dataplot=[]
        datacorr=[]
        for i,x in enumerate(data):
            zu=x[1]
            dzucorr=((1/(1/zu - 1/za + 1/z0))-z0  )
            datacorr.append(dzucorr/x0)                
    ret=list(np.array(datacorr))
    return(ret)

def stats(data):
    dataz3=data[0]
    DATA=[]
    for n,x in enumerate(dataz3):
        ni=int(x[1][-1])
        nf=int(int(x[0][-1])/ni)
        X=np.reshape(x[4],(ni,nf))
        R=np.reshape(x[3],(ni,nf))
        
        R=np.array(R[1:,:])
        X=np.array(X[1:,:])
        Xm=np.mean(X,0)
        Xsd=np.std(X,0)
        Rm=np.mean(R,0)
        Rsd=np.std(R,0)
        
        DATA.append([Rm+1j*Xm,Rsd+1j*Xsd])
        
    return(DATA)      