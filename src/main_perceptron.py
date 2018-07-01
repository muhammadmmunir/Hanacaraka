from Tkinter import *
from ttk import *
from PIL import ImageTk, Image
import tkFileDialog
import matplotlib.pyplot as plt
import numpy as np
import csv

#kelas yang diturunkan dari kelas Frame
class Example(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.parent = parent
        self.initUI()
        self.centerWindow()
    
    #mengatur window
    def initUI(self):
        
        self.parent.title("Pengenalan Huruf Hanacaraka")
        self.pack(fill=BOTH, expand=True)
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)
  
        lbl1 = Label(text="Silahkan buka file image")
        lbl1.config(font=("Arial", 10))
        lbl1.place(x=100, y=5)

        lbResult = Label(text="Hasil Pengenalan Huruf")
        lbResult.config(font=("Arial", 10))
        lbResult.place(x=100, y=130)
        
        self.result = Text(height=5, width=30)
        self.result.place(x=55, y=160)        
    
    #membuka file image
    def onOpen(self):
      
        ftypes = [('Python files', '*.png'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
        
        if fl != '':
            self.readFile(fl)

    #menampilkan file image
    def readFile(self, filename):
        
        #objek image dan photo image dari folder yang sekarang
        ha = Image.open(filename)
        ha = ha.resize((80, 50), Image.ANTIALIAS)
        han = ImageTk.PhotoImage(ha)
        label1 = Label(self, image=han)
        label1.image = han
        label1.place(x=130, y=30)
        self.filename = filename
        
        btnProcess = Button(text="Kenali", command=self.perceptron)
        btnProcess.place(x=135, y=100)
        
    def perceptron(self):
        
        nilaiU = self.processImage(self.filename)
        bobotDL = self.openDataTrain()
        net = self.testingData(nilaiU, bobotDL)
        hasil = self.check(net)        
        self.result.insert(INSERT, hasil+'\n')
        
    def processImage(self, filename):

        loc2 = 'D:/K/S\'\'\'\'\'\'/J/T/Project Akhir/dataset/uji/'
        uji = []
        uji.append(Image.open(filename).convert('L'))

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
        
        return nilaiU
    
    def openDataTrain(self):
        #membuka file csv yang berisi bobot semua pola dan menyimpannya
        loc3= 'D:/K/S\'\'\'\'\'\'/J/T/Project Akhir/dataset/data/'
        with open(loc3+'datatraining.csv', 'rb') as f:
            reader = csv.reader(f)
            bobotDL = list(reader)
    
        #convert dari elemen string ke int semua bobot dan bias
        for x in range(len(bobotDL)):
            for y in range(len(bobotDL[x])):
                bobotDL[x][y] = int(bobotDL[x][y])
        
        return bobotDL
    
    def testingData(self, nilaiU, bobotDL):
        #pengujian input terhadap semua pola huruf hanacaraka
        tetha = 160
        net = []
        for n in range(len(bobotDL)):
            xw = 0
            for x in range(len(bobotDL[n])-1):
                xw += nilaiU[0][x] * bobotDL[n][x]
                
            net.append(bobotDL[n][1000] + xw)
            
            print net

            if net[n] > tetha:
                net[n] = 1
            elif net[n] >= -tetha and net[n] <= tetha:
                net[n] = 0
            elif net[n] < -tetha:
                net[n] = -1   
                   
        
        return net
    
    def check(self, net):
        #pengecekan input masuk ke pola yang mana
        hanacaraka = ['ha','na','ca','ra','ka','da','ta','sa','wa','la',
                      'pa','dha','ja','ya','nya','ma','ga','ba','tha','nga']
        hasil = ""
        for x in range(len(hanacaraka)):
            if net[x] == 1:
                hasil = hanacaraka[x]    
            
        net_sum = 0
        for x in range(len(net)):
            net_sum = net_sum + net[x];
        
        if hasil == "" or net_sum > 1:
            hasil = "belum dikenali"
            
        print net

        return hasil
    
    #membuat window ditengah layar
    def centerWindow(self):
        
        w = 350
        h = 280
        
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

def main():
    
    root = Tk()
    app = Example(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()