import os
from user import User
from message import Message


def main():
    try:
        alice = User("Alice")
        bob = User("Bob")
        print("Llaves generadas.\n")

        content = input("Escribir el mensaje para Bob: ").strip()

        if not content:
            print("Error: el mensaje no puede estar vacío.")
            return

        msg = Message(content, sender=alice, receiver=bob)

        json_payload = msg.to_json()

        print("\nPayload JSON")
        print(json_payload)

        try:
            received = Message.from_json(json_payload)

        except ValueError as e:
            print(f"Error al procesar el JSON: {e}")
            return

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

        received.receive(bob)

        os.makedirs("jsons", exist_ok=True)
        filename = "jsons/tampered.json" if modif == "s" else "jsons/valid.json"
        with open(filename, "w") as f:
            f.write(received.to_json())
        print(f"\nJSON guardado en {filename}")

    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")

    except Exception as e:
        print(
            f"\nSe produjo un error inesperado: "
            f"{type(e).__name__}: {e}"
        )


if __name__ == "__main__":
    main()