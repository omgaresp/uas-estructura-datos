function printArray(arr) {
    return `[${arr.join(', ')}]`;
}

function merge(arr, l, m, r) {
    let arr1 = m - l + 1;
    let arr2 = r - m;

    let tempL = new Array(arr1);
    let tempR = new Array(arr2);

    for (let j = 0; j < arr1; j++) {
        tempL[j] = arr[l + j];
    }

    for (let k = 0; k < arr2; k++) {
        tempR[k] = arr[m + 1 + k];
    }

    let i = 0;
    let j = 0;
    let k = l;

    while (i < arr1 && j < arr2) {
        if (tempL[i] <= tempR[j]) {
            arr[k] = tempL[i];
            i += 1;
        } else {
            arr[k] = tempR[j];
            j += 1;
        }
        k += 1;
    }

    while (i < arr1) {
        arr[k] = tempL[i];
        i += 1;
        k += 1;
    }

    while (j < arr2) {
        arr[k] = tempR[j];
        j += 1;
        k += 1;
    }
}

function mergeSort(arr, l, r) {
    if (l < r) {
        let m = l + Math.floor((r - l) / 2);

        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

function main() {
    const arr = [54, 24, 15, 2, 12, 1, 80];

    console.log("=== MERGE SORT EN JAVASCRIPT ===");
    console.log(`Array inicial: ${printArray(arr)}`);

    mergeSort(arr, 0, arr.length - 1);
    console.log(`Array final: ${printArray(arr)}`);
}

main();