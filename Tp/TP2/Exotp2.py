import random
from Crypto.Util import number
import hashlib

debug = False
test = True

def gen_rsa_keypair(bits):
    # Étape 1 : Génération de p et q
    p = number.getPrime(bits // 2)
    q = number.getPrime(bits // 2)

    # Étape 2 : Calcul de n
    n = p * q

    # Étape 3 : Calcul de phi(n)
    phi_n = (p - 1) * (q - 1)

    # Étape 4 : Génération de l'exposant de chiffrement e
    # L'exposant e est généralement un petit nombre premier
    e = 65537

    # Vérification que e est premier avec phi(n) (pgcd(e, phi_n) doit être égal à 1)
    while number.GCD(e, phi_n) != 1:
        e = number.getPrime(bits // 3)  # Générer un nouvel e si nécessaire

    # Étape 5 : Calcul de l'exposant de déchiffrement d (inverse modulaire de e modulo phi(n))
    d = number.inverse(e, phi_n)

    # Étape 6 : Retourner la paire de clés publique/privée
    public_key = (e, n)
    private_key = (d, n)
    
    return public_key, private_key


# Exo 2

# 1.a Bob doit utiliser la clé publique de Alice pour chiffrer son message
# 1.b Alice doit utiliser ça clé priver pour dechiffrer le message que l'on lui envoie
# 2 c = m*e mod n pour le chiffrement et m = c*d mod n pour le déchiffrement

def rsa(msg, key):
    return pow(msg, key[0], key[1])

# print(rsa(562015, Bp))

msg = int.from_bytes("J'adore la programmation".encode('utf-8'), 'big')
# print(msg)
msg = msg.to_bytes((msg.bit_length() + 7) // 8, 'big').decode('utf-8')
# print(msg)

def sti(msg):
    return int.from_bytes(msg.encode('utf-8'), 'big')

def its(msg):
    return msg.to_bytes((msg.bit_length() + 7) // 8, 'big').decode('utf-8')

def rsa_enc(msg, key):
    msg = int.from_bytes(msg.encode('utf-8'), 'big')
    return rsa(msg, key)

def rsa_dec(msg, key):
    msg_dec = rsa(msg, key)
    return msg_dec.to_bytes((msg_dec.bit_length() + 7) // 8, 'big').decode('utf-8')

# message de tomas crypté
# clefs =(49305946713190178331685101770887049321272784225708294443436764890372104868233, 65167699646164877331317371317401837940241174188022295084726202562535201830271)
# messagecrypté = 6895038287525557109396783288511458527508329148439023615942010303654796867140
# print(rsa_dec(messagecrypté, clefs))

'''
Exo 3
1. Soit (𝐴𝑝, 𝐴𝑠) la paire de clefs d’Alice, et (𝐵𝑝, 𝐵𝑠) la paire de clefs de Bob.
(a) → Quelle clef doit utiliser Bob pour signer un message? 
Il doit utiliser ça propre clé secrete 

(b) → Quelle clef doit utiliser Alice pour vérifier l’authenticité du message qui prétend être signé par Bob? 
Elle doit utilisée la clé publique de Bob

2. Pour signer un message, on signe généralement un condensé (hash) du message, ce qui permet de signer des messages de toutes tailles et de s’assurer au passage de l’intégrité du message.
→ Quelle est la procédure de signature et quelle est la forme du message signé? 
𝑠 = 𝐻(𝑚)𝑑 mod 𝑛.
'''


def h(msg):
    msg = hashlib.sha256(msg.encode('utf-8')).hexdigest()
    if debug: print(f'h : {msg}')
    return msg

def rsa_sign(msg, key_pub, key_prv):
    ''' La clé priver du signataire doit crypté le hashage 
        La clé publique du destinataire doit encrypté le message'''
    return [rsa_enc(msg, key_pub), rsa_enc(h(msg), key_prv)]

def rsa_verif(msg, key_prv, key_pub):
    ''' 
    La clé priver du signataire doit crypté le hashage 
    La clé publique du destinataire doit encrypté le message
    '''
    if debug: print(f'msg[0] = {msg[0]}\n{type(msg[0])}\nmsg[1] = {msg[1]}\n{type(msg[1])}')
    msg_dec = rsa_dec(msg[0], key_prv)
    sign_dec = rsa_dec(msg[1], key_pub)
    if debug : print(msg_dec, sign_dec)
    return h(msg_dec) == sign_dec

'''
Exo 4 : 
1.La version de RSA qu’on a implémentée ici, qu’on appelle communémenttextbook RSA, souffre de plusieursproblème de sécurité.Par exemple, il est possible deforgerdes chiffrés valides à partir de chiffrés existants qu’on aurait interceptés.C’est ce qu’on appelle la malléabilité.

→Comment? 

Cela se produit parce que la fonction de chiffrement RSA est basée sur une opération de puissance modulaire et cette opération est linéaire. Donc si un attaquant intercepte un texte chiffré C correspondant à un message chiffré avec la clé publique de quelqu'un, il peut effectuer certaines opérations mathématiques sur C pour obtenir un nouveau texte chiffré C' qui sera utile pour déchiffrer le message sans connaitre la clé privée.

2.Un autre soucis est le déterminisme du chiffrement. C’est à dire que si on chiffre deux fois le même messageavec la même clef, on obtient deux fois le même chiffré.

→En quoi est-ce un problème?

c'est un problème car l'on peut facilement identifier des structure ou récupérer des informations qui se répetes d'un message a un autre c'est pour cela qu'au Tp 1 nous devions utiliser une structure avec une valeur initial pour éviter les répétitions.

3.Conclusion : c’estcompliquéd’implémenter correctement des algorithmes cryptographiques. Il vaut mieux éviter de le faire soi-même et plutôt utiliser des bibliothèques déjà existantes, libre, et surtout, largementéprouvées.

''' 
    
if test:
    bits = 2048  # Taille de la clé en bits
    Ap, As = gen_rsa_keypair(bits)
    Bp, Bs = gen_rsa_keypair(bits)

    msgA1 = "Bonjour je suis Alice"
    msgB1 = "Bonjour je suis Bob"
    # Si Bob veut envoyer un message a Alice
    msgB2 = rsa_enc(msgB1, Ap)
    # Si Alice veut décripter un message a Bob
    msgA2 = rsa_dec(msgB2, As)

    
    print(f"Je suis le message encrypter : {msgB2}")
    print(f"Je suis le message decrypter : {msgA2}")

    # Si Alice veut envoyer un message a Bob
    msgA3 = rsa_enc(msgA1, Bp)
    # Si Bob veut décripter un message a Alice
    msgB3 = rsa_dec(msgA3, Bs)
    
    
    print(f"Je suis le message encrypter : {msgA3}")
    print(f"Je suis le message decrypter : {msgB3}")

    msg = "Je suis un hachis de code !"

    msg_enc = rsa_enc(msg, Bp)
    msg_dec = rsa_dec(msg_enc, Bs)
    msg_sign = rsa_sign(msg, Bp, As)
    
    print(f'message : {msg}')
    print(f'message haché : {h(msg)}')
    print(f'message encodé sans signature : \n{rsa_enc(msg, Bp)}')
    print(f'message décodé sans signature : \n{rsa_dec(msg_enc, Bs)}')
    print(f'message encodé avec signature : \n[{rsa_enc(msg, Bp)}, {sti(h(msg))}]')
    print(f'message encodé avec signature encodé : \n{rsa_sign(msg, Bp, As)}')
    print(f'Verification signature : {rsa_verif(msg_sign, Bs, Ap)}')
    
    
    
    


