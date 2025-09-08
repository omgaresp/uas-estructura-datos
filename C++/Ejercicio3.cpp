#include <iostream>
#include <vector>
#include <string>
using namespace std;

// Tipo definido Persona
struct Persona {
    string nombre;
    string apellido1;
    string apellido2;
    
    Persona(string n, string a1, string a2) : nombre(n), apellido1(a1), apellido2(a2) {}
};

int main() {
    
    // ARRAY NORMAL
    cout << "=== ARRAY NORMAL ===" << endl;
    vector<int> arrayNumeros = {11, 12, 13, 14, 15};
    
    cout << "Recorrido inicial:" << endl;
    for (int i = 0; i < arrayNumeros.size(); i++) {
        cout << "[" << i << "]: " << arrayNumeros[i] << endl;
    }
    
    // Buscar el 11
    cout << "\nBuscando el valor 11:" << endl;
    bool encontrado = false;
    for (int i = 0; i < arrayNumeros.size(); i++) {
        if (arrayNumeros[i] == 11) {
            cout << "¡Encontrado! El valor 11 está en la posición " << i << endl;
            encontrado = true;
            break;
        } else {
            cout << "Posición " << i << ": " << arrayNumeros[i] << " - No es 11" << endl;
        }
    }
    
    arrayNumeros.insert(arrayNumeros.begin() + 4, 19);
    
    cout << "\nRecorrido después de la inserción:" << endl;
    for (int i = 0; i < arrayNumeros.size(); i++) {
        if (arrayNumeros[i] == 19) {
            cout << "[" << i << "]: " << arrayNumeros[i] << " ← NUEVO ELEMENTO INSERTADO" << endl;
        } else {
            cout << "[" << i << "]: " << arrayNumeros[i] << endl;
        }
    }

    cout << "\nRecorrido inverso:" << endl;
    for (int i = arrayNumeros.size() - 1; i >= 0; i--) {
        cout << "[" << i << "]: " << arrayNumeros[i] << endl;
    }
    
    // ARRAY CON TIPO DEFINIDO
    cout << "\n=== ARRAY CON TIPO DEFINIDO ===" << endl;
    vector<Persona> personas = {
        Persona("Juan", "García", "López"),
        Persona("María", "Rodríguez", "Martín"),
        Persona("Carlos", "Hernández", "Pérez")
    };
    
    cout << "Recorrido inicial:" << endl;
    for (int i = 0; i < personas.size(); i++) {
        cout << "[" << i << "]: " << personas[i].nombre << " " << personas[i].apellido1 << " " << personas[i].apellido2 << endl;
    }
    
    // Buscar a María
    cout << "\nBuscando a María:" << endl;
    encontrado = false;
    for (int i = 0; i < personas.size(); i++) {
        if (personas[i].nombre == "María") {
            cout << "¡Encontrada! María está en la posición " << i << endl;
            encontrado = true;
            break;
        } else {
            cout << "Posición " << i << ": " << personas[i].nombre << " - No es María" << endl;
        }
    }
    
    personas.insert(personas.begin() + 3, Persona("Omar", "García", "Espinoza"));
    
    cout << "\nRecorrido después de la inserción:" << endl;
    for (int i = 0; i < personas.size(); i++) {
        if (personas[i].nombre == "Omar") {
            cout << "[" << i << "]: " << personas[i].nombre << " " << personas[i].apellido1 << " " << personas[i].apellido2 << " ← NUEVA PERSONA INSERTADA" << endl;
        } else {
            cout << "[" << i << "]: " << personas[i].nombre << " " << personas[i].apellido1 << " " << personas[i].apellido2 << endl;
        }
    }

    cout << "\nRecorrido inverso:" << endl;
    for (int i = personas.size() -1; i >= 0; i--) {
        cout << "[" << i << "]: " << personas[i].nombre << " " << personas[i].apellido1 << " " << personas[i].apellido2 << endl;
    }
    
    return 0;
}