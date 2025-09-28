def merge(arr, l, m, r):
    arr1 = m - l + 1
    arr2 = r - m

    tempL = [0] * arr1
    tempR = [0] * arr2

    for j in range(0, arr1):
        tempL[j] = arr[l + j]

    for k in range(0, arr2):
        tempR[k] = arr[m + 1 + k]

    i = 0
    j = 0
    k = l

    while i < arr1 and j < arr2:
        if tempL[i] <= tempR[j]:
            arr[k] = tempL[i]
            i += 1
        else:
            arr[k] = tempR[j]
            j += 1
        k += 1

    while i < arr1:
        arr[k] = tempL[i]
        i += 1
        k += 1

    while j < arr2:
        arr[k] = tempR[j]
        j += 1
        k += 1

def mergeSort(arr, l, r):
    if l < r:
        m = l + (r - l)//2

        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)
        merge(arr, l, m, r)

def main():
    arr = [32, 17, 12, 6, 11, 5, 45]

    print("=== MERGE SORT EN PYTHON ===")
    print(f"Array inicial: {arr}")

    mergeSort(arr.copy(), 0, len(arr) - 1)

    arrSorted = arr.copy()
    mergeSort(arrSorted, 0, len(arrSorted) - 1)
    print(f"Array final: {arrSorted}")

if __name__ == "__main__":
    main()