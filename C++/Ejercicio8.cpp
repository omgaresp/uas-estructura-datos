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

void swap(vector<int>& arr, int j, int k) {
    int temp = arr[j];
    arr[j] = arr[k];
    arr[k] = temp;
}

int partition(vector<int>& arr, int l, int h) {
    int pvt = arr[h];
    int j = l - 1;

    for (int k = l; k < h; k++) {
        if (arr[k] < pvt) {
            j += 1;
            swap(arr, j, k);
        }
    }

    swap(arr, j + 1, h);
    return j + 1;
}

void quickSort(vector<int>& arr, int l, int h) {
    if (l < h) {
        int pi = partition(arr, l, h);

        quickSort(arr, l, pi - 1);
        quickSort(arr, pi + 1, h);
    }
}

int main() {
    vector<int> arr = {120, 23, 45, 9, 11, 19, 69};

    cout << "=== QUICK SORT EN C++ ===" << endl;
    cout << "Array inicial: ";
    printArray(arr);
    cout << endl;

    quickSort(arr, 0, arr.size() - 1);

    cout << "Array final: ";
    printArray(arr);
    cout << endl;

    return 0;
}