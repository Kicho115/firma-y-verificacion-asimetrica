def sign(message_hash, private_key):
    n, d = private_key
    signature = pow(message_hash, d, n) # (message ** d) % n
    return signature


def verify(message_hash, signature, public_key):
    n, e = public_key
    recovered = pow(signature, e, n) # (firma ** e) % n
    print("\nHash del mensaje recibido: ", message_hash)
    print("\nHash del mensaje generado: ", recovered)

    return recovered == message_hash


def rsa_encrypt(data, public_key):
    # Cifra un entero usando RSA con la llave pública (n, e)
    # Se usa para cifrar la clave de sesión con la llave pública del receptor

    n, e = public_key
    return pow(data, e, n)


def rsa_decrypt(data, private_key):
    # Descifra un entero usando RSA con la llave privada (n, d)
    # Se usa para recuperar la clave de sesión con la llave privada del receptor

    n, d = private_key
    return pow(data, d, n)