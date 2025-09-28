function printArray(arr) {
    return `[${arr.join(', ')}]`;
}

function bubbleSort(arr) {
    const n = arr.length;

    for (let i = 0; i < n - 1; i++) {
        let huboIntercambio = false;

        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                huboIntercambio = true;
            }
        }

        console.log(`Pasada ${i + 1}: ${printArray(arr)}`);

        if (!huboIntercambio) {
            console.log("Array ordenado.");
            break;
        }
    }
}

function main() {
    const arr = [54, 24, 15, 2, 12, 1, 80];

    console.log("=== BUBBLE SORT EN JAVASCRIPT ===");
    console.log(`Array inicial: ${printArray(arr)}`);

    bubbleSort(arr);

    console.log(`Array final: ${printArray(arr)}`);
}

main();