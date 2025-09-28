function printArray(arr) {
    return `[${arr.join(', ')}]`;
}

function partition(arr, l, h) {
    let pvt = arr[h];
    let j = l - 1;

    for (let k = l; k < h; k++) {
        if (arr[k] < pvt) {
            j += 1;
            swap(arr, j, k);
        }
    }

    swap(arr, j + 1, h);
    return j + 1;
}

function swap(arr, j, k) {
    [arr[j], arr[k]] = [arr[k], arr[j]];
}

function quickSort(arr, l, h) {
    if (l < h) {
        let pi = partition(arr, l, h);

        quickSort(arr, l, pi - 1);
        quickSort(arr, pi + 1, h);
    }
}

function main() {
    const arr = [54, 24, 15, 2, 12, 1, 80];

    console.log("=== QUICK SORT EN JAVASCRIPT ===");
    console.log(`Array inicial: ${printArray(arr)}`);

    quickSort(arr, 0, arr.length - 1);

    console.log(`Array final: ${printArray(arr)}`);
}

main();