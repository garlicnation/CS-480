class Prime(dict):

    def __init__(self):
        dict.__init__(self)
        self[1] = False
        self[2] = True

    def primelist(self):
        x = 2
        while True:
            if self[x]:
                yield x
            x+=1
    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        else:
            if isPrime(key):
                self[key] = True
            else:
                self[key] = False
            return dict.__getitem__(self, key)

def isPrime(n):
    if (n<2):
        return False    
    if (n%2==0):
        return False
    
    for i in range(3,n/2,2):
        if (n%i==0):
            return False
    return True
    
primes = Prime()

def pfactorsbrute(n):
    current = n
    primefactors = dict()
    prime = 2
    for prime in primes.primelist():
        if primes[current]:
            break
        else:
            while not primes[current] and (current%prime) == 0:
                current = current/prime
                if prime in primefactors:
                    primefactors[prime]+=1
                else:
                    primefactors[prime]=1
              
    if current in primefactors:
            primefactors[current] += 1
    else:
#        print "Setting primefactors @ %d to 1" % current
        primefactors[current] = 1
    return primefactors

def gcd(a, b):
    "Euclid's Algorithm"
    while b:
        a, b = b, a%b
    return a

def totient(n):
    print "Totient of ", n
    """
    Compute the number of positives < n that are
    relatively prime to n -- good solution!
    """
    # Case 1. n == 1
    if n == 1:
        print "Case 1"
        return 0
    
    factors = pfactorsbrute(n)
    #Case 2. n is prime
    if len(factors) == 0:
        print "Case 2"
        return n-1
    
    #Case 3. n has two relatively prime factors
    if len(factors) == 2:
        mn = []
        for factor in factors:
            exp = factors[factor]
            mn.append(factor**exp)
            
        if gcd(mn[0], mn[1]) == 1:
            print "Case 3. %d and %d are coprime" % (mn[0], mn[1])
            return totient(mn[0])*totient(mn[1])
    
    print "Cases 4 and 5"    
    components = []
    for factor in factors:
        exp = factors[factor]
        components.append(factor**exp - factor**(exp-1))
    
    print "Prime factors: %s" % (factors)    
    tot = reduce(lambda x, y: x*y, components)
    return tot

if __name__ == "__main__":
    print totient(240)
    print
    print totient(13)
    print
    print totient(10)
    print
    print totient(49)