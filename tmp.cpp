#include <iostream>
#include <vector>
#include <map>
#include <limits>

using namespace std;

const int INF = numeric_limits<int>::max();
const int N = 500001;

typedef pair<int, int> Pair;

struct Node {
    Pair value;
    Node* left;
    Node* right;

    Node() : value(make_pair(INF, 0)), left(nullptr), right(nullptr) {}

    Node(Node* left, Node* right) {
        this->value = min(left->value, right->value);
        this->left = left;
        this->right = right;
    }

    Node(int pos, int val) {
        this->value = make_pair(val, pos);
        this->left = nullptr;
        this->right = nullptr;
    }
};

typedef Node* SegmentTree;

Pair query(SegmentTree tree, int left, int right, int queryLeft, int queryRight) {
    if (queryLeft >= queryRight) {
        return make_pair(INF, 0);
    }

    if (left == queryLeft && right == queryRight) {
        return tree->value;
    }

    int mid = (left + right) / 2;
    Pair q1 = query(tree->left, left, mid, queryLeft, min(mid, queryRight));
    Pair q2 = query(tree->right, mid, right, max(mid, queryLeft), queryRight);
    return min(q1, q2);
}

SegmentTree update(SegmentTree tree, int left, int right, int pos, int val) {
    if (left == right - 1) {
        return new Node(pos, val);
    } else {
        int mid = (left + right) / 2;
        if (pos < mid) {
            return new Node(update(tree->left, left, mid, pos, val), tree->right);
        } else {
            return new Node(tree->left, update(tree->right, mid, right, pos, val));
        }
    }
}

SegmentTree build(int left, int right) {
    if (left == right - 1) {
        return new Node(left, INF);
    } else {
        int mid = (left + right) / 2;
        return new Node(build(left, mid), build(mid, right));
    }
}

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    vector<int> left(n);
    map<int, int> last;
    for (int i = 0; i < n; i++) {
        if (!last.count(a[i])) {
            left[i] = -1;
        } else {
            left[i] = last[a[i]];
        }
        last[a[i]] = i;
    }

    vector<SegmentTree> trees(n + 1);
    trees[0] = build(0, n);
    for (int i = 0; i < n; i++) {
        SegmentTree currentTree = trees[i];
        if (left[i] != -1) {
            currentTree = update(currentTree, 0, n, left[i], INF);
        }
        currentTree = update(currentTree, 0, n, i, left[i]);
        trees[i + 1] = currentTree;
    }

    int q;
    cin >> q;
    for (int i = 0; i < q; i++) {
        int l, r;
        cin >> l >> r;
        --l;
        Pair answer = query(trees[r], 0, n, l, r);
        if (answer.first < l) {
            cout << a[answer.second] << endl;
        } else {
            cout << "0" << endl;
        }
    }

    return 0;
}