using System;
using System.Collections.Generic;

class Persona {
    public string Nombre { get; set; }
    public string Apellido1 { get; set; }
    public string Apellido2 { get; set; }
    
    public Persona(string nombre, string apellido1, string apellido2) {
        Nombre = nombre;
        Apellido1 = apellido1;
        Apellido2 = apellido2;
    }
}

// ARRAY NORMAL
Console.WriteLine("=== ARRAY NORMAL ===");
List<int> arrayNumeros = new List<int> {11, 12, 13, 14, 15};

Console.WriteLine("Recorrido inicial:");
for (int i = 0; i < arrayNumeros.Count; i++) {
    Console.WriteLine($"[{i}]: {arrayNumeros[i]}");
}

// Buscar el 12
Console.WriteLine("\nBuscando el valor 12:");
bool encontrado = false;
for (int i = 0; i < arrayNumeros.Count; i++) {
    if (arrayNumeros[i] == 12) {
        Console.WriteLine($"¡Encontrado! El valor 12 está en la posición {i}");
        encontrado = true;
        break;
    } else {
        Console.WriteLine($"Posición {i}: {arrayNumeros[i]} - No es 12");
    }
}

arrayNumeros.Insert(0, 20);

Console.WriteLine("\nRecorrido después de la inserción:");
for (int i = 0; i < arrayNumeros.Count; i++) {
    if (arrayNumeros[i] == 20) {
        Console.WriteLine($"[{i}]: {arrayNumeros[i]} ← NUEVO ELEMENTO INSERTADO");
    } else {
        Console.WriteLine($"[{i}]: {arrayNumeros[i]}");
    }
}

Console.WriteLine("\nRecorrido inverso:");
for (int i = arrayNumeros.Count - 1; i >= 0; i--) {
    Console.WriteLine($"[{i}]: {arrayNumeros[i]}");
}

// ARRAY CON TIPO DEFINIDO
Console.WriteLine("\n=== ARRAY CON TIPO DEFINIDO ===");
List<Persona> personas = new List<Persona> {
    new Persona("Juan", "García", "López"),
    new Persona("María", "Rodríguez", "Martín"),
    new Persona("Carlos", "Hernández", "Pérez")
};

Console.WriteLine("Recorrido inicial:");
for (int i = 0; i < personas.Count; i++) {
    Console.WriteLine($"[{i}]: {personas[i].Nombre} {personas[i].Apellido1} {personas[i].Apellido2}");
}

// Buscar a Juan
Console.WriteLine("\nBuscando a Juan:");
encontrado = false;
for (int i = 0; i < personas.Count; i++) {
    if (personas[i].Nombre == "Juan") {
        Console.WriteLine($"¡Encontrado! Juan está en la posición {i}");
        encontrado = true;
        break;
    } else {
        Console.WriteLine($"Posición {i}: {personas[i].Nombre} - No es Juan");
    }
}

personas.Insert(1, new Persona("Omar", "García", "Espinoza"));

Console.WriteLine("\nRecorrido después de la inserción:");
for (int i = 0; i < personas.Count; i++) {
    if (personas[i].Nombre == "Omar") {
        Console.WriteLine($"[{i}]: {personas[i].Nombre} {personas[i].Apellido1} {personas[i].Apellido2} ← NUEVA PERSONA INSERTADA");
    } else {
        Console.WriteLine($"[{i}]: {personas[i].Nombre} {personas[i].Apellido1} {personas[i].Apellido2}");
    }
}

Console.WriteLine("\nRecorrido inverso:");
for (int i = personas.Count - 1; i >= 0; i--) {
    Console.WriteLine($"[{i}]: {personas[i].Nombre} {personas[i].Apellido1} {personas[i].Apellido2}");
}