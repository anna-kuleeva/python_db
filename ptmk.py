import datetime, sys, random, string, timeit
import sqlite3
from sqlite3 import Error


class Query:
    def __init__(self, fio, dob, sex):
        self.fio = fio
        self.dob = dob
        self.sex = sex

    def __str__(self):
        return f"('{self.fio}', '{self.dob}', '{self.sex}')"


class MyDB:
    def __init__(self):
        # Укажите свой путь к файлу!
        self.connection = create_connection("C:\\Users\\heath\\Desktop\\универ\\9 сем (я в шоке)\\test.sqlite")
        self.cur = self.connection.cursor()

    def create_table(self):
        try:
            self.cur.execute(
                '''CREATE TABLE IF NOT EXISTS employee(fio TEXT NOT NULL, date_of_birth DATE, sex TEXT NOT NULL);''')
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def insert_one(self, name, dob, s):
        insert_query = f"INSERT INTO employee (fio, date_of_birth, sex) VALUES ('{name}', '{dob}', '{s}');"
        try:
            self.cur.execute(insert_query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_query(self, query):
        try:
            self.cur.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def select_data(self, mode):
        # Вывод всех строк справочника сотрудников, с уникальным значением ФИО+дата,
        # отсортированным по ФИО. Вывести ФИО, Дату рождения, пол, кол-во полных лет.
        # select_query = f"SELECT DISTINCT fio, date_of_birth, sex, (date('now') - date_of_birth) FROM employee ORDER BY fio;"
        select_query = ""
        if mode == 3:
            select_query = f"SELECT *, (date('now') - date_of_birth) FROM employee" \
                       f" GROUP BY  fio, date_of_birth" \
                       f" ORDER BY fio;"
            self.cur.execute(select_query)
        elif mode == 5:
            #EXPLAIN QUERY PLAN
            # self.execute_query("CREATE INDEX IF NOT EXISTS fio_ind ON employee(fio, date_of_birth);")
            select_query = f"SELECT * FROM employee WHERE sex = 'Male' AND fio LIKE 'F%';"
            execution_time = timeit.timeit(lambda: self.cur.execute(select_query), number=1)
            print("Execution Time:", execution_time)
        rows = self.cur.fetchall()
        #for result in rows:
         #   print(result)

    def __del__(self):
        self.connection.close()

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def rand_date():
    start_date = datetime.date(1970, 1, 1)
    end_date = datetime.date(2005, 1, 1)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date

def randomword():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(32))

if __name__ == "__main__":
    db = MyDB()
    if sys.argv[1] == "1":
        db.create_table()
    elif sys.argv[1] == "2":
        argc = (len(sys.argv) - 2)
        values_list = f"INSERT INTO 'employee' (fio, date_of_birth, sex) VALUES "
        i = 2
        while argc > 0:
            query = Query(sys.argv[i], sys.argv[i + 1], sys.argv[i + 2])
            values_list += query.__str__()
            i += 3
            argc -= 3
            if argc == 0:
                values_list += ";"
            else:
                values_list += ","
        print(values_list)
        db.execute_query(values_list)
        # db.insert_one(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "3":
        db.select_data(3)
    elif sys.argv[1] == "4":
        values_mil = f"INSERT INTO 'employee' (fio, date_of_birth, sex) VALUES "
        for i in range(1000000):
            fio = randomword()
            dob = rand_date()
            sex = random.choice(['Male', 'Female'])
            # print(fio, dob, sex)
            query = Query(fio, dob, sex)
            values_mil += query.__str__()
            if i == (1000000 - 1):
                values_mil += ";"
            else:
                values_mil += ","
        db.execute_query(values_mil)
        values_hun = f"INSERT INTO 'employee' (fio, date_of_birth, sex) VALUES "
        for j in range(100):
            fio = "F" + randomword()
            dob = rand_date()
            sex = "Male"
            # print(fio, dob, sex)
            query = Query(fio, dob, sex)
            values_hun += query.__str__()
            if j == 99:
                values_hun += ";"
            else:
                values_hun += ","
        print(values_hun)
        db.execute_query(values_hun)
    elif sys.argv[1] == "5":
        db.select_data(5)
    elif sys.argv[1] == "6":
        db.execute_query("CREATE INDEX IF NOT EXISTS fio_ind ON employee(fio);")
        db.select_data(5)
    else:
        print("No such action!")
