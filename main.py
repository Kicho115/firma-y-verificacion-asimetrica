from keys import generate_keys
from signature import sign, verify

public_key, private_key = generate_keys()

message = 123456789 # @ricardo aqui deberiamos poder poner texto y aplicar hash para luego firmarlo 

signature = sign(message, private_key)

if (verify(message, signature, public_key)):
    print("La firma es valida")
else:
    print("La firma NO es valida")