#include <iostream>
#include <string>
#include "src/BST.h"

using namespace std;

void mostrarMenu() {
    cout << "\n--- GESTOR DE NUMEROS BST ---" << endl;
    cout << "Comandos disponibles:" << endl;
    cout << "  insert <n>   : Insertar numero" << endl;
    cout << "  search <n>   : Buscar numero" << endl;
    cout << "  delete <n>   : Eliminar numero" << endl;
    cout << "  inorder      : Recorrido In-Orden" << endl;
    cout << "  preorder     : Recorrido Pre-Orden" << endl;
    cout << "  postorder    : Recorrido Post-Orden" << endl;
    cout << "  height       : Ver altura del arbol" << endl;
    cout << "  size         : Ver cantidad de nodos" << endl;
    cout << "  export       : Guardar en archivo" << endl;
    cout << "  help         : Mostrar este menu" << endl;
    cout << "  exit         : Salir" << endl;
    cout << "-----------------------------" << endl;
}

int main() {
    BST arbol;

    arbol.load_from_file("exportado.txt");
    string comando;
    int valor;

    mostrarMenu();

    while (true) {
        cout << "\nBST> ";
        cin >> comando;

        if (comando == "exit") {
            cout << "Cerrando aplicacion..." << endl;
            break;
        }
        else if (comando == "insert") {
            if (cin >> valor) {
                arbol.insert(valor);
            } else {
                cout << "Error: Se esperaba un numero entero." << endl;
                cin.clear();
                cin.ignore(1000, '\n');
            }
        }
        else if (comando == "search") {
            if (cin >> valor) {
                arbol.search(valor);
            } else {
                cout << "Error: Se esperaba un numero entero." << endl;
                cin.clear();
                cin.ignore(1000, '\n');
            }
        }
        else if (comando == "delete") {
            if (cin >> valor) {
                arbol.remove(valor);
            } else {
                cout << "Error: Se esperaba un numero entero." << endl;
                cin.clear();
                cin.ignore(1000, '\n');
            }
        }
        else if (comando == "inorder") {
            arbol.inorder();
        }
        else if (comando == "preorder") {
            arbol.preorder();
        }
        else if (comando == "postorder") {
            arbol.postorder();
        }
        else if (comando == "height") {
            arbol.height();
        }
        else if (comando == "size") {
            arbol.size();
        }
        else if (comando == "export") {
            arbol.export_inorder("exportado.txt");
        }
        else if (comando == "help") {
            mostrarMenu();
        }
        else {
            cout << "Comando no reconocido. Escribe 'help' para ver la lista." << endl;
            cin.clear();
            cin.ignore(1000, '\n');
        }
    }

    return 0;
}