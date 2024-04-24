#include <stdio.h>

int findSpace(const char* sentence, int n) {
    int count = 0;
    // loop through sentence
    for (int i = 0; sentence[i] != '\0'; i++) {
        // if there is a space, note it and compare how many spaces there are to n
        if (sentence[i] == ' ') {
            count++;
            // if we're on the nth space, return i and end loop
            if (count == n) {
                return i; // Position of the nth space
            }
        }
    }
    return -1; // If there are fewer than n spaces or n is not a positive integer
}

int main() {
    const char* str = "This is a sentence.";

    int pointer1 = findSpace(str, 1);
    int pointer2 = findSpace(str, 3);
    int pointer3 = findSpace(str, 5);

    printf("Pointer 1: %d\n", pointer1); // Output: 4
    printf("Pointer 2: %d\n", pointer2); // Output: 9
    printf("Pointer 3: %d\n", pointer3); // Output: -1

    return 0;
}