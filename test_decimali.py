# Test della funzione converti_decimale

def converti_decimale(valore_str):
    """Converte stringhe con virgola o punto in float"""
    if not valore_str:
        return None

    # Rimuove spazi
    valore_str = str(valore_str).strip()

    if not valore_str:
        return None

    try:
        # Sostituisce virgola con punto
        valore_str = valore_str.replace(',', '.')
        return float(valore_str)
    except ValueError:
        return None

# Test della funzione
test_cases = [
    "200,34",      # Virgola italiana
    "200.34",      # Punto inglese
    "150,5",       # Una cifra decimale con virgola
    "150.5",       # Una cifra decimale con punto
    "1000,00",     # Zero decimali con virgola
    "1000.00",     # Zero decimali con punto
    "25",          # Solo intero
    "",            # Stringa vuota
    None,          # None
    "abc",         # Stringa non numerica
]

print("Test conversione decimali:")
print("=" * 40)

for test in test_cases:
    risultato = converti_decimale(test)
    print(f"Input: '{test}' -> Output: {risultato}")

print("=" * 40)
print("Test completati!")