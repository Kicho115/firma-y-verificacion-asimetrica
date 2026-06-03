from user import User
from message import Message


def main():
    try:
        # Crear a Alice y Bob con sus pares de llaves RSA
        alice = User("Alice")
        bob = User("Bob")
        print("Llaves generadas.\n")

        # Alice escribe el mensaje para Bob
        content = input("Escribir el mensaje para Bob: ").strip()

        if not content:
            print("Error: el mensaje no puede estar vacío.")
            return

        # Alice crea el mensaje
        msg = Message(
            content,
            sender=alice,
            receiver=bob
        )

        # Serializar a JSON
        json_payload = msg.to_json()

        print("\nPayload JSON")
        print(json_payload)

        # Reconstruir mensaje desde JSON
        try:
            received = Message.from_json(json_payload)

        except ValueError as e:
            print(f"Error al procesar el JSON: {e}")
            return

        # Simular modificación del contenido cifrado
        modif = input(
            "\n¿Simular alteración del mensaje en tránsito? (s/n): "
        ).strip().lower()

        if modif == "s":
            tampered = bytearray(received.encrypted_content)

            if len(tampered) > 0:
                tampered[0] ^= 0xFF

            received.encrypted_content = bytes(tampered)

            print(
                "(Atacante: primer byte del contenido cifrado modificado)\n"
            )

        # Bob recibe, descifra y verifica
        received.receive(bob)

    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")

    except Exception as e:
        print(
            f"\nSe produjo un error inesperado: "
            f"{type(e).__name__}: {e}"
        )


if __name__ == "__main__":
    main()