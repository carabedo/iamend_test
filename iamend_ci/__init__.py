import iamend_ci.bo as bo
import iamend_ci.theo as theo
import iamend_ci.fit as fit
import iamend_ci.so as so
import iamend_ci.plt as plt
import iamend_ci.ax as ax
import os
import pandas as pd
import numpy as np
#esto sirve para no tener daramas con el path en windows/unix
from pathlib import Path



class exp():
    def __init__(self,path):
        self.path=path
        try:
            infopath=[x for x in os.listdir(path) if 'info' in x][0]
            data_folder = Path(path)
            infofullpath=data_folder / infopath
            info=pd.read_csv(infofullpath)    
            self.info=info
            self.files=info.iloc[:,0]
            self.sigmas=info.iloc[:,1]
            self.espesores=info.iloc[:,2]
            if len(info.bobina.unique()) == 1:             
                self.bobina=bo.data_dicts[info.bobina[0]]     
                self.coil=bo.data[info.bobina[0]]   
            else:
                print('Mas de una bobina, separe las mediciones en carpetas para cada bobina.')
            self.data=so.load(self.path)
            self.f=so.getf(self.data)
            self.w=2*np.pi*self.f
        except:
            print('Falta archivo info, con nombres de archivos, conductividades, espesores y bobina utilizada')

 

    def normcorr(self):
        self.dzcorrnorm=so.corr(self.f,self.coil,[self.data],Vzu='all') 
        return        

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

