from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import random



def work():
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
        return shared_data   


    # 保存任务完成对象
    Futures = []

    # 保存结果
    results = []

    # 创建线程池
    with ThreadPoolExecutor(max_workers = 4) as executor:
        # 提交多个任务
        for i in range(1000):
            Futures.append(executor.submit(task, i))

        # 等待任务完成

        # 接收一个 Future 对象列表
        # 返回一个 可迭代对象，迭代顺序是 任务完成的顺序，而不是提交顺序
        # 非常适合 任务耗时不均匀 的情况，可以“先处理先完成的任务”
        for f in as_completed(Futures):
            results.append(f.result())
    return results

if __name__ == "__main__":
    print(work())