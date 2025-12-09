#include <iostream>
#include <cmath>
#include <vector>
using namespace std;

const int SIZE=20;
const int INF=999999;

struct Cell{
    int x,y;
    bool wall,visit;
    double real,heuristic,score;
    Cell* parent;
    Cell(int x,int y): x(x),y(y),real(INF),heuristic(0),score(INF),
    wall(false),visit(false),parent(NULL){}
};

double heuristic(Cell* a, Cell* b) {
    int x1 = b->x - a->x;
    int y1 = b->y - a->y;
    return sqrt(x1*x1 + y1*y1);
}
double findLow(vector<Cell*>list) {
    int low=0;
    for(int i=0;i<list.size();i++) {
        if (list[i]->score < list[low]->score) {
            low = i;
        }
    }
    return low;
}
bool InList(vector<Cell*>list, Cell* cell) {
    for (int i = 0; i < list.size(); i++) {
        if (list[i]->x == cell->x && list[i]->y == cell->y) {
            return true;
        }
    }
    return false;
}
void display(Cell* matrix[SIZE][SIZE], Cell* start, Cell* end, vector<Cell*> path) {
    cout << "   ";
    for (int j = 0; j < SIZE; j++)
        cout << j % 10;
    cout << endl;

    for (int i = 0; i < SIZE; i++) {
        cout << i % 10 << ": ";

        for (int j = 0; j < SIZE; j++) {
            Cell* c = matrix[i][j];
            bool onPath = false;
        for(int i = 0; i < path.size(); i++) {
            if(path[i]->x == c->x && path[i]->y == c->y) {
                onPath = true;
                break;
            }
        }
            if (c == start) cout << "S";
            else if (c == end) cout << "C";
            else if (onPath) cout << "*";
            else if (c->wall) cout << "#";
            else if (c->visit) cout << ",";
            else cout << ".";
        }
        cout << endl;
    }
}
vector<Cell*> astarF(Cell* matrix[SIZE][SIZE], Cell* start, Cell* end) {
    vector<Cell*> astar;
    start->real = 0;
    start->heuristic = heuristic(start, end);
    start->score = start->real+start->heuristic;
    astar.push_back(start);

    int kroki =0;
    while (!astar.empty()) {
        kroki++;
        int min = findLow(astar);
        Cell* c = astar[min];

        if (c== end) {
            cout<<"Kroki:"<<kroki<<endl;
            vector<Cell*> droga;
            while (c->parent) {
                droga.push_back(c);
                c = c->parent;
            }
            return droga;
        }
        astar.erase(astar.begin()+min);
        c->visit = true;

        int kierunki[4][2] = {{1,0},{0,1},{-1,0},{0,-1}};
        for (int i = 0; i < 4; i++) {
            int ix = c->x + kierunki[i][0];
            int iy = c->y + kierunki[i][1];
            if (ix < 0 || ix >= SIZE || iy < 0 || iy >= SIZE) continue;
            Cell* n = matrix[ix][iy];
            if (n->wall || n->visit) continue;

            double newX = c->real + 1;
            if (newX < n->real) {
                n->parent = c;
                n->real = newX;
                n->heuristic = heuristic(n, end);
                n->score = n->real + n->heuristic;
                if (!InList(astar, n)) astar.push_back(n);
            }
        }
    }
    cout << "Krokow: " << kroki << endl;
    return vector<Cell*>();
}

int main() {
    Cell* matrix[SIZE][SIZE];
    for (int i = 0; i < SIZE; i++)
        for (int j = 0; j < SIZE; j++)
            matrix[i][j] = new Cell(i, j);

    Cell* start = matrix[2][2];
    Cell* end = matrix[17][17];

    for (int i = 7; i < 15; i++) matrix[i][9]->wall = true;
    for (int j = 9; j < 15; j++) matrix[5][j]->wall = true;
    for (int i = 3; i < 15; i++) matrix[i][2]->wall = true;
    matrix[5][10]->wall = false;
    for (int i = 2; i < 12; i++) matrix[i][12]->wall = true;
    for (int j = 4; j < 11; j++) matrix[10][j]->wall = true;
    matrix[15][15]->wall = matrix[15][16]->wall = true;

    // blokowanie celu
    // matrix[17][16]->wall = true;
    // matrix[16][17]->wall = true;
    // matrix[18][17]->wall = true;
    // matrix[17][18]->wall = true;
    // cel = sciana
    // matrix[17][17]->wall = true; 

    vector<Cell*> path = astarF(matrix, start, end);
    cout << "Odleglosc: " << heuristic(start, end) << endl << endl;

    if (path.empty()) {
        cout << "NIE ZNALEZIONO!\n\n";
        vector<Cell*> empty;
        display(matrix, start, end, empty);
    } else {
        cout << "ZNALEZIONO!\n";
        cout << "Dlugosc: " << path.size() << "\n\n";
        display(matrix, start, end, path);

        cout << endl << "droga" << endl;
        for (int i = path.size()-1; i >= 0; i--)
            cout << "(" << path[i]->x << "," << path[i]->y << ") ";
        cout << "\n";
    }
}
