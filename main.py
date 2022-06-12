from sys import argv
from json import loads
from Translators.lang_brainfuck import lang_brainfuck_translate
from Translators.lang_length import lang_length_translate


def main() -> int:
    filename = argv[1]
    lang = langhandler(filename)
    translator_handler(filename, lang)
    return 0


def langhandler(filename: str) -> str:
    langs = {
        "b": "BRAINFUCK",
        "bf": "BRAINFUCK",
        "brainfuck": "BRAINFUCK",
        "lang_brainfuck": "BRAINFUCK",
        "len": "LENGTH",
        "lang_length": "LENGTH"
    }
    try:
        lang = argv[2]
    except IndexError:
        try:
            return langs[filename.split(".")[-1]]
        except KeyError:
            print("Language could not be detected!")
            exit(1)
    if lang.upper() in langs.values():
        return lang
    else:
        try:
            return langs[filename.split(".")[-1]]
        except KeyError:
            print("Language could not be detected!")
            exit(1)


def translator_handler(filename: str, lang: str) -> None:
    translation_dict = {
        "BRAINFUCK": lang_brainfuck_translate,
        "LENGTH": lang_length_translate
    }
    with open(filename, "rt") as f:
        translation_dict[lang](f.read(), filename.lower())

if __name__ == '__main__':
    main()
