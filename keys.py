import secrets
import math

def generate_keys():
    while True:
        p = generate_random_prime()
        q = generate_random_prime()

        while p == q:
            q = generate_random_prime()

        n = p * q # Este valor se comparte en ambas llaves

        # Totiente de euler
        tot = (p - 1) * (q - 1)

        e = 65537

        if (math.gcd(e, tot) != 1):
            continue
            
        d = multiplicative_inverse(e, tot)

        public_key = (n, e)
        private_key = (n, d)

        return public_key, private_key


def multiplicative_inverse(e, tot):
    gcd, x, _ = euclides(e, tot)
    if gcd != 1:
        raise ValueError("El inverso modular no existe")
    else:
        # Aseguramos que d sea positivo
        return x % tot

def euclides(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = euclides(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def is_prime(n):
    # Test de miller-rabin
    rounds = 40

    # Hallar r y d tal que n-1 = 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2 # Testigo entre 2 y n - 2 pq se genera con n - 3 y + 2
        x = pow(a, d, n) # b0   
        
        if x == 1 or x == n - 1:
            continue
        
        # pasamos por todos las potencias de 2 en n-1, como a^d ya esta, faltan r-1 pasos
        for _ in range(r - 1): # 
            # bi
            x = pow(x, 2, n)
            if x == n - 1:
                break
        # Si termina el for sin hacer break
        else:
            return False

    return True

def generate_random_number():
    bits = 1024
    n = secrets.randbits(bits)
    n = n | (1 << (bits - 1)) # Shift para asegurarse de que el bit mas significativo no sea cero (asegurar 1024 bits)
    n = n | 1 # OR en el bit menos significativo para forzar a que sea impar

    return n

def generate_random_prime():
    #i = 1
    while True:
        num = generate_random_number() 
        #print(f"candidato {i}: {num}")
            
        if is_prime(num):
            return num 
        
        #i = i + 1
