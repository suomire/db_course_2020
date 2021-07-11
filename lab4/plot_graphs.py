import matplotlib.pyplot as plt
import numpy as np
import json

"""
Дополнительный скрипт для построения графиков сразу после завершения эксперимента с нагрузкой БД

"""


def plot_and_save(threads, power):
    f = open("exp1/load_" + str(threads) + "_" + str(power) + ".log", 'r')

    queries = set()
    total_threads = set()
    mean_time = []
    queries_ms = []

    for x in f:
        s = json.loads(x)
        total_threads.add(s['total_threads'])
        queries.add(s['total_queries'])
        mean_time.append(s['mean_time'])
        queries_ms.append(s['query_ms'])
        print(s)

    print(total_threads, queries, mean_time, queries_ms)

    x_queries = list(queries)
    x_queries.sort()
    x_queries = x_queries * 4
    y = []

    if threads != 1:
        for i in range(0, len(mean_time), threads):
            res = sum(mean_time[i:i + 2]) / threads
            # res = sum(queries_ms[i:i + 2]) / threads
            y.append(res)
    else:
        y = mean_time
        # y = queries_ms
    print(x_queries, y, sep='\n')

    # зависимость среднего времени выполнения от количества запросов
    fig = plt.figure(figsize=(15, 12))
    for x in range(1):
        ax = fig.add_subplot(1, 1, x + 1)
        label1 = str(threads) + " thread(s) before optimization"
        label2 = str(threads) + " thread(s) with indexes"
        label3 = str(threads) + " thread(s) with prepare statement"
        label4 = str(threads) + " thread(s) with full optimization"
        ax.plot(x_queries[:power + 1], y[:power + 1], label=label1)
        ax.plot(x_queries[power + 1:2 * (power + 1)], y[1 * (power + 1):2 * (power + 1)], label=label2)
        ax.plot(x_queries[2 * (power + 1):3 * (power + 1)], y[2 * (power + 1):3 * (power + 1)], label=label3)
        ax.plot(x_queries[3 * (power + 1):], y[3 * (power + 1):], label=label4)
        ax.legend(loc='upper left')
        ax.set_xlabel('Number of queries')
        # ax.set_ylabel('Query per ms ')
        ax.set_ylabel('Mean time per query in ms')


    # fig.tight_layout()

    plt.savefig('images/exp1/graphs_' + str(threads) + "_" + str(power) + ".png")
    # plt.show()


if __name__ == '__main__':
    # threads_experiments = [1, 2, 5, 7, 10, 20]
    # queries_number = [1, 2, 4, 8, 10, 12, 14]

    threads_experiments = [1, 2, 5, 7, 10, 20]
    queries_number = [1, 2, 4, 8, 10]

    for x in threads_experiments:
        for y in queries_number:
            threads, power = x, y
            plot_and_save(threads, power)
