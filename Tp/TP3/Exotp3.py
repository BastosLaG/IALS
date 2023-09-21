import random

sbox = [9, 11, 12, 4, 10, 1, 2, 6, 13, 7, 3, 8, 15, 14, 0, 5]
xobs = [14, 5, 6, 10, 3, 15, 7, 9, 11, 0, 4, 1, 2, 8, 13, 12]

def enc (m, key):
    t = sbox[m ^ key[0]]
    c = sbox[t ^ key[1]]
    return c

def dec (c, key):
    t = xobs[c] ^ key[1]
    m = xobs[t] ^ key[0]
    return m


'''
Exercice 1.
    
    2 la famille de chiffrement par bloc 

    3 RSP

    4.
        a. 4 bits
        b. 8 bits
        c. 2 tours
        d. XOR avec la clef du tour ensuite passage vers la boîte S
        e. Au passage vers la boîte S
        f. Identité

Exercice 2.

 a. Le type KPA
 b.  t0 = s(p) ;
     p = k0 ^ t ;
     s^{1}(tO) ^ t = k0 = la clef

On peut plus faire le calcul en rajoutant un tour parce que il nous manque la valeur intermédiaire
3.
    a. 16
    b. Non car on ne pourras pas car plusieurs clé sont disponible selon les cas, même si on les a toutes cela reste introuvable
4.
    a. 
    (2**4)*2
    (2bit puissance (taille clé)) fois nombre de tour
    la clé est dans notre toycipher est compris entre 256 et 0 sous cette forme key = [0000, 0000]
    notre message est compris entrte 16 et 0 car sur 4 bit
'''
key = [11, 5]
m = 15
m1 = enc(m, key)
# print(m1)

# 5
# Test de brute force
def brute_force(m, m1):
    for i in range(2**4):
        k0 = i
        for j in range(2**4):
            k1 = j
            kt = [k0, k1]
            if m == dec(m1, kt):
                print(f"clé possible [{kt[0]},{kt[1]}]")
    return False

# print(brute_force(m, m1))

m1 = dec(m1, key)
# print(f"La vraie clé est : {key}")

'''
La réponse à la question est ce qu'on est sur de trouver la bonne clé est NON car le brute force nous donne beaucoup trop de correspondance différentes a tester. Mais cela peut etre utiliser pour réduire notre champs d'action cepandant sur une clé beaucoup plus grande cela reste inutilisable. Il faudrait comparer plusieurs messages claire et chiffrer jusqu'a éliminer les clé au cas par cas le temps de calcule se voit extrement allongé et quasiment aléatoire sur la réception des messages claire et chiffrer. 

6.
'''
def gen_m_cc(key, n):
    res = []
    for i in range(n):
        temp = random.randint(0, 15)
        res.append([temp, enc(temp, key)])
    return res

# print(gen_m_cc(key, 100))

'''
Exercice 3: 

1. →Pourquoi?

Notre fonction n'est pas linéaire a cause de la boite S qui brouille les entrés et les sorties.

2. →Écrivez une fonction qui calcule pour chaque couple(𝑚𝑎𝑠𝑘𝑖, 𝑚𝑎𝑠𝑘𝑜), pour combien des 16 paires entrée/-sortie de la boîte S on a une égalité de parité.
'''
debug = True

def cps(sbox):
    # eviter les cases vides et les out of range
    score_table = [[0 for _ in range(16)] for _ in range(16)]
    if debug: 
        for elem in score_table:
            print(elem)
    for mask_i in range(1, 16):
        for mask_o in range(1, 16):
            count = 0
            for i in range(16):
                input_masked = i & mask_i
                output_masked = sbox[i] & mask_o
                if bin(input_masked).count('1') % 2 == bin(output_masked).count('1') % 2 and bin(input_masked).count('1') % 2 == 1:
                    count += 1
            score_table[mask_i][mask_o] = count
    if debug: 
        print()
        for elem in score_table:
            print(f'{elem}')
    return score_table



def fbm(score_table):
    best_s = 0
    best_m = None

    for mask_i in range(1, 16):
        for mask_o in range(1, 16):
            score = score_table[mask_i][mask_o]
            if score > best_s:
                best_s = score
                best_m = (mask_i, mask_o)

    return best_m, best_s

score_table = cps(sbox)
s, m = fbm(score_table)
print(f"Score = : {s}\nmask = : {m}")

'''
la fonction me renvoie une paire mais d'autre paire sont égale a celle si c'est donc l'une des meillieures et pas la meillieure

Exo 4: 

'''

liste_m_cc = gen_m_cc(key, 16)
print(liste_m_cc)
