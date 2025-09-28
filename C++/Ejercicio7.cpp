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

void selectionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n; i++) {
        int minIndex = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }
        int actual = arr[i];
        arr[i] = arr[minIndex];
        arr[minIndex] = actual;
    }
}

int main() {
    vector<int> arr = {120, 23, 45, 9, 11, 19, 69};

    cout << "=== SELECTION SORT EN C++ ===" << endl;
    cout << "Array inicial: ";
    printArray(arr);
    cout << endl;

    selectionSort(arr);

    cout << "Array final: ";
    printArray(arr);
    cout << endl;

    return 0;
}