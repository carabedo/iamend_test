import iamend_ci.bo as bo
import iamend_ci.theo as theo
import iamend_ci.fit as fit
import iamend_ci.so as so
import iamend_ci.plt as plt
import iamend_ci.ax as ax
import iamend_ci.pxplt as px
import iamend_ci.plotbokeh as pb
import os
import pandas as pd
import numpy as np
import plotly.express as px
#esto sirve para no tener daramas con el path en windows/unix
from pathlib import Path
from sklearn.metrics import r2_score as R2
import logging

# definicion de la clase 'exp'

class exp():
    ''' Clase Experimentos:
    Se instancian con el nombre de la carpeta donde estan los archivos del solatron. Un carpeta para cada bobina, todo el experimento necesita una medicion en aire. Medicion en un patron para el ajuste efectivo del lift-off.
    '''
    def __init__(self,path,normcorr=True,test=True,dropfirst=True):
        self.path=path
        try:
            infopath=[x for x in os.listdir(path) if 'info' in x][0]
            data_folder = Path(path)
            infofullpath=data_folder / infopath
            info=pd.read_csv(str(infofullpath)) 

            self.info=info
            self.files=info.iloc[:,0]

            # self.info['muestras']=self.info.archivo.apply(lambda x: get_id(x))
            # #lo haria URL
            # muestras=pd.read_csv('./iamend_ci/muestras.csv')
            # self.info.conductividad=self.info.muestras.apply(lambda x: get_sigma(x,muestras))
            # self.info.espesor=self.info.muestras.apply(lambda x: get_esp(x,muestras))

            if len(info.bobina.unique()) == 1: 
                try:            
                    self.bobina=bo.data_dicts[info.bobina[0]]     
                except:
                    print('No se encontraron datos de la bobina: ', info.bobina[0])
                self.coil=bo.data[info.bobina[0]]   
            else:
                print('Mas de una bobina, separe las mediciones en carpetas para cada bobina.')
            
            # Cargo todos los cvs como diccionario de DFci

            try:
                self.data=so.load(self)
            except:
                self.data=so.load(self,separador=',')


            print(self.info)  

            self.f=so.getf(self)

            self.w=2*np.pi*self.f

            # Genero como atributos los dataframes
            for i,df_ci in enumerate(self.data):
                setattr(self,'df'+ str(i),df_ci)

            if normcorr==True:
                self.normcorr_dict(test=test,dropfirst=dropfirst)

        except Exception as e:
            print('No se pudieron cargar los archivos. Error: ', e)



    def normcorr_dict(self,test=True,dropfirst=True):
        '''
        Metodo que corrije las mediciones utilizando el benchmark harrison(xxxx)
        '''
        try:
            # diccionario con las variaciones de impedancias
            # corregidas y normalizadas (re + 1j imag)
            if test==True:
                dict_dzcorrnorm,data_test,dict_dzcorrnorm_test,medicion_aire=so.corrnorm_dict(self,test=test,dropfirst=dropfirst)
                # guardamos test y medicion en aire
                self.data_test=data_test
                self.dznorm_test_dict=dict_dzcorrnorm_test
                self.za=medicion_aire

                #
                df=pd.DataFrame(dict_dzcorrnorm)
                df_test=pd.DataFrame(dict_dzcorrnorm_test)
                df['f']=self.f
                df_test['f']=self.f
                dfdz=pd.melt(df,id_vars=df.columns[-1], var_name='muestra',value_name='dzcorrnorm')
                dfdz['imag']=np.imag(dfdz['dzcorrnorm'])
                dfdz['real']=np.real(dfdz['dzcorrnorm'])
                self.dznorm=dfdz
                dfdz_test=pd.melt(df_test,id_vars=df.columns[-1], var_name='muestra',value_name='dzcorrnorm')
                dfdz_test['imag']=np.imag(dfdz_test['dzcorrnorm'])
                dfdz_test['real']=np.real(dfdz_test['dzcorrnorm'])
                self.dznorm=dfdz
                self.dznorm_test=dfdz_test
                self.test=True
            else:
                dict_dzcorrnorm,medicion_aire=so.corrnorm_dict(self,test=test,dropfirst=dropfirst)
                # guardamos medicion en aire        
                self.za=medicion_aire
                df=pd.DataFrame(dict_dzcorrnorm)
                df['f']=self.f
                dfdz=pd.melt(df,id_vars=df.columns[-1], var_name='muestra',value_name='dzcorrnorm')
                dfdz['imag']=np.imag(dfdz['dzcorrnorm'])
                dfdz['real']=np.real(dfdz['dzcorrnorm'])
                self.dznorm=dfdz
                self.dznorm=dfdz
                self.test=False


        except Exception as e:
            print(e)

    def set_frange(self,f_inicial,f_final):
        # redifinimos f
        f_serie=pd.Series(self.f)
        f_new_mask=f_serie.between(f_inicial,f_final)
        self.f=f_serie[f_new_mask].values
        # ajustamos parametros geometricos effectivos en el rango
        ## filtramos de dznorm las frecuencias nuevas
        self.dznorm=self.dznorm[self.dznorm.f.between(f_inicial,f_final)]
        self.dznorm_test=self.dznorm_test[self.dznorm_test.f.between(f_inicial,f_final)]
        #self.fitpatron()
        # 



    # Ajustes
    def fitpatron(self,patron_filename='auto',param_geo='z1',plot=False, rango = None):

        if patron_filename=='auto':
            indice_patron=self.info[self.info.muestras.str.startswith('P')].iloc[0].name
            dzcorrnorm=self.dznorm[self.dznorm.muestra == self.info.iloc[indice_patron].archivo].dzcorrnorm.values
            esp=self.info.espesor.iloc[indice_patron]
            sigma=self.info.conductividad.iloc[indice_patron]
        else:
            indice_patron=self.info[self.info.archivo == patron_filename].iloc[0].name
            dzcorrnorm=self.dznorm[self.dznorm.muestra == patron_filename].dzcorrnorm.values
            esp=self.info.espesor.iloc[indice_patron]
            sigma=self.info.conductividad.iloc[indice_patron]


        try:
            if param_geo == 'z1':
             
                z1eff,uz1eff=fit.z1(self.f,self.coil,dzcorrnorm,esp,sigma,self.files[indice_patron])

                self.z1eff=z1eff[0]
                self.uz1eff=uz1eff
                self.coil[4]=self.z1eff
                self.patron_fitgeo={'filename':patron_filename,'param_geo': param_geo}

            elif param_geo == 'N':

                Neff=fit.N(self.f,self.coil,dzcorrnorm,esp,sigma,rango=rango)
                self.Neff=Neff[0]
                self.coil[3]=self.Neff

            elif param_geo == 'r2':
                r2eff=fit.r2(self.f,self.coil,dzcorrnorm,esp,sigma,rango=rango)
                self.r2eff=r2eff[0]
                self.coil[1]=self.r2eff

            if plot == True:
                pb.plot_fit_patron(self,param_geo,patron_filename)

            return True
        
        except Exception as e:
            print(e)   
            logging.exception("An exception was thrown!")                   
            return False

    def fitmues(self,figs=True):

        if not hasattr(self,'z1eff'):
            print('Ajustando z1 effectivo')
            if self.fitpatron():
                muestras=self.dznorm[self.dznorm.muestra.str.contains('M')].muestra.unique()
                self.info['mueff']=np.nan
                self.info['R2']=np.nan

                yteos={}
                for x in muestras:
                    row=self.info[self.info.muestras.str.contains(x)]
                    esp=row.espesor.values[0]
                    sigma=row.conductividad.values[0]
                    dzucorrnorm=self.dznorm[self.dznorm.muestra == x].dzcorrnorm.values

                    #mu(f,bo_eff,dzucorrnorm,dpatron,sigma, name):
                    fpar,fcov=fit.mu(self.f,self.coil,dzucorrnorm,esp,sigma,row.archivo.values[0])
                    self.info.loc[row.index.values[0],'mueff']=fpar
                    x0=2*np.pi*self.f*self.coil[-1]
                    yteo=theo.dzD(self.f,self.coil,sigma,esp,fpar,1500)/x0
                    yteos[x]=yteo

                    # validacion con test de la parte imaginaria
                    dzucorrnorm_test=self.dznorm_test[self.dznorm_test.muestra == x].dzcorrnorm.values
                    r2=R2(yteo.imag,dzucorrnorm_test.imag)
                    self.info.loc[row.index.values[0],'R2']=r2
                self.ypreds=yteos
        else:
            mylist = [self.za['filename_aire'], self.patron_fitgeo['filename']]
            pattern = '|'.join(mylist)
            muestras=self.info.archivo[~self.info.archivo.str.contains(pattern)]
            yteos={}
            for i in muestras.index:
                row=self.info.iloc[i]
                esp=row.espesor
                sigma=row.conductividad
                dzucorrnorm=self.dznorm[self.dznorm.muestra == row.archivo].dzcorrnorm.values
                #mu(f,bo_eff,dzucorrnorm,dpatron,sigma, name):
                fpar,fcov=fit.mu(self.f,self.coil,dzucorrnorm,esp,sigma,row.archivo)
                self.info.loc[i,'mueff']=fpar
                self.info.loc[i,'umueff']=fcov
                x0=2*np.pi*self.f*self.coil[-1]
                yteo=theo.dzD(self.f,self.coil,sigma,esp,fpar,1500)/x0
                yteos[row.archivo]=yteo
                if self.test==True:
                    # validacion con test de la parte imaginaria
                    dzucorrnorm_test=self.dznorm_test[self.dznorm_test.muestra == x].dzcorrnorm.values
                    r2=R2(yteo.imag,dzucorrnorm_test.imag)
                    self.info.loc[i,'R2']=r2
            self.ypreds=yteos

    def fitfmues(self,*args,**kwargs):

        if len(args) == 0:
            pass
        elif len(args)==1:
            print('fiteo en N tramos')
            n_splits_f=args[0]
            muestras=self.dznorm[self.dznorm.muestra.str.contains('M')].muestra.unique()
            coil_eff=self.coil
            fmu_fits={}
            for i,x in enumerate(muestras):
                name=x
                row=self.info[self.info.muestras.str.contains(x)]
                espesor=row.espesor.values[0]
                sigma=row.conductividad.values[0]
                dzucorrnorm=self.dznorm[self.dznorm.muestra == x].dzcorrnorm.values
                fmu_fit=fit.fmu(self.f,coil_eff,n_splits_f,dzucorrnorm,sigma,espesor,name)             
                for fn in range(n_splits_f):
                    fo=int(fmu_fit['fs'][fn][0]/1000)
                    ff=int(fmu_fit['fs'][fn][-1]/1000)
                    self.info.loc[self.info.muestras==x,'mu '+str(fo)+'k-'+str(ff)+'k']=fmu_fit['mues'][fn]   
                fmu_fits[x]=fmu_fit             
            self.fmues=fmu_fits

        elif len(args)==3:
            str_muestra=args[0]
            f0=args[1]
            ff=args[2]

            muestra=self.dznorm[self.dznorm.muestra.str.contains(str_muestra)].muestra.unique()
            coil_eff=self.coil
            fmu_fits={}
            name=muestra
            row=self.info[self.info.muestras.str.contains(x)]
            espesor=row.espesor.values[0]
            sigma=row.conductividad.values[0]
            dzucorrnorm=self.dznorm[self.dznorm.muestra == x].dzcorrnorm.values
            fmu_fit=fit.fmu(self.f,coil_eff,n_splits_f,dzucorrnorm,sigma,espesor,name)             
            for fn in range(n_splits_f):
                fo=int(fmu_fit['fs'][fn][0]/1000)
                ff=int(fmu_fit['fs'][fn][-1]/1000)
                self.info.loc[self.info.muestras==x,'mu '+str(fo)+'k-'+str(ff)+'k']=fmu_fit['mues'][fn]   
            fmu_fits[x]=fmu_fit             
            self.fmues=fmu_fits

            print('fiteo desde A a B')    

    # ploteos

    def implots(self):
        px.line(self.dznorm,x='f',y='imag',color='muestra',log_x=True)

    def replots(self):
        px.line(self.dznorm,x='f',y='real',color='muestra',log_x=True)


    def im(self,n):
        plt.im(self.dznorm[n+1],self.f,self.files[n+1])

    def re(self,n):
        plt.re(self.dznorm[n+1],self.f,self.files[n+1])


    def muesplot(self):
        pb.plot_fit_mues(self)
        
    def muplot(self,indice_muestra):
        fig=pb.plot_fit_mu(self,indice_muestra)
        return fig

        
    def fmuplot(self,muestra):
        pb.plot_fit_fmu(self,muestra)


    def set_z1eff(self,z1eff):
        setattr(self,'z1eff',z1eff)

    # imprime la string para la instancia
    def __str__(self):
        return f'Experimento ({self.path})'
    def __repr__(self):
        return f'Experimento ({self.path})'

## Auxiliar

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
        self['idznorm']=self['imag']/(self['2*pi*f']*self.l0)
        self['repeticion']=self['repeticion'].astype(str)
        return px.scatter(self, x='f',y='idznorm',color='repeticion',log_x=True)
    
    def repx(self):
        self['repeticion']=self['repeticion'].astype(str)
        return px.scatter(self, x='f',y='real',color='repeticion',log_x=True)
    
def get_id(x):
    if 'aire'in x.lower():
        return 'aire'
    elif 'm' in x.lower():
        return '_'.join(x.split('.')[0].split('_')[-2:])
    elif 'p' in x.lower():
        return '_'.join(x.split('.')[0].split('_')[-1:])
    else:
        return 'No se reconoce el nombre del archivo.'

def get_sigma(x,muestras):
    try:
        return muestras[muestras.nombre==x].conductividad.values[0]
    except:   
        return 0 
def get_esp(x,muestras):
    try:
        return muestras[muestras.nombre==x].espesor.values[0]*10e-3
    except:   
        return 0        
    
## LEGACY

    # def normcorr(self):
    #     '''
    #     Metodo que corrije las mediciones utilizando el benchmark harrison(xxxx)
    #     '''
    #     try:
    #         index_file_aire=self.files.index[self.files.str.lower().str.contains('aire')].values[0]
    #         self.index_aire=index_file_aire
    #         self.file_aire=self.files[index_file_aire]
    #         # diccionario con las variaciones de impedancias
    #         # corregidas y normalizadas (re + 1j imag)
    #         dict_dzcorrnorm,data_test=so.corrnorm(self,index_file_aire)
    #         self.data_test=data_test
    #         df=pd.DataFrame(dict_dzcorrnorm)
    #         df['f']=self.f
    #         dfdz=pd.melt(df,id_vars=df.columns[-1], var_name='muestra',value_name='dzcorrnorm')
    #         dfdz['imag']=np.imag(dfdz['dzcorrnorm'])
    #         dfdz['real']=np.real(dfdz['dzcorrnorm'])
    #         dfdz['muestra']=dfdz['muestra'].astype(int).map(pd.Series(self.files))
    #         dfdz['muestra']=dfdz['muestra'].apply(lambda x: x.split('_')[-1].split('.')[0])
    #         self.dznorm=dfdz
    #     except:
    #         print('Falta el archivo con la medicion de la impedancia en aire.')