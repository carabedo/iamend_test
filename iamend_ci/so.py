""" Modulo para el procesamiento de los archivos CVS del solartron"""
import os
import csv
import numpy as np


### nuevo v2

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

    f = np.asarray(f)
    w=2*np.pi*f
    rez=np.asarray(rez)
    imz=np.asarray(imz)
    n=np.asarray(n)
    i=np.asarray(i)
    out=list([n,i,f, rez,imz, w])
    out=np.array(out)
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
        datacorr=[]
        data=datams[1:]
        for i,x in enumerate(data):
            zu=x[0]
            dzucorr=((1/(1/zu - 1/za + 1/z0))-z0  )				
            datacorr.append(dzucorr/x0)    
    else:
        za=data[0][0]
        data=data[Vzu]
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


     