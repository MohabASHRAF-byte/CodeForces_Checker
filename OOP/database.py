import sqlite3


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
            t = list(i)
            t.insert(0, idx)
            p.append(tuple(t))
        self.conn.executemany("INSERT INTO problems VALUES(?,?,?)", p)
        self.conn.commit()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

