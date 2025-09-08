// Declarar e Inicializar la Matriz
const matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

console.log("Matriz 3x3:");
for (let i = 0; i < matriz.length; i++) {
    console.log(matriz[i]);
}

console.log("\n=== Recorrido Horizontal ===");
for (let i = 0; i < matriz.length; i++) { // Filas
    for (let j = 0; j < matriz[i].length; j++) { // Columnas
        console.log(`[${i}][${j}]: ${matriz[i][j]}`);
    }
}

console.log("\n=== Recorrido Vertical ===");
for (let j = 0; j < matriz[0].length; j++) {  // Columnas
    for (let i = 0; i < matriz.length; i++) {  // Filas
        console.log(`[${i}][${j}]: ${matriz[i][j]}`);
    }
}