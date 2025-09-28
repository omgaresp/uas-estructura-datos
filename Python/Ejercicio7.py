def selectionSort(arr):
    for i in range(len(arr)):
        min_index = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

def main():
    arr = [32, 17, 12, 6, 11, 5, 45]

    print("=== SELECTION SORT EN PYTHON ===")
    print(f"Array inicial: {arr}")

    selectionSort(arr.copy())

    arrSorted = arr.copy()
    selectionSort(arrSorted)
    print(f"Array final: {arrSorted}")

if __name__ == "__main__":
    main()