import glob
import sys
import pandas as pd
import numpy as np

def get_info(path,bobina=None):
    print('folder: '+path)
    files = glob.glob(path+ "*.csv")
    csv_files=[ x.split('/')[-1] for x in files]

    if len(csv_files)>1:
        lines=[]
        if bobina==None:
            try:
                bobina=input('Bobina?')

            except:
                print('Defina la bobina usada en el experimento.')

        for x in csv_files:
            lines.append([x, np.nan , np.nan ,np.nan,bobina])
        def get_id(x):
            if 'aire'in x.lower():
                return 'aire'
            
            elif 'P' in x:
                return [y for y in x.split('_') if 'P' in y][0].split('.')[0]
            
            elif '-' in x:
                
                return [y for y in x.split('_') if '-' in y][0].split('.')[0]

            else:
                return [y for y in x.split('_')][1].split('.')[0]
                print('No se reconoce el nombre del archivo.',x)


        def get_sigma(x,muestras):
            try:
                return muestras[muestras.nombre==x].conductividad.values[0]
            except:   
                return 0 
        def get_espesor(x,muestras):
            try:
                return muestras[muestras.nombre==x].espesor.values[0]*10e-3
            except:   
                return 0       
        def get_permeabilidad(x,muestras):
            try:
                return muestras[muestras.nombre==x].permeabilidad.values[0]
            except:   
                return 0     
            
        data=pd.DataFrame(lines)
        data.columns=['archivo','conductividad','permeabilidad','espesor','bobina']
        data['muestras']=data.archivo.apply(lambda x: get_id(x))
        muestras=pd.read_csv('./iamend_ci/datos/muestras.csv')
        data.conductividad=data.muestras.apply(lambda x: get_sigma(x,muestras))
        data.espesor=data.muestras.apply(lambda x: get_espesor(x,muestras))
        data.permeabilidad=data.muestras.apply(lambda x: get_permeabilidad(x,muestras))
        data=data.sort_values('archivo')
        data.to_csv(path+'info.txt',index=False)
    else:
        print('No se encontraron archivos, revise la ruta.')



def lista_mediciones():
    rootdir = './iamend_ci/datos/'
    for path in glob.glob(f'{rootdir}/*/'):
        print(path)