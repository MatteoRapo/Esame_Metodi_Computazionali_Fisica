import generatore_pacchetti_onda
import numpy as np
from scipy import fft
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from tqdm import tqdm,trange
from matplotlib.animation import PillowWriter

print('Questo programma genera, a partire da una distribuzione di probabilità, frequenze e ampiezze di un pacchetto d\'onda, ne fa la trasformata di Fourier e salva un grafico della parte reale e della parte immaginaria')
N=input("Selezionare il numero di componenti (compreso tra 2 e 1000) ")
distribuzione_in= input("Selezionare la distribuzione di probabilità tra \"predefinita\", \"gaussiana\", \"piatta\" ")
print('È possibile scegliere una relazione di dispersione per avere l\'evoluzione temporale del pacchetto d\'onda ')
dispersione_in=input("Selezionare la dispersione tra \"onde_profonde\", \"elettromagnetica\", \"cubica\", \"klein-gordon\" e \"quantistica\" ")

xx=np.linspace(0,1000,10000) #xx è stato scelto affinchè ci sia un numero di punti sufficienti e affinchè possa
                             #contenere il movimento del pacchetto per l'intervallo di tempo scelto
pacchetto=generatore_pacchetti_onda.pacchetto_onda(int(N),xx,dispersione=dispersione_in,distribuzione=distribuzione_in)
''' faccio il plot del pacchetto d'onda, fft produce il grafico di un periodo del pacchetto d'onda'''
plt.plot(xx[:len(pacchetto.iniziale)],pacchetto.iniziale[:len(pacchetto.iniziale)].real,color='blue',label='Parte reale')
plt.plot(xx[:len(pacchetto.iniziale)],pacchetto.iniziale[:len(pacchetto.iniziale)].imag,'--',label='parte immaginaria',color='orange')
plt.xlabel('x [m]')
plt.ylabel('ampiezza [u.a.]')
plt.legend()
plt.savefig('pacchetto_onda.png')

print("Il pacchetto d'onda è stato generato")

def animazione(t):
    '''questa funzione per ogni istante t aggiorna il plot con il pacchetto d\'onda calcolato nell\'istante scelto'''


    ampiezza_quadra = np.abs(pacchetto.evoluzione_temporale(xx , t/4))**2 #il tempo viene diviso per 4 perchè                                                                                     risultava troppo veloce il dt unitario 
    
    linea1.set_data(xx, ampiezza_quadra)
    time_text.set_text('tempo (s)='+'{:.1f}'.format(0.02*t))
    print(t)
    
fig,ax=plt.subplots(1,1)
linea1, =plt.plot([],[],label='Onda')
def init():
    '''condizioni iniziali del plot'''
    ax.set_xlim(min(xx),max(xx))
    ax.set_ylim(min(np.abs(pacchetto.evoluzione_temporale(xx,0)**2)), max(np.abs(pacchetto.evoluzione_temporale(xx,0)**2)))
    ax.set_xlabel('x [m]')
    ax.set_ylabel('potenza [u.a.]')
    return linea1,


time_text=ax.text(max(xx)*(3/4),max(np.abs(pacchetto.evoluzione_temporale(xx,0)**2))*(3/4),'',bbox=dict(facecolor='white', edgecolor='black'))
anim = ani.FuncAnimation(fig, animazione,frames=500, interval=1, blit=False, init_func=init)
'''anim si comporta come un ciclo for, in questo caso genera numeri da 1 a 500 e li mette come argomento di animazione'''
anim.save('onda.gif',writer='pillow',fps=50,dpi=100) 
print("Gif salvata, il programma è stato eseguito correttamente")
plt.close()
