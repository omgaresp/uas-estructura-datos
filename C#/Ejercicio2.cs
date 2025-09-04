using System;

// 1.Crear tipo definido / Clase
class Persona {
    public string Nombre { get; set; }
    public string Apellido1 { get; set; }
    public string Apellido2 { get; set; }

    public Persona(string nombre, string apellido1, string apellido2) {
        Nombre = nombre;
        Apellido1 = apellido1;
        Apellido2 = apellido2;
    }

    public override string ToString() {
        return $"{Nombre} {Apellido1} {Apellido2}";
    }
}

// 2.Utilizarlo en un Array (Da error por el IntelliSense al parecer y porque estoy usando dotnet-scripts)
Persona[] personas = {
    new Persona("Juan", "García", "López"),
    new Persona("María", "Rodríguez", "Martín"),
    new Persona("Carlos", "Hernández", "Pérez")
};

// Mostrar el array
Console.WriteLine("Array de Personas:");
for (int i = 0; i < personas.Length; i++) {
    Console.WriteLine($"[{i}]: {personas[i]}");
}