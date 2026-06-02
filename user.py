from keys import generate_keys
from signature import sign, verify
import hashlib


class User:
    def __init__(self):
        public_key, private_key = generate_keys()
        self.public_key = public_key
        self.private_key = private_key

    def prepare_message(self, message):
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

        n, _ = self.public_key
        return message_int % n

    def sign_message(self, message):
        # Firmar el mensaje usando la llave privada

        msg_int = self.prepare_message(message)
        signature = sign(msg_int, self.private_key)
        return signature

    def verify_signature(self, message, signature):
        # Verificar la firma de un mensaje usando la llave pública
        # Compara el hash recuperado con el hash del mensaje original

        msg_int = self.prepare_message(message)
        return verify(msg_int, signature, self.public_key)
