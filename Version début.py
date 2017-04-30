
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image, ImageTk


#_______DEF__________#

def noir_blanc():
    global data, vartest,Canevas,img,photo
    print('height')
    print(photo.height())
    print(len(data))
    print('widht')
    print(photo.width())
    
    for i in range(len(data)):
        p = data[i]
        r = int((p[0] + p[1] + p[2]) / 3)
        p = (r, r, r)
        data[i] = p           
    change_img()
 
    
def change_img():
    """permet de créer l' image temporaire à partir d'une modification"""
    global data, vartest,Canevas,img,photo
    img.putdata(data)
    img.save("tmp.png", "PNG")
    vartest=1
    img=Image.open('tmp.png')
    data = list(img.getdata())
    Canevas.delete(ALL)
    photo = ImageTk.PhotoImage(file='tmp.png')   
    Canevas.create_image(0,0,anchor=NW,image=photo)
    
    
def enregistrer_img():
    """créer une image temporaire à partir des modifications"""
    global vartest,Canevas,img, data
    img.putdata(data)
    img.save("tmp_final.png", "PNG")
   

def appliquer_filtre(filtre, *arg):
    """applique le filrte spécifié puis enregistre et affiche l'image"""
    global img

    if img is None:
        return
    else:
        # chargement(début)
        filtre(*arg)
        enregistrer()
        # chargement(fin)
        afficher()


def chargement(arg):
    """affiche un écran de chargement pendant que le filtre se met en place"""
    ## À FAIRE : faire
    pass


###############
##  Filtres  ##
###############


def negatif():
    global data
    for i in range(len(data)):
        p = data[i]
        p = (255 - p[0], 255 - p[1], 255 - p[2])
        data[i] = p
    change_img()

def seuil():
    global data
    for i in range(len(data)):
        p = data[i]
        r = int((p[0] + p[1] + p[2]) / 3)
        if r < 128:
            data[i] = (0, 0, 0)
        else:
            data[i] = (255, 255, 255)
    change_img()

def bruit_L(valeur):
    global data
    for i in range(len(data)):
        p = data[i]
        r = randint(-1, 1) * 255
        pxl = []
        for k in range(0, 3):
            j = int(p[k] + r * (int(valeur) / 100))
            if j > 255:
                pxl.append(255)
            elif j < 0:
                pxl.append(0)
            else:
                pxl.append(j)
        p = (pxl[0], pxl[1], pxl[2])
        data[i] = p


def bruit_C(valeur):
    global data
    for i in range(len(data)):
        p = data[i]
        r = randint(0, 2)
        pxl = [0] * 3
        for k in range(0, 3):
            if k == r:
                j = int(p[k] + 255 * (valeur / 100))
                if j > 255:
                    pxl[k] = 255
                else:
                    pxl[k] = j
            else:
                j = int(p[k] - 255 * (valeur / 100))
                if j < 0:
                    pxl[k] = 0
                else:
                    pxl[k] = j
        p = (pxl[0], pxl[1], pxl[2])
        data[i] = p


def essai():
    global vartest
    if vartest ==1:
        global Canevas
        global img
        global photo
        Canevas.delete(ALL)
        img=Image.open('tmp.png')
        photo = ImageTk.PhotoImage(file='tmp.png')   
        Canevas.create_image(0,0,anchor=NW,image=photo)
        data = list(img.getdata())

        Canevas.pack(side=BOTTOM)
    else:
       print('pas possible')

vartest=0
img = None
Mafenetre = Tk()   
text1 = Label(Mafenetre,text='Manipulationdes photos', fg='red' )
text1.pack()   

bou1 = Button(Mafenetre,text='Quitter', command=Mafenetre.destroy)
bou1.pack(side=BOTTOM, padx=3, pady=3) 

bou2 = Button(Mafenetre,text='Seuil', command=seuil)
bou2.pack(side=BOTTOM, padx=3, pady=3) 
  
bou3 = Button(Mafenetre,text='N&B', command=noir_blanc)
bou3.pack()

bou4 = Button(Mafenetre,text='Negatif', command=negatif)
bou4.pack()

bou5 = Button(Mafenetre,text='sauvegarde', command=enregistrer_img)
bou5.pack()

Mafenetre.title("Image")                                  # Titre de la fenetre

Canevas = Canvas(Mafenetre)              

filename = tkinter.filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('jpg files','.jpg'),('bmp files','.bmp'),('all files','.*')]) 
img = Image.open(filename)
data = list(img.getdata())
photo = ImageTk.PhotoImage(file=filename)

# sauvegarde une copie de la photo originale
img.putdata(data)
img.save("sauv_tmp.png", "PNG")

Canevas.config(height=photo.height()+30,width=photo.width()+30)  # Règle la taille du canvas par rapport à la taille de l'image 
Canevas.create_image(0,0,anchor=NW,image=photo)
Canevas.pack(side=BOTTOM)
                                            
Mafenetre.mainloop()
