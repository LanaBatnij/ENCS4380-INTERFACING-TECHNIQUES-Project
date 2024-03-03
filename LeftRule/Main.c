#include <stdio.h>
#include "API.h"

void log(char* text) {
    fprintf(stderr, "%s\n", text);
    fflush(stderr);
}

int main(int argc, char* argv[]) {
    log("Running...");
    API_setColor(0, 0, 'G');
    API_setText(0, 0, "abc");
    while (1) {
        if(API_wallLeft() && API_wallRight() && API_wallFront()){
            API_turnLeft();
            API_turnLeft();
        }else if(API_wallLeft() && !API_wallRight() && API_wallFront()){
            API_turnRight();
        }else if(!API_wallLeft() && API_wallRight() && API_wallFront()){
            API_turnLeft();
        }else if(!API_wallLeft() && API_wallRight() && !API_wallFront()){
            API_turnLeft();
        }else if(!API_wallLeft() && !API_wallRight() && API_wallFront()){
            API_turnLeft();
        }else if(!API_wallLeft() && !API_wallRight() && !API_wallFront()){
            API_turnLeft();
        }
        API_moveForward();
    }
}
