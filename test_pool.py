import threading
class Student:
    def __init__(self, names, ages):
        self.names = names
        self.ages = ages
        self.shared_data = 0
        self.lock = threading.Lock()
    
    def task(self, i):
        with self.lock:
            self.shared_data += 1
        print(f"姓名：{self.names[i]}, 年龄：{self.ages[i]}, 共享变量：{self.shared_data}")
        
    def run_task(self):
        for i in range(3):
            self.task(i)
        

class test_task():
    def __init__(self):
        self.names = ["A", "B", "C"]
        self.ages = [5, 8, 10]
        self.stu_test = Student(names = self.names, ages = self.ages)
        

    def run(self):
        self.stu_test.run_task()
        

if __name__ == "__main__":
    run_task = test_task()
    run_task.run()