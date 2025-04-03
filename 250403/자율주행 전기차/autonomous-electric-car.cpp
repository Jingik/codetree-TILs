#include <iostream>
#include <tuple>
#include <queue>
#include <vector>

#define MAX_N 20
#define MAX_M 400
#define DIR_NUM 4
#define NOT_EXISTS make_pair(-1, -1)

using namespace std;

int n, m;

int grid[MAX_N + 1][MAX_N + 1];

vector<tuple<int, int, int, int> > passengers;
bool moved_passenger[MAX_M];

// 현재 자동차의 위치와 남은 연료량
pair<int, int> car_pos;
int remaining_battery;

queue<pair<int, int> > bfs_q;
int step[MAX_N + 1][MAX_N + 1];
bool visited[MAX_N + 1][MAX_N + 1];

bool InRange(int x, int y) {
    return 1 <= x && x <= n && 1 <= y && y <= n;
}

bool CanGo(int x, int y) {
    return InRange(x, y) && !visited[x][y] && !grid[x][y];
}

// visited 배열을 초기화 해줍니다.
void InitializeVisited() {
    for(int i = 1; i <= n; i++)
        for(int j = 1; j <= n; j++)
            visited[i][j] = false;
}

void BFS(pair<int, int> start_pos) {
    // BFS 탐색을 위한 초기화 작업을 수행합니다.
    InitializeVisited();
    
    // 시작 위치를 queue에 넣습니다.
    int start_x, start_y;
    tie(start_x, start_y) = start_pos;
    
    visited[start_x][start_y] = true;
    step[start_x][start_y] = 0;
    bfs_q.push(make_pair(start_x, start_y));
    
    int dx[DIR_NUM] = {0, 1, 0, -1};
    int dy[DIR_NUM] = {1, 0, -1, 0};

    // BFS 탐색을 수행합니다.
    while(!bfs_q.empty()) {
        pair<int, int> curr_pos = bfs_q.front();
        int curr_x, curr_y;
        tie(curr_x, curr_y) = curr_pos;
        bfs_q.pop();

        for(int i = 0; i < DIR_NUM; i++) {
            int new_x = curr_x + dx[i];
            int new_y = curr_y + dy[i];

            if(CanGo(new_x, new_y)) {
                bfs_q.push(make_pair(new_x, new_y));
                step[new_x][new_y] = step[curr_x][curr_y] + 1;
                visited[new_x][new_y] = true;
            }
        }
    }
}

// best 위치를 새로운 위치로 바꿔줘야 하는지를 판단합니다.
bool NeedUpdate(pair<int, int> best_pos, pair<int, int> new_pos) {
    // 첫 후보 승객이라면
    // update가 필요합니다.
    if(best_pos == NOT_EXISTS)
        return true;

    int best_x, best_y;
    tie(best_x, best_y) = best_pos;
    
    int new_x, new_y;
    tie(new_x, new_y) = new_pos;
    
    // 거리, 행, 열 순으로 더 작은 경우에만 골라져야 합니다.
    return make_tuple(step[best_x][best_y], best_x, best_y) > 
           make_tuple(step[new_x][new_y], new_x, new_y);
}

// 가장 우선순위가 높은 승객을 찾아
// 목적지로 이동시킵니다.
bool MovePassenger() {
    // Step1. 자동차 위치로부터 각 승객까지의 
    //        최단거리를 전부 구합니다.
    
    // 시작 자동차 위치로부터 BFS를 진행합니다.
    BFS(car_pos);
    
    // Step2.
    // 태울 수 있는 승객 중
    // 가장 우선순위가 높은 승객의 출발 위치를 구합니다.
    pair<int, int> best_pos = NOT_EXISTS;
    int best_index = -1;
    for(int i = 0; i < (int) passengers.size(); i++) {
        int start_x, start_y, end_x, end_y;
        tie(start_x, start_y, end_x, end_y) = passengers[i];
        // 이미 태웠던 승객이거나, 아예 도달 불가능한 위치에 승객이 서있거나
        // 해당 위치에 있는 승객을 태우기까지의 연료가 부족하다면 불가능합니다.
        if(moved_passenger[i] || 
           !visited[start_x][start_y] ||
           step[start_x][start_y] > remaining_battery) continue;
        
        if(NeedUpdate(best_pos, make_pair(start_x, start_y))) {
            best_pos = make_pair(start_x, start_y);
            best_index = i;
        }
    }
    
    // Case2-1.
    // 현재 연료로 태울 수 있는 승객이 없다면
    // 불가능합니다.
    if(best_pos == NOT_EXISTS)
        return false;
    
    // Case2-2.
    // 승객의 위치로 이동합니다.
    int start_x, start_y, end_x, end_y;
    tie(start_x, start_y, end_x, end_y) = passengers[best_index];
    
    car_pos = make_pair(start_x, start_y);
    remaining_battery -= step[start_x][start_y];
    
    // Step3. 해당 승객을 이동시키기 위한 최단거리를 구합니다.
    
    // (start_x, start_y)를 시작점으로 하는 BFS를 이용해 
    // (end_x, end_y) 까지의 최단거리를 구합니다.
    BFS(make_pair(start_x, start_y));
    
    // Case3-1.
    // 도착점 도달 자체가 불가능 하거나
    // 도착점까지 가는 데 필요한 연료가 충분하지 않다면 불가합니다.
    if(!visited[end_x][end_y] || 
       step[end_x][end_y] > remaining_battery)
        return false;
    
    // Case3-2.
    // 이동이 가능한 경우
    // 승객을 도착지로 이동시킵니다.
    car_pos = make_pair(end_x, end_y);
    remaining_battery -= step[end_x][end_y];
    
    // 승객 이동 완료 표시를 하고, 배터리양이 충전됩니다.
    moved_passenger[best_index] = true;
    remaining_battery += step[end_x][end_y] * 2;
    
    return true;
}

int main() {
    cin >> n >> m >> remaining_battery;
    
    for(int i = 1; i <= n; i++)
        for(int j = 1; j <= n; j++) 
            cin >> grid[i][j];
    
    int car_x, car_y;
    cin >> car_x >> car_y;
    car_pos = make_pair(car_x, car_y);
    
    for(int i = 1; i <= m; i++) {
        int start_x, start_y, end_x, end_y;
        cin >> start_x >> start_y >> end_x >> end_y;
        passengers.push_back(make_tuple(
            start_x, start_y, end_x, end_y
        ));
    }
    
    // m명의 승객을 전부 옮길 수 있는지를 판단합니다.
    for(int i = 1; i <= m; i++) {
        bool is_moved = MovePassenger();
        
        // 전부 옮기는 것이 불가능한 경우라면 -1을 출력하고
        // 프로그램을 종료합니다.
        if(!is_moved) {
            cout << -1;
            return 0;
        }
    }
    
    // 남아있는 배터리의 양을 출력합니다.
    cout << remaining_battery;
}
