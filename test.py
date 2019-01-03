
def test_loop(i):
    print ("\tindex:{}".format(i))

FOR(i, 0, 8, '<', '+')
FOR(i, 0, 8, '<=', '+')
FOR(i, 5, 0, '>=', '-')
FOR(i, 6, 0, '>', '-')

beg = 2
end = 48
step = 3

FOR(i, beg, end, '<', step)

print("Loop 0-7:")
FOR(i, 0, 8, '<', '+', test_loop)

print("Loop 0-8:")
FOR(i, 0, 8, '<=', '+', test_loop)

print("Loop 5-0:")
FOR(i, 5, 0, '>=', '-', test_loop)

print("Loop 6-1:")
FOR(i, 6, 0, '>', '-', test_loop)

print("Loop 2-47:")
FOR(i, beg, end, '<', step, test_loop)

