def sign(message_hash, private_key):
    n, d = private_key
    signature = pow(message_hash, d, n) # (message ** d) % n
    return signature


def verify(message_hash, signature, public_key):
    n, e = public_key
    recovered = pow(signature, e, n) # (firma ** e) % n

    return recovered == message_hash