// Tipo definido Persona
class Persona {
    constructor(nombre, apellido1, apellido2) {
        this.nombre = nombre;
        this.apellido1 = apellido1;
        this.apellido2 = apellido2;
    }
}

// ARRAY NORMAL
console.log("=== ARRAY NORMAL ===");
let arrayNumeros = [11, 12, 13, 14, 15];

console.log("Recorrido inicial:");
arrayNumeros.forEach((numero, i) => {
    console.log(`[${i}]: ${numero}`);
});

// Buscar el 14
console.log("\nBuscando el valor 14:");
let encontrado = false;
for (let i = 0; i < arrayNumeros.length; i++) {
    if (arrayNumeros[i] === 14) {
        console.log(`¡Encontrado! El valor 14 está en la posición ${i}`);
        encontrado = true;
        break;
    } else {
        console.log(`Posición ${i}: ${arrayNumeros[i]} - No es 14`);
    }
}

arrayNumeros.splice(3, 0, 17);

console.log("\nRecorrido después de la inserción:");
arrayNumeros.forEach((numero, i) => {
    if (numero === 17) {
        console.log(`[${i}]: ${numero} ← NUEVO ELEMENTO INSERTADO`);
    } else {
        console.log(`[${i}]: ${numero}`);
    }
});

console.log("\nRecorrido inverso:");
/* El indice no se muestra inverso, investigue y es porque el toReversed() "crea" otro array igual solo que inverso
arrayNumeros.toReversed().forEach((numero, i) => {
    console.log(`[${i}]: ${numero}`);
});
*/
for (let i = arrayNumeros.length - 1; i >= 0; i--) {
    console.log(`[${i}]: ${arrayNumeros[i]}`);
}

// ARRAY CON TIPO DEFINIDO
console.log("\n=== ARRAY CON TIPO DEFINIDO ===");
let personas = [
    new Persona("Juan", "García", "López"),
    new Persona("María", "Rodríguez", "Martín"),
    new Persona("Carlos", "Hernández", "Pérez")
];

console.log("Recorrido inicial:");
personas.forEach((persona, i) => {
    console.log(`[${i}]: ${persona.nombre} ${persona.apellido1} ${persona.apellido2}`);
});

// Buscar a Carlos
console.log("\nBuscando a Carlos:");
encontrado = false;
for (let i = 0; i < personas.length; i++) {
    if (personas[i].nombre === "Carlos") {
        console.log(`¡Encontrado! Carlos está en la posición ${i}`);
        encontrado = true;
        break;
    } else {
        console.log(`Posición ${i}: ${personas[i].nombre} - No es Carlos`);
    }
}

personas.splice(0, 0, new Persona("Omar", "García", "Espinoza"));

console.log("\nRecorrido después de la inserción:");
personas.forEach((persona, i) => {
    if (persona.nombre === "Omar") {
        console.log(`[${i}]: ${persona.nombre} ${persona.apellido1} ${persona.apellido2} ← NUEVA PERSONA INSERTADA`);
    } else {
        console.log(`[${i}]: ${persona.nombre} ${persona.apellido1} ${persona.apellido2}`);
    }
});

console.log("\nRecorrido inverso:");
/* El indice no se muestra inverso, investigue y es porque el toReversed() "crea" otro array igual solo que inverso
personas.toReversed().forEach((persona, i) => {
    console.log(`[${i}]: ${persona.nombre} ${persona.apellido1} ${persona.apellido2}`);
});
*/
for (let i = personas.length - 1; i >= 0; i--) {
    const persona = personas[i];
    console.log(`[${i}]: ${persona.nombre} ${persona.apellido1} ${persona.apellido2}`);
}