from signature import verify
import hashlib


class Message:
    def __init__(self, content, sender):
        # La firma generada por el remitente
        # La llave pública del remitente para verificar después
        self.content = content
        self.sender_public_key = sender.public_key
        self.signature = sender.sign_message(content)

    def verify(self):
        # Verificar la firma del mensaje usando la llave pública del remitente
        # Compara el hash recuperado con el hash del mensaje original
        # Es necesario transformar el mensaje a un entero < n para evitar
        # desbordamiento y garantizar que la operación modular sea válida
        # Para preparar el mensaje se necesita
        # 1. Validar que no sea in input vacío
        # 2. Convertir el mensaje a un hash usando SHA-256
        # 3. Convertir el hash a un entero
        # 4. Reducir el entero módulo n para asegurarnos de que el mensaje hash se ajuste al tamaño de la clave

        if not isinstance(self.content, str):
            raise Exception("El mensaje debe ser una cadena de texto")
        if self.content == "":
            raise Exception("El mensaje no puede estar vacio")

        hashed = hashlib.sha256(self.content.encode()).digest()
        message_int = int.from_bytes(hashed)

        n, _ = self.sender_public_key
        msg_int = message_int % n

        return verify(msg_int, self.signature, self.sender_public_key)
