def insertionSort(arr):
    for i in range(1, len(arr)):
        actual = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > actual:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = actual

def main():
    arr = [32, 17, 12, 6, 11, 5, 45]

    print("=== INSERTION SORT EN PYTHON ===")
    print(f"Array inicial: {arr}")

    insertionSort(arr.copy())

    arrSorted = arr.copy()
    insertionSort(arrSorted)
    print(f"Array final: {arrSorted}")

if __name__ == "__main__":
    main()