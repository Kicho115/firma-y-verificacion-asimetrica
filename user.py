from keys import generate_keys
from signature import sign, verify, rsa_encrypt, rsa_decrypt
import hashlib


class User:
    def __init__(self, name="Usuario", public_key=None, private_key=None):
        self.name = name
        if public_key is not None and private_key is not None:
            self.public_key = public_key
            self.private_key = private_key
        else:
            public_key, private_key = generate_keys()
            self.public_key = public_key
            self.private_key = private_key

    @staticmethod
    def prepare_message(message, public_key):
        # Es necesario transformar el mensaje a un entero < n para evitar
        # desbordamiento y garantizar que la operación modular sea válida
        # Para preparar el mensaje se necesita
        # 1. Validar que no sea in input vacío
        # 2. Convertir el mensaje a un hash usando SHA-256
        # 3. Convertir el hash a un entero
        # 4. Reducir el entero módulo n para asegurarnos de que el mensaje hash se ajuste al tamaño de la clave

        if not isinstance(message, str):
            raise Exception("El mensaje debe ser una cadena de texto")
        if message == "":
            raise Exception("El mensaje no puede estar vacio")

        hashed = hashlib.sha256(message.encode()).digest()
        message_int = int.from_bytes(hashed)

        n, _ = public_key
        return message_int % n

    def sign_message(self, message):
        # Firmar un mensaje usando la llave privada
        msg_int = self.prepare_message(message, self.public_key)
        signature = sign(msg_int, self.private_key)
        return signature

    @staticmethod
    def verify_signature(message, signature, public_key):
        # Verificar la firma de un mensaje usando la llave pública
        # Compara el hash recuperado con el hash del mensaje original

        msg_int = User.prepare_message(message, public_key)
        return verify(msg_int, signature, public_key)

    def rsa_encrypt(self, data, target_pubkey):
        return rsa_encrypt(data, target_pubkey)

    def rsa_decrypt(self, data):
        return rsa_decrypt(data, self.private_key)

    def get_public_key_dict(self):
        n, e = self.public_key
        return {
            "n": str(n),
            "e": str(e)
        }