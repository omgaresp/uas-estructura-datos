function printArray(arr) {
    return `[${arr.join(', ')}]`;
}

function selectionSort(arr) {
    const n = arr.length;
    for (let i = 0; i < n - 1; i++) {
        let minIndex = i;
        for (let j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }
        if (minIndex !== i) {
            let actual = arr[i];
            arr[i] = arr[minIndex];
            arr[minIndex] = actual;
        }
    }
}

function main() {
    const arr = [54, 24, 15, 2, 12, 1, 80];

    console.log("=== SELECTION SORT EN JAVASCRIPT ===");
    console.log(`Array inicial: ${printArray(arr)}`);

    selectionSort(arr);

    console.log(`Array final: ${printArray(arr)}`);
}

main();