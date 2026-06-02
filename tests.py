from user import User

print("\nTESTS")

try:
    user = User()

    message = "Hola mundo"
    signature = user.sign_message(message)

    # Mensaje alterado
    other_user = User()
    print("\nTEST Mensaje alterado:", other_user.verify_signature("Hola mundo!", signature))

    # Llave incorrecta
    print("\nTEST Llave incorrecta:", other_user.verify_signature(message, signature))

    # Mensaje original (debe ser válido)
    print("\nTEST Mensaje original:", user.verify_signature(message, signature))
except Exception as e:
    print(f"\nERROR: {e}")