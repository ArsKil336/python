from decimal import Decimal


def newInt(
    IN="w",
    end="-е",
    sep="~~",
    text: str = "Введите число",
    errorText: str = "Это не число!",
    iskls=[],
    max="",
    min="",
):
    while True:
        try:
            if IN != "w":
                s = text.split(sep)
                text = (str(IN) + str(end)).join(s)
            text = "".join(text.split(": "))
            if iskls != []:
                l = []  # noqa: E741
                for i in iskls:
                    if i not in l:
                        l.append(i)
                iskls = l
                iskls.sort()
                d = ""
                d += " (запрещён ввод: "
                for i in iskls:
                    d += str(i)
                    if iskls[-1] != i:
                        d += ", "
                d += ")"
                text += d
            while True:
                n = int(input(text + ": "))
                if not (type(max) in (int, float)):
                    min = n
                if not (type(max) in (int, float)):
                    max = n
                if n <= max:
                    if n >= min:
                        if n not in iskls:
                            return n
                        else:
                            printPlus("Число находится в запрещённых! " + d)
                    else:
                        printPlus(f"Число меньше минимума! (макс. = {max})")
                else:
                    printPlus(f"Число больше максимума! (мин. = {min})")
        except ValueError:
            print(errorText)


def printPlus(
    *items, w: bool = True, sep=", ", sep_in_brackets=", ", brackets="()", end="\n"
):
    items = [*items]
    if items == []:
        print()
    else:
        x = 0
        for i in items:
            x += 1
            if x == len(items) and w:
                q = ""
            else:
                q = sep
            if isinstance(i, (list, tuple)):
                if brackets != "":
                    print(brackets[0], end="")
                p = 0
                for j in i:
                    p += 1
                    printPlus(
                        j,
                        w=p == len(i),
                        sep=sep_in_brackets,
                        sep_in_brackets=sep_in_brackets,
                        end="",
                    )
                if brackets != "":
                    print(brackets[-1], end=q)
            else:
                print(i, sep=sep, end=q)
        print(end, end="")


def claim(value, min="", max=""):

    if type(value) in [int, float]:
        if type(max) not in [int, float]:
            max = value
        if type(min) not in [int, float]:
            min = value
        if value > max:
            value = tryToInt(max)
        elif value < min:
            value = tryToInt(min)
        return value
    else:
        return 0


def ListToNums(List: list, iskls=[], max="", min=""):
    s = []
    for i in List:
        if i not in iskls:
            try:
                s.append(claim(int(i), min=min, max=max))
            except ValueError:
                pass
    return s


def newListNums(
    count: int = 0, text: str = "Введите числа через пробел: ", min="", max=""
):
    if "~~" in text:
        text = str(count).join(text.split("~~"))
    s = newList(text)
    if count == 0:
        return ListToNums(s, min=min, max=max)
    elif len(ListToNums(s)) >= count:
        return ListToNums(s, min=min, max=max)[:count]
    else:
        n = count - len(ListToNums(s))
        List = ListToNums(s, min=min, max=max)
        for i in range(n):
            List += [0]
        return List


def newList(text: str = "Введите слова через пробел: "):
    return input(text).split()


def ToInt(text: str):
    while True:
        try:
            return int(text)
        except ValueError:
            return ""


def rangeList(start: float = 0, end: float = 0, step: float = 1, is_vkl: bool = True):
    n = 10 ** max(
        len(str(start).split(".")[-1]),
        len(str(end).split(".")[-1]),
        len(str(step).split(".")[-1]),
    )
    start *= n
    step *= n
    end *= n
    end += int(is_vkl)
    list = []
    for i in range(int(start), int(end), int(step)):
        list.append(tryToInt(i / n))
    return list


def newFloat(
    text: str = "Введите число с плавающей точкой",
    errorText: str = "Это не число!",
    iskls=[],
):
    if type(iskls) not in [list, tuple]:
        iskls = [iskls]
    while True:
        try:
            text = "".join(text.split(": "))
            if iskls != []:
                new_list = []
                for i in iskls:
                    if i not in new_list:
                        new_list.append(i)
                iskls = new_list
                iskls.sort()
                text += " (запрещён ввод: "
                for i in iskls:
                    text += str(i)
                    if iskls[-1] != i:
                        text += ", "
                text += ")"
            while True:
                n = float(input(text + ": "))
                if n not in iskls:
                    return tryToInt(n)
                else:
                    printPlus("Число находится в запрещённых!")
        except ValueError:
            print(errorText)


def newRangeList(
    text1="Введите первое число: ",
    text2="Введите второе число: ",
    is_vkl: bool = True,
    text_step: str = "Введите шаг: ",
):
    "".join(text1.split(": "))
    text1 += ": "

    "".join(text2.split(": "))
    if is_vkl:
        text2 += " (включительно)"
    text2 += ": "

    start = newInt(text=text1)
    end = newInt(text=text2)
    step = newFloat(text_step)

    return rangeList(start=start, end=end, step=step, is_vkl=is_vkl)


def tryToInt(num: float):
    if abs(int(num) - num) <= 0.001:
        return int(num)
    elif abs(int(num) + 1 - num) <= 0.001:
        return int(num) + 1
    else:
        return num


def ToStr(value):
    Type = type(value)
    if Type is list or Type is tuple:
        l = []
        for i in value:
            l.append(ToStr(i))
        if Type is tuple:
            l = tuple(l)
        return l
    else:
        return str(value)


def ListMagic(list: list | tuple, value, operation="*"):
    type_now = type(list)
    new_list = []
    for el in list:
        if operation == "+":
            try:
                el += value
            except:
                el = str(el) + str(value)
            new_list.append(el)
        elif operation == "-":
            try:
                el -= value
                new_list.append(el)
            except:
                pass
        elif operation == "/":
            try:
                el /= value
                new_list.append(el)
            except:
                pass
        else:
            try:
                el *= value
                new_list.append(el)
            except:
                pass
    if type_now is tuple:
        new_list=tuple(new_list)
    return new_list