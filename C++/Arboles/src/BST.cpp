#include "BST.h"
#include <iostream>
#include <fstream>
#include <algorithm>

BST::BST() {
    root = nullptr;
}

BST::~BST() {
    destruirArbol(root);
}

void BST::destruirArbol(Nodo* nodo) {
    if (nodo != nullptr) {
        destruirArbol(nodo->left);
        destruirArbol(nodo->right);
        delete nodo;
    }
}

void BST::insert(int key) {
    bool exito = false;
    root = insertarRecursivo(root, key, exito);
    if (exito) {
        std::cout << "Exito: Nodo " << key << " insertado." << std::endl;
    } else {
        std::cout << "Error: El numero " << key << " ya existe en el arbol." << std::endl;
    }
}

void BST::search(int key) {
    std::cout << "Buscando ruta: ";
    bool encontrado = buscarRecursivo(root, key);
    if (encontrado) {
        std::cout << " -> ENCONTRADO" << std::endl;
    } else {
        std::cout << " -> NO EXISTE" << std::endl;
    }
}

void BST::remove(int key) {
    std::cout << "Intentando eliminar " << key << "..." << std::endl;
    root = eliminarRecursivo(root, key);
}

void BST::inorder() {
    std::cout << "In-Order: ";
    inordenRecursivo(root);
    std::cout << std::endl;
}

void BST::preorder() {
    std::cout << "Pre-Order: ";
    preordenRecursivo(root);
    std::cout << std::endl;
}

void BST::postorder() {
    std::cout << "Post-Order: ";
    postordenRecursivo(root);
    std::cout << std::endl;
}

void BST::height() {
    int h = calcularAltura(root);
    std::cout << "Altura del arbol: " << h << std::endl;
}

void BST::size() {
    int s = contarNodos(root);
    std::cout << "Total de nodos: " << s << std::endl;
}

void BST::export_inorder(std::string filename) {
    std::ofstream archivo(filename);
    if (archivo.is_open()) {
        exportarRecursivo(root, archivo);
        archivo.close();
        std::cout << "Arbol exportado a '" << filename << "' exitosamente." << std::endl;
    } else {
        std::cout << "Error al crear el archivo." << std::endl;
    }
}

void BST::load_from_file(std::string filename) {
    std::ifstream archivo(filename);
    if (archivo.is_open()) {
        int valor;
        bool ignorar_resultado;
        while (archivo >> valor) {
            root = insertarRecursivo(root, valor, ignorar_resultado);
        }
        archivo.close();
        std::cout << "Datos cargados desde '" << filename << "'." << std::endl;
    } else {
        std::cout << "No se encontro archivo de respaldo. Iniciando vacio." << std::endl;
    }
}

Nodo* BST::insertarRecursivo(Nodo* nodo, int valor, bool& exito) {
    // Caso base: Encontramos un hueco vacio -> INSERTAMOS
    if (nodo == nullptr) {
        exito = true;
        return new Nodo(valor);
    }

    // Regla BST: Menores a la izquierda, Mayores a la derecha
    if (valor < nodo->key) {
        nodo->left = insertarRecursivo(nodo->left, valor, exito);
    } else if (valor > nodo->key) {
        nodo->right = insertarRecursivo(nodo->right, valor, exito);
    }

    return nodo;
}

bool BST::buscarRecursivo(Nodo* nodo, int valor) {
    if (nodo == nullptr) {
        return false;
    }

    std::cout << nodo->key << " ";

    if (valor == nodo->key) {
        return true;
    }

    if (valor < nodo->key) {
        return buscarRecursivo(nodo->left, valor);
    } else {
        return buscarRecursivo(nodo->right, valor);
    }
}

Nodo* BST::eliminarRecursivo(Nodo* nodo, int valor) {
    if (nodo == nullptr) return nullptr;

    if (valor < nodo->key) {
        nodo->left = eliminarRecursivo(nodo->left, valor);
    } else if (valor > nodo->key) {
        nodo->right = eliminarRecursivo(nodo->right, valor);
    } else {

        // CASO 1: Hoja (sin hijos)
        if (nodo->left == nullptr && nodo->right == nullptr) {
            delete nodo;
            return nullptr;
        }
        // CASO 2: Un solo hijo
        else if (nodo->left == nullptr) {
            Nodo* temp = nodo->right;
            delete nodo;
            return temp;
        } else if (nodo->right == nullptr) {
            Nodo* temp = nodo->left;
            delete nodo;
            return temp;
        }
        // CASO 3: Dos hijos
        else {
            // Encontrar el sucesor (mínimo del subárbol derecho)
            Nodo* temp = encontrarMinimo(nodo->right);

            // Copiar el valor del sucesor al nodo actual
            nodo->key = temp->key;

            // Eliminar el sucesor original (que ahora es duplicado)
            nodo->right = eliminarRecursivo(nodo->right, temp->key);
        }
    }
    return nodo;
}

Nodo* BST::encontrarMinimo(Nodo* nodo) {
    Nodo* actual = nodo;
    // Bajar todo a la izquierda para encontrar el menor
    while (actual && actual->left != nullptr) {
        actual = actual->left;
    }
    return actual;
}


void BST::inordenRecursivo(Nodo* nodo) {
    if (nodo != nullptr) {
        inordenRecursivo(nodo->left);
        std::cout << nodo->key << " ";
        inordenRecursivo(nodo->right);
    }
}

void BST::preordenRecursivo(Nodo* nodo) {
    if (nodo != nullptr) {
        std::cout << nodo->key << " ";
        preordenRecursivo(nodo->left);
        preordenRecursivo(nodo->right);
    }
}

void BST::postordenRecursivo(Nodo* nodo) {
    if (nodo != nullptr) {
        postordenRecursivo(nodo->left);
        postordenRecursivo(nodo->right);
        std::cout << nodo->key << " ";
    }
}

int BST::calcularAltura(Nodo* nodo) {
    if (nodo == nullptr) return 0;
    return 1 + std::max(calcularAltura(nodo->left), calcularAltura(nodo->right));
}

int BST::contarNodos(Nodo* nodo) {
    if (nodo == nullptr) return 0;
    return 1 + contarNodos(nodo->left) + contarNodos(nodo->right);
}

void BST::exportarRecursivo(Nodo* nodo, std::ofstream& archivo) {
    if (nodo != nullptr) {
        exportarRecursivo(nodo->left, archivo);
        archivo << nodo->key << " ";
        exportarRecursivo(nodo->right, archivo);
    }
}