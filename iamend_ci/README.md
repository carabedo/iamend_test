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




### carga  y correccion datos



```python


import iamend_ci as ci

data=ci.so.load('carpeta con mediciones')

# lee las frecuencias utilizadas en el experimento

f=ci.so.getf(data)

# carga los parametros geometricos de la bobina
bo=ci.bo.bobpp1

# importa y corrige los valores de la impedancia
datacorr=ci.so.corr(f,bo,data)
```

### grafico datos

```python
# ploteo de la parte imaginaria de la impedancia corregida (parametros: x,Y,n= id medicion )
ci.plt.im(f,datacorr,1)
```

![](/imgs/1.png)

### ajuste permeabilidad

#### parametros geometricos efectivos

```phyton
dp=15e-3
sig=4e6
mup=1
# valor ajustado y grafico
z1eff,figz1=ci.fit.z1(f,bo,datacorr,0,dp,sig,mup)
```

#### permeabilidad relativa efectiva

```python
mueff,pltmu=ci.fit.mu(f,bo,datacorr,1,4e6,z1eff)
```

### densidad de corriente





