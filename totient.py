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
    """
    Compute the number of positives < n that are
    relatively prime to n -- good solution!
    """
    if n == 1:
        return 0
    
    factors = pfactorsbrute(n)
    if len(factors) == 0:
        return n-1
    
    case2 = False
    if len(factors) == 2:
        case2 = True
        mn = []
        for factor in factors:
            if factors[factor] != 1:
                case2 = False
            else:
                mn.append(factor)
    
    if case2:
        return totient(mn[0]) * totient(mn[1])
        
    components = []
    for factor in factors:
        exp = factors[factor]
        components.append(factor**exp - factor**(exp-1))
        
    tot = reduce(lambda x, y: x*y, components)
    return tot

if __name__ == "__main__":
    print pfactorsbrute(240)
    print totient(240)