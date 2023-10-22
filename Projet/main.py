from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *

win = Tk()
win.title('Gestionnaire de mot de passe')
win.geometry("800x150")
# win.resizable(0,0)

# retire tout les widgets
def remove_all_widgets():
    for widget in win.winfo_children():
        widget.grid_forget()

# affichage pour la création d'un compte
def create_id():
   global val_inscription, val_connexion
   val_inscription = True
   val_connexion = False
   
   remove_all_widgets()
   id_print("Veuillez vous inscrire")

# affichage pour la création de la connexion a un compte
def connexion_id():
   global val_connexion, val_inscription
   val_connexion = True
   val_inscription = False
   
   remove_all_widgets()
   id_print("Veuillez vous connecter")
   
   
def id_print(text):
   Label(win, text=text).grid(row=0, column=0, columnspan=2, sticky=EW)
   identif.grid(row=1, column=0)
   identifiant.grid(row=1, column=1)
   mot_de_passe.grid(row=2, column=0)
   motDePasse.grid(row=2, column=1)
   valider.grid(row=3, column=1, columnspan=1, sticky=EW)




# affichage pour connexion a ces mdp a lui 
def affichage_mdp_perso():
   global id, mdp_id 
   remove_all_widgets()
   data = []
   i = 1
   j = 1
   if id and mdp_id != "":
      Label(win, text="Site").grid(row=0, column=1, padx = 100, pady= 5, sticky = W)
      Label(win, text="Identifiant").grid(row=0, column=2, padx = 100, pady= 5, sticky = W)
      Label(win, text="Mot de passe").grid(row=0, column=3, padx = 100, pady= 5, sticky = W)
      with open("data.txt") as f:
         contenants = f.readlines()
         for line in contenants:
            contenant = line.split()
            data.append(contenant)
         # print(data)
      for line in data:
         temp = line[:2]
         line = line[2:]
         if temp[0] == id and temp[1] == mdp_id:   
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

def affichage_sup():
   global val, id, mdp_id
   val = True
   remove_all_widgets()
   Label(win, text="Veuillez choisir le numéro \nde la ligne à supprimer").grid(row=0, column=0, sticky = W)
   data1 = []
   data2 = []
   with open("data.txt") as f:
      contenants = f.readlines()
      for line in contenants:
         contenant = line.split()
         data1.append(contenant)
   for line in data1:
      temp = line[:2]
      line2 = line[2:]
      if temp[0] == id and temp[1] == mdp_id:   
         data2.append(line2)
   
   listSup['values'] = data2
   listSup.grid(row= 0, column= 1, padx=15)
   valider.grid(row=1, column=1, columnspan=1)



# rempli de nouveau id data.txt
def valide_action_data():
   global id, mdp_id, val
   # crypter MDP.get
   
   with open("data.txt", "a") as f:
      f.write(id + " " + mdp_id + " " +  siteWeb.get().upper() + " " + identifiant.get().upper() + " " + motDePasse.get() + " \n")
   siteWeb.delete(0, END)
   identifiant.delete(0, END)
   motDePasse.delete(0, END)



# se connecte
def valide_action_connexion():
   global id, mdp_id, val_connexion
   data = []
   # check si pas déjà créer
   with open("compte.txt") as f:
      contenants = f.readlines()
      for line in contenants:
         contenant = line.split()
         data.append(contenant)
   for elem in data:
      
      # decrypter nos elements 
      
      # si condition vrai alors log la personne
      if elem[0] == identifiant.get().upper() and elem[1] == motDePasse.get():
         val_connexion = False
         id = identifiant.get().upper()
         mdp_id = motDePasse.get()
         
         # Crypter nos données
         
         remove_all_widgets()
         siteWeb.delete(0, END)
         identifiant.delete(0, END)
         motDePasse.delete(0, END)
         mainMenu.delete(0, END)
         mainMenu.add_command(label="Mes MDP", command=affichage_mdp_perso)  
         mainMenu.add_command(label="Ajouter MDP", command=affichage_add)
         mainMenu.add_command(label="Supprimer MDP",command=affichage_sup)
         return
   # idantifiant ou mdp incorrect
   Label(win, 
         text="Identifiant ou mot de passe incorrect",
         fg="#ff0000").grid(row=0, column=2, rowspan=2, sticky=EW)
   identifiant.delete(0, END)
   motDePasse.delete(0, END)

# s'inscrit
def valide_action_inscription():
   global id, mdp_id, val_inscription
   data = []
   # check si pas déjà créer
   with open("compte.txt") as f:
      contenants = f.readlines()
      for line in contenants:
         contenant = line.split()
         data.append(contenant)
   for elem in data:
      # si condition vrai alors log la personne
      if elem[0] == identifiant.get().upper() or elem[1] == motDePasse.get():
         Label(win, 
               text="Identifiant ou mot de passe déjà utiliser par un autre utilisateur",
               fg="#ff0000").grid(row=0, column=2, rowspan=2, sticky=EW)
         return
   # idantifiant ou mdp incorrect
   val_inscription = False
   id = identifiant.get().upper()
   mdp_id = motDePasse.get()
   
   # ajouter notre fonction de cryptage de mdp 
   
   with open("compte.txt", "a") as f:
      f.write(identifiant.get().upper() + " " + motDePasse.get() + " \n")
   remove_all_widgets()
   siteWeb.delete(0, END)
   identifiant.delete(0, END)
   motDePasse.delete(0, END)
   mainMenu.delete(0, END)
   mainMenu.add_command(label="Mes MDP", command=affichage_mdp_perso)  
   mainMenu.add_command(label="Ajouter MDP", command=affichage_add)
   mainMenu.add_command(label="Supprimer MDP", command=affichage_sup)




# condition pour que la touche return fonctionne correctement
def valide_enter1(event):
   if val == True and siteWeb.get() != "" and identifiant.get() != "" and motDePasse.get() != "":
      return valide_action_data()
   if val_connexion == True and identifiant.get() != "" and motDePasse.get() != "":
      return valide_action_connexion()
   if val_inscription == True and identifiant.get() != "" and motDePasse.get() != "":
      return valide_action_inscription()
# condition pour que le Button fonctionne correctement
def valide_enter2():
   if val == True and siteWeb.get() != "" and identifiant.get() != "" and motDePasse.get() != "":
      return valide_action_data()
   if val_connexion == True and identifiant.get() != "" and motDePasse.get() != "":
      return valide_action_connexion()
   if val_inscription == True and identifiant.get() != "" and motDePasse.get() != "":
      return valide_action_inscription()





# val -> validate button
val = False
val_connexion = False
val_inscription = False

# id && mdp_id == compte log 
id = ""
mdp_id = ""

win.bind("<Return>", valide_enter1)
valider = Button(text="Valider", command=valide_enter2)

identif = Label(win, text="Identifiant", bd=2)
identifiant = Entry(bd=5)

mot_de_passe = Label(win, text="Mot de passe", bd=2)
motDePasse = Entry(bd=5, show="*")

site_web = Label(win, text="Site web", bd=2)
siteWeb = Entry(bd=5)

listSup = ttk.Combobox(win, width=50)

listbox = Listbox(win)

# header
mainMenu = Menu(win)
mainMenu.add_command(label="Créer compte", command=create_id)
mainMenu.add_command(label="Connexion compte", command=connexion_id)

win.config(menu=mainMenu)

connexion_id()

win.mainloop()