#include <bits/stdc++.h>

using namespace std;

struct Edge {
    int a, b, c;
    Edge() {}
    Edge(int a, int b, int c) : a(a), b(b), c(c) {}
};

int N, M, T, X, K;
vector<vector<int>> prob;
vector<Edge> e;
vector<vector<double>> inp, outp;
vector<vector<vector<vector<double>>>> tfd;
vector<vector<double>> re, im;
vector<vector<double>> cosTable, sinTable;

void initTable() {
    int levels = 18;
    cosTable.resize(levels);
    sinTable.resize(levels);
    for (int j = 1; j < levels; ++j) {
        int n = 1 << j;
        cosTable[j].resize(n / 2);
        sinTable[j].resize(n / 2);
        cosTable[j][0] = 1;
        sinTable[j][0] = 0;
        double qc = cos(2 * M_PI / n);
        double qs = sin(2 * M_PI / n);
        for (int i = 1; i < n / 2; ++i) {
            cosTable[j][i] = cosTable[j][i - 1] * qc - sinTable[j][i - 1] * qs;
            sinTable[j][i] = sinTable[j][i - 1] * qc + cosTable[j][i - 1] * qs;
        }
    }
}

void transform(vector<double>& real, vector<double>& imag) {
    int n = real.size();
    if (n <= 1) return;
    int levels = __builtin_ctz(n);

    vector<int> rev(n);
    for (int i = 0; i < n; ++i) {
        rev[i] = (rev[i >> 1] >> 1) | ((i & 1) << (levels - 1));
        if (rev[i] > i) {
            swap(real[i], real[rev[i]]);
            swap(imag[i], imag[rev[i]]);
        }
    }

    for (int size = 2; size <= n; size *= 2) {
        int halfsize = size / 2;
        int tablestep = n / size;
        for (int i = 0; i < n; i += size) {
            for (int j = i, k = 0; j < i + halfsize; ++j, k += tablestep) {
                double tpre = real[j + halfsize] * cosTable[levels][k] + imag[j + halfsize] * sinTable[levels][k];
                double tpim = -real[j + halfsize] * sinTable[levels][k] + imag[j + halfsize] * cosTable[levels][k];
                real[j + halfsize] = real[j] - tpre;
                imag[j + halfsize] = imag[j] - tpim;
                real[j] += tpre;
                imag[j] += tpim;
            }
        }
    }
}

void init(int index, double p) {
    inp[index].resize(T + 1);
    outp[index].resize(T + 1);
    for (int i = 0; i <= T; ++i) inp[index][i] = prob[index][i] / 100000.0;

    int s = 100000;
    for (int i = 0; i <= T; ++i) {
        s -= prob[index][i];
        outp[index][i] = s / 100000.0 * p;
    }

    tfd[index].resize(K);
    for (int i = 2; i < K; ++i) {
        int start = (1 << (i - 1)) + 1;
        int end = (1 << i) + 1;
        int len = 2 * (end - start);
        tfd[index][i].resize(2, vector<double>(len));
        copy(inp[index].begin() + start, inp[index].begin() + min(T + 1, start + len / 2), tfd[index][i][0].begin());
        transform(tfd[index][i][0], tfd[index][i][1]);
    }
}

void update(int index, int id, double x) {
    outp[index][id] = x;
    if (id + 1 <= T) outp[index][id + 1] += x * inp[index][1];
    if (id + 2 <= T) outp[index][id + 2] += x * inp[index][2];

    for (int i = 2; i < K; ++i) {
        if ((((id + 1) >> (i - 2)) & 1) == 1) break;
        int start = id - (1 << (i - 1)) + 1;
        int end = id + 1;
        int len = 2 * (end - start);

        fill(re[i].begin(), re[i].end(), 0);
        fill(im[i].begin(), im[i].end(), 0);
        copy(outp[index].begin() + start, outp[index].begin() + min(T + 1, start + len / 2), re[i].begin());
        transform(re[i], im[i]);

        for (int j = 0; j < len; ++j) {
            double tre = tfd[index][i][0][j] * re[i][j] - tfd[index][i][1][j] * im[i][j];
            double tim = tfd[index][i][1][j] * re[i][j] + tfd[index][i][0][j] * im[i][j];
            re[i][j] = tre;
            im[i][j] = tim;
        }
        transform(im[i], re[i]);

        for (int j = 0; id + j + 2 <= T && j < len; ++j) outp[index][id + j + 2] += re[i][j] / len;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    cin >> N >> M >> T >> X;
    K = __builtin_ctz(1 << (31 - __builtin_clz(T))) + 2;

    e.resize(M);
    prob.resize(M, vector<int>(T + 1));
    inp.resize(M);
    outp.resize(M);
    tfd.resize(M);
    re.resize(K);
    im.resize(K);

    for (int i = 0; i < K; ++i) {
        re[i].resize(1 << i);
        im[i].resize(1 << i);
    }

    vector<vector<int>> dist(N, vector<int>(N, numeric_limits<int>::max() / 2));
    for (int i = 0; i < N; ++i) dist[i][i] = 0;
    for (int i = 0; i < M; ++i) {
        int a, b, c;
        cin >> a >> b >> c;
        a--; b--;
        e[i] = Edge(a, b, c);
        dist[a][b] = min(dist[a][b], c);
        for (int j = 1; j <= T; ++j)
            cin >> prob[i][j];
    }

    for (int k = 0; k < N; ++k)
        for (int i = 0; i < N; ++i)
            for (int j = 0; j < N; ++j)
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);

    vector<double> res(N);
    for (int i = 0; i < N - 1; ++i) res[i] = dist[i][N - 1] + X;
    res[N - 1] = 0;

    initTable();
    for (int i = 0; i < M; ++i) init(i, dist[e[i].b][N - 1] + X);

    for (int t = 1; t <= T; ++t) {
        for (int i = 0; i < M; ++i) update(i, t - 1, res[e[i].b]);
        fill(res.begin(), res.end(), numeric_limits<double>::infinity());
        res[N - 1] = 0;
        for (int i = 0; i < M; ++i) res[e[i].a] = min(res[e[i].a], e[i].c + outp[i][t]);
    }

    cout << fixed << setprecision(10) << res[0] << endl;
    return 0;
}
