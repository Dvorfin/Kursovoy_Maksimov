import psycopg2 as sql
from psycopg2 import Error


def connection():  # функция установки соединения с бд
    con = None
    try:
        con = sql.connect(
            database='test',     # db name
            user='postgres',     # username
            password='1',        # user pass
            host='127.0.0.1',    # ip (foreign/local)
            port='5432'          # port
        )
    except (Exception, Error) as error:
        print("Connection failed, error: ", error)
    finally:
        if con:
            print("Database opened successfully")
            return con


def insert_data(table_name, val):  # attr - список атрибутов, values - строка значений
    con = connection()
    # метод курсор соединения, используется для выполненния команд
    # т.к. инесртить надо будет только в main и prog_name,
    # то есть только два случая инсерта
    # пример входных данных:
    # values = "2, 2, 2, 2"  - вводимая строка данных в main
    # insert_data('main', values)  - вызов функции

    if table_name == 'main':
        query = "INSERT INTO main (prog_name, error_num, error_stat, error_importance) " \
                "VALUES(" + val + ")"
    else:
        query = "INSERT INTO prog_name (name) VALUES('" + val + "')"
        print(query)
    cur = con.cursor()
    cur.execute(  # выполенение запроса к бд
        query
    )

    con.commit()  # коммитит изменения в бд
    print("Record inserted successfully")
    cur.close()  # закрывает общение с бд


def select_all(table_name):
    con = connection()
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM " + table_name
    )

    # возвращает список кортежей
    rows = cur.fetchall()
    for row in rows:  # идем по кортежу
        for i in range(len(rows[0])):  # идем по списку в кортеже
            print(row[i], end=' ')
        print()

    print("Selection done successfully")
    con.close()


def select_all_inner():  # возвращает иннер селект из мейна
    con = connection()
    cur = con.cursor()
    # селект из main сгруппированный по названию программы
    query = '''SELECT u_id, T.name, num, stat, value
            FROM public.main AS P
            INNER JOIN prog_name AS T ON  P.prog_name = T."key" 
            INNER JOIN error_num ON P.error_num = error_num."key"
            INNER JOIN error_stat ON P.error_stat = error_stat."key"
            INNER JOIN error_importance ON P.error_importance = error_importance."key"
            ORDER BY name'''

    query_with_condition = '''SELECT u_id, T.name, error_num, error_stat, error_importance
                    FROM public.main
                    INNER JOIN prog_name AS T ON  main.prog_name = T."key"
                    WHERE main.prog_name = '1'
                    '''
    cur.execute(
        query
    )

    rows = cur.fetchall()  # возвращает список кортежей

    print("-" * 80)
    for row in rows:  # идем по кортежу
        for i in range(len(rows[0])):  # идем по списку в кортеже
            val = row[i]
            if type(val) == str:
                print('{:<16}'.format(val.strip()), end='')
            else:
                print('{:<8}'.format(val), end='')
        print()
    print("-" * 80)
    print("Selection done successfully")
    con.close()
    return rows


def delete_data(table_name, attr, val):  # мб понадобится, хз
    con = connection()
    cur = con.cursor()
    cur.execute(
        "DELETE from " + table_name + " where " + attr + " = " + val
    )
    con.commit()
    print("Delete done successfully")
    con.close()


def data_handler_from_main():  # надо подумать надо обработкой
    lst = []
    tup = select_all_inner()[1]
    for i in range(len(tup)):
        lst.append(tup[i])
    lst[1] = lst[1].replace(' ', '')
    lst[3] = lst[3].replace(' ', '')
    lst[4] = lst[4].replace(' ', '')
    return lst


if __name__ == '__main__':
    #insert_data(prog_name, attr, value): # attr - список атрибутов, val - список значений

    # select_all('error_num')
    # select_all('error_stat')
    # select_all('error_importance')
    # select_all('prog_name')
    # select_all('main')
    # select_all_inner()

    print(data_handler_from_main())

# не получается в бд передавать данные запросом
# insert into prog_name values("name_of_programm")
# ругается на то, что не в тот атрибут пишется значение,
# хотя с установленным праймари кеем должно работать

# чтобы заносить данные в main, нам нужно знать название программы
# чтобы сопоставить ее айдишник с именем, чтобы в инсерте указать
# правильный айди проги
