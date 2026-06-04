import json as json_module
import os
import sys

from message import Message
from user import User

KEYS_DIR = "keys"
JSONS_DIR = "jsons"


def _save_user_keys(user):
    key_file = os.path.join(KEYS_DIR, f"{user.name}.json")
    if os.path.exists(key_file):
        return
    os.makedirs(KEYS_DIR, exist_ok=True)
    with open(key_file, "w") as f:
        json_module.dump(
            {
                "name": user.name,
                "public_key": {
                    "n": str(user.public_key[0]),
                    "e": str(user.public_key[1]),
                },
                "private_key": {
                    "n": str(user.private_key[0]),
                    "d": str(user.private_key[1]),
                },
            },
            f,
            indent=2,
        )


def _load_user(name):
    key_file = os.path.join(KEYS_DIR, f"{name}.json")
    if not os.path.exists(key_file):
        return None
    with open(key_file) as f:
        data = json_module.load(f)
    return User(
        name=data["name"],
        public_key=(int(data["public_key"]["n"]), int(data["public_key"]["e"])),
        private_key=(int(data["private_key"]["n"]), int(data["private_key"]["d"])),
    )


def _cli_mode(filepath):
    if not os.path.exists(filepath):
        print(f"Error: archivo '{filepath}' no encontrado.")
        return

    with open(filepath) as f:
        json_str = f.read()

    try:
        received = Message.from_json(json_str)
    except ValueError as e:
        print(f"Error al procesar el JSON: {e}")
        return

    albert = _load_user(received.receiver_name)
    if albert is None:
        print(
            f"Error: no hay llaves guardadas para '{received.receiver_name}'.\n"
            f"Ejecuta primero el modo interactivo para generarlas."
        )
        return

    received.receive(albert)


def _interactive_mode():
    einstein = _load_user("einstein") or User("einstein")
    albert = _load_user("albert") or User("albert")
    print("Llaves generadas.\n")

    _save_user_keys(einstein)
    _save_user_keys(albert)

    content = input("Escribir el mensaje para albert: ").strip()

    if not content:
        print("Error: el mensaje no puede estar vacío.")
        return

    msg = Message(content, sender=einstein, receiver=albert)

    json_payload = msg.to_json()

    print("\nPayload JSON")
    print(json_payload)

    try:
        received = Message.from_json(json_payload)

    except ValueError as e:
        print(f"Error al procesar el JSON: {e}")
        return

    modif = (
        input("\n¿Simular alteración del mensaje en tránsito? (s/n): ").strip().lower()
    )

    if modif == "s":
        tampered = bytearray(received.encrypted_content)

        if len(tampered) > 0:
            tampered[0] ^= 0xFF

        received.encrypted_content = bytes(tampered)

        print("(Atacante: primer byte del contenido cifrado modificado)\n")

    received.receive(albert)

    os.makedirs(JSONS_DIR, exist_ok=True)
    filename = os.path.join(
        JSONS_DIR, "tampered.json" if modif == "s" else "valid.json"
    )
    with open(filename, "w") as f:
        f.write(received.to_json())
    print(f"\nJSON guardado en {filename}")


def main():
    try:
        if len(sys.argv) > 1:
            _cli_mode(sys.argv[1])
        else:
            _interactive_mode()

    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")

    except Exception as e:
        print(f"\nSe produjo un error inesperado: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
