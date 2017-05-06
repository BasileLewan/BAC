import random
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image, ImageTk
import os
import time


global vartest, effets, bruit


# ==================== DEF==================================

def aff_effet(vartest,eff):
    global effets
    if vartest>=0:
        if vartest> len(effets):
            effets.append(eff)
        else:
            temp=len(effets)
            effets [temp-1:]=[]
        mess= str(effets)
        trace_effet(mess)  # permet de visualiser les effets mis en place       

def aPropos():
    tkinter.messagebox.showinfo("A propos","Théo et Basile")


def change_img(eff):
    """permet de créer l' image temporaire à partir d'une modification"""
    global data, vartest,Canevas,img,photo,effets 
    img.putdata(data)
    vartest= vartest+1
    nom_fic= "tmp" + str(vartest) + ".png"    
    img.save(nom_fic, "PNG")    
    img=Image.open(nom_fic)
    data = list(img.getdata())   
    Canevas.delete(ALL)
    photo = ImageTk.PhotoImage(file= nom_fic)   
    Canevas.create_image(0,0,anchor=NW,image=photo)
    aff_effet(vartest,eff)
     

def clic(event):   #   voir si on le garde
    """ Gestion de l'événement Clic gauche sur la zone graphique """
    global data, photo
    # position du pointeur de la souris
    X = event.x
    Y = event.y
    print(X,Y)
    height_1=photo.height()
    width_1=photo.width()        
    p = data[Y*width_1+ X]
    print(p[0],p[1],p[2])


def enregistrer_img():
    """créer une image temporaire à partir des modifications"""
    global vartest,Canevas,img, data
    if vartest>=0:      
        img.putdata(data)
        img.save("tmp_final.png", "PNG")
 

def ouvrir():
    global data, photo, img, Canevas, Mafenetre, vartest, effets 
    filename = tkinter.filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('jpg files','.jpg'),('bmp files','.bmp'),('all files','.*')]) 
    if filename:       
      
        statinfo= os.stat(filename)    # récupère taille du fichier
        taille =round(statinfo.st_size/1024)  # conversion en Ko
        descr= str(taille) + " ko"    # prépare le message à afficher
        Texte3.set('taille : ' + descr)  # affichage dans le label
        Texte2.set('Patience....' ) # affichage dans le label       
                    
        Mafenetre.update_idletasks()  # mise à jour de l'affichage      
        # rajouter   test taille et message sur la taille ex si > 1000 000
        
        debut=time.time()  # timestamp heure
        print("debut",debut)              
        img = Image.open(filename)
               
        print(img.format, img.size, img.mode)  #  info sur img        
       
        print("après ouverture",time.time())
        data=list(img.getdata())  
        print("après data",time.time())        
        vartest=0 # permet de savoir qu'une image est chargée
        photo = ImageTk.PhotoImage(file=filename)   
        img.putdata(data)
        print("après img put data",time.time())           
        img.save("tmp0.png", "PNG")  # sauvegarde une copie de l'image chargée
        print("après sauvegarde" ,time.time())
        # récupère la définition de l'écran de l'ordinateur
        ecran_W= Mafenetre.winfo_screenwidth()
        ecran_H= Mafenetre.winfo_screenheight()
        print("ecran W", ecran_W)
        print("ecran H", ecran_H)       
        
        # on crée une fenêtre au max égale à (width écran -100) et (height écran -200)
        h1= photo.height()
        print('photo height =',h1)
        h=min(h1,ecran_H-300)
        print("h=",h)
        
        w1=photo.width() 
        print('photo width=',w1)                     
        w=min(w1,ecran_W-200)
        print("w=",w)       
        Canevas = Canvas(Mafenetre)
        
        taille_ecran= str(w+150)+"x"+str(h+150)+ "+20+10"  # modifie la géométrie de la fenêtre
        Mafenetre.geometry(taille_ecran)
        Mafenetre.update()
        print(Mafenetre.geometry()) 

        # détermine si on fair un scroll
        
        
        # Règle la taille du canvas par rapport à la taille de l'image 
        Canevas.config(scrollregion=(0,0,w1+100,h1+100),height=h,width=w)        
        Canevas.bind('<Button-1>', clic)  # ana sur bouton gauche
        Canevas.pack(side=LEFT)
        
        # scroll vertical
        s1 = Scrollbar(Mafenetre, command=Canevas.yview)
        s1.pack(side=RIGHT, fill=Y)
        Canevas.configure(yscrollcommand=s1.set)
 
        # scroll horizontal
        s2 = Scrollbar(Mafenetre,orient=HORIZONTAL, command=Canevas.xview)
        s2.pack(side=BOTTOM, fill=X)  
        Canevas.configure(xscrollcommand=s2.set)        
        
        description= "height:" + str(h1) + "," + "weight:" + str(w1)
        Texte2.set('photo : ' + description)
        print("avant aff photo", time.time())   
        
        Canevas.create_image(0,0,anchor=NW,image=photo)
        print("apres aff photo", time.time())   




def retour_arr(): 
    """permet de récupérer l' image précédente"""
    global data, vartest,Canevas,img,photo
    if vartest>0:
        vartest= vartest-1        
        nom_fic= "tmp" + str(vartest) + ".png" 
        img=Image.open(nom_fic)
        data = list(img.getdata())
        Canevas.delete(ALL)
        photo = ImageTk.PhotoImage(file=nom_fic)   
        Canevas.create_image(0,0,anchor=NW,image=photo)
        ##Canevas.create_text(50,20,text="hello canvas") # exemple de saisie
        aff_effet(vartest,"")

   
def retrouve_img():
    """permet de récupérerl' image initiale"""
    global data, vartest,Canevas,img,photo,effets
    if vartest>0:   
        img=Image.open('tmp0.png')
        data = list(img.getdata())
        Canevas.delete(ALL)
        photo = ImageTk.PhotoImage(file='tmp0.png')   
        Canevas.create_image(0,0,anchor=NW,image=photo)
        vartest=0
        effets=[]
        trace_effet("")

def trace_effet(effets):    
    Texte.set('effets réalisés -> ' + effets)


#########################################
##  Filtres  ##
#########################################

def bruit_C():
    global bruit
    if vartest>=0: # si au moins une image chargée
        if bruit == "":   
            print("je passe")
            bruit="C"
            bruit_spec()
        
     
def bruit_L():
    global bruit   
    if vartest>=0: # si au moins une image chargée
        if bruit == "": 
            bruit="L" 
            bruit_spec()
        
 
def bruit_spec():
    global s,val 
    s=Spinbox(Mafenetre, from_=0, to= 100, increment=5 )
    s.pack()        
    val = Button(Mafenetre, text="Valider", command=bruit_traite)
    val.pack()   

    
def bruit_traite():
    global choix, s,data, val,bruit
    choix = s.get()
    if bruit=="C":
        valeur1=int(choix)    
        for i in range(len(data)):
            p = data[i]
            r = random.randint(0, 2)
            pxl = [0] * 3
   
            for k in range(0, 3):
                if k == r:
                    j = int(p[k] + 255 * (int(valeur1) / 100))
                    if j > 255:
                        pxl[k] = 255
                    else:
                        pxl[k] = j
                else:
                    j = int(p[k] - 255 * (int(valeur1) / 100))
                    if j < 0:
                        pxl[k] = 0
                    else:
                        
                        pxl[k] = j
            p = (pxl[0], pxl[1], pxl[2])
            data[i] = p       

    if bruit=="L":    
        if vartest>=0:
            valeur1=int(choix)    
            for i in range(len(data)):
                p = data[i]
                r = random.randint(-1, 1) * 255
                pxl = []
                for k in range(0, 3):
                    j = int(p[k] + r * (int(valeur1) / 100))
                    if j > 255:
                        pxl.append(255)
                    elif j < 0:
                        pxl.append(0)
                    else:
                        pxl.append(j)
                p = (pxl[0], pxl[1], pxl[2])
                data[i] = p
    
    if bruit=="C":
        effet="BC"
    else:
        effet="BL"
    voir =" "*3 +choix
    taille=len(voir)
    effet=effet+voir[taille-3:]
    change_img(effet) 
    s.destroy()  # supprime spinbox sur bruit_c
    val.destroy() # supprime bouton "val" sur choix  bruit_c
    bruit=""    
    
def negatif():
    global data
    if vartest>=0:    
        for i in range(len(data)):
            p = data[i]
            p = (255 - p[0], 255 - p[1], 255 - p[2])
            data[i] = p
        change_img("Negat")
    
   
def noir_blanc():
    global data
    print(vartest)
    if vartest>=0:   
        for i in range(len(data)):
            p = data[i]
            r = int((p[0] + p[1] + p[2]) / 3)
            p = (r, r, r)
            data[i] = p
        change_img("Noir_B")


def seuil():
    global data
    if vartest>=0:
        for i in range(len(data)):
            p = data[i]
            r = int((p[0] + p[1] + p[2]) / 3)
            if r < 128:
                data[i] = (0, 0, 0)
            else:
                data[i] = (255, 255, 255)
        change_img("Seuil")
     
     
#=============== PRG ===============================

vartest=-1 # gestion des images, -1 au départ,0 si une photo chargé, N effets
Mafenetre = Tk() 
bruit="" # pour bruit_cet bruit_l
effets=[]  # pour tracer la suite des filtres aplliqués

# Création d'un widget Menu
menubar = Menu(Mafenetre)

menufichier = Menu(menubar,tearoff=0)
menufichier.add_command(label="Ouvrir une image",command=ouvrir)
menufichier.add_separator()
menufichier.add_command(label="Sauvegarder l'image",command=enregistrer_img)

menufichier.add_command(label="Réinitialise l'image",command=retrouve_img)
menufichier.add_separator()
menufichier.add_command(label="Quitter",command=Mafenetre.destroy)
menubar.add_cascade(label="Fichier", menu=menufichier)

menuEffet = Menu(menubar,tearoff=0)
menuEffet.add_command(label="Bruit_C",command=bruit_C)
menuEffet.add_command(label="Bruit_L",command=bruit_L)
menuEffet.add_command(label="Negatif",command=negatif)
menuEffet.add_command(label="N&B",command=noir_blanc)
menuEffet.add_command(label="Seuil",command=seuil)
menubar.add_cascade(label="Effet", menu=menuEffet)

menuDivers = Menu(menubar,tearoff=0)
menuDivers.add_command(label="A propos",command=aPropos)
menubar.add_cascade(label="Divers", menu=menuDivers)

# Affichage du menu
Mafenetre.config(menu=menubar)
text1 = Label(Mafenetre,text='Manipulation des photos', fg='red' )
text1.pack() 

Mafenetre.title("Photo_manip")    # Titre de la fenetre
bou1 = Button(Mafenetre,text='Retour Arr', command=retour_arr)
bou1.pack(side=TOP, padx=3, pady=3) 

# pour visualiser les effets

Texte3 = StringVar()
# LabelRes3 = Label(Mafenetre, textvariable = Texte3, fg ='blue', bg= 'white')
LabelRes3 = Label(Mafenetre, textvariable = Texte3, fg ='blue')
LabelRes3.pack(side = TOP, padx = 1, pady = 1)

Texte2 = StringVar()
LabelRes2 = Label(Mafenetre, textvariable = Texte2, fg ='red')
LabelRes2.pack(side = TOP, padx = 1, pady = 1)

Texte = StringVar()
LabelResultat = Label(Mafenetre, textvariable = Texte, fg ='green')
LabelResultat.pack(side = TOP, padx = 1, pady = 1)
 
Mafenetre.geometry('500x300+20+10')  # 500 p large par 300 H  positionnée en (20, 10) sur l'écran.      #                            
Mafenetre.resizable(width=True, height=True)
Mafenetre.mainloop()
