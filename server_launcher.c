#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PORT "8080"

int main() {
    char command[256];

    printf("===========================================\n");
    printf("  Smart Attendance Alert System\n");
    printf("===========================================\n");
    printf("  Server running at http://localhost:%s\n", PORT);
    printf("  Open: http://localhost:%s/login.html\n", PORT);
    printf("  Press Ctrl+C to stop.\n");
    printf("===========================================\n\n");

    snprintf(command, sizeof(command), "python3 -m http.server %s --cgi", PORT);

    int ret = system(command);

    if (ret != 0) {
        fprintf(stderr, "\n[ERROR] Failed to start server.\n");
        fprintf(stderr, "Make sure Python 3 is installed.\n");
        return 1;
    }

    return 0;
}