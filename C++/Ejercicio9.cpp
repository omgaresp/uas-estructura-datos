#include <iostream>
#include <vector>

using namespace std;

void printArray(const vector<int>& arr) {
    cout << "[";
    for (int i = 0; i < arr.size(); i++) {
        cout << arr[i];
        if (i < arr.size() - 1) cout << ", ";
    }
    cout << "]";
}

void merge(vector<int>& arr, int l, int m, int r) {
    int arr1 = m - l + 1;
    int arr2 = r - m;

    vector<int> tempL(arr1);
    vector<int> tempR(arr2);

    for (int j = 0; j < arr1; j++) {
        tempL[j] = arr[l + j];
    }

    for (int k = 0; k < arr2; k++) {
        tempR[k] = arr[m + 1 + k];
    }

    int i = 0;
    int j = 0;
    int k = l;

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

void mergeSort(vector<int>& arr, int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;

        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

int main() {
    vector<int> arr = {120, 23, 45, 9, 11, 19, 69};

    cout << "=== MERGE SORT EN C++ ===" << endl;
    cout << "Array inicial: ";
    printArray(arr);
    cout << endl;

    mergeSort(arr, 0, arr.size() - 1);

    cout << "Array final: ";
    printArray(arr);
    cout << endl;

    return 0;
}