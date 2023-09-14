import random
import taktoy

debug = True

def compute_differential_characteristics ():
    sbox_dc = [[0 for j in range(0, 16)] for i in range(0, 16)]
    for i in range(0, 16):
        for j in range(0, 16):
            sbox_dc[i ^ j][taktoy.sbox[i] ^ taktoy.sbox[j]] += 1
    if debug:
        print('\n> XOR differential table:')
        print('     ', end='')
        for i in range(0, 16):
            print('%2x ' % i, end='')
        print('\n   +-', end='')
        for i in range(0, 16):
            print('---', end='')
        for i in range(0, 16):
            print('\n%2x | ' % i, end='')
            for j in range(0, 16):
                print('%2d ' % sbox_dc[i][j], end='')
    return sbox_dc

def get_most_probable_diff_sbox_io (dc):
    mpd = 0
    for i in range(0, 16):
        for j in range(0, 16):
            mpd = max(mpd, dc[i][j] % 16)
    if debug:
        print('\n> Most probable diff have %x occurences\n' % mpd)
        print('> Most probable sbox input --> output:')
    in_out = []
    for i in range(0, 16):
        for j in range(0, 16):
            if dc[i][j] == mpd:
                in_out.append((i, j))
                if debug:
                    print('%x --> %x' % (i, j))
    return in_out

def get_possible_intermediate_values (diff_io):
    in_diff, out_diff = diff_io
    if debug:
        print('\n> Selected diff in/out: %x --> %x' % (in_diff, out_diff))
        print('> Possibles i0 ^ i1 --> o0 ^ o1:')
    piv = []
    for i0 in range(0, 16):
        i1 = i0 ^ in_diff
        if taktoy.sbox[i0] ^ taktoy.sbox[i1] == out_diff:
            piv.append(i0)
            if debug:
                print('%x ^ %x --> %x ^ %x' %
                      (i0, i1, taktoy.sbox[i0], taktoy.sbox[i1]))
    return piv

def generate_pairs (count, in_diff, key):
    if debug:
        print('\n> Generating %d known plain/cipher pairs with in diff of %d' %
              (count, in_diff))
    known0 = []
    known1 = []
    for i in range(0, count):
        p0 = random.randint(0, 15)
        c0 = taktoy.simplified_enc(p0, key)
        known0.append((p0, c0))
        p1 = p0 ^ in_diff
        c1 = taktoy.simplified_enc(p1, key)
        known1.append((p1, c1))
    return known0, known1

def find_good_pair (known0, known1, out_diff):
    if debug:
        print('\n> Searching for a pair with out diff of %d' % out_diff)
    for i in range(0, len(known0)):
        if known0[i][1] ^ known1[i][1] == out_diff:
            if debug:
                print('> Found: p0 = %x, p1 = %x --> c0 = %x, c1 = %x' %
                      (known0[i][0], known1[i][0], known0[i][1], known1[i][1]))
            return [known0[i][0], known0[i][1]]
    print('Can\'t find good pair…')

def test_key (key, known0, known1):
    bad = False
    for i in range(0, len(known0)):
        if (taktoy.simplified_enc(known0[i][0], key) != known0[i][1] or
            taktoy.simplified_enc(known1[i][0], key) != known1[i][1]):
            bad = True
    return not bad

def attack (piv, p0, c0, known0, known1):
    if debug:
        print('\n> Bruteforcing on reduced key space…')
    for i in range(0, len(piv)):
        k0 = piv[i] ^ p0
        k1 = taktoy.sbox[piv[i]] ^ c0
        if test_key((k0, k1), known0, known1):
            if debug:
                print('Key found: %x %x' % (k0, k1))
            return (k0, k1)
        else:
            if debug:
                print('Bad attempt: %x %x' % (k0, k1))
    return None

if __name__ == '__main__':
    key = (random.randint(0, 15), random.randint(0, 15))
    print('Real key: %x %x' % key)
    dc = compute_differential_characteristics()
    mpd_io = get_most_probable_diff_sbox_io(dc)
    s = random.randint(0, len(mpd_io) - 1)
    piv = get_possible_intermediate_values(mpd_io[s])
    known0, known1 = generate_pairs(8, mpd_io[s][0], key)
    p0, c0 = find_good_pair(known0, known1, mpd_io[s][1])
    k = attack(piv, p0, c0, known0, known1)
    if k is not None:
        print('Key: %x %x' % k)
