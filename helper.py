import glob
import sys
import pandas as pd

path = './iamend_ci/datos'+sys.argv[1] 
print('folder: '+path)
files = glob.glob(path+ "*.csv")
csv_files=[ x.split('/')[-1] for x in files]

print()
lines=[]
try:
    bobina = sys.argv[2]
    for x in csv_files:
        lines.append([x, '0' , '0' ,bobina])
except:
    bobina=input('Bobina?')
    for x in csv_files:
        lines.append([x, '0' , '0' ,bobina])

txt_file = path+'info.txt'


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
def get_esp(x,muestras):
    try:
        return muestras[muestras.nombre==x].espesor.values[0]*10e-3
    except:   
        return 0       
    

data=pd.DataFrame(lines)
data.columns=['archivo','conductividad','espesor','bobina']
data['muestras']=data.archivo.apply(lambda x: get_id(x))
muestras=pd.read_csv('./iamend_ci/muestras2.csv')
data.conductividad=data.muestras.apply(lambda x: get_sigma(x,muestras))
data.espesor=data.muestras.apply(lambda x: get_esp(x,muestras))

data.to_csv(path+'info.txt',index=False)