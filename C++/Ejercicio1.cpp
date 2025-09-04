#include <iostream>
using namespace std;

int main() {
    // 1.Declarar un Array en C++
    int array1[5] = {0}; // Inicializado con ceros
    
    // 2.Inicializar un Array en C++
    int array2[] = {11, 12, 13, 14, 15};
    
    // Mostrar los arrays
    cout << "Array vacío: ";
    for (int i = 0; i < 5; i++) {
        cout << array1[i] << " ";
    }
    cout << endl;
    
    cout << "Array inicializado: ";
    for (int i = 0; i < 5; i++) {
        cout << array2[i] << " ";
    }
    cout << endl;
    
    return 0;
}