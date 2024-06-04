// Note: 5850986
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.Arrays;
import java.io.BufferedReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.TreeSet;
import java.util.StringTokenizer;
import java.io.InputStream;
 
/**
 * Built using CHelper plug-in
 * Actual solution is at the top
 * @author gridnevvvit
 */
public class main_java {
        public static void main(String[] args) {
                InputStream inputStream = System.in;
                OutputStream outputStream = System.out;
                InputReader in = new InputReader(inputStream);
                PrintWriter out = new PrintWriter(outputStream);
                TaskE solver = new TaskE();
                solver.solve(1, in, out);
                out.close();
        }
}
 
class TaskE {
    public void solve(int testNumber, InputReader in, PrintWriter out) {
        TreeSet <Integer> integers = new TreeSet<Integer>();
        int n = in.nextInt(), m = in.nextInt();
        int pos[] = new int [n], need[] = new int[n], t[] = new int[n];
        integers.add(-1);
        integers.add(n);
        Arrays.fill(need, 0);
        for(int i = 0; i < n; i++)
            pos[in.nextInt() - 1] = i;
        for(int i = 0; i < m; i++)
            need[in.nextInt() - 1] = 1;
        long ans = 0;
        for(int i = 0; i < n; i++) {
            if (need[i] == 1){
                integers.add(pos[i]);
            } else {
                int r, l;
                r = integers.higher(pos[i]) - 1;
                l = integers.lower(pos[i]) + 1;
                ans += r - l + 1;
                for(int j = r; j >= 0; j -= (j + 1) & -(j + 1))
                    ans -= t[j];
                for(int j = l - 1; j >=0 ; j -=(j + 1) & -(j + 1))
                    ans += t[j];
                for(int j = pos[i]; j < n; j += (j + 1) & -(j + 1))
                    t[j] ++;
            }
        }
 
        out.println(ans);
    }
}
 
class InputReader {
    private BufferedReader reader;
    private StringTokenizer tokenizer;
 
    public InputReader(InputStream stream) {
        reader = new BufferedReader(new InputStreamReader(stream));
        tokenizer = null;
    }
 
    public String next() {
        while (tokenizer == null || !tokenizer.hasMoreTokens()) {
            try {
                tokenizer = new StringTokenizer(reader.readLine());
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        return tokenizer.nextToken();
    }
 
    public int nextInt() {
        return Integer.parseInt(next());
    }
 
    }