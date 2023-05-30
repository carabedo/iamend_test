import iamend_ci.bo as bo
import iamend_ci.theo as theo
import iamend_ci.fit as fit
import iamend_ci.so as so
import iamend_ci.plt as plt
import iamend_ci.pxplt as px
import iamend_ci.plotbokeh as pb
import iamend_ci.tools as tools
import os
import pandas as pd
import numpy as np
import plotly.express as px
#esto sirve para no tener daramas con el path en windows/unix
from pathlib import Path
from sklearn.metrics import r2_score as R2
import logging
import traceback

path_muestras_csv = os.path.join(os.path.dirname(__file__), "datos", 'muestras.csv')


# definicion de la clase 'exp'

class Experimento():
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

            self.f=so.getf(self)

            self.w=2*np.pi*self.f
            
            self.x0=self.w*self.bobina['L0']

            # Genero como atributos los dataframes
            for i,df_ci in enumerate(self.data):
                setattr(self,'df'+ str(i),df_ci)

            if normcorr==True:
                self.normcorr(test=test,dropfirst=dropfirst)

        except Exception as e:
            print("There was an error: " + e.args[0] + ". The line where the code failed was " + str(traceback.extract_stack()[-1][1]))



    def normcorr(self,test=True,dropfirst=True):
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
            print("There was an error: " + e.args[0] + ". The line where the code failed was " + str(traceback.extract_stack()[-1][1]))


    def set_frange(self,f_inicial,f_final):
        # redifinimos f
        f_serie=pd.Series(self.f)
        f_new_mask=f_serie.between(f_inicial,f_final)
        self.f=f_serie[f_new_mask].values
        self.w=2*np.pi*self.f
        self.x0=self.w*self.bobina['L0']
        # ajustamos parametros geometricos effectivos en el rango
        ## filtramos de dznorm las frecuencias nuevas
        self.dznorm=self.dznorm[self.dznorm.f.between(f_inicial,f_final)]
        self.dznorm_test=self.dznorm_test[self.dznorm_test.f.between(f_inicial,f_final)]
        #self.fitpatron()
        # 



    # Ajustes
    def fitPatron(self,patron_filename='auto',param_geo='z1',plot=False, rango = None):

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
             
                z1eff,uz1eff=fit.z1(self.f,self.coil,dzcorrnorm,esp,sigma)

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
                pb.plot_fit_patron(self,param_geo,indice_patron)

        
        except Exception as e:
            print(e)   
            logging.exception("An exception was thrown!")                   
            return False
        

    def fitEspesorNc(self,indice_muestras,mur):
        '''
        Funcion para ajustar espesores no conductores, sobre placa ferromagnetica
            indice_muestras (lista): indice de muestras para ajustar el liftoff
            mur (float): mur de la placa ferromagnetica
        '''
        #solo sobre las muestras de la lista de indices
        yteos={}
        for i in indice_muestras:
            row=self.info.iloc[i]
            esp=row.espesor
            sigma=row.conductividad
            dzucorrnorm=self.dznorm[self.dznorm.muestra == row.archivo].dzcorrnorm.values
            #mu(f,bo_eff,dzucorrnorm,dpatron,sigma, name):
            fpar,fcov=fit.z1(self.f,self.coil,dzucorrnorm,esp,sigma,mur=mur)
            self.info.loc[i,'loeff']=fpar
            self.info.loc[i,'uloeff']=fcov
            x0=self.x0
            bob_eff=self.coil.copy()
            bob_eff[4]=fpar[0]

            yteo=theo.dzD(self.f,bob_eff,sigma,esp,mur,1500)/x0
            yteos[row.archivo]=yteo
            if self.test==True:
                # validacion con test de la parte imaginaria
                dzucorrnorm_test=self.dznorm_test.iloc[i].dzcorrnorm.values
                r2=R2(yteo.imag,dzucorrnorm_test.imag)
                self.info.loc[i,'R2']=r2
            self.ypreds=yteos
        return self.info.iloc[indice_muestras]
    


    def fitDosCapas(self,indice_archivo,muestra_inferior,muestra_superior,param):
  
        row_inferior=self.info.iloc[indice_archivo]
        nombre_archivo=row_inferior.archivo

        capa_inferior={
             'sigma' : row_inferior.conductividad,
             'mur' : row_inferior.permeabilidad,
             'indice_archivo' : indice_archivo
        }


        if muestra_superior.lower() == 'nc':

            capa_superior={
                'sigma' : 0,
                'mur' : 1
            }


            if param == 'd':

                fpar, fcov=fit.fit2capas(self,capa_superior,capa_inferior,param='d')
                return fpar,fcov
            else:
                 pass
        else:
            pass
            


        

    def fitMues(self,indice_muestras='all'):
        '''
        indice_muestras (lista): indice de muestras para ajustar el mu
        '''
        if indice_muestras=='all':
            #ajusto sobre todas las muestras
                if not hasattr(self,'z1eff'):
                    self.fitPatron()
                muestras=self.dznorm[self.dznorm.muestra.str.contains('M')].muestra.unique()
                self.info['mueff']=np.nan
                self.info['R2']=np.nan

                yteos={}
                for x in muestras:
                    print('Ajustando mur',x)
                    row=self.info[self.info.archivo.str.contains(x,case=False)]
                    esp=row.espesor.values[0]
                    sigma=row.conductividad.values[0]
                    dzucorrnorm=self.dznorm[self.dznorm.muestra == x].dzcorrnorm.values

                    #mu(f,bo_eff,dzucorrnorm,dpatron,sigma, name):
                    fpar,fcov=fit.mu(self.f,self.coil,dzucorrnorm,esp,sigma,row.archivo.values[0])
                    self.info.loc[row.index.values[0],'mueff']=fpar
                    x0=self.x0
                    yteo=theo.dzD(self.f,self.coil,sigma,esp,fpar,1500)/x0
                    yteos[x]=yteo

                    # validacion con test de la parte imaginaria
                    if self.test == True:
                        dzucorrnorm_test=self.dznorm_test[self.dznorm_test.muestra == x].dzcorrnorm.values
                        r2=R2(yteo.imag,dzucorrnorm_test.imag)
                        self.info.loc[row.index.values[0],'R2']=r2
                self.ypreds=yteos

        else:
            #solo sobre las muestras de la lista de indices
            yteos={}
            for i in indice_muestras:
                row=self.info.iloc[i]
                print('Ajustando mur',row.archivo)
                esp=row.espesor
                sigma=row.conductividad
                dzucorrnorm=self.dznorm[self.dznorm.muestra == row.archivo].dzcorrnorm.values
                #mu(f,bo_eff,dzucorrnorm,dpatron,sigma, name):
                fpar,fcov=fit.mu(self.f,self.coil,dzucorrnorm,esp,sigma,row.archivo)
                self.info.loc[i,'mueff']=fpar
                self.info.loc[i,'umueff']=fcov
                x0=self.x0
                yteo=theo.dzD(self.f,self.coil,sigma,esp,fpar,1500)/x0
                yteos[row.archivo]=yteo
                if self.test==True:
                    # validacion con test de la parte imaginaria
                    dzucorrnorm_test=self.dznorm_test[self.dznorm_test.muestra == row.archivo].dzcorrnorm.values
                    r2=R2(yteo.imag,dzucorrnorm_test.imag)
                    self.info.loc[i,'R2']=r2
                self.ypreds=yteos
            return self.info.iloc[indice_muestras]
 
    def fitfMues(self,*args,**kwargs):

        if len(args) == 0:
            print('definir cantidad de intervalos')
        elif len(args)==1:
            print('fiteo en N intervalos')
            n_splits_f=args[0]
            muestras=self.dznorm[self.dznorm.muestra.str.contains('M')].muestra.unique()
            coil_eff=self.coil
            fmu_fits={}
            for i,x in enumerate(muestras):
                name=x
                row=self.info[self.info.archivo.str.contains(x)]
                espesor=row.espesor.values[0]
                sigma=row.conductividad.values[0]
                dzucorrnorm=self.dznorm[self.dznorm.muestra == x].dzcorrnorm.values
                fmu_fit=fit.fmu(self.f,coil_eff,n_splits_f,dzucorrnorm,sigma,espesor,name)             
                for fn in range(n_splits_f):
                    fo=int(fmu_fit['fs'][fn][0]/1000)
                    ff=int(fmu_fit['fs'][fn][-1]/1000)
                    self.info.loc[self.info.archivo==x,'mu '+str(fo)+'k-'+str(ff)+'k']=fmu_fit['mues'][fn]   
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
                self.info.loc[self.info.archivo==x,'mu '+str(fo)+'k-'+str(ff)+'k']=fmu_fit['mues'][fn]   
            fmu_fits[x]=fmu_fit             
            self.fmues=fmu_fits

            print('fiteo desde A a B')   

    def fitSigma(self,indice_muestra,bounds=[0.1e6,20e6],plot=True):
        i=indice_muestra
        row=self.info.iloc[i]
        esp=row.espesor
        mur=row.permeabilidad
        dzucorrnorm=self.dznorm[self.dznorm.muestra == row.archivo].dzcorrnorm.values
        #mu(f,bo_eff,dzucorrnorm,dpatron,sigma, name):
        fpar,fcov=fit.sigma(self.f,self.coil,dzucorrnorm,esp,mur,bounds)
        self.info.loc[i,'sigma_eff']=fpar
        self.info.loc[i,'usigmaa_eff']=fcov
        x0=self.x0
        yteo=theo.dzD(self.f,self.coil,fpar,esp,mur,1500)/x0

        if plot == True:
            pb.plot_fit_sigma(self,indice_muestra,yteo.imag)
        return self.info.iloc[indice_muestra]
    

    def fitMuSigma(self,indice_muestra,plot=True,bounds=[[1,0.1e6],[100,10e6]]):
        i=indice_muestra
        row=self.info.iloc[i]
        esp=row.espesor
        dzucorrnorm=self.dznorm[self.dznorm.muestra == row.archivo].dzcorrnorm.values
        #mu(f,bo_eff,dzucorrnorm,dpatron,sigma, name):
        fpar,fcov=fit.muSigma(self.f,self.coil,dzucorrnorm,esp,bounds)
        self.info.loc[i,'mur_eff']=fpar[0]
        self.info.loc[i,'sigma_eff']=fpar[1]

        x0=self.x0
        yteo=theo.dzD(self.f,self.coil,fpar[1],esp,fpar[0],1500)/x0

        if plot == True:
            pb.plot_fit_sigma(self,indice_muestra,yteo.imag)
        return self.info.iloc[indice_muestra]
    # ploteos

    def implots(self,lib='bokeh'):
        if lib=='bokeh':
            pb.implots(self)
        else:
            fig=px.line(self.dznorm,x='f',y='imag',color='muestra',log_x=True)
            fig.show()

    def replots(self,lib='bokeh'):
        if lib=='bokeh':
            pb.replots(self)
        else:
            fig=px.line(self.dznorm,x='f',y='real',color='muestra',log_x=True)
            fig.show()



    def implot(self,n,static=False):
        if static == True:
            archivo=self.info.iloc[n].archivo
            y=self.dznorm[self.dznorm.muestra== self.info.iloc[1].archivo]
            plt.im(y,self.f,archivo)
        else:
            pb.plot_im(self,n)

    def replot(self,n,static=False):
        if static == True:
            archivo=self.info.iloc[n].archivo
            y=self.dznorm[self.dznorm.muestra== self.info.iloc[1].archivo]
            plt.re(y,self.f,archivo)
        else:
            pb.plot_re(self,n)


    def muesplot(self):
        pb.plot_fit_mues(self)
        
    def muplot(self,indice_muestra):
        fig=pb.plot_fit_mu(self,indice_muestra)
        return fig

        
    def fmuplot(self,muestra):
        pb.plot_fit_fmu(self,muestra)




    def update_z1eff(self,z1eff):
        setattr(self,'z1eff',z1eff)
        self.coil[4]=self.z1eff
        
    def update_permeabilidad(self,nombre_muestra,mueff):
        self.info.loc[self.info.muestras==nombre_muestra,'permeabilidad']=mueff

    def update_conductividad(self,nombre_muestra,sigmaeff):
        self.info.loc[self.info.muestras==nombre_muestra,'conductividad']=sigmaeff
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
    
