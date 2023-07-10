import requests
from bs4 import BeautifulSoup
import time
import subprocess
import sqlite3

# contest / gym id
contest_id = 1846
# problem index
problem = 'a'
#  c++ file path in pc
path = r"main.cpp"


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("problems.db")
        self.cur = self.conn.cursor()
        self.available = True
        self.tests = list()

    def get_test(self):
        return self.tests

    def do_work(self, idx: str):
        self.cur.execute(f'SELECT ROWID,* FROM problems WHERE indx="{idx}"')
        rows = self.cur.fetchall()
        # print(rows)
        # print(len(rows))
        if len(rows) == 0:
            self.available = False
            return
        testss = list()
        for row in rows:
            inp, out = str(), str()
            for line in str(row[2]).strip().split('\n'):
                inp += (line.strip() + '\n')
            for line in str(row[3]).strip().split('\n'):
                out += (line.strip() + '\n')
            testss.append((inp.strip(), out.strip()))
        self.tests = testss

    def display(self):
        for test in self.get_test():
            print(test[0])
            print('-' * 100)
            print(test[1])
            print('*' * 100)

    def is_ava(self):
        return self.available

    def push(self, li: list, idx: str):
        p = list()
        for i in li:
            tt = list(i)
            tt.insert(0, idx)
            p.append(tuple(tt))
        self.conn.executemany("INSERT INTO problems VALUES(?,?,?)", p)
        self.conn.commit()

    def __del__(self):
        self.conn.commit()
        self.conn.close()


#
# ob = DB()
# ob.do_work("1145B")
# print(ob.is_ava())
# # ob.do_work()
# # ob.get_test()
# ob.display()
# ob.push(li, "1146B")
# ob.display()

def assign_str(idx: int, li: list):
    tmp = str()
    try:
        tmp = li[idx]
    except IndexError:
        pass
    return tmp


def assign_char(idx: int, li: str):
    tmp = '*'
    try:
        tmp = li[idx]
    except IndexError:
        pass
    return tmp


def assign_line(idx: int, li: list):
    tmp = list()
    try:
        tmp = li[idx]
    except IndexError:
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


class Run:
    cpp_file_path = path

    compile_command = f"g++ {cpp_file_path} -o compiled_cpp_file"
    input_string = str()

    def do_work(self, cppInput: str):
        self.input_string = cppInput
        # Compile the C++ file
        compile_command = f"g++ {self.cpp_file_path} -o compiled_cpp_file"
        subprocess.run(compile_command, shell=True, check=True)

        # Run the compiled C++ file
        run_command = "./compiled_cpp_file"
        process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=True)

        # Pass input string to the running process
        output, error = process.communicate(input=self.input_string.encode())
        output = output.decode().strip()
        error = error.decode().strip()
        return len(error) != 0, error if error else output


class Timer:

    def __init__(self):
        self.start_time = time.time()

    def calc(self):
        return time.time() - self.start_time


class Codeforces:
    contestId, problemIdx, contest_type = 0, 0, 0
    inputList, outputList = [], []
    db = DB()

    def __init__(self):
        self.ob = Timer()

    def t(self):
        print(self.ob.calc())

    def get_tests(self, idd: int, idx):
        indx = f'{idd}{idx.upper()}'
        self.db.do_work(indx)
        if self.db.is_ava():
            return self.db.get_test()
        self.contestId = idd
        self.problemIdx = idx.upper()
        self.contest_type = "problemset" if self.contestId < 3000 else "gym"
        li = self.do_work()
        if not self.db.is_ava():
            self.db.push(li, indx)
        return li

    def do_work(self):
        soup = self.get_page()
        self.inputList = self.get_input(soup).copy()
        self.outputList = self.get_output(soup).copy()
        li = list()
        for i, ii in zip(self.inputList, self.outputList):
            li.append((i, ii))
        return li

    def get_page(self):
        if self.contestId > 3000:
            url = f"https://codeforces.com/gym/{self.contestId}/problem/{self.problemIdx}"
        else:
            url = f"https://codeforces.com/problemset/problem/{self.contestId}/{self.problemIdx}"
        page = requests.get(url)
        if page.status_code != 200:
            print("Problem Not found ")
            return
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    @staticmethod
    def get_input(content: BeautifulSoup):
        codeforces_input = content.find_all("div", attrs={"class", "input"})
        li = list()
        for test in codeforces_input:
            test = test.find("pre")
            test_with_lines = test.find_all("div")
            psh = str()
            if len(test_with_lines) == 0:
                psh = test.text
            else:
                for ii in test:
                    psh += (ii.text + '\n')
            li.append(psh.strip())
        return li

    @staticmethod
    def get_output(content: BeautifulSoup):
        codeforces_output = content.find_all("div", attrs={"class", "output"})
        li = list()
        for test in codeforces_output:
            test = test.find("pre").text.strip()
            li.append(test)
        return li


def print_red(text):
    RED = '\033[91m'  # ANSI escape sequence for red text
    RESET = '\033[0m'  # ANSI escape sequence to reset the text color

    print(RED + text + RESET, end='')


def print_green(text):
    GREEN = '\033[92m'  # ANSI escape sequence for green text
    RESET = '\033[0m'  # ANSI escape sequence to reset the text color

    print(GREEN + text + RESET, end='')


ob = Timer()
ProgramRun = Run()
codeforces = Codeforces()
codeforces_tests = codeforces.get_tests(contest_id, problem)
print(ob.calc())
cnt = 1
val = True
for t in codeforces_tests:
    # codeforces input / output
    ci = t[0]
    co = t[1]
    # er
    er, user_output = ProgramRun.do_work(ci)
    checker = Checker(user_output, co)
    res = checker.do_work()
    isValid = 'T' if checker.is_valid(res) else 'F'
    if isValid == 'T':
        print_green(f'Test {cnt} : {isValid}')
    else:
        print_red(f'Test {cnt} : {isValid}')
        val = False
    print()
    cnt += 1
    #  l for line
    for ll in res:
        for seg in ll:
            for ch in seg:
                if ch == '*':
                    print_red(ch)
                else:
                    print_green(ch)
            print(end=' ')
        print()
    print()
if val:
    print_green("Time elapsed : " + str(round(ob.calc(), 5)))
else:
    print_red("Time elapsed : " + str(round(ob.calc(), 5)))
del codeforces.db
