import time

class colorPrint():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'

    @staticmethod
    def info(data):
        print(colorPrint.OKBLUE + '[' + time.strftime("%Y-%m-%d %X") + '] - ' + '[INF]'  + data + colorPrint.END)

    @staticmethod
    def ok(data):
        print(colorPrint.OKGREEN + '[' + time.strftime("%Y-%m-%d %X") + '] - ' + '[INF]' + data + colorPrint.END)
        
    @staticmethod
    def warning(data):
        print(colorPrint.OKBLUE + '[' + time.strftime("%Y-%m-%d %X") + '] - ' + '[WAR]'  + data + colorPrint.END)

    @staticmethod
    def error(data):
        print(colorPrint.ERROR + '[' + time.strftime("%Y-%m-%d %X") + '] - ' + '[ERR]'  + data + colorPrint.END)
