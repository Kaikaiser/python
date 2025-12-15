# import threading
# import queue
# import time


# class Future:
#     """简单 Future：存储结果 / 异常 / 完成状态"""
#     def __init__(self):
#         self._done = False
#         self._result = None
#         self._exception = None
#         self._cond = threading.Condition()

#     def done(self):
#         return self._done

#     def result(self, timeout=None):
#         """等待任务完成并返回结果"""
#         with self._cond:
#             if not self._done:
#                 self._cond.wait(timeout)

#             if self._exception:
#                 raise self._exception

#             return self._result

#     def set_result(self, result):
#         with self._cond:
#             self._result = result
#             self._done = True
#             self._cond.notify_all()

#     def set_exception(self, exc):
#         with self._cond:
#             self._exception = exc
#             self._done = True
#             self._cond.notify_all()


# class ThreadPool:
#     """自定义线程池"""
#     def __init__(self, max_workers=4):
#         self.max_workers = max_workers
#         self.tasks = queue.Queue()
#         self.threads = []
#         self._shutdown = False

#         for _ in range(max_workers):
#             t = threading.Thread(target=self._worker)
#             t.daemon = True
#             t.start()
#             self.threads.append(t)

#     def _worker(self):
#         """线程池内部线程的循环任务"""
#         while True:
#             try:
#                 fn, args, kwargs, future = self.tasks.get(timeout=0.1)
#             except queue.Empty:
#                 if self._shutdown:
#                     break
#                 continue

#             try:
#                 result = fn(*args, **kwargs)
#                 future.set_result(result)
#             except Exception as e:
#                 future.set_exception(e)
#             finally:
#                 self.tasks.task_done()

#     def submit(self, fn, *args, **kwargs):
#         """提交一个任务"""
#         future = Future()
#         self.tasks.put((fn, args, kwargs, future))
#         return future

#     def shutdown(self, wait=True):
#         """关闭线程池"""
#         self._shutdown = True
#         if wait:
#             for t in self.threads:
#                 t.join()




import threading
import queue
import time

""" Future用来存放 任务完成结果的状态 """
class Future:
    def __init__(self) -> None:
        self._cond = threading.Condition()
        self._result = None
        self.done = False


    # 等待任务完成取结果
    def result(self, timeout = None):
        with self._cond:
            if not self.done:
                self._cond.wait(timeout) # 未得到结果就进行睡眠

            return self._result

    # 获取结果唤醒result
    def set_result(self, result):
        with self._cond:
            self.done = True
            self._result = result
            self._cond.notify_all()

    # 异常获取
    def set_exception(self):
        pass


""" ThreadPool线程池 """
class ThreadPool:
    def __init__(self, max_workers = 8) -> None:
        self.max_workers = max_workers  # 最大线程数
        self.tasks = queue.Queue()  # 存放任务的队列
        self.threads = []
        self.is_shutdown = False

    def init_workers(self):
        """ 初始化长期工作线程，避免重复创建 """
        for _ in range(self.max_workers):
            t = threading.Thread(target = self.worker)
            t.start()
            self.threads.append(t)

    def worker(self):
        while(True):
            task = self.tasks.get()
            try:
                func, future, args, kwargs = task
                result = func(*args, **kwargs)
                future.set_result(result)

            except Exception as e:
                pass
            finally:
                self.tasks.task_done()


    def submit(self, func, *args, **kwargs):
        # 提交一个任务
        future = Future()
        self.tasks.put((func, future, args, kwargs))
        return future
        

    def shutdown(self, wait = True):
        """设置worker退出条件"""
        # 使用put将睡眠的get给唤醒
        for _ in self.threads:
            self.tasks.put[None]

        for t in self.threads:
            t.join()
        

    





