from message import prepare_message
from signature import sign, verify
from keys import generate_keys

print("\nTESTS")

message = "Hola mundo"
msg = prepare_message(message)
public_key, private_key = generate_keys()

signature = sign(msg, private_key)

# Mensaje alterado
altered = prepare_message("Hola mundo!")
print("\nTEST Mensaje alterado:", verify(altered, signature, public_key))

# Llave incorrecta
fake_key = (public_key[0], public_key[1] + 2)
print("\nTEST Llave incorrecta:", verify(msg, signature, fake_key))

# Mensaje vacío
empty = prepare_message("")
sig_empty = sign(empty, private_key)
print("\nTEST Mensaje vacío:", verify(empty, sig_empty, public_key))