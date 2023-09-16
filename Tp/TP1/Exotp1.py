import random

# Boite S du Systeme PRESENT 

# N    0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
# 𝑆(𝑛) 12 5  6  11 9  0  10 13 3  14 15 8  4  7  1  2

# l'index des nombre est egale a N

debug = False
debug1 = True
debug2 = True
debug3 = True

sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
key = [5,11]

def round(k, s):
    return sbox[k ^ s]

def enc(key, msg):
    t = round(key[0], msg)
    c = round(key[1], t)
    if debug: print(f'msg clair : {msg} -> msg chiffré : {c}')
    return c

# 8 = 1000
# 5 = 0101 
# 11 = 1011
# 1000 ^ 0101 = 1101 ^ 1011 = 0110 
# 8 ^ 5 = 13 ^ 11 = 6
 
# 6 ^ 11 = 0110 ^ 1011 = 1101 = 13 
# 13 ^ 5 = 1101 ^ 0101 = 1000 = 8

xobs = [sbox.index(i) for i in range (16)]


def round_back(k, s):
    return xobs[s] ^ k

def dec(key, msg_enc):
    t = round_back(key[1], msg_enc)
    c = round_back(key[0], t)
    if debug: print(f'msg chiffré : {msg} -> msg décoder : {c}')
    return c


if debug1: 
    print(f'{sbox}\n{xobs}')
    msg = 8
    c = enc(key,8)
    d = dec(key, enc(key,8)) 

# Exo 2
# encryptage d'un octet 


def enc_byte(key, byte):
    temp = [byte & 15, byte >> 4]
    res = 0
    for i in range(len(key)):
        temp[i] = round(key[i], temp[i])
    res = temp[0] + (temp[1] << 4)
    if debug:
        print(f"Chiffrement d'un octet : {bin(byte)[2:].zfill(8)} -> {byte} -> {res}")
    return res

def dec_byte(key, byte):
    temp = [byte & 15, byte >> 4]
    res = 0
    for i in range(len(key)):
        temp[i] = round_back(key[i], temp[i])
    res = temp[0] + (temp[1] << 4)
    if debug:
        print(f"Déchiffrement d'un octet : {bin(byte)[2:].zfill(8)} -> {byte} -> {res}")
    return res



def enc_file(key, filename):
    f0 = open('./' + filename, "rb")
    num = f0.read()
    liste = list(num)
    
    f1 = open('./' + filename + '.enc', "wb")
    
    for i in range(len(liste)):
        liste[i] = enc_byte(key, liste[i])
    f1.write(bytearray(liste))
        
    f0.close()
    f1.close
    

def dec_file(key, filename):
    f0 = open('./' + filename + '.enc', "rb")
    num = f0.read()
    liste = list(num)

    f1 = open('dec' + filename , "wb")
    
    for i in range(len(liste)):
        liste[i] = dec_byte(key, liste[i])
    f1.write(bytearray(liste))
    
    f0.close()
    f1.close()
    
    if debug:
        print(liste)
        print(len(liste))
        
if debug2: 
    byte = ord('Z')
    enc_byte(key, byte)
    dec_byte(key,(enc_byte(key, byte)))
    
    enc_file(key, 'note.txt')
    dec_file(key, 'note.txt')

# Exo 3

# Fonction pour générer un IV aléatoire de 1 octet
def generate_random_iv():
    return random.randint(0, 255)

def enc_file_CBC(key, filename):
    f0 = open('./' + filename, "rb")
    iv = generate_random_iv()  # Générer un IV aléatoire
    valeur_CBC = iv
    if debug: print(f"Valeur d'initialisation : {valeur_CBC}")
    num = f0.read()
    liste = list(num)
    
    f1 = open('./' + filename + '.enc', "wb")
    
    # Écrire l'IV dans le fichier chiffré
    f1.write(iv.to_bytes(1, byteorder='big'))
    
    for i in range(len(liste)):
        valeur_CBC = (valeur_CBC ^ liste[i])
        if debug : print(f"Valeur d'initialisation : {valeur_CBC}")
        liste[i] = enc_byte(key, valeur_CBC)
    f1.write(bytearray(liste))

    if debug:
        print(liste)
        print(len(liste))

    f0.close()
    f1.close()

def dec_file_CBC(key, filename):
    f0 = open('./' + filename + '.enc', "rb")
    
    # Lire l'IV depuis le fichier chiffré
    iv = int.from_bytes(f0.read(1), byteorder='big')
    valeur_CBC = iv
    if debug: print(f"Valeur d'initialisation : {valeur_CBC}")
    num = f0.read()
    liste = list(num)

    f1 = open(filename + '.dec', "wb")
    
    for i in range(len(liste)):
        liste[i] = dec_byte(key, liste[i])
        temp = liste[i] 
        liste[i] = (valeur_CBC ^ liste[i]) % 256
        valeur_CBC = temp 
        if debug: print(f"Valeur d'initialisation : {valeur_CBC}\t liste[i] : {liste[i]}")
    
    f1.write(bytearray(liste))
    
    f0.close()
    f1.close()
    
    if debug:
        print(liste)
        print(len(liste))



if debug3: 
    key = (9,0)
    f = open("texte.txt", "wb")
    f.write(bytearray("coucou?coucou!".encode("utf-8")))
    f.close()

    enc_file(key, "texte.txt")
    dec_file(key, "texte.txt")

    '''
    1. Je remarque qu'il y a une répétition du motif : &ö•&ö•ò&ö•&ö•³ 

    2. Je propose de l'attaquer avec une analyse de fréquence 
    '''
    
    f = open("texte_CBC.txt", "wb")
    f.write(bytearray("coucou?coucou!".encode("utf-8")))
    f.close()

    enc_file_CBC(key, "texte_CBC.txt")
    dec_file_CBC(key, "texte_CBC.txt")
    '''
    4. l'avantage du vecteur d'initialisation est de mieux masquer notre passage dans un flux d'information et d'etre moins repérable par l'humain
    '''