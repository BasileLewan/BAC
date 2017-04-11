from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image, ImageTk


Mafenetre = Tk()                
Mafenetre.title("Image")                                  # Titre de la fenetre

Canevas = Canvas(Mafenetre)              

filename = tkinter.filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('jpg files','.jpg'),('bmp files','.bmp'),('all files','.*')]) 


photo = ImageTk.PhotoImage(file=filename)                  # travaille avec différents types d'images

Canevas.config(height=photo.height(),width=photo.width())  # Règle la taille du canvas par rapport à la taille de l'image 
Canevas.create_image(0,0,anchor=NW,image=photo)            
Canevas.pack()                                              

Mafenetre.mainloop()
