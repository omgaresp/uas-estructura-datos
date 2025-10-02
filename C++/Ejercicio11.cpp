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

void shellSort(vector<int>& arr) {
    int size = arr.size();
    int gapSize = size / 2;

    while (gapSize > 0) {
        for (int i = gapSize; i < size; i++) {
            int temp = arr[i];
            int j = i;
            while (j >= gapSize && arr[j - gapSize] > temp) {
                arr[j] = arr[j - gapSize];
                j -= gapSize;
            }
            arr[j] = temp;
        }
        gapSize /= 2;
    }
}

int main() {
    vector<int> arr = {120, 23, 45, 9, 11, 19, 69};

    cout << "=== SHELL SORT EN C++ ===" << endl;
    cout << "Array inicial: ";
    printArray(arr);
    cout << endl;

    shellSort(arr);

    cout << "Array final: ";
    printArray(arr);
    cout << endl;

    return 0;
}