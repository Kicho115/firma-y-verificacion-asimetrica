from keys import generate_keys
from signature import sign, verify
from main import prepare_message

def run_test_cases():
    # Valores comunes para las pruebas
    pub, priv = generate_keys() # Generar llaves
    n, _ = pub # Extraer n para preparar mensajes
    message = "Pruebas de firma digital" # Mensaje original para las pruebas
    msg_int = prepare_message(message, n) # Preparar el mensaje original
    signature = sign(msg_int, priv) # Firmar el mensaje original

    # Mensaje vacio
    print("\n1. Mensaje vacio... ")
    try:
        empty_msg = prepare_message("", n)
        if verify(empty_msg, signature, pub):
            print("Error: Acepto mensaje vacio (deberia fallar).")
        else:
            print("Exito: Mensaje vacio rechazado correctamente.")
    except Exception as e:
        print(f"Exito: El sistema atrapo el error: {e}")

    # Mensaje alterado
    print("\n2. Mensaje alterado... ")
    altered_msg = prepare_message("Mensaje alterado", n)
    if not verify(altered_msg, signature, pub):
        print("Exito: Firma invalida para mensaje alterado.")
    else:
        print("Error: Se acepto el mensaje alterado.")

    # Llave incorrecta
    print("\n3. Llave incorrecta... ")
    wrong_pub, _ = generate_keys()
    if not verify(msg_int, signature, wrong_pub):
        print("Exito: Firma invalida con llave incorrecta.")
    else:
        print("Error: Se acepto la firma con llave incorrecta.")

    # Firma incorrecta
    print("\n4. Firma incorrecta... ")
    wrong_signature = signature + 1  # Modificar la firma
    if not verify(msg_int, wrong_signature, pub):
        print("Exito: Se rechazo firma falsa invalida.")
    else:
        print("Error: Se acepto la firma falsa.")

    # Happy path: Firma valida
    print("\n5. Firma valida... ")
    if verify(msg_int, signature, pub):
        print("Exito: Firma valida verificada correctamente.")
    else:
        print("Error: No se pudo verificar una firma valida.")

if __name__ == '__main__':
    run_test_cases()

