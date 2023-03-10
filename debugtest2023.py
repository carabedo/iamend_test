import iamend_ci as ci
import numpy as np
import pandas as pd
import os
import csv 

## legacy
from pathlib import Path

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

def load(path,separador=';'):
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
        if ('info' not in file) & ('csv' in file):
            data.append(read(file,separador)) 
    return data  

class exp():
    def __init__(self,path):
        self.path=path
        try:
            infopath=[x for x in os.listdir(path) if 'info' in x][0]
            data_folder = Path(path)
            infofullpath=data_folder / infopath
            info=pd.read_csv(str(infofullpath)) 
            self.info=info
            self.files=info.iloc[:,0]
            self.sigmas=info.iloc[:,1]
            self.espesores=info.iloc[:,2]

            if len(info.bobina.unique()) == 1:             
                self.bobina=ci.bo.data_dicts[info.bobina[0]]     
                self.coil=ci.bo.data[info.bobina[0]]   
            else:
                print('Mas de una bobina, separe las mediciones en carpetas para cada bobina.')
            
            try:
                self.data=load(self.path)
            except:
                self.data=load(self.path,separador=',')

            print(self.info)  
            self.f=exp1.f
            self.w=2*np.pi*self.f
            # Genero como atributos los dataframes
            for i,file_data in enumerate(self.data):
                columns_names=["Index", "Sweep Number","Frequency (Hz)" , 
                "Impedance Real (Ohms)","Impedance Imaginary (Ohms)","2*pi*f"]
                df=pd.DataFrame(file_data.T, columns=columns_names)
                # usando setattr genero de manera dinamica los nombres 
                # de los atributos
                setattr(self,'df'+ str(i),df)
        except Exception as e:
            print(e)


    def normcorr(self):
        self.dzcorrnorm=corr0(self.f,self.coil,[self.data]) 
        # muestras=[x.split('_')[-1][:3] for x in self.files.values if (('Aire' not in x) & ('Pat' not in x)) ]
        muestras=[x.split('_')[-1].split('.')[0] for x in self.files.values if ('Aire' not in x) ]
        idzcorr=pd.DataFrame(np.array(self.dzcorrnorm).imag.T, columns=muestras)
        idzcorr['f']=self.f
        redzcorr=pd.DataFrame(np.array(self.dzcorrnorm).real.T, columns=muestras)
        redzcorr['f']=self.f
        self.imdz=idzcorr
        self.redz=redzcorr  


def corr0(f,bo,dataraw):
    """ corrige y normaliza los datos, toma como input el vector de frecuencias, la info de la bobina y los datos
        devuelve una lista de arrays, cada array es la impedancia compleja corregida y normalizada para cada frecuencia, parte real y parte imaginaria
        para recuperar la parte real  (.real) e imaginaria (.imag)
    """
    datams=stats0(dataraw)
    w=np.pi*2*f
    Z0=bo[-2]
    x0=w*Z0.imag              
   
    x0=f*2*np.pi*bo[-1]
    z0=np.real(bo[-2])+1j*x0
    
    #[0] primer archivo 0[0] f 0[1]z   0[2]w 
    za=datams[0][0]
    datacorr=[]
    data=datams[1:]
    for i,x in enumerate(data):
        zu=x[0]
        dzucorr=((1/(1/zu - 1/za + 1/z0))-z0  )				
        datacorr.append(dzucorr/x0)          
    ret=list(np.array(datacorr))
    return(ret)

def stats0(data):
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




### NEW

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

    za_mean_aire=lista_z_mean[index_file_aire]
    datacorr=[]
    for m,z_mean in enumerate(lista_z_mean):
        if m != index_file_aire:
            print(m)
            zu=z_mean
            dzucorr=((1/(1/zu - 1/za_mean_aire + 1/z0))-z0  )				
            datacorr.append(dzucorr/x0)    
    return datacorr



def stats(exp):
    ''' excluyendo la primer repeticion para cada muestra devuelve lista de valores medios por f y sus desvios'''
    data_mean=[]
    data_std=[]
    for m,datamuestra in enumerate(exp.data):
        #excluimos la primer repeticion
        real_mean=exp.data[0][exp.data[0].repeticion != 0 ].groupby('f')['real'].mean().values
        imag_mean=exp.data[0][exp.data[0].repeticion != 0 ].groupby('f')['imag'].mean().values
        real_std=exp.data[0][exp.data[0].repeticion != 0 ].groupby('f')['real'].std().values
        imag_std=exp.data[0][exp.data[0].repeticion != 0 ].groupby('f')['imag'].std().values
        data_mean.append(real_mean+1j*imag_mean)
        data_std.append(real_std+1j*imag_std)
    return data_mean,data_std

exp1=ci.exp('../iamend_ci/datos/m1_316')


exp0=exp('../iamend_ci/datos/m1_316')
exp0.normcorr()

exp1.normcorr()


print(exp1.dzcorrnorm[0].mean().round(3))
print(exp0.dzcorrnorm[0].mean().round(3))

