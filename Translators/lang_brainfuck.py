import re
import os
from typing import Tuple

def lang_brainfuck_translate(rawcode: str, name:str) -> int:
    code = clean(rawcode)
    if "," in code:
        keyvec, countvec = optimizer(code)
        outcode = translator(keyvec, countvec)
    else:
        outcode = renderer(code)
    compiler(outcode, ".".join(name.split(".")[:-1]))
    return 0


def clean(rawcode: str) -> str:
    return "".join(re.findall(r"<|>|\+|\-|,|\.|\[|\]", rawcode))


def optimizer(code: str) -> Tuple[list[str], list[int]]:
    keyvec = []
    countvec = []
    prev = ""
    for command in code:
        if prev != command or command in ".[]":
            prev = command
            keyvec.append(command)
            countvec.append(1)
        else:
            countvec[-1] += 1
    return (keyvec, countvec)


def translator(keyvec: list[str], countvec: list[int]) -> str:
    outcode = ["#include <stdio.h>", "int main() {", "int array[30000] = {0};", "int idx = 0;"]
    for index in range(len(keyvec)):
        match keyvec[index]:
            case ".":
                outcode.append("putchar(array[idx]);")
            case ",":
                outcode.append("array[idx] = getchar();")
            case "[":
                outcode.append("while (array[idx]) {")
            case "]":
                outcode.append("}")
            case "+":   
                outcode.append(f"array[idx]+= {countvec[index]};")
            case "-":
                outcode.append(f"array[idx]-= {countvec[index]};")
            case "<":
                outcode.append(f"idx-= {countvec[index]};")
            case ">":
                outcode.append(f"idx+= {countvec[index]};")
            case _:
                pass
    outcode.append("return 0;")
    outcode.append("}")
    return "\n".join(outcode)

def compiler(code: str, name: str) -> None:
    try:
        with open("out.cpp", "wt") as f:
            f.write(code)
        os.system("g++ out.cpp -o {}".format(name))
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

def renderer(code:str) -> str:
    output = ""
    memory = [0] * 30000
    idx = 0
    index = 0
    fwloops, bwloops = findloops(code)
    while index != len(code):
        match code[index]:
            case ".":
                output += chr(memory[idx])
            case "+":
                memory[idx] = (memory[idx] + 1) % 256
            case "-":
                memory[idx] = memory[idx]-1 if memory[idx] > 0 else 255
            case "<":
                idx -= 1
            case ">":
                idx += 1
            case "[":
                if memory[idx] == 0:
                    index = int(fwloops[str(index)])
            case "]":
                if memory[idx] != 0:
                    index = int(bwloops[str(index)])
            case _:
                pass
        index += 1
    return "#include <iostream>\nint main() {\nstd::cout << \""+output[:-1]+"\";\nreturn 0;\n}"

def findloops(code: str) -> Tuple[dict[str:str],dict[str:str]]:
    fwloops = {}
    bwloops = {}
    loopstack = []
    for i, e in enumerate(code):
        if e == "[":
            loopstack.append(i)
        elif e == "]":
            fwloops[str(loopstack[-1])] = str(i)
            bwloops[str(i)] = str(loopstack[-1])
            loopstack.pop()
    return (fwloops, bwloops)