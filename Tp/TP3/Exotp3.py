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
        temp = i
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

# count parity score
def cps(sbox, mask_i, mask_o):
    count = 0
    for input in range(16):
        output = sbox[input]
        if bin(input & mask_i).count('1') % 2 == bin(output & mask_o).count('1') % 2:
            count += 1
    return count


# find best mask
def fbm(sbox):
    best_mask_i = 0
    best_mask_o = 0
    best_score = 0

    for mask_i in range(1, 15):
        for mask_o in range(1, 15):
            score = cps(sbox, mask_i, mask_o)
            if score > best_score:
                best_score = score
                best_mask_i = mask_i
                best_mask_o = mask_o
    return best_mask_i, best_mask_o

i, o = fbm(sbox)
print(f'best_mask_i = {i}, best_mask_o = {o}')

'''
la fonction me renvoie une paire mais d'autre paire sont égale a celle si c'est donc l'une des meillieures et pas la meillieure

Exo 4: 

1.
'''

liste_m_cc = gen_m_cc(key, 16)
print(liste_m_cc)

'''
2. 
'''

def s_k0(m_cc, sbox, mask_i, mask_o):
    score_k0 = []
    list_k0 = []
    for elem in m_cc:
        msg_cl = elem[0]
        msg_cr = elem[1]
        count = 0
        for k0 in range(0,15):
            t = sbox[msg_cl ^ k0]
            if bin(t & mask_i).count('1') % 2 == bin(msg_cr & mask_o).count('1') % 2:
                count += 1
        score_k0.append(count)
    if debug: print(f'Score obtenu pour k0 : \t{score_k0}')
    for k in score_k0:
        if k == max(score_k0):
            list_k0.append(score_k0.index(k))
            score_k0[score_k0.index(k)] = 0
    if debug: print(f'k0 possible : \t\t{list_k0}')
    return list_k0

s_k0(liste_m_cc, sbox, i, o)




def count_parity_equalities(S_box, mask_in, mask_out):
    count = 0
    for input in range(16):
        output = S_box[input]
        if bin(input & mask_in).count('1') % 2 == bin(output & mask_out).count('1') % 2:
            count += 1
    return count


def find_best_masks(S_box):
    best_mask_in = 0
    best_mask_out = 0
    best_score = 0

    for mask_in in range(1, 16):  # Start from 1 to exclude mask with all 0s
        for mask_out in range(1, 16):
            score = count_parity_equalities(S_box, mask_in, mask_out)
            if score > best_score or (score == best_score and (bin(mask_in).count('1') + bin(mask_out).count('1') > bin(best_mask_in).count('1') + bin(best_mask_out).count('1'))):
                best_score = score
                best_mask_in = mask_in
                best_mask_out = mask_out

    return best_mask_in, best_mask_out


def generate_known_pairs(k0, k1):
    known_pairs = []
    for m in range(16):
        c = enc(m, key)
        known_pairs.append((m, c))
    return known_pairs

# Exemple d'utilisation
k0 = 0x5A3C
k1 = 0x9B7E
known_pairs = generate_known_pairs(k0, k1)
print(known_pairs)


def score_k0(S_box, k0_candidates, k1, known_pairs):
    scores = {}
    for k0 in k0_candidates:
        score = 0
        for m, c in known_pairs:
            t = enc(m, key)
            if count_parity_equalities(S_box, m, c) == count_parity_equalities(S_box, t, c):
                score += 1
        scores[k0] = score
    return scores

def select_k0_candidates(scores, threshold):
    k0_candidates = [k0 for k0, score in scores.items() if score >= threshold]
    return k0_candidates
