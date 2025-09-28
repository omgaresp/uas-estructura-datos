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

void bubbleSort(vector<int>& arr) {
    int n = arr.size();

    for (int i = 0; i < n - 1; i++) {
        bool huboIntercambio = false;

        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                huboIntercambio = true;
            }
        }

        cout << "Pasada " << (i + 1) << ": ";
        printArray(arr);
        cout << endl;

        if (!huboIntercambio) {
            cout << "Array ordenado." << endl;
            break;
        }
    }
}

int main() {
    vector<int> arr = {120, 23, 45, 9, 11, 19, 69};

    cout << "=== BUBBLE SORT EN C++ ===" << endl;
    cout << "Array inicial: ";
    printArray(arr);
    cout << endl;

    bubbleSort(arr);

    cout << "Array final: ";
    printArray(arr);
    cout << endl;

    return 0;
}