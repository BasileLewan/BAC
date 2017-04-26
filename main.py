from random import randint
from tkinter import*
from PIL import Image, ImageTk  # Attention : conflit de 'Image' dans Tkinter et pillow
import tkinter.messagebox
import tkinter.filedialog
# import os

img = None

######################
## Autres fonctions ##
######################


def ouvrir_img():
    """Choisir une image et céer sa liste de pixels"""
    global data, img
    # img = Image.open('gdtst.jpg')
    # img = Image.open('tst.png')
    filename = tkinter.filedialog.askopenfilename(title="Ouvrir une image",
                                                  filetypes=[('jpg files', '.jpg'),
                                                             ('bmp files', '.bmp'),
                                                             ('png files', '.png'),
                                                             ('all files', '.*')])  # ouverture de l'image
    img = Image.open(filename)
    data = list(img.getdata())


    """ Sans PIL :
    img = open("tst.pbm")
    type = img.readline()
    ln = img.readline()
    lg = img.readline()
    format = img.readline()
    if (type != "P6") or (format != "255"):
        print("mauvais format d'image")
    data = []
    for i in range(int(ln) * int(lg)):
        tmp_data = img.readline()
        tmp = (tmp_data[0:2], tmp_data[4:6], tmp_data[8:10])
        data.append(tmp)
    """
    enregistrer_img()
    afficher_img()


def afficher_img():
    """aficher l'image dans la fenêtre"""
    global Canevas, fenetre
    img = ImageTk.PhotoImage(file='tmp.png')  # travaille avec différents types d'images
    tmp_img = Image.open('tmp.png')
    if img.height() > fenetre.winfo_screenheight() or img.width() > fenetre.winfo_screenwidth():
        if img.width() > img.height():
            definition = (fenetre.winfo_screenwidth(), int(img.height() * (fenetre.winfo_screenwidth() / img.width())))
            img = ImageTk.PhotoImage(tmp_img.resize(definition))
        else:
            definition = (int(img.width() * (fenetre.winfo_screenheight() / img.height())), fenetre.winfo_screenheight())
            img = ImageTk.PhotoImage(tmp_img.resize(definition))
    else:
        pass
    Canevas.config(height=img.height(), width=img.width())  # taille du canvas par rapport à la taille de l'image
    Canevas.create_image(0, 0, anchor=NW, image=img)
    Canevas.pack()
    fenetre.mainloop()


def enregistrer_img():
    """créer une image temporaire à partir des modifications"""
    ## À FAIRE : retours en arrière/avant
    img.putdata(data)
    img.save("tmp.png", "PNG")


def appliquer_filtre(filtre, *arg):
    """applique le filrte spécifié puis enregistre et affiche l'image"""
    global img

    if img is None:
        return
    else:
        # chargement(début)
        filtre(*arg)
        enregistrer_img()
        # chargement(fin)
        afficher_img()


def chargement(arg):
    """affiche un écrazn de chargement pendant que le filtre se met en place"""
    ## À FAIRE : faire
    pass


###############
##  Filtres  ##
###############

def noir_blanc():
    global data
    print('les crêpes')
    for i in range(len(data)):
        p = data[i]
        r = int((p[0] + p[1] + p[2]) / 3)
        p = (r, r, r)
        data[i] = p


def negatif():
    global data
    for i in range(len(data)):
        p = data[i]
        p = (255 - p[0], 255 - p[1], 255 - p[2])
        data[i] = p


def seuil():
    global data
    for i in range(len(data)):
        p = data[i]
        r = int((p[0] + p[1] + p[2]) / 3)
        if r < 128:
            data[i] = (0, 0, 0)
        else:
            data[i] = (255, 255, 255)


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

##############
## Fenêtre  ##
##############

fenetre = Tk()
fenetre.title("gros logiciel samer")                                  # Titre de la fenetre
Canevas = Canvas(fenetre)

## création du menu :
menubar = Menu(fenetre)
fenetre.config(menu=menubar)

# menu fichier :
menufichier = Menu(menubar, tearoff=0)
menufichier.add_command(label="Ouvrir une image", command=ouvrir_img)
menubar.add_cascade(label="Fichier", menu=menufichier)

# menu filtres :
menufiltres = Menu(menubar, tearoff=0)
menufiltres.add_command(label="Noir & blanc", command=lambda: appliquer_filtre(noir_blanc))
menufiltres.add_command(label="Negatif", command=lambda: appliquer_filtre(negatif))
menufiltres.add_command(label="Seuil", command=lambda: appliquer_filtre(seuil))
menufiltres.add_command(label="Bruit de chrominance", command=lambda: appliquer_filtre(bruit_C, 10))
menufiltres.add_command(label="Bruit de luminance", command=lambda: appliquer_filtre(bruit_L, 10))
menubar.add_cascade(label="Filtres", menu=menufiltres)


fenetre.mainloop()

""" tests (ne pas prendre en compte)
valeur = int(input("?"))
bruit_C(valeur)
print(data)
im.putdata(data)
im.save("final.png", "PNG")
im.show()
"""

# os.system("pause")
