import re


class CodeParser:
    ROUND_BRACKETS = ["[(]", "[)]"]
    SQUARE_BRACKETS = ["[\[]", "[\]]"]
    FIGURE_BRACKETS = ["[{]", "[}]"]
    REMOVE_EXTRA_SYMBOLS = 1

    def LoadFromFile(self, path, removeExtra):
        with open(path, "r") as file_obj:
            extracted = file_obj.read()
            if removeExtra:
                extracted = re.sub(r"\n", "", extracted)
            return extracted

    def CheckBracketsPairing(self, string, bracketType):
        m1 = re.findall(bracketType[0], string)
        m2 = re.findall(bracketType[1], string)

        if (m1 is None and m2 is None) or (len(m1) == len(m2)):
            return True
        else:
            return False


def main():
    parser = CodeParser()
    # res = parser.CheckBracketsPairing("int main(){ int a[]= {5, 2}; return 0;}", CodeParser.SQUARE_BRACKETS)
    print(parser.LoadFromFile(r"D:\source.cpp", CodeParser.REMOVE_EXTRA_SYMBOLS))


main()
