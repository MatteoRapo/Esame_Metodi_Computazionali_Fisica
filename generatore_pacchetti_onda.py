import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import fft
from tqdm import trange

def distribuzione_frequenze(ni):       #le funzioni distribuzione_frequenze e funzione_cumulativa non sono necessarie
    pp=np.zeros(len(ni))               #sono state definite per eseguire test e verificare che funzionassero
    mask1=(ni>=0)&(ni<=2)              #correttamente
    mask2=(ni>2)&(ni<=3)
    pp[mask1]=(1/3)*ni[mask1]
    pp[mask2]=(2/3)*(3-ni[mask2])
    return pp
def funzione_cumulativa(ni):
    pp=np.zeros(len(ni))
    mask1=(ni>=0)&(ni<=2)
    mask2=(ni>2)&(ni<=3)
    pp[mask1]=(1/6)*(ni[mask1]**2)
    pp[mask2]=-2+(2/3)*(3*ni[mask2]-0.5*ni[mask2]**2)
    return pp
def cumulativa_inversa(pp):
    ''' per trovare la forma analitica della cumulativa inversa si sono invertite le due relazioni quadratiche trovate nella funzione cumulativa (il cui integrale è 1) e sono stati scelti i rami di parabola che rendessero continua l'inversa'''
    ni=np.zeros(len(pp))
    mask1=(pp>=0)&(pp<=(2/3))
    mask2=(pp>(2/3))&(pp<=1)
    ni[mask1]=np.sqrt(6*pp[mask1])
    ni[mask2]=-np.sqrt(-3*pp[mask2]+3)+3
    return ni
#per verificare che la cumulativa inversa funzioni
#plt.hist(cumulativa inversa(np.random.random(1000)),bins=50)
#plt.show()
def generatore_ampiezze(ni,a):
    '''si moltiplica random (che genera un numero casuale da 0 a 1 per la radice quadrata delle frequenze, in python non occorre utilizzare il ciclo for'''
    ampiezze=a*np.random.random(len(ni))*np.sqrt(ni)
    return ampiezze
def spettro(ni,a):
    ''' questa funziona serve a \"rendere continuo\" lo spettro delle ampiezze, infatti occorre aumentare la lunghezza dell\'array, se lo si fa tramite fft l'array delle ampiezze viene riempito di 0 in fondo, in questo modo invece si ha corrispondenza tra le ampiezze e le frequenze scelte casualmente'''  
    
    ni1=np.linspace(0,3,2000)
    amp1=np.zeros(2000)
    for i in range(len(ni)):
        for j in range(len(ni1)):
            if np.abs(ni[i]-ni1[j])<1/(1000/3):   #questa condizione serve per confrontare la frequenza generata
                amp1[j]=a[i]                      #casualmente e quella del campione "continuo", 2000/3 è il passo del
    return amp1                                   #linspace, viene diviso ulteriormente per 2 per evitare che ci siano
                                                  #due frequenze alla quale viene assegnata la stessa ampiezza
                                                  
def numero_onda(ni,dispersione='onde_profonde',c=1,b=1):
    '''il numero d'onda che viene calcolato a partire dalla relazione di dispersione data'''
    kk=np.zeros(len(ni))
    omega=2*ni*np.pi
    if dispersione=='onde_profonde':
        kk=(omega)**2/c
        return kk
    elif dispersione=='elettromagnetica':
        kk=(omega)/np.sqrt(c)
        return kk
    elif dispersione=='cubica':
        kk=(omega**2/c)**(1/3)
        return kk
    elif dispersione=='Klein-Gordon':
        kk=(omega**2-b)/c
        return kk
    elif dispersione=='quantistica':
        kk=np.sqrt(omega)/c**(1/4)
        return kk
    else:
        print('dispersione non corretta')
        return None
class pacchetto_onda:
    '''oggetto pacchetto_onda che viene poi usato nel main'''
    def  __init__(self,N,xx,a=1,distribuzione='predefinita',dispersione='lineare',c=1,b=1):
        if distribuzione=='predefinita':
            self.frequenze=cumulativa_inversa(np.random.random(N))
        elif distribuzione=='gaussiana':
            self.frequenze=np.random.normal(loc=1.5,scale=0.33,size=N)
        elif distribuzione=='piatta':
            self.frequenze=3*np.random.random(N)
        else:
            print('Distribuzione non esistente')
            return None
        self.ampiezza=generatore_ampiezze(self.frequenze,a)
        self.spettro=spettro(self.frequenze,self.ampiezza)
        self.numero_onda=numero_onda(self.frequenze,dispersione,c,b)
        self.iniziale=fft.rfft(self.spettro,n=len(xx))   #si usa la rfft perchè lo spettro delle ampiezze è reale
    def evoluzione_temporale(self,x,t):
        onda=np.zeros(len(x))*1j
        for i in range(len(self.frequenze)):
            onda=onda+self.ampiezza[i]*np.exp((self.numero_onda[i]*x-2*np.pi*self.frequenze[i]*t)*1j) 
        return onda      
       
#per l'evoluzione temporale è stata usata la sovrapposizione di onde monocromatiche con il numero d'onda definito dalla relazione di dispersione e la fase ottenuta dal prodotto tra omega e il tempo
