from tkinter import *
from tkinter.filedialog import *

win = Tk()
win.title('Gestionnaire de mot de passe')
win.geometry("800x150")
# win.resizable(0,0)


val = False


def remove_all_widgets():
    for widget in win.winfo_children():
        widget.grid_forget()

def touche_entrer(event):
   valide_action()

def valide_action():
   with open("data.txt", "a") as f:
      f.write(siteWeb.get().upper() + " " + identifiant.get().upper() + " " + motDePasse.get() + " \n")
   siteWeb.delete(0, END)
   identifiant.delete(0, END)
   motDePasse.delete(0, END)

def valide_enter(event):
   if val == True:
      valide_action()
   else: 
      print("T con ou quoi ?")

def affichage_mdp():
   global val 
   val = False
   remove_all_widgets()
   data = []
   i = 0
   j = 1
   with open("data.txt") as f:
      contenants = f.readlines()
      for line in contenants:
         contenant = line.split()
         data.append(contenant)
   for line in data:
      Label(win, text=str(i)).grid(row=i, column=0)
      for col in line:
         Label(win, text=col).grid(row=i, column=j)
         j += 1
      i += 1
      j = 1   
            
def affichage_add():
   global val
   val = True
   remove_all_widgets()
   identif.grid(row=0, column=0)
   identifiant.grid(row=0, column=1)
   mot_de_passe.grid(row=1, column=0)
   motDePasse.grid(row=1, column=1)
   site_web.grid(row=2, column=0)
   siteWeb.grid(row=2, column=1)
   valider.grid(row=3, column=1, columnspan=1)

valider = Button(text="Valider", command=valide_action)

identif = Label(win, text="Identifiant", bd=2)
identifiant = Entry(bd=5)
mot_de_passe = Label(win, text="Mot de passe", bd=2)
motDePasse = Entry(bd=5, show="*")
site_web = Label(win, text="Site web", bd=2)
siteWeb = Entry(bd=5)
listbox = Listbox(win)
win.bind("<Return>", valide_enter)


mainMenu = Menu(win)
mainMenu.add_command(label="Mes mots de passes", command=affichage_mdp)  
mainMenu.add_command(label="Ajouter un mot de passe", command=affichage_add)
mainMenu.add_command(label="Supprimer un mot de passe")




win.config(menu=mainMenu)
win.mainloop()