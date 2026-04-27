from keys import generate_keys
from signature import sign, verify
import hashlib

# Es necesario transformar el mensaje a un entero < n para evitar
# desbordamiento y garantizar que la operación modular sea válida.
def prepare_message(message, n):
    # Para preparar el mensaje se necesita
    # 1. Validar que no sea in input vacío
    # 2. Convertir el mensaje a un hash usando SHA-256
    # 3. Convertir el hash a un entero
    # 4. Reducir el entero módulo n para asegurarnos de que el mensaje hash se ajuste al tamaño de la clave
    # 5. Tiene que retornar el mensaje preparado como un entero

    # 1
    if not isinstance(message, str):
        raise Exception("El mensaje debe ser una cadena de texto")
    if message == "":
        raise Exception("El mensaje no puede estar vacio")

    # 2 y 3
    hash_object = hashlib.sha256(message.encode("utf-8"))
    hash_hex = hash_object.hexdigest()
    message_int = int(hash_hex, 16)

    # 4 y 5 - SHA256 hex -> int mod n
    return message_int % n

def main():
    try:
        # Generar las claves
        public_key, private_key = generate_keys()
        n, _ = public_key

        # Solicitar el mensaje al usuario
        message = input("Introduce el mensaje a firmar: ")
        if not message:
            raise Exception("El mensaje no puede estar vacio")

        # Preparar el mensaje
        msg_int = prepare_message(message, n)

        # Firmar el mensaje
        signature = sign(msg_int, private_key)
        print(f"\nFirma generada: {signature}")

        # Verificar la firma
        is_valid = verify(msg_int, signature, public_key)
        print(f"\nLa firma es valida?: {'Si' if is_valid else 'No'}")

    except Exception as e:
        print(f"Error en el sistema: {e}")

if __name__ == "__main__":
    main()