# -*- coding: utf-8 -*-
"""
Created on Fri May 19 22:24:11 2017

@author: anggitamahardika
"""

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

'=======BUKA GAMBAR========='
loc= 'D:/K/S\'\'\'\'\'\'/J/T/Project Akhir/dataset/latih/'
gambar=[]
gambar.append(Image.open(loc + 'ha.png').convert('L'))
gambar.append(Image.open(loc + 'na.png').convert('L'))
gambar.append(Image.open(loc + 'ca.png').convert('L'))
gambar.append(Image.open(loc + 'ra.png').convert('L'))
gambar.append(Image.open(loc + 'ka.png').convert('L'))
gambar.append(Image.open(loc + 'da.png').convert('L'))
gambar.append(Image.open(loc + 'ta.png').convert('L'))
gambar.append(Image.open(loc + 'sa.png').convert('L'))
gambar.append(Image.open(loc + 'wa.png').convert('L'))
gambar.append(Image.open(loc + 'la.png').convert('L'))
gambar.append(Image.open(loc + 'pa.png').convert('L'))
gambar.append(Image.open(loc + 'dha.png').convert('L'))
gambar.append(Image.open(loc + 'ja.png').convert('L'))
gambar.append(Image.open(loc + 'ya.png').convert('L'))
gambar.append(Image.open(loc + 'nya.png').convert('L'))
gambar.append(Image.open(loc + 'ma.png').convert('L'))
gambar.append(Image.open(loc + 'ga.png').convert('L'))
gambar.append(Image.open(loc + 'ba.png').convert('L'))
gambar.append(Image.open(loc + 'tha.png').convert('L'))
gambar.append(Image.open(loc + 'nga.png').convert('L'))


i=0
nilaiX = [[] for j in range(20)] #UNTUK MENYIMPAN NILAI X DARI MASING-MASING POLA
for polaKe in range (20):
    pixel = gambar[polaKe].load()

    x,y = gambar[polaKe].size
    #print 'ukuran gambar:', x,'x',y
    threshold = 160
    for baris in range (x):
        for kolom in range (y):
            if pixel[baris,kolom] >= threshold:
                pixel[baris,kolom] = 0
            else:
                pixel[baris,kolom] = 1
    #plt.imshow(gambar[i],cmap='Greys')
    
    #MENYIMPAN NILAI X PADA POLA KE I
    for baris in range (x):
        for kolom in range (y):
            nilaiX[polaKe].append(pixel[baris,kolom])
            
#MENGUBAH X KE BIPOLAR
for polaKe in range (20):
    for bobotKe in range (1000):
        if nilaiX[polaKe][bobotKe] == 0:
           nilaiX[polaKe][bobotKe] = -1

#print 'banyak data: ', len(nilaiX)
#print 'nilai x: ', nilaiX[1]

'=========PERHITUNGAN=========='
alpha= 1
tetha= 160 #NILAI AMBANG

#iteratif=0
aktivasi=[]
b=[] #MENYIMPAN BIAS
#MEMBUAT LIST NILAI TARGET AWAL
target=[] #MENYIMPAN TARGET
W=[[] for j in range(21)] #MENYIMPAN BOBOT
for polaKe in range (21):
    target.append(-1)
    b.append(0)
    aktivasi.append(0)
    #DEKLARASI NILAI BOBOT AWAL
    for bobotKe in range (1000):
        W[polaKe].append(0)
                         

a=1
#for polaKe in range (20): #PERULANGAN UNTUK PENGUJIAN MASING2 POLA
cek=True
while cek: #BANYAKNYA ITERASI PADA PENGENALAN POLA N 
    nilai=0
    print 'Iterasi ', a
    for dataKe in range (20): #PERULANGAN SEBANYAK DATA DALAM 1 ITERASI
        #for targetKe in range (20):
            #target[targetKe]=0
    
        #DEKLARASIKAN NILAI TARGET
        #if iteratif == polaKe:
        target[0]=1
        
        #MENGHITUNG Y_IN          
        y_in=0    
        for bobotKe in range (1000):        
            y_in += W[dataKe][bobotKe]*nilaiX[dataKe][bobotKe]
        y_in = y_in+b[dataKe]
    
        #Y_IN KE FUNGSI AKTIVASI
        if y_in > tetha:
            fungsi = 1
        elif y_in >= -tetha and y_in <= tetha:
            fungsi = 0
        elif y_in < -tetha:
            fungsi = -1    
        aktivasi[dataKe]=fungsi
        print aktivasi[dataKe]
    
        #PERBAIKAN BOBOT ATAU TIDAK    
        if aktivasi[dataKe] != target[dataKe]:
            for bobotKe in range (1000):
                W[dataKe+1][bobotKe] = W[dataKe][bobotKe] + (alpha*target[dataKe] * nilaiX[dataKe][bobotKe])
            b[dataKe+1] = (b[dataKe]) + (alpha*target[dataKe])
        else:
            for bobotKe in range (1000):
                W[dataKe+1][bobotKe]=W[dataKe][bobotKe]
            b[dataKe+1]=b[dataKe]            
         
    #PENGECEKAN APAKAH ITERASI BERLANJUT
    for dataKe in range (20):
        if aktivasi[dataKe] != target[dataKe]:
            nilai=nilai+1
            
    if nilai > 0:
        cek = 1
        for bobotKe in range (1000):
            W[0][bobotKe] = W[20][bobotKe]
        b[0] = b[20]
    else:
        cek= 0
        bobotAkhir = W[20]
        biasAkhir = b[20]
        
    a=a+1
    print '\n'


       

#MENYIMPAN KE CSV
#save=np.asarray(gambar)
##save = list(gambar.getdata())
##width, height = gambar.size 
##save = [save[i * width:(i + 1) * width] for i in xrange(height)]
#np.savetxt('tes.csv', nilaiX[19],fmt="%d", delimiter='\n')


