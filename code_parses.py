import re

class CodeParser:
    ROUND_BRACKETS = ["[(]", "[)]"]
    SQUARE_BRACKETS = ["[\[]", "[\]]"]
    FIGURE_BRACKETS = ["[{]", "[}]"]
    REMOVE_EXTRA_SYMBOLS = 1

    def __init__(self):
        self.__string = ""

    def load_from_file(self, path, remove_extras):
        with open(path, "r") as file_obj:
            extracted = file_obj.read()
            if remove_extras: #если нужно, то удаляются переносы строк
                extracted = re.sub(r"(?:\n|\r)", " ", extracted)
            self.__string = extracted
            return extracted

    def check_brackets_pairing(self, bracket_type): #проверяется просто парность скобок по их количеству, а не правильность их расстановки
        m1 = re.findall(bracket_type[0], self.__string)
        m2 = re.findall(bracket_type[1], self.__string)

        if (m1 is None and m2 is None) or (len(m1) == len(m2)):
            return True
        else:
            return False

    def check_unused_names(self): #возвращает список единожды упомянутых в коде переменных, работает только с правильно именованными переменными, поэтому проверку правильности надо произвести заранее
        custom_names = re.findall("(?:class\s*|struct\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*{", self.__string) #нашли имена типов классов и структур, теперь их надо добавить к поиску
                                                                                                       #alias и typedef не учитываются
        str = ""
        for item in custom_names:
            str += item + "\s*|"
        pattern = ("(?:" + str + "auto\s*|short\s*|long\s*|char\s*|int\s*|float\s*|double\s*|bool\s*|)"
                                 "(?:\*?\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*[\[;,=)]") #паттерн, учитывающий стандартыне типы, типы классов и структур
        print(pattern)
        names = re.findall(pattern, self.__string) #здесь найдены все имена переменных в программе, включая имена классов, структур и стандартных имен С++
        names = list(set(names)) #удаление повторов, так как имена у локальных переменных разных блоков кода могут повотряться
        #теперь пробежимся по всему файлу для каждого имени и найдем, сколько раз оно встречалось в коде, по предположению, если имя встретилось единожды, значит было только объявлено и не использовалось, что и требуется найти
        report = []
        print(names)
        for name in names:
            name_count = re.findall("(?:\s+|\()" + name + "(?:\s+|[-=\[;\)+\*/%^])", self.__string)
            if len(name_count) == 1:
                report.append(name)
        print(report)
        return report

def main():
    parser = CodeParser()
    parser.load_from_file(r"D:\source.cpp", CodeParser.REMOVE_EXTRA_SYMBOLS)
    parser.check_unused_names()


main()
