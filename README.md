# PUT - (P)ython(U)niversal(T)ranslator

A Python based universal translator to c++ for a variaty of [esolangs](https://esolangs.org/).

## [Brainfuck](https://esolangs.org/wiki/Brainfuck)

### Extensions:

```
.b
.bf
.lang_brainfuck
```
 or specified via the second command line argument specifying the language.

### Features:
- Code Summation (n lines of `idx++` become `idx += n`)
- Code Rendering (if no input command is given the output is calculated beforehand and the only command is `std::cout << render`)


## [Length](https://esolangs.org/wiki/Length)

### Extensions:

```
.len
.lang_length
```
 or specified via the second command line argument specifying the language.

### Features:
- Code Rendering (if no input command is given the output is calculated beforehand and the only command is `std::cout << render`)

## Authors

- [@TheEyeOfAres](https://www.github.com/TheEyeOfAres)


## License

[MIT](https://choosealicense.com/licenses/mit/)