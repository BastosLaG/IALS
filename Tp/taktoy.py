sbox = [3, 14, 1, 10, 4, 9, 5, 6, 8, 11, 15, 2, 13, 12, 0, 7]
# sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2] # from PRESENT
xobs = [14, 2, 11, 0, 4, 6, 7, 15, 8, 5, 3, 9, 13, 12, 1, 10]

def round (msg, subkey):
    return sbox[msg ^ subkey]

def enc (msg, key):
    t0 = round(msg, key[0])
    t1 = round(t0, key[1])
    return t1

def simplified_enc (msg, key):
    t0 = round(msg, key[0])
    return t0 ^ key[1]
