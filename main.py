import threading
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# =========================
# ЗАВДАННЯ 1 — Race condition
# =========================

counter = 0

def increment():
    global counter
    for _ in range(100000):
        counter += 1

def task1():
    global counter
    counter = 0

    t1 = threading.Thread(target=increment)
    t2 = threading.Thread(target=increment)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Task 1 result:", counter)

# =========================
# ЗАВДАННЯ 2 — Lock
# =========================

lock = threading.Lock()
counter_lock = 0

def increment_lock():
    global counter_lock
    for _ in range(100000):
        with lock:
            counter_lock += 1

def task2():
    global counter_lock
    counter_lock = 0

    t1 = threading.Thread(target=increment_lock)
    t2 = threading.Thread(target=increment_lock)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Task 2 result:", counter_lock)

# =========================
# ЗАВДАННЯ 3 — Без mutable state
# =========================

def increment_func(x):
    return x + 1

def task3():
    data = [1, 2, 3, 4, 5]
    result = list(map(increment_func, data))
    print("Task 3:", result)

# =========================
# ЗАВДАННЯ 4 — ThreadPoolExecutor
# =========================

def square(x):
    return x * x

def task4():
    data = [1,2,3,4,5]
    with ThreadPoolExecutor() as executor:
        result = list(executor.map(square, data))
    print("Task 4:", result)

# =========================
# ЗАВДАННЯ 5 — parallel_map
# =========================

def parallel_map(func, data):
    with ThreadPoolExecutor() as executor:
        return list(executor.map(func, data))

def task5():
    print("Task 5:", parallel_map(square, [1,2,3,4]))

# =========================
# ЗАВДАННЯ 6 — Порівняння часу
# =========================

def task6():
    data = range(1_000_000)

    start = time.time()
    list(map(square, data))
    print("Normal map:", time.time() - start)

    start = time.time()
    parallel_map(square, data)
    print("Parallel map:", time.time() - start)

# =========================
# ЗАВДАННЯ 7 — CPU-bound
# =========================

def heavy_task(x):
    total = 0
    for i in range(10_000_00):
        total += i * x
    return total

def task7():
    data = [1,2,3,4]

    start = time.time()
    list(map(heavy_task, data))
    print("Sequential:", time.time() - start)

    start = time.time()
    with ThreadPoolExecutor() as executor:
        list(executor.map(heavy_task, data))
    print("ThreadPool:", time.time() - start)

    start = time.time()
    with ProcessPoolExecutor() as executor:
        list(executor.map(heavy_task, data))
    print("ProcessPool:", time.time() - start)

# =========================
# ЗАВДАННЯ 8 — Pipeline
# =========================

def task8():
    data = range(100)

    with ThreadPoolExecutor() as executor:
        mapped = list(executor.map(lambda x: x*x, data))

    filtered = list(filter(lambda x: x > 100, mapped))
    result = sum(filtered)

    print("Task 8:", result)

# =========================
# ЗАВДАННЯ 9 — pipeline API
# =========================

def pipeline(data, steps):
    for step in steps:
        data = step(data)
    return data

def task9():
    result = pipeline(
        range(10),
        [
            lambda d: map(lambda x: x*x, d),
            lambda d: filter(lambda x: x > 10, d),
            lambda d: sum(d)
        ]
    )
    print("Task 9:", result)

# =========================
# ЗАВДАННЯ 10 — Safe map
# =========================

def risky(x):
    if x == 0:
        raise ValueError("Zero!")
    return 10 / x

def safe_parallel_map(func, data):
    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(func, x) for x in data]

        for f in futures:
            try:
                results.append(f.result())
            except Exception as e:
                results.append(str(e))

    return results

def task10():
    print("Task 10:", safe_parallel_map(risky, [1,2,0,5]))

# =========================
# ЗАВДАННЯ 11 — транзакції
# =========================

def task11():
    transactions = range(1_000_000)

    with ThreadPoolExecutor() as executor:
        filtered = list(filter(lambda x: x % 2 == 0, transactions))
        mapped = list(executor.map(lambda x: x * 2, filtered))

    print("Task 11:", sum(mapped))

# =========================
# ЗАВДАННЯ 12 — API simulation
# =========================

def fetch_data(x):
    time.sleep(1)
    return x

def task12():
    data = range(10)

    start = time.time()
    list(map(fetch_data, data))
    print("Sequential:", time.time() - start)

    start = time.time()
    with ThreadPoolExecutor() as executor:
        list(executor.map(fetch_data, data))
    print("Parallel:", time.time() - start)

# =========================

if __name__ == "__main__":
    for _ in range(3):
        task1()

    task2()
    task3()
    task4()
    task5()
    task6()
    task7()
    task8()
    task9()
    task10()
    task11()
    task12()
