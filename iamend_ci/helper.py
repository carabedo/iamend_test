import glob
import sys

path = sys.argv[1] 
print('folder: '+path)
files = glob.glob(path+ "*.csv")
csv_files=[ x.split('/')[-1] for x in files]
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

with open(txt_file, 'w') as f:
    # write csv file names to text file
    f.write('archivo,conductividad,espesor,bobina'+'\n')
    for line in lines:
        f.write(','.join(line) + '\n')

