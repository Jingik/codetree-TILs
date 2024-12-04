#include <iostream>
using namespace std;

int n;
int board[501][501];
int c_y, c_x; // clean y,x
// 왼, 아, 오, 위
int dy[4] = { 0,1,0,-1 };
int dx[4] = { -1,0,1,0 };
// percent
// 5, 10, 10, 2, 7, 7, 2, 1, 1, alpha
int percent[9] = { 5,10,10,2,7,7,2,1,1 };
int py[4][10] = {
	{0,-1,1,-2,-1,1,2,-1,1,0 },
	{2,1,1,0,0,0,0,-1,-1,1},
	{0,-1,1,-2,-1,1,2,-1,1,0},
	{-2,-1,-1,0,0,0,0,1,1,-1}
};
int px[4][10] = {
	{-2,-1,-1,0,0,0,0,1,1,-1},
	{0,-1,1,-2,-1,1,2,-1,1,0 },
	{2,1,1,0,0,0,0,-1,-1,1},
	{0,-1,1,-2,-1,1,2,-1,1,0},
};

int total_out;

bool inRange(int y, int x) {
	if (y < 0 || y >= n || x < 0 || x >= n)
		return false;
	else
		return true;
}

void clean(int y, int x, int d) {
	int alpha;
	int curr = board[y][x];
	int sum = 0;
	for (int i = 0; i < 9; i++) {
		int ny = y + py[d][i];
		int nx = x + px[d][i];
		// 범위체크
		if (inRange(ny, nx) == false) {
			total_out += curr * (percent[i] * 0.01);
			sum += curr * (percent[i] * 0.01);
			continue;
		}
		
		board[ny][nx]+= curr * (percent[i] * 0.01);
		sum += curr * (percent[i] * 0.01);
	}
	// alpha 자리
	if (inRange(y + py[d][9], x + px[d][9]))
		board[y + py[d][9]][x + px[d][9]] += curr - sum;
	else
		total_out += curr - sum;

	// curr 사라짐
	board[y][x] = 0;
}

// 나선형 움직임
void solve() {
	int now = 0;
	int len = 1;
	int cnt = 0;
	int d = 0;
	int y = c_y, x = c_x;
	int ny, nx;
	while (y!=0 || x != 0) {
		ny = y + dy[d];
		nx = x + dx[d];

		//cout << '(' << ny<<','<< nx << ')' << '\n';
		clean(ny, nx, d);

		now++;
		if (now == len) {
			d = (d + 1) % 4;
			now = 0;
			cnt++;
			if (cnt == 2) {
				cnt = 0;
				len++;
			}
		}
		y = ny;
		x = nx;
	}
	cout << total_out << '\n';
}

int main(void) {
	ios_base::sync_with_stdio(false);
	cin.tie(NULL); cout.tie(NULL);

	cin >> n;
	c_y = c_x = n / 2;
	for (int i = 0; i < n; i++)
		for (int j = 0; j < n; j++)
			cin >> board[i][j];

	solve();

	return 0;
}

// 틀린 이유	
// - alpha 자리도 범위가 벗어날 수 있음
//   -> 따라서 total_out 에도 합산해야 함
// - alpha 자리는 이동한 먼지(범위를 나간것도 포함)의 합을
//   curr에서 빼준것을 합치는 것
// - curr은 먼지이동 후 전부 사라짐
