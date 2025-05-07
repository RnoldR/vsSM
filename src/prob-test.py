import math

n = 2.0
p = 0.11

never = (1 - p) ** n

once = 1 - never

print('p        ', p)
print('times    ', n)
# print('observed ', observed)
print('never    ', never)
print('once     ', once)

pn = 0.1
x = 1 - (1 - pn ** (1 / n))
print('x', x)
