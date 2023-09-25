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

    public_key = (e, n)
    private_key = (d, n)
    s = pow(m,d,n)
    
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

# Le module RSA n
n = 47775493107113604137

fake_value = 0x9c03f7cded2f7444

diff = uNum.GCD(n, fake_value - 1)

p = diff
q = n // p

print(f"p = {p}, q = {q}")

