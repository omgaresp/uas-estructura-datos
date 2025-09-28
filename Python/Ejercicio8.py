def partition(arr, l, h):
    pvt = arr[h]

    j = l - 1

    for k in range(l, h):
        if arr[k] < pvt:
            j += 1
            swap(arr, j, k)

    swap(arr, j + 1, h)
    return j + 1


def swap(arr, j, k):
    arr[j], arr[k] = arr[k], arr[j]

def quickSort(arr, l, h):
    if l < h:
        pi = partition(arr, l, h)

        quickSort(arr, l, pi - 1)
        quickSort(arr, pi + 1, h)

def main():
    arr = [32, 17, 12, 6, 11, 5, 45]

    print("=== QUICK SORT EN PYTHON ===")
    print(f"Array inicial: {arr}")

    quickSort(arr.copy(), 0, len(arr) - 1)

    arrSorted = arr.copy()
    quickSort(arrSorted, 0, len(arrSorted) - 1)
    print(f"Array final: {arrSorted}")

if __name__ == "__main__":
    main()