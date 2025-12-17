#ifndef NODO_H
#define NODO_H

struct Nodo {
    int key;       // Valor del nodo
    Nodo* left;    // Puntero al subárbol izquierdo
    Nodo* right;   // Puntero al subárbol derecho

    // Constructor para facilitar la creación de nodos
    Nodo(int valor) {
        key = valor;
        left = nullptr;
        right = nullptr;
    }
};

#endif