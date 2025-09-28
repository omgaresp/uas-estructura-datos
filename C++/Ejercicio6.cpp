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

void insertionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; i++) {
        int actual = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > actual) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = actual;
    }
}

int main() {
    vector<int> arr = {120, 23, 45, 9, 11, 19, 69};

    cout << "=== INSERTION SORT EN C++ ===" << endl;
    cout << "Array inicial: ";
    printArray(arr);
    cout << endl;

    insertionSort(arr);

    cout << "Array final: ";
    printArray(arr);
    cout << endl;

    return 0;
}