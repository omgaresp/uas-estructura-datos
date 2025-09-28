def bubbleSort(arr):
    n = len(arr)

    for i in range(n - 1):
        hubo_intercambio = False

        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                hubo_intercambio = True

        print(f"Pasada {i + 1}: {arr}")

        if not hubo_intercambio:
            print("Array ordenado.")
            break

def main():
    arr = [32, 17, 12, 6, 11, 5, 45]

    print("=== BUBBLE SORT EN PYTHON ===")
    print(f"Array inicial: {arr}")

    bubbleSort(arr.copy())

    arrSorted = arr.copy()
    bubbleSort(arrSorted)
    print(f"Array final: {arrSorted}")

if __name__ == "__main__":
    main()