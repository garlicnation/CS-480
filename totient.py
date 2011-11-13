def gcd(a, b):
    "Euclid's Algorithm"
    while b:
        a, b = b, a%b
    return a