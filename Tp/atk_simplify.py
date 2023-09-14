import sys
import random

sbox = [3, 14, 1, 10, 4, 9, 5, 6, 8, 11, 15, 2, 13, 12, 0, 7]

debug = True

def round (m, sk):
    return sbox[m ^ sk]

def enc (msg, key):
    tmp = round(msg, key[0])
    ctx = round(tmp, key[1])
    return ctx

def simplified_enc (msg, key):
    tmp = round(msg, key[0])
    return tmp ^ key[1]

def compute_differential_characteristics ():
    sbox_dc = [[0 for j in range(16)] for i in range(16)]
    for i in range(16):
        for j in range(16):
            sbox_dc[i ^ j][sbox[i] ^ sbox[j]] += 1
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
        print('')
    return sbox_dc

def get_most_probable_diff_io (dc):
    mpd = 0
    for i in range(16):
        for j in range(16):
            mpd = max(mpd, dc[i][j] % 16)
    if debug:
        print(f'> most probable diff have {mpd} occurences')
    in_out = []
    for i in range(16):
        for j in range(16):
            if dc[i][j] == mpd:
                in_out.append((i, j))
    if debug:
        print('> Most probable sbox in/out:')
        for io in in_out:
            print(f'- {io[0]} --> {io[1]}')
    return in_out

def get_possible_intermediate_values (diff_io):
    in_diff, out_diff = diff_io
    if debug:
        print(f'> Working with {diff_io}')
    piv = []
    for i0 in range(16):
        i1 = i0 ^ in_diff
        if sbox[i0] ^ sbox[i1] == out_diff:
            piv.append(i0)
        if debug:
            print(f'{i0} ^ {i1} --> {sbox[i0]} ^ {sbox[i1]}')
    return piv


def generate_pairs (count, in_diff, key):
    known0 = []
    known1 = []
    for i in range(count):
        p0 = random.randint(0, 15)
        c0 = simplified_enc(p0, key)
        known0.append((p0, c0))
        p1 = p0 ^ in_diff
        c1 = simplified_enc(p1, key)
        known1.append((p1, c1))
    return known0, known1

def find_good_pair (known0, known1, out_diff):
    for i in range(len(known0)):
        if known0[i][1] ^ known1[i][1] == out_diff:
            if debug:
                print(f'> Good pair: {known0[i][0]} -> {known0[i][1]}, {known1[i][0]} -> {known1[i][1]}')
            return known0[i]
    print('> FAIL.')
    sys.exit(1)


def attack (piv, p0, c0, known0, known1):
    for i in range(len(piv)):
        k0 = piv[i] ^ p0
        k1 = sbox[piv[i]] ^ c0
        bad = False
        print(f'KEY TEST: {(k0,k1)}')
        for pc in known0:
            if simplified_enc(pc[0], (k0, k1)) != pc[1]:
                bad = True
        for pc in known1:
            if simplified_enc(pc[0], (k0, k1)) != pc[1]:
                bad = True
        if bad: print('> Bad attempt')
        else: return (k0, k1)
    return None
    
if __name__ == '__main__':
    key = (random.randint(0, 15), random.randint(0, 15))
    print('Real key:', key)
    sbox_dc = compute_differential_characteristics()
    mpd_io = get_most_probable_diff_io(sbox_dc)
    in_diff, out_diff = mpd_io[random.randint(0, len(mpd_io) - 1)]
    piv = get_possible_intermediate_values((in_diff, out_diff))
    known0, known1 = generate_pairs(8, in_diff, key)
    p0, c0 = find_good_pair(known0, known1, out_diff)
    k = attack(piv, p0, c0, known0, known1)
    if k is None:
        print('> Attack failed.')
    else:
        if k == key:
            print(f'> SUCCESS! key is {k}')
        else:
            print(f'> Oups! {k} is not {key}')