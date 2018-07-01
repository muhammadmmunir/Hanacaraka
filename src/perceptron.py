from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import csv

loc2 = 'D:/K/S\'\'\'\'\'\'/J/T/Project Akhir/dataset/uji/'
uji = []
uji.append(Image.open(loc2+'ha.png').convert('L'))
uji.append(Image.open(loc2+'ga.png').convert('L'))
uji.append(Image.open(loc2+'da.png').convert('L'))
uji.append(Image.open(loc2+'ca.png').convert('L'))
uji.append(Image.open(loc2+'ja.png').convert('L'))
uji.append(Image.open(loc2+'ka.png').convert('L'))
uji.append(Image.open(loc2+'tha.png').convert('L'))
uji.append(Image.open(loc2+'ta.png').convert('L'))
uji.append(Image.open(loc2+'dha.png').convert('L'))
uji.append(Image.open(loc2+'ba.png').convert('L'))
uji.append(Image.open(loc2+'ma.png').convert('L'))
uji.append(Image.open(loc2+'nga.png').convert('L'))
uji.append(Image.open(loc2+'nya.png').convert('L'))
uji.append(Image.open(loc2+'ra.png').convert('L'))
uji.append(Image.open(loc2+'wa.png').convert('L'))
uji.append(Image.open(loc2+'ya.png').convert('L'))

i=0
nilaiU = [[] for j in range(len(uji))] #UNTUK MENYIMPAN NILAI X DARI MASING-MASING POLA
for polaKe in range (len(uji)):
    pixel = uji[polaKe].load()

    x,y = uji[polaKe].size
    #print 'ukuran gambar:', x,'x',y
    threshold = 160
    for baris in range (x):
        for kolom in range (y):
            if pixel[baris,kolom] >= threshold:
                pixel[baris,kolom] = 0
            else:
                pixel[baris,kolom] = 1
    #plt.imshow(uji[i],cmap='Greys')
    
    #MENYIMPAN NILAI X PADA POLA KE I
    for baris in range (x):
        for kolom in range (y):
            nilaiU[polaKe].append(pixel[baris,kolom])
            
#MENGUBAH X KE BIPOLAR
for polaKe in range (len(uji)):
    for bobotKe in range (1000):
        if nilaiU[polaKe][bobotKe] == 0:
           nilaiU[polaKe][bobotKe] = -1

#menyimpan bobot ke file csv
#with open('datatrainingbias.csv', 'a') as myfile:
#    wr = csv.writer(myfile, delimiter=',')
#    wr.writerow(biasAkhir)

#membuka file csv yang berisi bobot semua pola dan menyimpannya
loc3= 'D:/K/S\'\'\'\'\'\'/J/T/Project Akhir/dataset/data/'
with open(loc3+'datatraining.csv', 'rb') as f:
    reader = csv.reader(f)
    bobotDL = list(reader)
    
#convert dari elemen string ke int semua bobot dan bias
for x in range(len(bobotDL)):
    for y in range(len(bobotDL[x])):
        bobotDL[x][y] = int(bobotDL[x][y])

#pengujian input terhadap semua pola huruf hanacaraka
tetha = 160
net = []
for n in range(len(bobotDL)):
    xw = 0
    for x in range(len(bobotDL[n])-1):
        xw += nilaiU[15][x] * bobotDL[n][x]
        
    net.append(bobotDL[n][1000] + xw)

    if net[n] > tetha:
        net[n] = 1
    elif net[n] >= -tetha and net[n] <= tetha:
        net[n] = 0
    elif net[n] < -tetha:
        net[n] = -1    

#pengecekan input masuk ke pola yang mana
hanacaraka = ['ha','na','ca','ra','ka','da','ta','sa','wa','la',
              'pa','dha','ja','ya','nya','ma','ga','ba','tha','nga']
hasil = ""
for x in range(len(hanacaraka)):
    if net[x] == 1:
        hasil = hanacaraka[x]    
    
if hasil == "":
    hasil = "belum dikenali"

print hasil
