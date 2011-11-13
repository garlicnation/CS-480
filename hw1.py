alphabet = 'abcdefghijklmnopqrstuvwxyz'

letter_lookup_table=dict()
number_lookup_table = [" "]

for i in range(1,len(alphabet)+1):
    letter_lookup_table[alphabet[i-1]] = i
    letter_lookup_table[alphabet[i-1].upper()] = i
    
    number_lookup_table.append(alphabet[i-1])
    

def letters_to_numbers(string):
    ret = []
    for letter in string:
        if letter in letter_lookup_table:
            ret.append(letter_lookup_table[letter])
    return ret


def gcd(a,b):
    if a == 0:
        return b
    while not b == 0:
        if a>b:
            a = a-b
        else:
            b = b-a
    return a

def extended_gcd(a, b):
    x, y = 0, 1
    lastx, lasty = 1, 0
    while b != 0:
        #print "Dividend: %d Divisor: %d Quotient: %d Remainder: %d x: %d y: %d" % (a, b, a//b, a%b, x, y)
        quotient = a//b
        a, b = b, a%b
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastx, lasty

def mult_inverses(i):
    stuff = [x for x in range(i) if gcd(x,i) == 1]
    #print stuff
    return [(x, extended_gcd(x,i)[0] % i) for x in stuff]

def additive_encrypt(string, key):
    return [(letter+key)%26 for letter in letters_to_numbers(string)]

def additive_decrypt(string, key):
    return [number_lookup_table[(number-key)%26] for number in string]

def mult_encrypt(string, key):
    return [(letter*key[0])%26 for letter in letters_to_numbers(string)]

def mult_decrypt(string, key):
    return [number_lookup_table[(number*key[1])%26] for number in string]

def aff_encrypt(string, key):
    return [(letter*key[0][0] + key[1])%26 for letter in letters_to_numbers(string)]

def aff_decrypt(string, key):
    return [number_lookup_table[(number*key[0][1] - key[1])%26] for number in string]  


        

if  __name__ == "__main__":
    z34 = range(34)
    add_inverses_z34 = [(0,0)]+[(i,34-i) for i in range(18)]
    
    z34_s = mult_inverses(34)
    
    print z34
    print add_inverses_z34
    print z34_s
    
    print extended_gcd(80979, 323)[1]%80979
    
    plaintext="This is an exercise"
    
    ciphertext =  additive_encrypt(plaintext,15)
    print ciphertext
    
    decipheredtext = additive_decrypt(ciphertext,15)
    print "%s" % str(decipheredtext)
    
    mult_key = mult_inverses(26)
    key = 7
    
    for inverse in mult_key:
        if inverse[0] == key:
            key = inverse
            break
        
    ciphertext = mult_encrypt(plaintext,key)
    decipheredtext = mult_decrypt(ciphertext,key)
    
    print ciphertext
    print decipheredtext
    
    key = [11,13]
    for inverse in mult_key:
        if inverse[0] == key[0]:
            key[0] = inverse
            break
        
    ciphertext = aff_encrypt(plaintext,key)
    decipheredtext = aff_decrypt(ciphertext,key)
    
    print ciphertext
    print decipheredtext
    
    print [number_lookup_table[i] for i in [8, 16, 12, 4, 10, 3, 7, 9, 6, 14, 1, 13, 5, 15, 2, 11]]