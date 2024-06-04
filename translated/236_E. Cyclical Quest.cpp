#include <bits/stdc++.h>

using namespace std;

struct Node {
    Node* go[26];
    Node* suf;
    Node* nxt;
    int val;
    int cnt;

    Node(Node* suf, int val) : suf(suf), val(val), cnt(0), nxt(nullptr) {
        memset(go, 0, sizeof(go));
    }

    Node() : Node(nullptr, 0) {}
};

vector<Node*> nodes;
Node* root;
Node* last;

void extend(int w) {
    Node* p = last;
    Node* np = new Node();
    np->val = p->val + 1;
    np->cnt = 1;
    nodes.push_back(np);

    while (p != nullptr && p->go[w] == nullptr) {
        p->go[w] = np;
        p = p->suf;
    }

    if (p == nullptr) {
        np->suf = root;
    } else {
        Node* q = p->go[w];
        if (p->val + 1 == q->val) {
            np->suf = q;
        } else {
            Node* nq = new Node(q->suf, p->val + 1);
            memcpy(nq->go, q->go, sizeof(q->go));
            nq->val = p->val + 1;
            nodes.push_back(nq);
            q->suf = nq;
            np->suf = nq;
            while (p != nullptr && p->go[w] == q) {
                p->go[w] = nq;
                p = p->suf;
            }
        }
    }
    last = np;
}

int repetend(const string& s) {
    int n = s.size();
    vector<int> nxt(n + 1, 0);
    nxt[0] = -1;
    for (int i = 1; i <= n; ++i) {
        int j = nxt[i - 1];
        while (j >= 0 && s[j] != s[i - 1])
            j = nxt[j];
        nxt[i] = j + 1;
    }
    int a = n - nxt[n];
    if (n % a == 0)
        return a;
    return n;
}

void solve() {
    root = new Node();
    last = root;
    nodes.push_back(root);

    string s;
    cin >> s;
    int n = s.size();
    for (char c : s) {
        extend(c - 'a');
    }

    vector<Node*> first(n + 1, nullptr);
    for (Node* node : nodes) {
        node->nxt = first[node->val];
        first[node->val] = node;
    }

    for (int i = n; i >= 0; --i) {
        for (Node* u = first[i]; u != nullptr; u = u->nxt)
            if (u->suf != nullptr)
                u->suf->cnt += u->cnt;
    }

    int nQ;
    cin >> nQ;
    for (int i = 0; i < nQ; ++i) {
        string buf;
        cin >> buf;
        int rep = repetend(buf);
        Node* cur = root;
        int l = 0;
        int len = buf.size();

        for (int j = 0; j < len; ++j) {
            int w = buf[j] - 'a';
            while (cur != nullptr && cur->go[w] == nullptr) {
                cur = cur->suf;
                if (cur != nullptr)
                    l = cur->val;
            }
            if (cur != nullptr && cur->go[w] != nullptr) {
                cur = cur->go[w];
                ++l;
            } else {
                cur = root;
                l = 0;
            }
        }
        int ans = 0;
        if (l == len)
            ans += cur->cnt;
        for (int j = 1; j < rep; ++j) {
            if (l == len) {
                --l;
                if (l <= cur->suf->val)
                    cur = cur->suf;
            }
            int w = buf[j - 1] - 'a';
            while (cur != nullptr && cur->go[w] == nullptr) {
                cur = cur->suf;
                if (cur != nullptr)
                    l = cur->val;
            }
            if (cur != nullptr && cur->go[w] != nullptr) {
                cur = cur->go[w];
                ++l;
            } else {
                cur = root;
                l = 0;
            }
            if (l == len)
                ans += cur->cnt;
        }
        cout << ans << endl;
    }
}

int main() {
    solve();
    return 0;
}
