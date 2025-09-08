#include <iostream>
#include <string>
using namespace std;

// Crear tipo definido / Struct
struct Persona {
    string nombre, apellido1, apellido2;
    
    Persona(string n, string a1, string a2) {
        nombre = n;
        apellido1 = a1;
        apellido2 = a2;
    }
    
    string toString() {
        return nombre + " " + apellido1 + " " + apellido2;
    }
};

// Utilizarlo en un Array
int main() {
    Persona personas[3] = {
        Persona("Juan", "García", "López"),
        Persona("María", "Rodríguez", "Martín"),
        Persona("Carlos", "Hernández", "Pérez")
    };
    
    // Mostrar el array
    cout << "Array de Personas:" << endl;
    for (int i = 0; i < 3; i++) {
        cout << "[" << i << "]: " << personas[i].toString() << endl;
    }
    
    return 0;
}