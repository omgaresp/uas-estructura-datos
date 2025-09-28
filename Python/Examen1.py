entrada = input("Ingresa 10 números separados por comas (x,x,x,x,x,x,x,x,x,x): ")

numeros = [int(x.strip()) for x in entrada.split(',') if x.strip()]

if len(numeros) != 10:
    print(f"Error: Se esperaban 10 números, pero se ingresaron {len(numeros)}")
else:
    print("="*50)
    print("RESULTADO")
    print("="*50)

    print(f"Números en el mismo orden: {numeros}")

    print(f"Números en orden inverso: {numeros[::-1]}")

    suma = sum(numeros)
    promedio = suma / len(numeros)
    print(f"Suma: {suma}")
    print(f"Promedio: {promedio:.2f}")

    max = max(numeros)
    min = min(numeros)
    print(f"Número mayor: {max}")
    print(f"Número menor: {min}")

    pares = sum(1 for num in numeros if num % 2 == 0)
    impares = sum(1 for num in numeros if num % 2 != 0)
    print(f"Números pares: {pares}")
    print(f"Números impares: {impares}")

    print("="*50)