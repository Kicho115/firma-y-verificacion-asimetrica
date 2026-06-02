from user import User
from message import Message

def main():
    try:
        user = User()

        # Solicitar el mensaje al usuario
        content = input("Introduce el mensaje a firmar: ")
        if not content:
            raise Exception("El mensaje no puede estar vacio")

        # Crear el mensaje (se firma automáticamente)
        msg = Message(content, user)
        print(f"\nFirma generada: {msg.signature}")

        # Check para modificar el mensaje (simula una alteración del contenido original)
        modified = input("Quieres modificar el mensaje original? (Enter para omitir): ")
        if modified:
            msg.content = input("Introduce el mensaje modificado: ")

        # Verificar la firma
        is_valid = msg.verify()
        print(f"\nLa firma es valida?: {'Si' if is_valid else 'No'}")

    except Exception as e:
        print(f"Error en el sistema: {e}")

if __name__ == "__main__":
    main()