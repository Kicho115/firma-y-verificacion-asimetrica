import json
import base64
import cipher
from user import User


class Message:
    def __init__(self, content, sender, receiver):
        #1. Genera una session key aleatoria (256 bits)
        #2. Cifra el contenido con esa session key (XOR stream cipher)
        #3. Cifra la session key con la llave pública RSA del receptor
        #4. Firma el contenido original con la llave privada del emisor
        
        session_key = cipher.generate_session_key()

        self.encrypted_content = cipher.encrypt(content, session_key)

        session_key_int = int.from_bytes(session_key, "big")
        self.encrypted_session_key = sender.rsa_encrypt(
            session_key_int,
            receiver.public_key
        )

        self.signature = sender.sign_message(content)

        self.sender_public_key = sender.public_key
        self.sender_name = sender.name
        self.receiver_name = receiver.name

    def to_json(self):
        return json.dumps({
            "sender": self.sender_name,
            "receiver": self.receiver_name,
            "sender_public_key": {
                "n": str(self.sender_public_key[0]),
                "e": str(self.sender_public_key[1]),
            },
            "encrypted_content": base64.b64encode(
                self.encrypted_content
            ).decode(),
            "encrypted_session_key": str(self.encrypted_session_key),
            "hash_algorithm": "SHA-256",
            "signature": str(self.signature),
        }, indent=2)

    @classmethod
    def from_json(cls, json_str):
        obj = cls.__new__(cls)

        try:
            data = json.loads(json_str)

            obj.sender_name = data["sender"]
            obj.receiver_name = data["receiver"]

            obj.sender_public_key = (
                int(data["sender_public_key"]["n"]),
                int(data["sender_public_key"]["e"]),
            )

            obj.encrypted_content = base64.b64decode(
                data["encrypted_content"]
            )

            obj.encrypted_session_key = int(
                data["encrypted_session_key"]
            )

            obj.signature = int(data["signature"])

        # Errores para JSONs con formato incorrecto
        except json.JSONDecodeError:
            raise ValueError("El archivo JSON tiene un formato inválido.")

        except KeyError as e:
            raise ValueError(
                f"Falta el campo requerido en el JSON: {e}"
            )

        return obj

    def receive(self, receiver):
       
        # El receptor descifra y verifica el mensaje:
        # 1. Descifra la session key con su llave privada RSA
        # 2. Descifra el contenido con la session key recuperada
        # 3. Verifica la firma con la llave pública del emisor

        # Verificar que el receptor sea el destinatario correcto
        if receiver.name != self.receiver_name:
            print(
                f"Error: este mensaje fue enviado a "
                f"{self.receiver_name} y no a {receiver.name}."
            )
            return None, False

        # Descifrar la session key con RSA
        try:
            session_key_int = receiver.rsa_decrypt(
                self.encrypted_session_key
            )

            session_key = session_key_int.to_bytes(32, "big")

        # Errores de excepción
        except OverflowError:
            print("Error: la clave de sesión no pudo recuperarse. ")
            return None, False

        except Exception as e:
            print(f"Error al descifrar la clave de sesión: {e}")
            return None, False

        print("La clave de sesión fue recuperada correctamente.")

        # Descifrar el contenido
        try:
            content = cipher.decrypt(
                self.encrypted_content,
                session_key
            )

        except UnicodeDecodeError:
            print(
                "Error: el contenido del mensaje fue alterado o está corrupto y no puede descifrarse."
            )
            return None, False

        except Exception as e:
            print(f"Error al descifrar el contenido: {e}")
            return None, False

        print("El contenido fue descifrado correctamente.")

        # Verificar la firma digital
        try:
            is_valid = User.verify_signature(
                content,
                self.signature,
                self.sender_public_key
            )

        except Exception as e:
            print(f"Error durante la verificación de la firma: {e}")
            return None, False

        # Resultado
        print("\n-------------------------------")
        print(f"Emisor    : {self.sender_name}")
        print(f"Receptor  : {receiver.name}")
        print(f"Mensaje   : {content}")
        print(f"Firma     : " f"{'VÁLIDA' if is_valid else 'INVÁLIDA'}")
        print("-------------------------------")

        return content, is_valid