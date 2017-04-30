from random import randint
from tkinter import*
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image, ImageTk  # Attention : conflit de 'Image' dans Tkinter et pillow
import os

img = None
no = -1


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
    global Canevas, fenetre, no
    img = ImageTk.PhotoImage(file="tmp_%ld.png" % no)  # travaille avec différents types d'images

    if img.height() > fenetre.winfo_screenheight() or img.width() > fenetre.winfo_screenwidth():
        tmp_img = Image.open("tmp_%ld.png" % no)
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
    global no
    no += 1
    img.putdata(data)
    img.save("tmp_%ld.png" % no, "PNG")
    suppr = no - 5
    if suppr < 0:
        return
    else:
        os.remove("tmp_%ld.png" % suppr)


def retours(sens):
    """remplace l'image actuelle par une image temporaire précédente, permettant de revenir sur une modification"""
    # À FAIRE : problème : quand on retourne plusieurs fois en arrière (ex:3)  qu'on modifie un nombre inférieur de
    # fois (ex:1) et qu'on retourne en avant, on retombe sur les images d'avant le premier retour (ex: 5-3+2 = 5 => on
    # retourne sur l'image qu'on avait avant le premier retour)
    # À FAIRE (aussi) : trouver un moyen de supprimer toutes les images temporaires quand on a finit
    global img, data, no
    no = no + sens
    if no < 0:
        return
    try:
        img = Image.open("tmp_%ld.png" % no)
        data = list(img.getdata())
        afficher_img()
    except:
        no = no - sens


def appliquer_filtre(filtre, *val):
    """applique le filrte spécifié puis enregistre et affiche l'image"""
    if img is None:
        return
    effacer()
    # chargement(début)
    # print('val = ', val)
    filtre(*val)
    enregistrer_img()
    # chargement(fin)
    afficher_img()


def defvaleur(filtre, val):
    """demande à l'utilisateur de spécifier une valeur pour un filtre"""
    curseur = Tk()
    curseur.title("definition d'une valeur")

    def sortie():
        curseur.destroy()
        print('valeur = ', tmp_val)
        appliquer_filtre(filtre, tmp_val)

    def tmp(val):
        global tmp_val
        tmp_val = int(val)

    if val == 1:
        defval = (0, 100)
    elif val == 0:
        defval = (-100, 100)
    echelle = Scale(curseur, from_=defval[0], to=defval[1], resolution=1, orient=HORIZONTAL, length=300, width=20,
                    label="valeur du filtre", tickinterval=100, variable=val, command=tmp)
    echelle.pack(padx=10, pady=10)
    btn = Button(curseur, text='Ok', command=sortie)
    btn.pack(pady=10)
    curseur.mainloop()


def chargement(arg):
    """affiche un écran de chargement pendant que le filtre se met en place"""
    ## À FAIRE : faire
    pass


def effacer():
    """Permet d'effacer l'image qui est affichée"""
    global Canevas
    Canevas.delete(ALL)

###############
##  Filtres  ##
###############


def noir_blanc():
    global data
    # print('les crêpes')
    for i in range(len(data)):
        p = data[i]
        r = int((p[0] + p[1] + p[2]) / 3)
        data[i] = (r, r, r)


def negatif():
    global data
    for i in range(len(data)):
        p = data[i]
        data[i] = (255 - p[0], 255 - p[1], 255 - p[2])


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
        data[i] = (pxl[0], pxl[1], pxl[2])



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
        data[i] = (pxl[0], pxl[1], pxl[2])


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
menufichier.add_command(label="Effacer", command=effacer)
menubar.add_cascade(label="Fichier", menu=menufichier)

# menu filtres :
menufiltres = Menu(menubar, tearoff=0)
menufiltres.add_command(label="Noir & blanc", command=lambda: appliquer_filtre(noir_blanc))
menufiltres.add_command(label="Negatif", command=lambda: appliquer_filtre(negatif))
menufiltres.add_command(label="Seuil", command=lambda: appliquer_filtre(seuil))
menufiltres.add_command(label="Bruit de chrominance", command=lambda: defvaleur(bruit_C, 1))
menufiltres.add_command(label="Bruit de luminance", command=lambda: defvaleur(bruit_L, 1))
menubar.add_cascade(label="Filtres", menu=menufiltres)

# menu Édition :
menuedition = Menu(menubar, tearoff=0)
menuedition.add_command(label="Retour arrière", command=lambda: retours(-1))
menuedition.add_command(label="Refaire", command=lambda: retours(1))
menubar.add_cascade(label="Édition", menu=menuedition)

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
