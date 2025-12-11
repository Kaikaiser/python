from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import random




def work():
    print("-----------这是map线程池的实现-----------")
    # 共享数据
    shared_data = 0
    # 锁
    lock = threading.Lock()

    # 任务函数
    def task(i):
        nonlocal shared_data
        t = random.uniform(0.3, 1)
        time.sleep(t)
        with lock:
            shared_data += 1
            print(f"Task {i}: shared_data is {shared_data}, sleep for {t} seconds")
        return i, shared_data   


    # 任务参数
    tasks = [i for i in range(20)]

    # 保存结果
    results = []

    # 创建线程池
    with ThreadPoolExecutor(max_workers = 8) as executor:
        # executor.map(func, iterable)， map 可以自动把 iterable 里的每个元素作为参数传入 func， 按循环分发线程
        # 使用map 包含自动提交任务、等待结果、按顺序返回结果(按照输入顺序)
        # 按照的顺序是任务提交顺序 但是线程执行时不是乱序执行的
        results = list(executor.map(task, tasks))
    # zip是压缩 把两个列表的参数聚合在一起 *是拆包，是把聚合的分开
    task_index, values = zip(*results)
    task_index = list(task_index)
    values = list(values)
    return task_index, values

if __name__ == "__main__":
    print(work())