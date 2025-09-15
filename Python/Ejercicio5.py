def bubble_sort_with_visualization(arr):
    n = len(arr)
    
    for i in range(n - 1):
        hubo_intercambio = False
        
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                # Intercambiar
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
    
    bubble_sort_with_visualization(arr.copy())
    
    # Mostrar resultado final
    arr_sorted = arr.copy()
    bubble_sort_with_visualization(arr_sorted)
    print(f"Array final: {arr_sorted}")

if __name__ == "__main__":
    main()