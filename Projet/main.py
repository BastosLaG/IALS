# Import tkinter in the notebook
from tkinter import *
from tkinter.filedialog import *

win = Tk()

win.title('Gestionnaire de mot de passe')
# Set the Geometry
win.geometry("800x200")
win.resizable(0,0)



label = Label(win, text="Hello World")
nomDeDomaine = Entry()

def affichage():
   label.pack()
   nomDeDomaine.pack()


affichage()
win.mainloop()
# print("Python Version Info:", sys.version_info)
