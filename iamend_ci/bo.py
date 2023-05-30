"""Modulo con los valores geometricos nominales para las bobinas"""
import numpy
#r1 r2 dh N z1 l0
#bobina matias
m1=[1.15e-3,2.95e-3,2.48e-3,387,0.7e-3,14.55,375.75e-06]

pp1=[3e-3,4.56e-3,5.02e-3,253,1.16e-3,5.53,345.85e-06]
c=[4e-3,4.50e-3,10e-3,216,0.4e-3,1,353e-6]

# bobinas azules
# r1    r2      dh      N   z1     r0  l0
a=[7.8e-3,8.60e-3,14.8e-3,400,0.5e-3,7.92,149e-6]
b=[4e-3,8.60e-3,14.8e-3,800,0.4e-3,1,353e-6]

mu0 = 4*numpy.pi*1e-7
z0pp1=5.53+1j*345.85e-06


data={
'm1' :[1.15e-3,2.95e-3,2.48e-3,387,0.7e-3,14.55,375.75e-06] ,
'pp1' :[3e-3,4.56e-3,5.02e-3,253,1.16e-3,5.53,345.85e-06],
'c' : [4e-3,4.50e-3,10e-3,216,0.4e-3,1,353e-6],
'a' : [7.8e-3,
       8.60e-3,
       14.8e-3,
       400,
       0.5e-3,
       7.92,
       149e-6],
'b' :[7.8e-3,8.60e-3,14.8e-3,800,0.4e-3,1,353e-6]
}


data_dicts = { 

'm1' : {
    'r1' : 1.15e-3,
    'r2' : 2.95e-3,
    'dh' : 2.48e-3,
    'N'  : 387,
    'z1' : 0.7e-3,
    'L0' : 375.75e-06,
    'R0'  : 14.55,
    'nombre' : 'm1'
}
,
'pp1' : {
    'r1' : 3e-3,
    'r2' : 4.56e-3,
    'dh' : 5.02e-3,
    'N'  : 253,
    'z1' : 1.16e-3,
    'L0' : 345.85e-06,
    'R0'  : 5.53,
    'nombre' : 'pp1'
}
,
'a' : {
    'r1' : 7.8e-3,
    'r2' : 8.60e-3,
    'dh' : 15.02e-3,
    'N'  : 400,
    'z1' : 0.5e-3,
    'L0' : 149e-06,
    'R0'  : 7.92,
    'nombre' : 'a'
}
,
'b' : {
    'r1' : 7.8e-3,
    'r2' : 8.60e-3,
    'dh' : 15.02e-3,
    'N'  : 400,
    'z1' : 1.16e-3,
    'L0' : 345.85e-06,
    'R0'  : 5.53,
    'nombre' : 'b'
}
} 