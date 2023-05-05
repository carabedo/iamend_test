import numpy as numpy
import scipy as scipy
import matplotlib.pyplot as plt

def sig(k,sigma,f,mur):
    """ funcion auxiliar"""
    mu0 = 4*numpy.pi*1e-7
    k2=1j*2*numpy.pi*f*mu0*mur*sigma
    return (k*mur-numpy.sqrt(k**2+k2))/(k*mur+numpy.sqrt(k**2+k2))

def sig2(k,sigma,f,d,mur):
    """ funcion auxiliar"""
    mu0 = 4*numpy.pi*1e-7
    k2=1j*2*numpy.pi*f*mu0*mur*sigma
    la=numpy.sqrt(k**2+k2)
    return (((la+k*mur)*(k*mur-la)+numpy.exp(-2*la*d)*(la-k*mur)*(k*mur+la))/((la+k*mur)*(k*mur+la)+numpy.exp(-2*la*d)*(la-k*mur)*(k*mur-la)))



def sigj(k,sigma,f,mur,z):
    """ funcion auxiliar"""
    mu0 = 4*numpy.pi*1e-7
    k2=1j*2*numpy.pi*f*mu0*mur*sigma
    la=numpy.sqrt(k**2+k2)
    return (2*k*mur*numpy.exp(la*z)/(la+k*mur))



def sig3(k,sigma1,sigma2,f,d,mur1,mur2):
    """ funcion auxiliar"""
    mu0 = 4*numpy.pi*1e-7
    k21=1j*2*numpy.pi*f*mu0*mur1*sigma1
    k22=1j*2*numpy.pi*f*mu0*mur2*sigma2

    la1=numpy.sqrt(k**2+k21)
    la2=numpy.sqrt(k**2+k22)

    up=(la1*mur2 + la2*mur1)*(k*mur1-la1)+numpy.exp(-2*la1*d)*(la1*mur2-la2*mur1)*(k*mur1+la1)
    down=(la1*mur2 + la2*mur1)*(k*mur1+la1)+numpy.exp(-2*la1*d)*(la1*mur2-la2*mur1)*(k*mur1-la1)
    return (up/down)


def ji(k,r1,r2):
    """ funcion auxiliar"""
    return     scipy.integrate.quad(lambda x: x*scipy.special.jv(1,x) ,k*r1,k*r2)[0]

def expz(k,z1,z2):
    """ funcion auxiliar"""
    return ((numpy.exp(-k*z1)-numpy.exp(-k*z2)))/(k**(3))


# integral imaginaria

def cquad(func, a, b, **kwargs):
    """ funcion auxiliar"""
    def real_func(x):
        return numpy.real(func(x))
    def imag_func(x):
        return numpy.imag(func(x))
    real_integral = scipy.integrate.quad(real_func, a, b, **kwargs)
    imag_integral = scipy.integrate.quad(imag_func, a, b, **kwargs)
    return (real_integral[0] + 1j*imag_integral[0])

# funciones finales

# def edyquad(f):
#     """ funcion auxiliar"""
#     aint=(1j*mu0*numpy.pi*N**2)/(L0*((r2-r1)*dh)**2)
#     return aint*cquad(lambda k: sig(k,sigma,f)*(ji(k,r1,r2)*expz(k,z1,z1+dh))**2,0,5000)


def sig3(k,sigma1,sigma2,f,d,mur1,mur2):
    """ funcion auxiliarm figura 3.2 [theo]
    conductor ferromagnetico 1 de espesor d
    conductor ferromagnetico 2 de espesor inf
    """
    mu0 = 4*numpy.pi*1e-7
    k2_1=1j*2*numpy.pi*f*mu0*mur1*sigma1
    k2_2=1j*2*numpy.pi*f*mu0*mur2*sigma2

    la1=numpy.sqrt(k**2+k2_1)
    la2=numpy.sqrt(k**2+k2_2)

    up=(la1*mur2 + la2*mur1)*(k*mur1-la1)+numpy.exp(-2*la1*d)*(la1*mur2-la2*mur1)*(k*mur1+la1)
    down=(la1*mur2 + la2*mur1)*(k*mur1+la1)+numpy.exp(-2*la1*d)*(la1*mur2-la2*mur1)*(k*mur1-la1)
    return (up/down)

# funciones auxiliares



def iconf(av,uav,bv,ubv):
    for i,a in enumerate(av):
        b=bv[i]
        ub=ubv[i]
        ua=uav[i]
        plt.figure(figsize=[8,2])
        x11=a-ua
        x12=a+ua
        y1=1
        x21=b-ub
        x22=b+ub
        y2=1
        plt.plot([x11,x12],[y1,y1], linewidth=15, alpha=0.5, label='_nolegend_')
        plt.plot([x21,x22],[y2,y2], linewidth=15, alpha=0.5, label='_nolegend_')
        plt.plot(a,y1, 'ok')
        plt.plot(b,y2, 'vk')
        plt.ylim([0,2])
        plt.legend([str('%.2E' % a),str('%.2E' % b)])
        #get current axes
        ax = plt.gca()
        plt.ticklabel_format(style='sci', axis='x', scilimits=(-3,-3))

        #hide y-axis
        ax.get_yaxis().set_visible(False)
