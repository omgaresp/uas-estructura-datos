// Crear tipo definido / Clase
class Persona {
    constructor(nombre, apellido1, apellido2) {
        this.nombre = nombre;
        this.apellido1 = apellido1;
        this.apellido2 = apellido2;
    }
    
    toString() {
        return `${this.nombre} ${this.apellido1} ${this.apellido2}`;
    }
}

// Utilizarlo en un Array
let personas = [
    new Persona("Juan", "García", "López"),
    new Persona("María", "Rodríguez", "Martín"),
    new Persona("Carlos", "Hernández", "Pérez")
];

// Mostrar el array
console.log("Array de Personas:");
personas.forEach((persona, index) => {
    console.log(`[${index}]: ${persona.toString()}`);
});