#include <bits/stdc++.h>
#define pb push_back
#define mp make_pair
#define pii pair<int, int>

using namespace std;

map<pii, int> m, given;

struct node{
    int prior, par;
};

struct DSU{
    node a[100001];

    DSU(){
       // a = new node[n+1];
        for(int j = 1; j <= 100000; j++)
            a[j].par = j, a[j].prior = 1;
    }

    int leader(int x){
        if(a[x].par == x) return x;
        return (a[x].par = leader(a[x].par));
    }

    void add(int u, int v){
        if(u == v) return ;
        int par1 = leader(u);
        int par2 = leader(v);
        if(a[par1].prior > a[par2].prior){
            a[par1].prior += a[par2].prior;
            a[par2].par = par1;
        }
        else{
            a[par2].prior += a[par1].prior;
            a[par1].par = par2;
        }
    }
};

int n, initPar[100001] = {0}, par[100001] = {0}, level[100001] = {0}, mark[100001] = {0}, val[100001] = {0};  // if mark[j] == 1 then active : if 2 then visited completely

vector<pii> back;
vector<int> adj[100001];

void dfs(int src, int from){
    if(mark[src] == 2) return;
    if(mark[src]){
        back.pb(mp(src, from));
        return;
    }
    cout << src << ' ';
    level[src] = level[from] + 1;
    initPar[src] = par[src] = from;
    mark[src]++;

    for(int j = 0; j < (int)adj[src].size(); j++){
        int cur = adj[src][j];
        if(cur == from) continue;
        dfs(cur, src);
    }
    mark[src]++;
}

vector<int> processBackEdges(){
    int num = 1;
    DSU dsu;

    cout << "here!" << endl;
    for(int i = 0; i < back.size(); ++i) {
      cout << back[i].first << " " << back[i].second << endl;
    }
    cout << "here!" << endl;
    for(int j = 0; j < (int)back.size(); j++){
        int to = back[j].first, from = back[j].second;

        while(level[from] > level[to]){
          cout << from << ' ';
            int cur = val[from];
            if(cur != 0) dsu.add(num, cur);
            val[from] = num;
            from = par[from];
        }
        cout << '\n';
        to = back[j].first, from = back[j].second;
        //from = par[from];
        while(level[from] > level[to]){
            int t = par[from];
            par[from] = to;
            from = t;
        }
        num++;
        //cout << num << endl;
    }
    vector<int> ans;
    int sizes[100001] = {0};

    for(int j = 1; j <= num; j++) {
        cout << "leader of " << j << " is " << dsu.leader(j) << endl;
        sizes[dsu.leader(j)]++;
    }

    for(int j = 1; j < num; j++){
        if(sizes[j] != 1) continue;

        int to = back[j-1].first, from = back[j-1].second;
        //cout << from << " " << to << endl;
        ans.pb(given[mp(from, to)]);
        while(from != to){
            ans.pb(given[mp(from, initPar[from])]);
            from = initPar[from];
        }
    }
    return ans;
}

int main(){
    int m;
    cin >> n >> m;
    for(int j = 1; j <= m; j++){
        int u, v;
        cin >> u >> v;
        adj[u].pb(v);
        adj[v].pb(u);
        given[mp(u,v)] = j;
        given[mp(v,u)] = j;
    }
    for(int j = 1; j <= n; j++) {
        if(!mark[j]) dfs(j, 0);
        cout << '\n';
    }
    //cout << "dfs done!" << endl;
    vector<int> ans = processBackEdges();

    sort(ans.begin(), ans.end());
    cout << ans.size() << endl;
    for(int j = 0; j < (int)ans.size(); j++)
        cout << ans[j] << " ";
    cout << endl;
    return 0;
}
