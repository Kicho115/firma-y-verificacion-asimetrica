import secrets
import hashlib


def generate_session_key():
    # Genera una clave de sesión aleatoria de 256 bits (32 bytes)
    # Esta clave se usará para cifrar el mensaje con un cifrado simétrico educativo
    return secrets.token_bytes(32)


def _expand_key(key, length):
    # Expande la clave usando SHA-256 en modo contador para generar un keystream
    # del largo necesario para cubrir el mensaje completo
    # Se concatena la clave con un contador de 4 bytes y se hashea repetidamente

    keystream = b""
    counter = 0
    while len(keystream) < length:
        keystream += hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
        counter += 1
    return keystream[:length]


def encrypt(plaintext, key):
    # Cifra el mensaje usando XOR con un keystream derivado de la clave de sesión
    # 1. Convierte el texto plano a bytes
    # 2. Expande la clave para igualar la longitud del mensaje
    # 3. Aplica XOR byte a byte entre el mensaje y el keystream

    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")

    keystream = _expand_key(key, len(plaintext))
    ciphertext = bytes(a ^ b for a, b in zip(plaintext, keystream))
    return ciphertext


def decrypt(ciphertext, key):
    # Descifra el mensaje aplicando XOR con el mismo keystream
    # El proceso es idéntico al cifrado por la propiedad del XOR

    keystream = _expand_key(key, len(ciphertext))
    plaintext_bytes = bytes(a ^ b for a, b in zip(ciphertext, keystream))
    return plaintext_bytes.decode("utf-8")
