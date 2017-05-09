# -*- coding: utf-8 -*-
"""
2017

@author: Théo and basile
"""

from random import randint
from tkinter import*
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image, ImageTk  # Attention : conflit de 'Image' dans Tkinter et pillow
import os
import shutil

global vartest, effets, eff, bruit, val_bruit, fenetre, taille, trace_m, max_E, effets_Back, no # À quoi ça sert ?

####################
# Autres fonctions #
####################


def afficher_img():
    """aficher l'image dans la fenêtre"""

    global Canevas, fenetre, no, s1, s2, trace_m
    img = ImageTk.PhotoImage(file="tmp_%ld.png" % no)  # travaille avec différents types d'images
                           
    # redimensionne l'image affichée selon la taille de l'écran si elle est plus grande           
    ecran_W = fenetre.winfo_screenwidth()
    ecran_H = fenetre.winfo_screenheight()
       
    if (img.height()+250) > ecran_W or (img.width()+250) > ecran_H:         
        tmp_img = Image.open("tmp_%ld.png" % no)               
        if img.width() > img.height():
            definition = (ecran_W-250, int(img.height() * (ecran_W-250) / img.width()))
            img = ImageTk.PhotoImage(tmp_img.resize(definition))
                 
        else:
            definition = (int(img.width() * (ecran_H-250) / img.height()), ecran_H-250)
            img = ImageTk.PhotoImage(tmp_img.resize(definition))      
    else:
        pass    
    effacer()
    
    h1 = img.height()
    h = min(h1, ecran_H-250)
    w1 = img.width()
    w = min(w1, ecran_W-250)

    taille_ecran = str(w+80)+"x"+str(h+80) + "+10+10"  
    fenetre.geometry(taille_ecran)  # modifie la géométrie de la fenêtre
    fenetre.update()
            
    # règle le scrolll       
    if (h+w) < (h1+w1):  # si taille  finale < taille photo
        # Règle la taille du canvas par rapport à la taille de l'image
        Canevas.config(scrollregion=(0, 0, w1, h1), height=h, width=w)
    else:
        Canevas.config(scrollregion=(0, 0, w1, h1), height=h, width=w)
    Canevas.pack(side=LEFT)
 
    Canevas.create_image(0, 0, anchor=NW, image=img)
    Texte2.set('')  # affichage dans le label
 
    fenetre.mainloop()


def aff_effet(vartest, eff, sens_op):
    """permet de gérer l'affichage des effets"""     
    global effets, trace_m, max_E, effets_Back
        
    if vartest >= 0:
        if vartest > len(effets):
            effets.append(eff)
            if sens_op == 1:
                temp = len(effets)
                effets_Back.append(eff)
           
            if sens_op == 4:  # refaire demandé
                temp = len(effets)
                
                effets[vartest-1] = effets_Back[vartest-1]  # mettre -1 à cause e l'indice
                
        else:
            temp = len(effets)
            
            effets[temp-1:] = []
            temp = len(effets)
            
        mess = str(effets)
        
        trace_effet(mess)  # permet de visualiser les effets mis en place 
        

def appliquer_filtre(filtre, *val):
    """applique le filtre spécifié puis enregistre et affiche l'image"""
    global eff, vartest, val_bruit, trace_m, max_E
    if val_bruit == 0:
        if img is None:
            return
        effacer()
        # chargement(début)
        
        chargement2()
        filtre(*val)
        
        
        vartest = vartest+1
        
        max_E = max_E+1
        
        aff_effet(vartest, eff, 1)
        
        enregistrer_img()  # On crée une nouvelle image temporaire pour chaque filtre appliqué
        tmp = str(filtre.__name__) + '({})'.format(str(*val))
        with open('tmp_preset.py', 'a') as f:
            f.write("   {}\n".format(tmp))
        # chargement(fin)
        
        afficher_img()


def aPropos():
    """permet de montrer les créateurs du programme"""   
    tkinter.messagebox.showinfo("A propos", " ce programme a été créé par Théo et Basile, 2017")
    
    
def chargement(arg):
    """affiche un écran de chargement pendant que le filtre se met en place"""
    ## À FAIRE : faire
    pass


def chargement2():
    """affiche un message pendant que le filtre se met en place"""
    global taille, fenetre
    if taille < 2000:
        Texte2.set('Patience....')  # affichage dans le label
    else:
        Texte2.set('Patience le fichier est gros....')  # affichage dans le label
    fenetre.update_idletasks()  # mise à jour de l'affichage 


def defvaleur(filtre, val):
    """demande à l'utilisateur de spécifier une valeur pour les filtres qui le nécessite"""
    global val_bruit, trace_m
    val_bruit = val_bruit+1
    
    if val_bruit == 1:
        curseur = Tk()
        curseur.title("choix d'une valeur")
    
        def sortie():
            global val_bruit, tmp_val, trace_m
            curseur.destroy()
            val_bruit = 0
            
            appliquer_filtre(filtre, tmp_val)
    
        def tmp(val):
            global tmp_val
            tmp_val = int(val)
    
        # 'val' permet de savoir quelle est l'échelle du curseur
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

                            
def effacer():
    """Permet d'effacer l'image qui est affichée"""
    global Canevas
    Canevas.delete(ALL)


def effacer_2():
    """Permet d'effacer l'image qui est affichée ainsi que labels"""
    global Canevas, vartest, effets, effets_Back, max_E, no

    Canevas.delete(ALL)
    Texte3.set("")  # vide le label         
    Texte2.set("")  # vide le label   
    Texte.set("")  # vide le label 
    fenetre.update_idletasks()  # mise à jour de l'affichage 
   
    vartest = 0
    effets = []
    effets_back = []  # À quoi ça sert ?
    max_E = 0
    no = -1
    Texte.set("")         
                         

def enregistrer_img():
    """crée une nouvelle image temporaire à partir des modifications"""
    global no
    no += 1
    img.putdata(data)
    img.save("tmp_%ld.png" % no, "PNG")
    # On ne conserve que les 5 dernières images temporaires :
    suppr = no - 5
    if suppr < 0:
        return
    else:
        os.remove("tmp_%ld.png" % suppr)


def export_preset():
    """Permet d'exporter la suite de filtres appliqués comme un fichier de preset"""
    place = tkinter.filedialog.asksaveasfilename(title="Enregistrer sous...",
                                                       filetypes=[('Python', '.py')],
                                                       defaultextension='py')

    # Évite une erreur si l'utilisateur ne spécifie pas de fichier
    if place:
        pass
    else:
        return
    shutil.copyfile('preset.py', place)


def exporter():
    """permet à l'utilisateur de sauvegarder l'image sous la forme qui lui convient"""
    global emplacement, img, type
    emplacement = tkinter.filedialog.asksaveasfilename(title="Enregistrer sous...",
                                                       filetypes=[('jpg files', '.jpg'),
                                                                  ('bmp files', '.bmp'),
                                                                  ('png files', '.png')],
                                                       defaultextension='png')
    # bug (qui vient de tkinter) : si l'utilisateur selectionne un format (ex:jpg) et écrase une image d'un autre format
    # (ex:png) alors l'extension est celle du fichier écrasé (ex:png)

    # Évite une erreur si l'utilisateur ne spécifie pas de fichier
    if emplacement:
        pass
    else:
        return

    if img is None:
        return
    type = emplacement[-3] + emplacement[-2] + emplacement[-1]
    img.save(emplacement, type)


def exporter2():  # c'est quoi la différence par rapport à l'autre Exporter() ?
    """créer une image temporaire à partir des modifications"""
    global vartest, Canevas, img, data
    if vartest >= 0:
        img.putdata(data)	
        choixF = tkinter.filedialog.asksaveasfilename(title="Enregister cette image",
                                                      filetypes=[('PNG files', '.png')], defaultextension='.jpg')
        if choixF:
            img.save(choixF, "PNG")       


def ouvrir_img():
    """Choisir une image et céer sa liste de pixels"""
    global data, img, filename, vartest, taille, trace_m, effets, effets_Back, max_E, no
    # global data, img,filename, vartest,s1,s2, scroll_E

    filename = tkinter.filedialog.askopenfilename(title="Ouvrir une image",
                                                  filetypes=[('jpg files', '.jpg'),
                                                             ('bmp files', '.bmp'),
                                                             ('png files', '.png'),
                                                             ('all files', '.*')])  # ouverture de l'image

    # Évite une erreur si l'utilisateur ne spécifie pas d'image
    if filename:
        pass
    else:
        return
        
    vartest = 0
    effets = []
    effets_back = []
    max_E = 0
    no = -1
    Texte.set("")
    
    img = Image.open(filename)
    
    mess = "Format:" + str(img.format) + ",taille:"+str(img.size) + ",mode:" + str(img.mode)
    
    Texte3.set(mess)  # affichage dans le label      
    fenetre.update_idletasks()  # mise à jour de l'affichage 
 
    statinfo = os.stat(filename)    # récupère taille du fichier
    taille = round(statinfo.st_size/1024)  # conversion en Ko
    descr = str(taille) + " ko"    # prépare le message à afficher
    mess2 = mess + ", Taille photo : "+descr
    Texte3.set(mess2)  # affichage dans le label
    if taille < 2000:
        Texte2.set('Patience....')  # affichage dans le label
    else:
        Texte2.set('Patience le fichier est gros....')  # affichage dans le label
    
    
    fenetre.update_idletasks()  # mise à jour de l'affichage 
                                                   
    data = list(img.getdata())
    enregistrer_img()
    afficher_img()              


def preset():
    """Execute un fichier de préreglages"""
    filename = tkinter.filedialog.askopenfilename(title="Ouvrir un fichier de préreglages",
                                                  filetypes=[('fichier presets', '.py'),
                                                             ('all files', '.*')])
    # Évite une erreur si l'utilisateur ne spécifie pas de fichier
    if filename:
        pass
    else:
        return
    shutil.copyfile(filename, "tempreset.py")
    from tempreset import liste
    # chrg
    liste()
    enregistrer_img()
    # chrg
    afficher_img()


def retours(sens):
    """remplace l'image actuelle par une image temporaire précédente, permettant de revenir sur une modification"""
    # À FAIRE : problème : quand on retourne plusieurs fois en arrière (ex:3)  qu'on modifie un nombre inférieur de
    # fois (ex:1) et qu'on retourne en avant, on retombe sur les images d'avant le premier retour (ex: 5-3+2 = 5 => on
    # retourne sur l'image qu'on avait avant le premier retour)
    # À FAIRE (aussi) : trouver un moyen de supprimer toutes les images temporaires quand on a finit
    global img, data, no, vartest, trace_m, max_E
    
        
    possible = 1
    if sens > 0:
        if vartest == max_E:
            possible = 0
  
    if sens < 0:
        if vartest == 0:
            possible = 0
    
    if possible == 1:
            
        no = no + sens
        
        if no < 0:
            return
        try:
            img = Image.open("tmp_%ld.png" % no)
        except:
            no = no - sens
            
        
        vartest = vartest + sens
        
        if sens < 0:
            aff_effet(vartest, "", 3)  # retour arr
        else:
            aff_effet(vartest, "", 4)  # refaire
                 
        chargement2()
        data = list(img.getdata())
        afficher_img()         


def sauve():
    """ Enregistre l'image à l'emplacement précédent"""
    global emplacement, type
    # renvoie à la définition d'un emplacement de sauvegarde si le précedent n'existe pas
    if emplacement:
        pass
    else:
        exporter()
        return
    img.save(emplacement, type)


def trace_effet(effets):
    """permet de tracer l'effet"""    
    Texte.set('effets réalisés -> ' + effets)
    

#############
#  Filtres  #
#############


def bruit_C(valeur):
    global data, eff, tmp_val
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
    eff = "BC"+str(valeur)
    tmp_val = 0
    
 
def bruit_L(valeur):
    global data, eff, tmp_val
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
    eff = "BL" + str(valeur)
    tmp_val = 0

  
def negatif():
    global data, eff
    for i in range(len(data)):
        p = data[i]
        data[i] = (255 - p[0], 255 - p[1], 255 - p[2])
    eff = "Negat"

    
def noir_blanc():
    global data, eff
    for i in range(len(data)):
        p = data[i]
        r = int((p[0] + p[1] + p[2]) / 3)
        data[i] = (r, r, r)
    eff = "Noir_B"


def seuil():
    global data, eff
    for i in range(len(data)):
        p = data[i]
        r = int((p[0] + p[1] + p[2]) / 3)
        if r < 128:
            data[i] = (0, 0, 0)
        else:
            data[i] = (255, 255, 255)
    eff = "Seuil"


###################
# Initialisation  #
###################

effets=[]  # pour tracer la suite des filtres appliqués à afficher
effets_Back=[] # pour tracer la suite des filtres appliqués

eff=""
img = None
no = -1  # correspond au numéro qui sera affecté à chaque image temporaire
vartest=-1 # gestion des images, -1 au départ,0 si une photo chargé, N effets
bruit="" # pour bruit_cet bruit_l
val_bruit=0
trace_m=2   #  pour tracer selon mes besoins
max_E=0

with open('preset.py', 'w') as f:
    f.write('from main import noir_blanc, negatif, seuil, bruit_L, bruit_C\n')
    f.write('def liste():\n')

##############
## Fenêtre  ##
##############

fenetre = Tk()
fenetre.title("modif photos")    # Titre de la fenetre
         
Canevas = Canvas(fenetre) 

# création du menu :
menubar = Menu(fenetre)
fenetre.config(menu=menubar)

# menu fichier :
menufichier = Menu(menubar, tearoff=0)
menufichier.add_command(label="Ouvrir une image", command=ouvrir_img)
menufichier.add_separator()
menufichier.add_command(label="Enregistrer sous", command=exporter2)
menufichier.add_command(label="Enregistrer", command=sauve)
menufichier.add_separator()
menufichier.add_command(label="Effacer", command=effacer_2)
menufichier.add_separator()
menufichier.add_command(label="Quitter", command=fenetre.destroy)
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
menuedition.add_command(label="Importer des préreglages", command=preset)
menuedition.add_command(label="Exporter les préreglages", command=export_preset)
menubar.add_cascade(label="Édition", menu=menuedition)

menuDivers = Menu(menubar, tearoff=0)
menuDivers.add_command(label="A propos", command=aPropos)
menubar.add_cascade(label="Divers", menu=menuDivers)

Texte3 = StringVar()
# LabelRes3 = Label(Mafenetre, textvariable = Texte3, fg ='blue', bg= 'white')
LabelRes3 = Label(fenetre, textvariable=Texte3, fg='blue', font=("Helvetica", 10))
LabelRes3.pack(side=TOP, padx=1, pady=1)
Texte2 = StringVar()
LabelRes2 = Label(fenetre, textvariable=Texte2, fg='red', font=("Helvetica", 10))
LabelRes2.pack(side=TOP, padx=1, pady=1)

Texte = StringVar()
LabelResultat = Label(fenetre, textvariable=Texte, fg='green', font=("Helvetica", 10))
LabelResultat.pack(side=TOP, padx=1, pady=1)


fenetre.geometry('600x300+20+10')  # 600 p large par 300 H  positionnée en (20, 10) sur l'écran.      #  

Canevas.config(scrollregion=(0, 0, 600, 300), width=600, height=300)
# scroll vertical
s1 = Scrollbar(fenetre, command=Canevas.yview)
s1.pack(side=RIGHT, fill=Y)
Canevas.configure(yscrollcommand=s1.set)
# scroll horizontal
s2 = Scrollbar(fenetre, orient=HORIZONTAL, command=Canevas.xview)
s2.pack(side=BOTTOM, fill=X)  
Canevas.configure(xscrollcommand=s2.set)

fenetre.mainloop()
