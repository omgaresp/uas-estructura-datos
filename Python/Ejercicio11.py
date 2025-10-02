def shellSort(arr):
    size = len(arr)
    gapSize = size // 2

    while gapSize > 0:
        for i in range(gapSize, size):
            temp = arr[i]
            j = i
            while j >= gapSize and arr[j - gapSize] > temp:
                arr[j] = arr[j - gapSize]
                j -= gapSize
            arr[j] = temp
        gapSize //= 2

def main():
    arr = [32, 17, 12, 6, 11, 5, 45]

    print("=== SHELL SORT EN PYTHON ===")
    print(f"Array inicial: {arr}")

    shellSort(arr)

    print(f"Array final: {arr}")

if __name__ == "__main__":
    main()