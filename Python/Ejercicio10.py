def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heapSort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

def main():
    arr = [32, 17, 12, 6, 11, 5, 45]

    print("=== MERGE SORT EN PYTHON ===")
    print(f"Array inicial: {arr}")

    heapSort(arr.copy())

    arrSorted = arr.copy()
    heapSort(arrSorted)
    print(f"Array final: {arrSorted}")

if __name__ == "__main__":
    main()