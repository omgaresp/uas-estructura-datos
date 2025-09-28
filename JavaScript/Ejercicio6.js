function printArray(arr) {
    return `[${arr.join(', ')}]`;
}

function inertionSort(arr) {
    const n = arr.length;
    for (let i = 1; i < n; i++) {
        let actual = arr[i];
        let j = i - 1;
        while (j >= 0 && arr[j] > actual) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = actual;
    }
}

function main() {
    const arr = [54, 24, 15, 2, 12, 1, 80];

    console.log("=== INSERTION SORT EN JAVASCRIPT ===");
    console.log(`Array inicial: ${printArray(arr)}`);

    inertionSort(arr);

    console.log(`Array final: ${printArray(arr)}`);
}

main();