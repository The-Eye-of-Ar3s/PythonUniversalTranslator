from calendar import c
import os


def count_sequence(lst, seq):
     count = 0
     len_seq = len(seq)
     upper_bound = len(lst)-len_seq+1
     for i in range(upper_bound):
         if lst[i:i+len_seq] == seq:
             count += 1
     return count


def lang_length_translate(rawcode:str, name:str) -> int:
    tokens = tokenizer(rawcode)
    if tokens.count(9) > count_sequence(tokens, [14, 9]) + count_sequence(tokens, [25, 9]): 
# if there is no 9 operation (if a 9 follows a 14 or 25 that means it is used as input for those operations) the output will always be the same so we can calculate it beforehand
        outcpp = translator(tokens)
    else:
        outcpp = render(tokens)
    compiler(outcpp, ".".join(name.split(".")[:-1]))


def tokenizer(code: str) -> list[int]:
    return [len(i) for i in code.replace("\r","").split("\n")]


def translator(tokens: list[int]) -> str:
    prevop = 0
    linecount = 1
    condclose = 0
    outcode = [
        "#include <stdio.h>",
        "#include <vector>",
        "using namespace std;",
        "#define CALL_VARIALBLE(name) goto name;",
        "int main() {",
        "vector<int> stack;",
        "int A;",
        "int B;"
        ]
    for token in tokens:
        if prevop == 14:
            outcode[-1] = outcode[-1]+f"{token};"
            prevop = 0
            if condclose > 0:
                outcode.append("}"*condclose)
                condclose = 0
        elif prevop == 25:
            outcode[-1] = outcode[-1]+f"{token});"
            prevop = 0
            if condclose > 0:
                outcode.append("}"*condclose)
                condclose = 0
        else:
            match token:
                case 9: # Inp operation. Pushes the ascii value of the first byte of stdin to the stack.
                    outcode.append(f"label{linecount}:")
                    outcode.append("stack.push_back(getchar());")
                    linecount += 1
                    prevop = token
                    if condclose > 0:
                        outcode.append("}"*condclose)
                        condclose = 0
                case 10: # Add operation. Pops the top two values from the stack and pushes their sum onto the stack.
                    outcode.append(f"label{linecount}:")
                    outcode.append("A = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("B = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("stack.push_back(A + B);")
                    prevop = token
                    linecount+=1
                    if condclose > 0:
                        outcode.append("}"*condclose)
                        condclose = 0
                case 11: # Sub operation. Pops value A from the stack and then value B. Pushes value B - A onto the stack.
                    outcode.append(f"label{linecount}:")
                    outcode.append("A = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("B = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("stack.push_back(B - A);")
                    prevop = token
                    linecount+=1
                    if condclose > 0:
                        outcode.append("}"*condclose)
                        condclose = 0
                case 12: #Dup operation. Duplicates the top value of the stack.
                    outcode.append(f"label{linecount}:")
                    outcode.append("stack.push_back(stack.back());")
                    prevop = token
                    linecount+=1
                    if condclose > 0:
                        outcode.append("}"*condclose)
                        condclose = 0
                case 13: # Cond operation. Pops the top value from the stack. If it is 0, skip the next instruction. If the instruction to be skipped is gotou or push, skip that instructions argument as well.
                    outcode.append(f"label{linecount}:")
                    outcode.append("A = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("if (A == 0) {")
                    prevop = token
                    linecount+=1
                    condclose += 1
                case 14: # Gotou operation. Sets the program counter to the value of the line under the instruction, skipping that line.
                    outcode.append(f"label{linecount}:")
                    outcode.append("goto label")
                    prevop = token
                    linecount+=1
                case 15: # Outn operation. Pops the top of the stack and outputs it as a number.
                    outcode.append(f"label{linecount}:")
                    outcode.append("A = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("printf(\"%d\", A);")
                    prevop = token
                    linecount+=1
                    if condclose > 0:
                        outcode.append("}"*condclose)
                        condclose = 0
                case 16: # Outa operation. Pops the top of the stack and outputs its ascii value.
                    outcode.append(f"label{linecount}:")
                    outcode.append("A = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("putchar(A);")
                    prevop = token
                    linecount+=1
                    if condclose > 0:
                        outcode.append("}"*condclose)
                        condclose = 0
                case 17: # Rol operation. Rotates the stack to the left: [ 7 6 5 ] -> [ 6 5 7 ]
                    outcode.append(f"label{linecount}:")
                    outcode.append("rotate(stack.begin(), stack.begin()+1, stack.end());")
                    prevop = token
                    linecount+=1
                    if condclose > 0:
                        outcode.append("}"*condclose)
                        condclose = 0
                case 18: # Swap operation. Swaps the top two values of the stack: [ 7 6 5 ] -> [ 6 7 5 ]
                    outcode.append(f"label{linecount}:")
                    outcode.append("A = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("B = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("stack.push_back(B);")
                    outcode.append("stack.push_back(A);")
                    prevop = token
                    linecount+=1
                    if condclose > 0:
                        outcode.append("}"*condclose)
                        condclose = 0
                case 20: # Mul operation. Pops the top two values from the stack and pushes their product onto the stack.
                    outcode.append(f"label{linecount}:")
                    outcode.append("A = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("B = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("stack.push_back(A*B);")
                    prevop = token
                    linecount+=1
                    if condclose > 0:
                        outcode.append("}"*condclose)
                        condclose = 0
                case 21: # Div operation. Pops value A from the stack and then value B. Pushes value B / A onto the stack.
                    outcode.append(f"label{linecount}:")
                    outcode.append("A = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("B = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("stack.push_back(B / A);")
                    prevop = token
                    linecount+=1
                    if condclose > 0:
                        outcode.append("}"*condclose)
                        condclose = 0
                case 23: # Pop operation. Pops the top value of the stack.
                    outcode.append(f"label{linecount}:")
                    outcode.append("stack.pop_back();")
                    prevop = token
                    linecount+=1
                    if condclose > 0:
                        outcode.append("}"*condclose)
                        condclose = 0
                case 24: # Gotos operation. Pops the top of the stack and sets the program counter to it (indexed starting at 1).
                    outcode.append(f"label{linecount}:")
                    outcode.append("A = stack.back();")
                    outcode.append("stack.pop_back();")
                    outcode.append("CALL_VARIALBLE(std::format(\"label{}\", A));")
                    prevop = token
                    linecount+=1
                    if condclose > 0:
                        outcode.append("}"*condclose)
                        condclose = 0
                case 25: # Push operation. Pushes the value of the line under this instruction to the stack, skipping that line.
                    outcode.append(f"label{linecount}:")
                    outcode.append("stack.push_back(")
                    prevop = token
                    linecount+=1
                case 27: # // Ror operation. Rotates the stack to the right: [ 7 6 5 ] -> [ 5 7 6 ]
                    outcode.append(f"label{linecount}:")
                    outcode.append("rotate(stack.begin(), stack.end()-1, stack.end());")
                    prevop = token
                    linecount+=1
                    if condclose > 0:
                        outcode.append("}"*condclose)
                        condclose = 0
                case _:
                    pass
    outcode.append("return 0;")
    outcode.append("}")
    return "\n".join(outcode)
    

def render(tokens: list[int]) -> str:
    tokens.append(-1)
    stack = []
    output = ""
    skip = False
    token = tokens[0]
    index = 0
    temp = 0
    sif = skipiffailed(tokens)
    while tokens[index] != -1:
        token = tokens[index]
        match token:
            case 10:
                temp = stack[-1]+stack[-2]
                stack.pop()
                stack.pop()
                stack.append(temp)
                index += 1
            case 11:
                temp = stack[-2]-stack[-1]
                stack.pop()
                stack.pop()
                stack.append(temp)
                index += 1
            case 12:
                stack.append(stack[-1])
                index += 1
            case 13:
                if stack[-1] == 0:
                    if tokens[index+1] != 13 and tokens[index+1] != 25:
                        tokens += 1
                    else:
                        tokens += 2
                else:
                    index += sif[str(index)]
            case 14:
                if tokens[index+1] != -1:
                    index = tokens[index+1]
                else:
                    index += 1
            case 15:
                output += str(stack.pop())
                index += 1
            case 16:
                output += chr(stack.pop())
                index += 1
            case 17:
                stack.rotate(1)
                index += 1
            case 18:
                temp = stack[-2]
                stack[-2] = stack[-1]
                stack[-1] = temp
                index += 1
            case 20:
                temp = stack[-2]*stack[-1]
                stack.pop()
                stack.pop()
                stack.append(temp)
                index += 1
            case 21:
                temp = int(stack[-2]/stack[-1])
                stack.pop()
                stack.pop()
                stack.append(temp)
                index += 1
            case 23:
                stack.pop()
                index += 1
            case 24:
                try:
                    tempindex = int(stack.pop())
                    if tokens[tempindex] != -1:
                        index = tempindex
                    else:
                        index += 1
                except:
                    index = len(tokens)
            case 25:
                if index+2 < len(tokens):
                    stack.append(tokens[index+1])
                    index += 2
                else:
                    index = len(tokens)
            case 27:
                stack.rotate(-1)
                index += 1
            case _:
                index = len(tokens)
    return "#include <iostream>\nint main() {\nstd::cout << \""+output[:-1]+"\";\nreturn 0;\n}"



def skipiffailed(tokens: list[int]) -> dict[str:str]:
    rd = {}
    prev = 0
    ind = []
    for i, e in enumerate(tokens):
        if e == 13:
            ind.append(i)
        if e != 13 and prev == 13:
            for j in ind:
                rd[str(j)] = i
            ind = []
    return rd


def compiler(code: str, name: str) -> None:
    try:
        with open("out.cpp", "wt") as f:
            f.write(code)
        os.system("g++ out.cpp -o {}".format(name))
    except Exception as e:
        print(f"Error: {e}")
        exit(1)