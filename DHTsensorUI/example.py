import sys

from collections import deque

arr = [10,9,8,7,6,5,4,3,2,1]
a = deque(arr)

a.pop()
a.appendleft(11)

print (a)
print (arr)
