
#include <iostream>
#include <cstring>
#include <algorithm>
#include <vector>
#include <queue>
using namespace std;
typedef pair<int,int> ii;
const int N = 2e5+5, INF = 1<<30;
ii t[N<<2], a[N];
int P[N], lazy[N<<2], ans[N];
int n;
queue<int> Q;
void build(int v, int tl, int tr){
    if (tl == tr){
        t[v] = {tl, tl};
        lazy[v] = 0;
        return;
    }
    if (tl > tr) return;
    int tm = (tl+tr)>>1;
    build(v<<1, tl, tm);
    build(v<<1|1, tm+1, tr);
    t[v].first = min(t[v<<1].first, t[v<<1|1].first);
    t[v].second = max(t[v<<1].second, t[v<<1|1].second);
    lazy[v] = 0;
}
void update(int v, int tl, int tr, int l, int r, int u){
    if (lazy[v]!=0){
        t[v].first += lazy[v];
        t[v].second += lazy[v];
        if (tl != tr){
            lazy[v<<1] += lazy[v];
            lazy[v<<1|1] += lazy[v];
        }
        lazy[v] = 0;
    }
    if (tl > tr || tr < l || r < tl) return;
    if (l <= tl && tr <= r){
        t[v].first += u;
        t[v].second += u;
        if (tl == tr) return;
        lazy[v<<1] += u;
        lazy[v<<1|1] += u;
        return;
    }
    int tm = (tl+tr)/2;
    update(v<<1,tl,tm,l,r,u);
    update(v<<1|1,tm+1,tr,l,r,u);
    t[v].first = min(t[v<<1].first, t[v<<1|1].first);
    t[v].second = max(t[v<<1].second, t[v<<1|1].second);
}
ii get(int v, int tl, int tr, int l, int r){
    if (lazy[v]!=0){
        t[v].first += lazy[v];
        t[v].second += lazy[v];
        if (tl != tr){
            lazy[v<<1] += lazy[v];
            lazy[v<<1|1] += lazy[v];
        }
        lazy[v] = 0;
    }
    if (tl > tr || tr < l || r < tl) return {INF, -INF};
    if (l <= tl && tr <= r) return t[v];
    int tm = (tl+tr)/2;
    ii A = get(v<<1,tl,tm,l,r);
    ii B = get(v<<1|1,tm+1,tr,l,r);
    ii res;
    res.first = min(A.first, B.first);
    res.second = max(A.second, B.second);
    return res;
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    cin >> n;
    for(int i=1;i<=n;++i){
        cin >> a[i].first;
        a[i].second = i;
    }
    for(int i=0;i<=n;++i) P[i] = i;
    sort(a+1, a+1+n);
    build(1, 0, n);
    for(int i=1;i<=n;++i){
        int j = i-1;
        if (j>0){
            Q.push(a[j].second);
            if (a[j].first != a[i].first){
                while(!Q.empty()){
                    update(1,0,n,Q.front(),n,-2);
                    Q.pop();
                }
            }
        }
        ii A = get(1,0,n,0,a[i].second-1);
        ii B = get(1,0,n,a[i].second,n);
        ans[a[i].second] = (B.second - A.first);
    }
    while(!Q.empty()) Q.pop();
    sort(a+1, a+1+n, greater<ii>());
    build(1, 0, n);
    for(int i=1;i<=n;++i){
        int j = i-1;
        if (j>0){
            Q.push(a[j].second);
            if (a[j].first != a[i].first){
                while(!Q.empty()){
                    update(1,0,n,Q.front(),n,-2);
                    Q.pop();
                }
            }
        }
        ii A = get(1,0,n,0,a[i].second-1);
        ii B = get(1,0,n,a[i].second,n);
        ans[a[i].second] = max(ans[a[i].second], B.second - A.first - 1);
    }
    for(int i=1;i<=n;++i) cout << (ans[i]>>1) << ' ';
}
