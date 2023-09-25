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
    (2**8)*2 == 512
    la clé est dans notre toycipher est compris entre 512 et 0 sous cette forme key = [0000, 0000]
    se résultat est faux et on se rapproche plus des 2**13
'''

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

# print("Exo 2 :")
key = [11, 5]
m = 15
m1 = enc(m, key)
# print(m1)
# print(brute_force(m, m1))
m1 = dec(m1, key)
print(f"La vraie clé est : {key}")

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

def p(nmb): 
    # retourne la pariter binaire 
    result = 0
    while nmb > 0:
        if nmb%2 == 1:
            result += 1
        nmb = nmb>>1
    return result

def gep(): 
    # tout les résultats (in, out) possible de la boiteS
    l = []
    for i in range(16):
        l.append((i, sbox[i]))
    return l

def cps():
    # eviter les cases vides et les out of range
    score_table = {}
    msgsbox = gep()
    for mask_i in range(1, 16):
        for mask_o in range(1, 16):
            score_table[(mask_i, mask_o)] = 0
            for msg in msgsbox:
                input_masked = msg[0] & mask_i
                output_masked = msg[1] & mask_o
                if (p(input_masked)+p(output_masked)) % 2 ==  0:
                    score_table[(mask_i, mask_o)] += 1
    if debug: print(score_table)
    return score_table


def fbm(score_table):
    best_s, best_m = 0, []
    maskCouples = []
    for mask_i in range(1, 16):
        for mask_o in range(1, 16):
            if score_table[mask_i, mask_o] > best_s and mask_o+mask_i !=0:
                best_s = score_table[mask_i, mask_o]
                maskCouples = [[(mask_i, mask_o), (p(mask_i)+p(mask_o))%2]]
                
            elif score_table[mask_i, mask_o] == best_s and mask_o+mask_i !=0: 
                maskCouples += [[(mask_i, mask_o), (p(mask_i)+p(mask_o)%2)]]
                
    best_s = 0
    for couple in maskCouples:
        if couple[1] > best_s:
            best_s = couple[1]
            best_m = couple[0]
    return best_m , best_s

print("Exo 3 :")
score_table = cps()
m, s = fbm(score_table)
print(f"Score = : {s}\nmask = : {m}")

'''
la fonction me renvoie une paire mais d'autre paire sont égale a celle si c'est donc l'une des meillieures et pas la meillieure

Exo 4: 

1.
'''
print("\nExo 4 :")
liste_m_cc = gen_m_cc(key, 16)
print(f"liste generer aléatoirement : \n{liste_m_cc}\n")

'''
3.
'''
def approximation_k0(liste_m, sbox, best_mask):
    max = 0
    m = best_mask # best mask
    liste_best_k0 = list()
    # test pariter pour chaque k0 
    for k0 in range(15):
        count = 0    
        for msg in liste_m:
            t = sbox[k0 ^ msg[0]]
            if (p(t&m[0])+p(msg[1]&m[1]))%2 == 0:
                count += 1
        if abs(count-8) > max:
            max = abs(count-8)
        elif abs(count-8) == max:
            liste_best_k0.append(k0) 
    if debug: print('\nprint best k0_poss :',liste_best_k0)
    return liste_best_k0

best_mask = fbm(cps())[0]
k0 = approximation_k0(liste_m_cc, sbox, best_mask)

print("Exo 5")
def approximation_k1(liste_m, k0, sbox, xobs):
    count = 0    
    liste_k_poss = list()
    for k in k0:
        t0 = sbox[k^liste_m[0][0]]
        t1 = xobs[liste_m[0][1]]
        k1 = t0 ^ t1
        liste_k_poss.append([k, k1])
    for k in liste_k_poss:
        count = 0
        for msg, msgC in liste_m:
            if msgC != enc(msg, k) or msg != dec(msgC, k):
                break
            count += 1
        if count == len(liste_m):
            if debug: print(f"La cles est égale a : {k}")
            return k
    return None

k1 = approximation_k1(liste_m_cc, k0, sbox, xobs)

debug = False

sbox = [9, 11, 12, 4, 10, 1, 2, 6, 13, 7, 3, 8, 15, 14, 0, 5]
xobs = [sbox.index(i) for i in range (16)]
count = 0 
liste_test = []
keys = []
best_mask = fbm(cps())[0]
for i in range(1000):
    k0, k1 = random.randint(0, 15), random.randint(0, 15)
    keys = [k0, k1]
    liste_test = gen_m_cc(keys, 16)
    if approximation_k1(liste_test, approximation_k0(liste_test, sbox, best_mask), sbox, xobs) != None: 
        count += 1
    i+=1
print(f"Le pourcentage de bonne réponse est : {count/10}%")

print("Exo 6 :")

'''
1. liste_m * nombre de clé possible (15*15 dans se cas = 225) juste pour un probable k0
2. c'est beaucoup plus rapide 
3. Oui car cela reste une instruction cpu a parcourir 
4. [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 2, 1] il y a environ 20% de différence c'est énorme 
'''
sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 2, 1]
xobs = [sbox.index(i) for i in range (16)]
count = 0 
liste_test = []
keys = []
best_mask = fbm(cps())[0]
for i in range(1000):
    k0, k1 = random.randint(0, 15), random.randint(0, 15)
    keys = [k0, k1]
    liste_test = gen_m_cc(keys, 16)
    if approximation_k1(liste_test, approximation_k0(liste_test, sbox, best_mask), sbox, xobs) != None: 
        count += 1
    i+=1
print(f"Le pourcentage de bonne réponse est : {count/10}%")
