"""
параметры: количество потоков, количество запросов
количество запросов варьировать с помощью экспоненциальной функции

алгоритм прохода:
    выбирается кол-во потоков (ака юзеры) : один поток - одно подключение
    нагружать потоки запросами экспоненциально
    сохранять результаты эксперимента
    выводить графически

"""

import queries
import db_utils as utils
import threading
import numpy as np
import json

import logging
import random
import time

conn_params = None
times_res = []
after_prepare = False


def num_queries(n):
    return pow(2, n)


def wait_for_threads():
    while threading.active_count() > 1:
        continue


def create_indexes():
    conn, cursor = utils.connect()
    for ci_q in utils.create_idxs:
        cursor.execute(ci_q)
    utils.close_connection(conn, cursor)


def execute_query(i, thread_cursor):
    prep_line = ""
    queries_list = queries.l_of_queries
    if after_prepare:
        prep_line = "execute "
        queries_list = ["query_1 (%(min_date)s, %(max_date)s)", "query_2 (%s)", "query_3 (%s)", "query_4 ",
                        "query_5 (%s)"]

    if i == 0:
        item1, item2 = random.choice(queries.albums_release_dates), random.choice(queries.albums_release_dates)
        min_date = min(item1, item2)
        max_date = max(item1, item2)
        thread_cursor.execute("explain analyze " + prep_line + queries_list[i],
                              {'min_date': min_date, 'max_date': max_date})
    elif i == 1:
        thread_cursor.execute("explain analyze " + prep_line + queries_list[i],
                              (random.choice(queries.countries_singers),))

    elif i == 2:
        thread_cursor.execute("explain analyze " + prep_line + queries_list[i],
                              (random.choice(queries.record_label_ids),))

    elif i == 3:
        thread_cursor.execute("explain analyze " + prep_line + queries_list[i])

    else:
        thread_cursor.execute("explain analyze " + prep_line + queries_list[i],
                              (random.choice(queries.albums_names),))

    res = thread_cursor.fetchall()
    ex_time = float(res[-1][0].split(": ")[1].split(" ")[0])
    plan_time = float(res[-2][0].split(": ")[1].split(" ")[0])
    return ex_time + plan_time


def thread_func(n, pull_queries, num_threads):
    global times_res
    conn, cursor = utils.connect()
    times = []
    if after_prepare:
        for q in queries.prep_sqls:
            cursor.execute(q)

    for i in range(pull_queries):
        rand_i = random.randint(0, 4)
        t = execute_query(rand_i, cursor)
        execute_query(rand_i, cursor)
        times.append(t)

    times = np.array(times)
    res = np.sum(times)
    times_res.append((pull_queries, res / pull_queries))
    utils.close_connection(conn, cursor)
    thread_work_time_ms = time.thread_time_ns() / 10 ** 6

    log_result = {"total_threads": num_threads + 1,
                  "thread_num": n + 1,
                  "total_queries": pull_queries,
                  "mean_time": res / len(times),
                  "query_ms": pull_queries / thread_work_time_ms}

    json_log = json.dumps(log_result)
    logging.info(json_log)  # ms !!!


def start_experiment(max_n_of_threads, max_n_of_queries):
    for num_threads in range(max_n_of_threads - 1, max_n_of_threads):
        print('number of threads: ', num_threads + 1)
        for i in range(max_n_of_queries + 1):
            pq = num_queries(i)
            threads = []
            for t in range(num_threads + 1):
                x = threading.Thread(target=thread_func, args=(t, pq, num_threads), name=t)
                threads.append(x)
                x.start()
                # запрет на запуск потоков с увеличенным кол-вом запросов
                if t == num_threads:
                    wait_for_threads()


if __name__ == '__main__':
    global after
    log_format = "%(message)s"
    queries.get_global_list()

    threads_experiments = [1, 2, 5, 7, 10, 20]
    queries_number = [1, 2, 4, 8, 10, 12, 14]

    max_num_of_threads = 1
    max_num_of_queries = 1  # 2 ^ (max_num_of_queries) =  1024, try 500! or 1000

    filename_log = "exp1/load_" + str(max_num_of_threads) + "_" + str(max_num_of_queries) + ".log"
    # filename_log = "load_q" + ".log"
    logging.basicConfig(filename=filename_log,
                        # filename='data/load.log',
                        filemode='w', format=log_format,
                        level=logging.INFO)

    print('dropping indexes')
    utils.dropping_idxs()

    print('start new experiment without optimization')
    start_experiment(max_num_of_threads, max_num_of_queries)

    print('optimize with index adding')
    create_indexes()

    print('start new experiment with indexes')
    start_experiment(max_num_of_threads, max_num_of_queries)

    print('dropping indexes')
    utils.dropping_idxs()

    print("after_prepare")
    after_prepare = True

    print('start new experiment with prepares')
    start_experiment(max_num_of_threads, max_num_of_queries)

    print('optimize with index adding and prepare statement')
    print('add indexes')
    create_indexes()

    print('start new experiment with full optimisation')
    start_experiment(max_num_of_threads, max_num_of_queries)
