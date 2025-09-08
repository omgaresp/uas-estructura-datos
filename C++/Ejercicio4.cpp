#include <iostream>
#include <iomanip>

using namespace std;

int main() {
    // Declarar e Inicializar la Matriz
    int matriz[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    cout << "Matriz 3x3:" << endl;
    for (int i = 0; i < 3; i++) {
        cout << "[";
        for (int j = 0; j < 3; j++) {
            cout << matriz[i][j];
            if (j < 2) cout << ", ";
        }
        cout << "]" << endl;
    }

    cout << "\n=== Recorrido Horizontal ===" << endl;
    for (int i = 0; i < 3; i++) { // Filas
        for (int j = 0; j < 3; j++) { // Columnas
            cout << "[" << i << "][" << j << "]: " << matriz[i][j] << endl;
        }
    }

    cout << "\n=== Recorrido Vertical ===" << endl;
    for (int j = 0; j < 3; j++) {  // Columnas
        for (int i = 0; i < 3; i++) {  // Filas
            cout << "[" << i << "][" << j << "]: " << matriz[i][j] << endl;
        }
    }

    return 0;
}