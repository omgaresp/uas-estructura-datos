#ifndef BST_H
#define BST_H

#include <string>
#include "nodo.h"

class BST {
private:
    Nodo* root;


    Nodo* insertarRecursivo(Nodo* nodo, int valor, bool& exito);
    Nodo* eliminarRecursivo(Nodo* nodo, int valor);
    Nodo* encontrarMinimo(Nodo* nodo);

    bool buscarRecursivo(Nodo* nodo, int valor);

    void inordenRecursivo(Nodo* nodo);
    void preordenRecursivo(Nodo* nodo);
    void postordenRecursivo(Nodo* nodo);

    int calcularAltura(Nodo* nodo);
    int contarNodos(Nodo* nodo);

    void exportarRecursivo(Nodo* nodo, std::ofstream& archivo);

    void destruirArbol(Nodo* nodo);

public:
    BST();
    ~BST();

    void insert(int key);
    void remove(int key);
    void search(int key);

    void inorder();
    void preorder();
    void postorder();

    void height();
    void size();

    void export_inorder(std::string filename);
    void load_from_file(std::string filename);
};

#endif