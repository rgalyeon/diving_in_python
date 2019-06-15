import sys

num_steps = int(sys.argv[1])
for i in range(1, num_steps + 1):
    print(" " * (num_steps - i) + "#" * i)
