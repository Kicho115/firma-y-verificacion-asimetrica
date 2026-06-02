from user import User

def main():
    try:
        user = User()

        # Solicitar el mensaje al usuario
        message = input("Introduce el mensaje a firmar: ")
        if not message:
            raise Exception("El mensaje no puede estar vacio")

        # Firmar el mensaje
        signature = user.sign_message(message)
        print(f"\nFirma generada: {signature}")

        # Check para modificar el mensaje
        modified = input("Quieres modificar el mensaje original? (Enter para omitir): ")
        if modified:
            message = input("Introduce el mensaje modificado: ")

        # Verificar la firma
        is_valid = user.verify_signature(message, signature)
        print(f"\nLa firma es valida?: {'Si' if is_valid else 'No'}")

    except Exception as e:
        print(f"Error en el sistema: {e}")

if __name__ == "__main__":
    main()