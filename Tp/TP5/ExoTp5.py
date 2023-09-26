import Crypto.Util.number as uNum
import random
import time

test = False

def gen_rsa(b):
    p = uNum.getPrime(b//2)
    q = uNum.getPrime(b//2)
    n = p*q
    
    phi_n = (p-1)*(q-1)
    e = 65537
    
    while uNum.GCD(e, phi_n) != 1:
        e = uNum.getPrime(b // 3)
    d = uNum.inverse(e, phi_n)
    
    d = uNum.inverse(e,phi_n)
    m = random.randint(1,n)

    s = pow(m,d,n)
    # public_key = (e, n)
    # private_key = (d, n)
    return s

def gen_crtrsa(b):
    p = uNum.getPrime(b//2)
    q = uNum.getPrime(b//2)
    n = p*q
    
    phi_n = (p-1)*(q-1)
    e = 65537

    while uNum.GCD(e, phi_n) != 1:
        e = uNum.getPrime(bits // 3)
    d = uNum.inverse(e, phi_n)
    
    dp = d % p-1
    dq = d % q-1

    iq = q-1 % p
    
    m = random.randint(1,n)

    sp = pow(m,dp,p)
    sq = pow(m,dq,q)
    s = sq + q * (iq * (sp - sq) % p )
    return s

# start = time.time()
# for i in range(100):
#     gen_rsa(1024)
# end = time.time()

# print(f"{end - start} secondes")


# """
# 2. La clef privée dépend de plus de variables
# """

# start = time.time()
# for i in range(100):
#     gen_crtrsa(1024)
# end = time.time()

# print(f"{end - start} secondes")

"""
6. La division des calculs à l'aide de dp,qp améliore un peu la rapiditer 

Exo 2
1. résultat faux 
s = fa7a82e289efdd33
    9c03f7cded2f7444
    
vrai résultat = 3f010be37eb5eca9
"""

import Crypto.Util.number as number

def dec_to_hex(num):
    return hex(num)[2:]

def sp(n,s,s_prime):
    return dec_to_hex(number.GCD(n,s-s_prime))

key_p = (17, 47775493107113604137)

soriginal = int("3f010be37eb5eca9",16)
sfaux = int("014bc14b1e9873ce93",16)

qr20 = sp(key_p[1],soriginal,sfaux)

print(f"Valeur de q retrouvée : {qr20}")


q = int(qr20,16)

def find_p(n,q):
    p = n // q
    return p
print("q :",q)
p = find_p(key_p[1],q)
print("p :",p,"\n")

def find_key_prv(p,q,e):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = number.inverse(e, phi_n)
    private_key = (d,n)
    
    return private_key

key_prv = find_key_prv(p,q,key_p[0])  

print(f"Valeur de privée key retrouvée : {key_prv}")


def decrypt_message(key_prv,msg):
    n = key_prv[1]
    d = key_prv[0]
    msg_dec = pow(msg, d, n)
    return msg_dec

msg_dec = decrypt_message(key_prv,soriginal)

print(f"Valeur de message décryptée : {msg_dec}")

'''
Valeur de privée key retrouvée : (22482584984930046353, 47775493107113604137)
Valeur de message décryptée : 24761341331221528199
'''