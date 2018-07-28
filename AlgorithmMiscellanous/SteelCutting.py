import myIO
import profile

price = myIO.read_dict("steel_cutting", lambda x: int(x), lambda y: int(y))


def cut_rod(price_table, length):
    max_len = max(price_table.keys())
    if length == 0:
        return 0
    profit = 0
    for sub in range(max(0, length - max_len), length):
        profit = max(profit, price_table[length - sub] + cut_rod(price_table, sub))
    return profit


def memoized_cut_rod(price_table, length):
    memo = [None] * (length + 1)
    for i in range(0, length + 1):
        memo[i] = -1
    return memoized_cut_rod_aux(price_table, length, memo)


def memoized_cut_rod_aux(price_table, length, memo):
    max_len = max(price_table.keys())
    if memo[length] >= 0:
        return memo[length]
    if length == 0:
        return 0
    profit = 0
    for sub in range(max(0, length - max_len), length):
        profit = max(profit, price_table[length - sub] + memoized_cut_rod_aux(price_table, sub, memo))
    memo[length] = profit
    return profit


myIO.new("steel_result")

for i in range(1, 13):
    i = 2 << i
    profile.fire()
    print memoized_cut_rod(price, i)
    myIO.write("{%s, %s},\n" % (i, profile.check()))
