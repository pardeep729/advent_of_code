import re

def mul(x,y):
    return x * y

def mul_parser(text): 
    pattern = r"mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\)" # Pattern to look for (mul, do or don't)
    matches = re.findall(pattern, text) # Find all matches
    total = 0
    evaluate_muls = True # Evaluate muls at start
    for m in matches:
        if m == "do()":
            evaluate_muls = True
            continue
        elif m == "don't()":
            evaluate_muls = False
            continue
        
        if evaluate_muls:
            total += eval(m)

    return total

# Example
example = r"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
print("Example:", mul_parser(example))

# Actual input
with open('../input.txt', 'r') as file:
    input_text = file.read()
    
print("Actual Input:", mul_parser(input_text))