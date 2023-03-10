import os
import pandas as pd
import csv
import plotly.express as px
import numpy as np

def read(file, separador):
    # lee archivo csv del solatron
    # se puede definir el separador
    z=list()
    with open(file, 'r') as csvfile:
        spam = csv.reader(csvfile, delimiter=separador)
        #lineas del header
        next(spam)
        next(spam)
        next(spam)
        next(spam)

        for row in spam:
            z.append(row)
    df=pd.DataFrame(z)
    df=df.iloc[:,[0,1,4,12,13]]
    df.columns=['indice','repeticion','f','real','imag']
    df=df.astype(float)
    df.indice=df.indice.astype('int')
    df.repeticion=df.repeticion.astype('int')
    return df


class DataFrameCI(pd.DataFrame):
    # construyo esta clase para extender la funcionalidad 
    # del dataframe de pandas, le agrego la posibilidad
    # de graficar las 11 mediciones que se realizan sobre 
    # cada muestra
    def __init__(self,filename,bobina,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # solo me deja agregar atributos que no sean listas.
        self.filename=filename
        self.l0=bobina['L0']
    def impx(self):
        self['idznorm']=self['Impedance Imaginary (Ohms)']/(self['2*pi*f']*self.l0)
        self['Sweep Number']=self['Sweep Number'].astype(float).astype(int)
        return px.line(self, x='Frequency (Hz)',y='idznorm',color='Sweep Number',log_x=True)

def load(path,bobina,separador=';'):
    """ carga archivos en la carpeta actual, todos deben pertenecer a un mismo experimento, mismas frecuencias y misma cantidad de repeticiones, se le puede asginar la direccion en disco de la carpeta a la variable path (tener cuidado con los //), si path=0 abre una ventana de windows para elegirla manualmente
    --------------------------------------------------------------------------------------
    devuelve una lista: 
        data: lista de los df de cada archivo, cada indice es una matriz con los datos crudos de cada archivo
        
        
    """    
    
    folder_path = path
    filepaths=[]
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        filenames.sort()
        for i,j in enumerate(filenames):
            filepaths.extend([dirpath + '/'+j])
        break
    data=list()
    for k,filepath in enumerate(filepaths):
        if ('info' not in filepath) & ('csv' in filepath):
            df=read(filepath,separador)
            dfci=DataFrameCI(filename=filenames[k],bobina=bobina,data=df)
            data.append(dfci) 
    return data  


def getf(exp):
    '''encuentra y chequea que todos los archivos del experimento tengan los mismos
    valores de frecuencia'''

    if len(set([x.repeticion.max() for x in exp.data])) > 1:
        print('Inconsistencia en los archivos en la cantidad de repeticiones')
        
    
    lista_fs=[x[x['repeticion']==1]['f'] for x in exp.data ]
    
    if (np.array(lista_fs)-np.array(lista_fs[0])).sum().sum()==0:
        return np.sort(np.array(list(set(lista_fs[0]))))
    else:
        print('Inconsistencia en los archivos para el rango de frecuencias.')



def corrnorm(exp,index_file_aire):
    """ corrige y normaliza los datos, toma como input el vector de frecuencias, la info de la bobina y los datos
        devuelve una lista de arrays, cada array es la impedancia compleja corregida y normalizada para cada frecuencia, parte real y parte imaginaria
        para recuperar la parte real  (.real) e imaginaria (.imag)
        
        z=re+i*2pi*f*l0
    """ 
    lista_z_mean,data_std=stats(exp)
    w=np.pi*2*exp.f
    
    z0=exp.bobina['R0']+1j*w*exp.bobina['L0']
    x0=w*exp.bobina['L0']  

    za=lista_z_mean[index_file_aire]
    datacorrnorm={}
    for m,z_mean in enumerate(lista_z_mean):
        if m != index_file_aire:
            zu=z_mean
            dzucorr=((1/(1/zu - 1/za+ 1/z0))-z0  )				
            datacorrnorm[str(m)]=dzucorr/x0
    return datacorrnorm

def split_train_test(exp):
    pass


def stats(exp):
    ''' excluyendo la primer repeticion para cada muestra devuelve lista de valores medios por f y sus desvios'''
    data_mean=[]
    data_std=[]

    for m,datamuestra_m in enumerate(exp.data):
        #excluimos la primer repeticion

        real_mean=datamuestra_m[datamuestra_m.repeticion != 0 ].groupby('f')['real'].mean().values
        imag_mean=datamuestra_m[datamuestra_m.repeticion != 0 ].groupby('f')['imag'].mean().values
        real_std=datamuestra_m[datamuestra_m.repeticion != 0 ].groupby('f')['real'].std().values
        imag_std=datamuestra_m[datamuestra_m.repeticion != 0 ].groupby('f')['imag'].std().values

        data_mean.append(real_mean+1j*imag_mean)
        data_std.append(real_std+1j*imag_std)

    return data_mean,data_std


###### LEGACY

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