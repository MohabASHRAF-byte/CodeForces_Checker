from codefores import Codeforces
from run_file import Run
from test_checker import Checker

def print_red(text):
    RED = '\033[91m'  # ANSI escape sequence for red text
    RESET = '\033[0m'  # ANSI escape sequence to reset the text color

    print(RED + text + RESET, end='')


def print_green(text):
    GREEN = '\033[92m'  # ANSI escape sequence for green text
    RESET = '\033[0m'  # ANSI escape sequence to reset the text color

    print(GREEN + text + RESET, end='')


ProgramRun = Run()
codeforces = Codeforces()
codeforces_tests = codeforces.get_tests(1846, "b")
cnt = 1
for test in codeforces_tests:
    codeforces_input = test[0]
    codeforces_output = test[1]
    error, user_output = ProgramRun.do_work(codeforces_input)
    checker = Checker(user_output, codeforces_output)
    res = checker.do_work()
    isValid = 'T' if checker.is_valid(res) else 'F'
    if isValid == 'T':
        print_green(f'Test {cnt} : {isValid}')
    else:
        print_red(f'Test {cnt} : {isValid}')
    print()
    cnt += 1

    for line in res:
        for seg in line:
            for ch in seg:
                if ch == '*':
                    print_red(ch)
                else:
                    print_green(ch)
            print(end=' ')
        print()
    print()
