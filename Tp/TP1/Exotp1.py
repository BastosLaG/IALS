# Boite S du Systeme PRESENT 

# N    0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
# 𝑆(𝑛) 12 5  6  11 9  0  10 13 3  14 15 8  4  7  1  2

# l'index des nombre est egale a N

debug = True
debug1 = False
debug2 = False
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
    t1 = byte & 15
    t2 = byte >> 4
    temp = [t1, t2]
    res = 0
    for i in range(len(key)):
        t = round(key[0], int(temp[i]))
        temp[i] = round(key[1], int(t))
    temp[0] = temp[0] << 4
    if debug: print(f'temp0 = {temp[0]}{type(temp[0])} temp1 = {temp[1]}{type(temp[1])}')
    res = temp[0] + temp[1]
    if debug: print(f"Encryptage d'un byte : {bin(byte)[2:].zfill(8)} -> {byte} -> {res}")
    return res


def dec_byte(key, byte):
    t1 = byte & 15
    t2 = byte >> 4
    temp = [t1, t2]
    res = 0 
    for i in range(len(key)):
        t = round_back(key[1], int(temp[i]))
        temp[i] = round_back(key[0], int(t))
    temp[0] = temp[0] << 4
    if debug: print(f'temp0 = {temp[0]}{type(temp[0])} temp1 = {temp[1]}{type(temp[1])}')
    res = temp[0] + temp[1]
    if debug: print(f"Décryptage d'un byte : {bin(byte)[2:].zfill(8)} -> {byte} -> {res}")
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

    f1 = open('./' + filename + '.dec', "wb")
    
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
    print(byte)
    enc_byte(key, byte)
    dec_byte(key,(enc_byte(key, byte)))
    
    # enc_file(key, 'note.txt')
    # dec_file(key, 'note.txt')



# Exo 3

if debug3: 
    key = (9,0)
    f = open("texte.txt", "wb")
    f.write(bytearray("coucou?coucou!".encode("utf-8")))
    f.close()

    enc_file(key, "texte.txt")
    dec_file(key, "texte.txt")

'''
Je remarque qu'il y a une répétition du motif : &ö•&ö•ò&ö•&ö•³ 

Je propose de l'attaquer avec une analyse de fréquence 
'''

def enc_file_CBC(key, filename):
    f0 = open('./' + filename, "rb")
    valeur_CBC = 598367 # utiliser une clé aléatoire plus tard
    if debug : print(f"La valeur d'initialisation : {valeur_CBC}")
    num = f0.read()
    liste = list(num)
    
    f1 = open('./' + filename + '.enc', "wb")
    
    for i in range(len(liste)):
        valeur_CBC = (valeur_CBC ^ liste[i]) % 255
        print(f"valeur CBC = {valeur_CBC}")
        liste[i] = enc_byte(key, valeur_CBC)
    f1.write(bytearray(liste))
        
    f0.close()
    f1.close
    

def dec_file_CBC(key, filename):
    f0 = open('./' + filename + '.enc', "rb")
    valeur_CBC = 0
    num = f0.read()
    liste = list(num)

    f1 = open(filename+'.dec', "wb")
    
    for i in range(len(liste)):
        liste[i] = dec_byte(key, liste[i])
        # valeur_CBC = 
        # liste[i] ^ 
    f1.write(bytearray(liste))
    
    f0.close()
    f1.close()
    
    if debug:
        print(liste)
        print(len(liste))
        
if debug3: 
    key = (9,0)
    f = open("texte_CBC.txt", "wb")
    f.write(bytearray("coucou?coucou!".encode("utf-8")))
    f.close()

    enc_file_CBC(key, "texte_CBC.txt")
    '''
    c'est déjà mieux : &ö•&ö•ò&ö•&ö•³ -> fAÅû‘‚Ib-ý‚«
    valeur_CBC = 598367 # utiliser une clé aléatoire plus tard 
    '''
    dec_file_CBC(key, "texte_CBC.txt")
        
        
        
        
        
        
        
        
        
        

