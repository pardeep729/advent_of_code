import re

def mul(x,y):
    return x * y

def mul_parser(text): 
    pattern = r"mul\([0-9]{1,3},[0-9]{1,3}\)" # Pattern to look for
    matches = re.findall(pattern, text) # Find all matches
    total = 0
    for m in matches:
        total += eval(m)

    return total

# Example
example = r"xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
print("Example:", mul_parser(example))

# Actual input
with open('../input.txt', 'r') as file:
    input_text = file.read()
print("Actual Input:", mul_parser(input_text))