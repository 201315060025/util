# encoding: utf-8
"""
auto: blx
target:  简要说明 log 的使用方法
"""
import sys
import os
import time
sys.path.append(os.getcwd())
# import log
from log import get_module_logger

""" 
def get_module_logger(module_name,
                      ch_level=logging.WARNING,
                      enable_fh=True,
                      fh_level=logging.INFO,
                      log_dir=None)
                      
module_name :当前log的类型
ch_level: 级别
log_dir: log文件的路径
"""

# log_exe = get_module_logger("test", log_dir=os.getcwd())

class LogExecute:
    def __init__(self, module_name, log_dir):
        self.logger = get_module_logger(module_name, log_dir=log_dir)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warn(self, message):
        self.logger.warn(message)



class Student:
    def __init__(self,
                name: str,
                age: int,
                logger: LogExecute,
                sex: str = 'man'):
        self.name = name
        self.age = age
        self.logger = logger
        self.sex = sex

    def say(self):
        self.logger.info(f"{self.name} start sing..")
        time.sleep(1)
        print(self.name, "say we all same..")

    def play(self):
        self.logger.info(f"{self.name} start play bock")
        print(f"{self.name} is playing")
        time.sleep(5)
        self.logger.warn(f"{self.name} play long time and need to sleep")

    def test_error(self):
        self.logger.error(f"{self.name} is error..")

if __name__ == "__main__":
    log_obj = LogExecute("Test", os.getcwd())
    stu = Student("blx", 12, log_obj)
    stu.say()
    stu.play()
    stu.test_error()