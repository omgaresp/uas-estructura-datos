function printArray(arr) {
    return `[${arr.join(', ')}]`;
}

function shellSort(arr) {
    let size = arr.length;
    let gapSize = Math.floor(size / 2);

    while (gapSize > 0) {
        for (let i = gapSize; i < size; i++) {
            let temp = arr[i];
            let j = i;
            while (j >= gapSize && arr[j - gapSize] > temp) {
                arr[j] = arr[j - gapSize];
                j -= gapSize;
            }
            arr[j] = temp;
        }
        gapSize = Math.floor(gapSize / 2);
    }
}

function main() {
    const arr = [54, 24, 15, 2, 12, 1, 80];

    console.log("=== SHELL SORT EN JAVASCRIPT ===");
    console.log(`Array inicial: ${printArray(arr)}`);

    shellSort(arr);

    console.log(`Array final: ${printArray(arr)}`);
}

main();