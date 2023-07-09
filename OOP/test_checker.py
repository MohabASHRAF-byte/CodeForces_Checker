def assign_str(idx: int, li: list):
    tmp = str()
    try:
        tmp = li[idx]
    except Exception:
        pass
    return tmp


def assign_char(idx: int, li: str):
    tmp = '*'
    try:
        tmp = li[idx]
    except Exception:
        pass
    return tmp


def assign_line(idx: int, li: list):
    tmp = list()
    try:
        tmp = li[idx]
    except Exception:
        pass
    return tmp


def segment_checker(user: str, code: str):
    s = str()
    for i in range(max(len(user), len(code))):
        userChar = assign_char(i, user)
        codeChar = assign_char(i, code)
        if userChar == codeChar:
            s += userChar
        else:
            s += '*'
    return s


def test_line_checker(user: str, code: str):
    try:
        user = user.split(' ')
    except Exception:
        pass
    try:
        code = code.split(' ')
    except Exception:
        pass
    li = list()
    for i in range(max(len(user), len(code))):
        userSeg = assign_str(i, user)
        codeSeg = assign_str(i, code)
        x = segment_checker(userSeg, codeSeg)
        li.append(x)
    return li


class Checker:
    ret = list()
    user, codeforces = list, list
    n1, n2 = 0, 0

    def __init__(self, str1: str, str2: str):
        self.user = [i.strip() for i in str1.strip().split('\n')]
        self.codeforces = [i.strip() for i in str2.strip().split('\n')]

    def do_work(self):
        self.n1, self.n2 = len(self.user), len(self.codeforces)
        ret = self.check()
        return ret

    def check(self):
        li = list()
        for i in range(max(self.n1, self.n2)):
            userLine = assign_line(i, self.user)
            codeforcesLine = assign_line(i, self.codeforces)
            x = test_line_checker(userLine, codeforcesLine)
            li.append(x)
        return li

    @staticmethod
    def is_valid(ret: list):
        for i in ret:
            for ii in i:
                for iii in ii:
                    if iii == '*':
                        return False
        return True
