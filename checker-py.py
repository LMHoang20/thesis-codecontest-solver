
n, k = map(int, input().split())
prices = [int(input()) for _ in range(n)]
ans = int(input())
buy = []
sell = []
for i in range(n-1):
    if prices[i] < prices[i+1]:
        buy.append(i)
    elif prices[i] > prices[i+1]:
        sell.append(i)
if len(buy) > k or len(sell) > k:
    print("WA")
else:
    profit = 0
    for i in range(min(len(buy), len(sell))):
        profit += prices[sell[i]] - prices[buy[i]]
    if profit == ans:
        print("OK")
    else:
        print("WA")
