import iamend_ci.bo as bo
import iamend_ci.theo as theo
import iamend_ci.fit as fit
import iamend_ci.so as so
import iamend_ci.plt as plt
import iamend_ci.ax as ax
import iamend_ci.pxplt as px
import os
import pandas as pd
import numpy as np
import plotly.express as px
#esto sirve para no tener daramas con el path en windows/unix
from pathlib import Path


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
                self.bobina=bo.data_dicts[info.bobina[0]]     
                self.coil=bo.data[info.bobina[0]]   
            else:
                print('Mas de una bobina, separe las mediciones en carpetas para cada bobina.')
            
            # Cargo todos los cvs como lista de DFci

            try:
                self.data=so.load(self.path,bobina=self.bobina)
            except:
                self.data=so.load(self.path,bobina=self.bobina,separador=',')

            print(self.info)  

            self.f=so.getf(self)

            self.w=2*np.pi*self.f

            # Genero como atributos los dataframes
            for i,df_ci in enumerate(self.data):

                setattr(self,'df'+ str(i),df_ci)

        except Exception as e:
            print(e)





    def normcorr(self):
        '''
        Metodo que corrije las mediciones utilizando el benchmark harrison(xxxx)
        '''
        index_file_aire=self.files.index[self.files.str.lower().str.contains('aire')].values[0]

        # exp data dzcorrnorm
        self.dzcorrnorm=so.corrnorm(self,index_file_aire) 
        print('Normalizando y corrigiendo con los datos: ',self.files[index_file_aire])

        # self.dzcorrnorm=so.corr(self.f,self.coil,[self.data],Vzu='all') 
        # df dzcorrnorm

        # muestras=[x.split('_')[-1].split('.')[0] for x in self.files.values if ('Aire' not in x) ]
        # idzcorr=pd.DataFrame(np.array(self.dzcorrnorm).imag.T, columns=muestras)
        # idzcorr['f']=self.f
        # redzcorr=pd.DataFrame(np.array(self.dzcorrnorm).real.T, columns=muestras)
        # redzcorr['f']=self.f
        # self.imdz=idzcorr
        # self.redz=redzcorr  




    def implots(self):
        if hasattr(self,'imdz'):
            dfm = self.imdz.melt('f', var_name='muestra', value_name='imdzcorrnorm')
            return px.line(dfm, x='f',y='imdzcorrnorm',color='muestra',log_x=True)
        else:
            print('Es necesario corregir y normalizar los datos. Utilice el metodo .normcorr()')
    def replots(self):
        if hasattr(self,'redz'):
            dfm = self.redz.melt('f', var_name='muestra', value_name='redzcorrnorm')
            return px.line(dfm, x='f',y='redzcorrnorm',color='muestra',log_x=True)
        else:
            print('Es necesario corregir y normalizar los datos. Utilice el metodo .normcorr()')

    def im(self,n):
        plt.im(self.dzcorrnorm[n+1],self.f,self.files[n+1])

    def re(self,n):
        plt.re(self.dzcorrnorm[n+1],self.f,self.files[n+1])


    def fitpatron(self):
        try:
            pathpatron=[x for x in self.files if 'patron' in x][0]
            self.path_patron=pathpatron
            # -1 por q el aire no esta en dzcorrnorm
            index=self.files[self.files == pathpatron].index[0]
            z1eff,figz1fit=fit.z1(self.f,self.coil,self.dzcorrnorm[index-1],self.espesores[index],self.sigmas[index],self.files[index])
            self.z1eff=z1eff[0]
            self.coil[4]=self.z1eff

        except:
            print('Corrija y normalice los datos usando .normcorr()')               
        return 

    def fitmues(self):
        mues=[]
        muesfigs=[]
        try:
            for i,x in enumerate(self.dzcorrnorm):
                index=i+1
                fpar,fig=fit.mu(self.f,self.coil,x,self.espesores[index],self.sigmas[index],self.files[index])
                mues.append(fpar[0])
                muesfigs.append(fig)
            mues.insert(0,0)    
            self.mues=mues
            self.muesfigs=muesfigs
            self.info['mu_eff']=self.mues
        except:
            print('Corrija y normalice los datos usando .normcorr()')
        return



    def fitfmues(self,n=-1,fn=4):
        if n==-1 :
            pass
        else:
            self.fmues=fit.fmu(self.f,self.coil,fn,self.dzcorrnorm[n],self.sigmas[n+1],self.files[n+1])






    # imprime la string para la instancia
    def __str__(self):
        return f'Experimento ({self.path})'
    def __repr__(self):
        return f'Experimento ({self.path})'

