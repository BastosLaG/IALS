import random
from Crypto.Util import number
import hashlib


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

# Exemple d'utilisation :
bits = 2048  # Taille de la clé en bits
Ap, As = gen_rsa_keypair(bits)
Bp, Bs = gen_rsa_keypair(bits)

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

def rsa_enc(msg, key):
    msg_enc = int.from_bytes(msg.encode('utf-8'),'big')
    return rsa(msg_enc, key)

def rsa_dec(msg, key):
    msg_dec = rsa(msg, key)
    return msg_dec.to_bytes((msg_dec.bit_length() + 7) // 8, 'big').decode('utf-8')


msgA = "Bonjour je suis Alice"
msgB = "Bonjour je suis Bob"

# Si Bob veut envoyer un message a Alice
msgB = rsa_enc(msgB, Ap)
# print("Je suis le message encrypter")
# print(msgB) 
# Si Alice veut décripter un message a Bob
msgB = rsa_dec(msgB, As)
# print("Je suis le message decrypter")
# print(msgB) 

# Si Alice veut envoyer un message a Bob
msgA = rsa_enc(msgA, Bp)
# print("Je suis le message encrypter")
# print(msgA)
# Si Bob veut décripter un message a Alice
msgA = rsa_dec(msgA, Bs)
# print("Je suis le message decrypter")
# print(msgA) 

# message de tomas crypté
clefs =(49305946713190178331685101770887049321272784225708294443436764890372104868233, 65167699646164877331317371317401837940241174188022295084726202562535201830271)
messagecrypté = 6895038287525557109396783288511458527508329148439023615942010303654796867140
print(rsa_dec(messagecrypté, clefs))

# Exo 3

# 1. Soit (𝐴𝑝, 𝐴𝑠) la paire de clefs d’Alice, et (𝐵𝑝, 𝐵𝑠) la paire de clefs de Bob.
# (a) → Quelle clef doit utiliser Bob pour signer un message? Il doit utiliser ça propre clé secrete
# (b) → Quelle clef doit utiliser Alice pour vérifier l’authenticité du message qui prétend être signé par Bob? Elle doit utilisée la clé publique de Bob

# 2. Pour signer un message, on signe généralement un condensé (hash) du message, ce qui permet de signer des
# messages de toutes tailles et de s’assurer au passage de l’intégrité du message.
# → Quelle est la procédure de signature et quelle est la forme du message signé? 
# 𝑠 = 𝐻(𝑚)𝑑 mod 𝑛.

msg = "Je suis un hachis de code !"

Ap, As = gen_rsa_keypair(bits)
Bp, Bs = gen_rsa_keypair(bits)

def h(msg):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

def rsa_sign(msg):
    return msg + str(h(msg))

print(msg)
print(type(msg))
print(h(msg))
print(type(h(msg)))

print(str(rsa_enc(msg, Bp)))
print(type(str(rsa_enc(msg, Bp))))

c = rsa_enc(rsa_sign(msg), Bp)
print(c)
print(type(c))

d = str(rsa_dec(c, Bs))
print(d)
print(type(d))
