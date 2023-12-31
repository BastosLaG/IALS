from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from cryptography.fernet import Fernet
import hashlib
import os

win = Tk()
win.title('Gestionnaire de mot de passe')
# win.geometry("800x150")
# win.resizable(0,0)

# Pack a big frame so, it behaves like the window background
big_frame = ttk.Frame(win)
big_frame.grid(padx=800, pady=400)

# Set the initial theme
win.tk.call("source", "azure.tcl")
win.tk.call("set_theme", "light")

hash_mdp = hashlib.sha256()

# retire tout les widgets
def remove_all_widgets():
   for widget in win.winfo_children():
      widget.grid_forget()
   tree.delete(*tree.get_children())

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
   change_theme.grid(row=3, column=0)
   valider.grid(row=3, column=1, columnspan=1, sticky=EW)

# affichage pour connexion a ces mdp a lui 
def affichage_mdp_perso():
   global id, mdp_id 
   remove_all_widgets()
   data = []
   i = 1
   if id and mdp_id != "":
      tree.grid(row=10, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")
      scrollbar.grid(row=10, column=3, sticky='ns')
      with open("data.txt", 'r') as file:
         contenants = file.readlines()
         for line in contenants:
            contenant = line.split()
            data.append(contenant)
      # print(data)
      for line in data:
         # print(line)
         temp = line[:2]
         line = line[2:]
         with open('unlock.key', 'rb') as unlock:
            key = unlock.read()
         f = Fernet(key=key)
         if temp[0] == id and temp[1] == mdp_id.decode('utf-8'):   
            # ttk.Label(win, text=str(i)).grid(row=i, column=0)
            tree.insert("", END, iid=i, values=(f.decrypt(line[0].encode('utf-8')).decode('utf-8'),
                                                f.decrypt(line[1].encode('utf-8')).decode('utf-8'), 
                                                f.decrypt(line[2].encode('utf-8')).decode('utf-8')))
            i += 1

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
   change_theme.grid(row=3, column=0)


def affichage_supprimer():
   global val, id, mdp_id, val_supprimer
   val_supprimer = True
   remove_all_widgets()
   Label(win, text="Veuillez choisir le numéro \nde la ligne à supprimer").grid(row=0, column=0, sticky = W)
   change_theme.grid(row=1, column=0)
   data1 = []
   data2 = []
   with open("data.txt") as file:
      contenants = file.readlines()
      for line in contenants:
         contenant = line.split()
         data1.append(contenant)
   for line in data1:
      temp = line[:2]
      line2 = line[2:]
      with open('unlock.key', 'rb') as unlock:
         key = unlock.read()
      f = Fernet(key=key)
      if temp[0] == id and temp[1] == mdp_id.decode('utf-8'):
         # print(line2)
         decrypted_line2 = []
         for elem in line2:
            decrypted_elem = f.decrypt(elem.encode('utf-8')).decode('utf-8')
            decrypted_line2.append(decrypted_elem)
         # print(decrypted_line2)
         data2.append(decrypted_line2)
   listSup['values'] = data2
   listSup.grid(row= 0, column= 1, padx=15)
   valider.grid(row=1, column=1, columnspan=1)


# rempli de nouveau id data.txt
def valide_action_add():
   global id, mdp_id, val
   # crypter MDP.get
   # Récupération de la clé
   with open('unlock.key', 'rb') as unlock:
      key = unlock.read()
   # print(key)
   f = Fernet(key=key)
     
   enc_id_siteweb = f.encrypt(identifiant.get().encode('utf8'))
   enc_site_web = f.encrypt(siteWeb.get().upper().encode('utf8'))
   enc_mdp = f.encrypt(motDePasse.get().encode('utf8'))
   
   with open("data.txt", "ab") as f:
      f.write(id.encode('utf8') + b" " + mdp_id + b" " +  enc_site_web + b" " + enc_id_siteweb + b" " + enc_mdp + b" \n")
   siteWeb.delete(0, END)
   identifiant.delete(0, END)
   motDePasse.delete(0, END)

def valide_supprimer(texte):
   data = []
   res = texte.split()
   res2 = ""
   with open("data.txt", "r") as file:
      contenants = file.readlines()
      for line in contenants:
         contenant = line.split()
         data.append(contenant)
   with open("data.txt", 'w') as file:
      for line in data:
         temp = line[:2]
         line2 = line[2:]
         for elem in line:
            res2 += elem + ' '
         res2 += '\n'
         with open('unlock.key', 'rb') as unlock:
            key = unlock.read()
         f = Fernet(key=key)
         
         if id != temp[0] or mdp_id != temp[1].encode('utf-8') or res[0] != (f.decrypt(line2[0].encode('utf-8')).decode('utf-8')) or res[1] != (f.decrypt(line2[1].encode('utf-8')).decode('utf-8')) or res[2] != (f.decrypt(line2[2].encode('utf-8')).decode('utf-8')):
            file.write(res2)
         res2 = ""
   listSup.delete(0, END)
   return
   

# se connecte
def valide_action_connexion():
   global id, mdp_id, val_connexion
   data = []
   # check si pas déjà créer
   with open("compte.txt", 'rb') as file:
      contenants = file.readlines()
      for line in contenants:
         contenant = line.split()
         data.append(contenant)
   for elem in data:
      
      # Récupération de la clé
      with open('unlock.key', 'rb') as unlock:
         key = unlock.read()
      f = Fernet(key=key)
      
      # si condition vrai alors log la personne
      if elem[0] == identifiant.get().upper() or f.decrypt(elem[1]) == (hashlib.sha256(motDePasse.get().encode('utf-8')).digest()):
         val_connexion = False
         id = identifiant.get().upper()
         mdp_id = elem[1]

         remove_all_widgets()
         siteWeb.delete(0, END)
         identifiant.delete(0, END)
         motDePasse.delete(0, END)
         mainMenu.delete(0, END)
         mainMenu.add_command(label="Mes MDP", command=affichage_mdp_perso)  
         mainMenu.add_command(label="Ajouter MDP", command=affichage_add)
         mainMenu.add_command(label="Supprimer MDP",command=affichage_supprimer)
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
   # Récupération de la clé
   with open('unlock.key', 'rb') as unlock:
      key = unlock.read()
   f = Fernet(key=key)
   
   # check si pas déjà créer
   with open("compte.txt", 'r') as file:
      contenants = file.readlines()
      for line in contenants:
         contenant = line.split()
         data.append(contenant)
   for elem in data:
      # si condition fausse alors log la personne
      if elem[0] == identifiant.get().upper() or elem[1] == f.encrypt((hashlib.sha256(motDePasse.get().encode('utf-8')).digest())):
         Label(win, 
               text="Identifiant ou mot de passe déjà utiliser par un autre utilisateur",
               fg="#ff0000").grid(row=0, column=2, rowspan=2, sticky=EW)
         return
   # idantifiant ou mdp correct
   val_inscription = False
   id = identifiant.get().upper()
   mdp_id = f.encrypt((hashlib.sha256(motDePasse.get().encode('utf-8')).digest()))
   
   with open("compte.txt", "ab") as f:
      f.write(id.encode('utf-8') + b" " + mdp_id + b" \n")

   remove_all_widgets()
   siteWeb.delete(0, END)
   identifiant.delete(0, END)
   motDePasse.delete(0, END)
   mainMenu.delete(0, END)
   mainMenu.add_command(label="Mes MDP", command=affichage_mdp_perso)  
   mainMenu.add_command(label="Ajouter MDP", command=affichage_add)
   mainMenu.add_command(label="Supprimer MDP", command=affichage_supprimer)


# condition pour que la touche return fonctionne correctement
def valide_enter1(event=NONE):
   if val == True and siteWeb.get() != "" and identifiant.get() != "" and motDePasse.get() != "":
      return valide_action_add()
   if val_connexion == True and identifiant.get() != "" and motDePasse.get() != "":
      return valide_action_connexion()
   if val_inscription == True and identifiant.get() != "" and motDePasse.get() != "":
      return valide_action_inscription()
   if val_supprimer == True and listSup.get() != "":
      return valide_supprimer(listSup.get())


def change_theme_enter():
   if win.tk.call("ttk::style", "theme", "use") == "azure-dark":
      win.tk.call("set_theme", "light")
   else:
      win.tk.call("set_theme", "dark")


#open the key
with open('unlock.key', 'rb') as unlock:
     key = unlock.read()
f = Fernet(key=key)

# if os.path.exists('data.enc'):
print("Decodage data.enc")
with open('data.enc', 'rb') as encrypted_file:
   encrypted = encrypted_file.read()
decrypted = f.decrypt(encrypted)
print("Ecriture data.txt")
with open('data.txt', 'wb') as decrypted_file:
   decrypted_file.write(decrypted)
print("Remove data_enc\n")
os.remove('data.enc')
   
# if os.path.exists('compte.enc'):
print("Decodage compte.enc")
with open('compte.enc', 'rb') as encrypted_file:
   encrypted = encrypted_file.read()
decrypted = f.decrypt(encrypted)
print("Ecriture compte.txt")
with open('compte.txt', 'wb') as decrypted_file:
   decrypted_file.write(decrypted)
print("Remove compte_enc\n")
os.remove('compte.enc')


# val -> validate button
val = False
val_connexion = False
val_inscription = False
val_supprimer = False

# id && mdp_id == compte log 
id = ""
mdp_id = ""

win.bind("<Return>", valide_enter1)
valider = ttk.Button(text="Valider", command=valide_enter1, padding=5)
change_theme = ttk.Button(text="Theme", command=change_theme_enter, padding=5)

identif = ttk.Label(win, text="Identifiant")
identifiant = ttk.Entry()

mot_de_passe = ttk.Label(win, text="Mot de passe")
motDePasse = ttk.Entry(show="*")

site_web = ttk.Label(win, text="Site web")
siteWeb = ttk.Entry()

listSup = ttk.Combobox(win, width=50)

tree = ttk.Treeview(win, columns=('Site Web', 'Nom d’utilisateur', 'Mot de passe'), show='headings')
tree.heading('Site Web', text='Site Web')
tree.heading('Nom d’utilisateur', text='Nom d’utilisateur')
tree.heading('Mot de passe', text='Mot de passe')

scrollbar = ttk.Scrollbar(win, orient=VERTICAL, command=tree.yview)
tree.config(yscrollcommand=scrollbar.set)

# header
mainMenu = Menu(win)
mainMenu.add_command(label="Créer compte", command=create_id)
mainMenu.add_command(label="Connexion compte", command=connexion_id)
win.config(menu=mainMenu)


connexion_id()

win.mainloop()

print("Encodage data.txt")
with open('data.txt', 'rb') as unlock:
   data = unlock.read()
enc_data = f.encrypt(data)
print("Ecriture data.enc")
with open('data.enc', 'wb') as unlock:
   unlock.write(enc_data)
print("Remove data_txt\n")
os.remove('data.txt')

print("Encodage compte.txt")
with open('compte.txt', 'rb') as unlock:
   data = unlock.read()
enc_data = f.encrypt(data)
print("Ecriture compte.enc")
with open('compte.enc', 'wb') as unlock:
   unlock.write(enc_data)
print("Remove compte_txt\n")
os.remove('compte.txt')