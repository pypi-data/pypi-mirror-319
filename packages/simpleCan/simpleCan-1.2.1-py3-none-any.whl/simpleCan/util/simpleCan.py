"""
Created on 2024-11-26
@author: Liu Jiajie(Chris)
@contact: chris.liu@scania.com.cn
"""
import logging
from simpleCan.util import xldriver
from simpleCan.util.task  import Task
from simpleCan.util.signal_table import Signal_table_messageList

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)

class SimpleCan:

    def __init__(self):
        # create a list to store all messages sending to DDU
        self.tasklist = []
        self.st = Signal_table_messageList()
        xldriver.setup()

    # use the below functions if you need to set up Can signal environment
    def update_Excel_path(self, path):
        self.st.setExcelPath(path)
        self.env_setup()

    # from messagelist, read all the messages and convert them into tasks.
    # then append to taskList
    def env_setup(self,duration = 60):
        messageList = self.st.get_messageList()
        for i in range(len(messageList)):
            self.tasklist.append(Task(message_id=messageList[i].id,
                                      data=messageList[i].data,
                                      period=messageList[i].period,
                                      duration=duration))
    def env_run(self):
        for task in self.tasklist:
            task.task_run()

    # this function simply creates a task that sends message through Can channel
    # each task contains four attributes:
    # message_id -- id of the message you want to send
    # data  -- data of the message you want to send. Example: [0,0,0,0,0,0,0,0]
    # period -- frequency of the message you want to send. Unit in seconds.
    # duration -- If you need explanation for this, then your intelligence level is not suitable for using this package.
    def sendMessage(self, message_id, data, period, duration = 30):
        task = Task(message_id=message_id,
                    data = data,
                    period = period,
                    duration = duration)
        self.tasklist.append(task)
        task.task_run()


    def modifyMessage(self, message_id, data):
        try:
            for task in self.tasklist:
                if task.get_messageID() == message_id:
                    task.task_modifyData(newData = data)
        except Exception as e:
            logging.error(e)

    def endAllTasks(self):
        for task in self.tasklist:
            task.task_stop()






