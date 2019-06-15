import sys

digit_string = sys.argv[1]
digit_sum = 0
for i in digit_string:
    digit_sum += int(i)
print(digit_sum)
