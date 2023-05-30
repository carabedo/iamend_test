# iamend_ci

Libreria para la estimacion de la permeabilidad relativa efectiva usando mediciones de impedancia de una bobina sobre materiales conductores ferromagneticos. Contiene submodulos para la importancion de mediciones realizadas con `Solartron 1260A`, grafico de impedancias y correciones de efectos no ideales en los contactos.

### implementacion del modelo teorico de dood,deeds

`iamend_ci.theo.zo()`

![img](https://raw.githubusercontent.com/carabedo/iamend_ci/master/imgs/0_1.png)

`iamend_ci.theo.dzD()`

![img](https://raw.githubusercontent.com/carabedo/iamend_ci/master/imgs/0_2.png)

`iamend_ci.theo.jhf()`

![img](https://raw.githubusercontent.com/carabedo/iamend_ci/master/imgs/0_3.png)

con:

![img](https://raw.githubusercontent.com/carabedo/iamend_ci/master/imgs/0_4.png)




### Carga y correccion datos

Cada experimento debe constar de:

- una medicion en aire, para el la correcion de los efectos no ideales.
- una medicion en un patron de mu,sigma y espesor conocido, para el ajuste de los parametros geometricos de la bobina.
- mediciones en patrones donde se busque ajustar algun parametro.
- todos los archivos deben estar en la misma carpeta
- la carpeta debe contener un archivo `info.cv` con la informacion de cada archivo.

Ejemplo de `info.csv`:

```
archivo,conductividad,espesor,bobina,muestras
Exp_aire.csv,0.0,0.0,pp1,aire
Exp_1010-M01.csv,3830000.0,0.065,pp1,1010-M01
Exp_P066.csv,610200.0,0.14957,pp1,P066
```
En este experimento, el archivo `Exp_aire.csv` es la medicion en aire. `Exp_P066.csv` es la medicion sobre el patron y `Exp_1010-M01.csv` es la medicion sobre la muestra a caracterizar. El nombre de la muestra esta separado por `_`. Las nombres de las muestras siguen la siguiente forma `MATERIAL-MUESTRA`.


Para cargar todos los archivos de un experimento usamos la clase `Exp`, la cual inicializamos con la ruta de la carpeta que contiene los datos:

```python

import iamend_ci as ci

exp=ci.exp('.//iamend_ci//datos//pp1_manual//')
# lee las frecuencias utilizadas en el experimento
f=ci.so.getf(data)

# carga los parametros geometricos de la bobina
bo=ci.bo.bobpp1

# importa y corrige los valores de la impedancia
datacorr=ci.so.corr(f,bo,data)
```

### Grafico datos

```python
# ploteo de la parte imaginaria de la impedancia corregida (parametros: x,Y,n= id medicion )
ci.plt.im(f,datacorr,1)
```

![](/imgs/1.png)

### Ajuste permeabilidad

#### Parametros geometricos efectivos

```phyton
dp=15e-3
sig=4e6
mup=1
# valor ajustado y grafico
z1eff,figz1=ci.fit.z1(f,bo,datacorr,0,dp,sig,mup)
```

#### Permeabilidad relativa efectiva

```python
mueff,pltmu=ci.fit.mu(f,bo,datacorr,1,4e6,z1eff)
```

### Densidad de corriente





