#include <iostream>

#define MAX_N 1000000

using namespace std;

int n;
int customers[MAX_N];
int leader_capacity, member_capacity;

int RequiredMemberNum(int customer_num) {
    if(customer_num <= 0)
        return 0;
    if(customer_num % member_capacity == 0)
        return customer_num / member_capacity;
    else
        return (customer_num / member_capacity) + 1;
}

int main() {
    ios_base::sync_with_stdio(false); 
    cin.tie(nullptr); cout.tie(nullptr);

    // 입력:
    cin >> n;
    for(int i = 0; i < n; i++)
        cin >> customers[i];
    cin >> leader_capacity >> member_capacity;
    
    long long ans = 0;

    for(int i = 0; i < n; i++) {
        ans++;
        ans += RequiredMemberNum(customers[i] - leader_capacity);
    }

    cout << ans;
    
    return 0;
}
