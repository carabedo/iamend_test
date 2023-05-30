import pandas as pd
import csv
import plotly.express as px
import numpy as np
#esto sirve para no tener daramas con el path en windows/unix
from pathlib import Path #falta implementar
import traceback

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
        self['idznorm']=self['imag']/(2*np.pi*self['f']*self.l0)
        self['repeticion']=self['repeticion'].astype(str)
        return px.scatter(self, x='f',y='idznorm',color='repeticion',log_x=True)
    def repx(self):
        self['repeticion']=self['repeticion'].astype(str)
        return px.scatter(self, x='f',y='real',color='repeticion',log_x=True)
    
def load(exp,separador=';'):
    folder_path=exp.path
    filepaths=exp.info.archivo.values

    #hay que remplazar por diccionario se mezclan los datos.
    data=list()
    for k,filepath in enumerate(filepaths):
        if ('info' not in filepath) & ('csv' in filepath):
            df=read(folder_path+'/'+filepath,separador)
            dfci=DataFrameCI(filename=filepath,bobina=exp.bobina,data=df)
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





def corrnorm_dict(exp,test=True,dropfirst=True):
    """ corrige y normaliza los datos, toma como input el vector de frecuencias, la info de la bobina y los datos
        devuelve una lista de arrays, cada array es la impedancia compleja corregida y normalizada para cada frecuencia, parte real y parte imaginaria
        para recuperar la parte real  (.real) e imaginaria (.imag)
        
        z=re+i*2pi*f*l0
    """ 
    data_mean,data_std,data_test=stats_dict(exp,test=test,dropfirst=dropfirst)

    w=np.pi*2*exp.f
    
    z0=exp.bobina['R0']+1j*w*exp.bobina['L0']
    x0=w*exp.bobina['L0']  
    try:
        # correccion muestras
        filename_aire=exp.info.archivo[exp.info.archivo.str.contains('aire',case=False)].values[0]
        za=data_mean[filename_aire]
        datacorrnorm={}
        datacorrnorm_test={}
        filename_muestras=[x for x in data_mean.keys() if not filename_aire in x]
        for m,filename_muestra in enumerate(filename_muestras):
            z_mean=data_mean[filename_muestra]
            zu=z_mean
            dzucorr=((1/(1/zu - 1/za+ 1/z0))-z0  )				
            datacorrnorm[filename_muestra]=dzucorr/x0
            # correcion test
            if test==True:
                zu_test=data_test[filename_muestra].real+1j*data_test[filename_muestra].imag
                dzucorr=((1/(1/zu_test - 1/za+ 1/z0))-z0  )	
                datacorrnorm_test[filename_muestra]=dzucorr.values/x0
            # con el .values le saco los indices		

        medicion_aire={'filename_aire': filename_aire, 'za': za}
        if test==True:
            return datacorrnorm,data_test,datacorrnorm_test,medicion_aire
        else:
            return datacorrnorm,medicion_aire
    except Exception as e:
        print(e)




def stats_dict(exp,test=True,dropfirst=True):
    ''' excluyendo la primer repeticion para cada muestra devuelve lista de valores medios por f y sus desvios'''
    data_mean={}
    data_std={}
    data_test={}

    for m,datamuestra_m in enumerate(exp.data):
        filename=datamuestra_m.filename

        #excluimos la primer repeticion
        if dropfirst==True:
            df=datamuestra_m[datamuestra_m.repeticion != 1 ]
        else:
            df=datamuestra_m
        
        #separamos de manera aleatoria un valor de impedancia para cada frecuencia
        if test==True:
            df_test=df.groupby('f').sample(1)
            #boramos del dataset original esos valores
            df.loc[df_test.index,'imag']=np.nan
            data_test[filename]=df_test

        #calculamos mean y std 
        
        real_mean=df.groupby('f')['real'].mean().values
        imag_mean=df.groupby('f')['imag'].mean().values
        real_std=df.groupby('f')['real'].std().values
        imag_std=df.groupby('f')['imag'].std().values

        data_mean[filename]=real_mean+1j*imag_mean
        data_std[filename]=real_std+1j*imag_std

    return data_mean,data_std,data_test



def corrnorm(exp,filename_muestra,repeticion):
    w=np.pi*2*exp.f
    z0=exp.bobina['R0']+1j*w*exp.bobina['L0']
    x0=exp.x0
    za=exp.za['za']
    indice_muestra=exp.info[exp.info.archivo == filename_muestra].index.values[0]
    df_muestra=exp.data[indice_muestra]
    df_repeticion=df_muestra[df_muestra.repeticion == repeticion]
    zu_serie=df_repeticion.real + 1j*df_repeticion.imag
    zu=zu_serie.values
    dzucorr=((1/(1/zu - 1/za+ 1/z0))-z0  )
    dzucorrnorm=dzucorr/x0
    return dzucorrnorm

