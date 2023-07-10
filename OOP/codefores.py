import requests
from bs4 import BeautifulSoup
from database import DB
from timer import Timer


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



