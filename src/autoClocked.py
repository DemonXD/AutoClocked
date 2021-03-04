#################################################
#   Author     : Miles Xu
#   Date       : 2021/03/02 17:50
#   Email      : kanonxmm@163.com
#   License    : MIT
#   Desc.      : 自动网页打卡程序
#   Python lib : Python -> 3.7.7
#                APScheduler
#                selenium
#   过程描述    : 
#################################################
import datetime
import os
import time
import functools
import logging
from random import randint
from selenium import webdriver
# 实现规避检测
from selenium.webdriver import ChromeOptions
from apscheduler.schedulers.background import BackgroundScheduler


def create_logger(path):
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("AutoClocked_logger")

    # logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.WARN)
 
    # create the logging file handler
    fh = logging.FileHandler(f"{path}\\test.log")
 
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger
 

def check_can_clock(func):
    """ check the clock time is suitable or not
        修饰类方法的时候，第一个参数肯定为self，即类的实例
    Args:
        func ([type]):
        Desc.        : 1. 生成打卡时间
                       2. 判断当前时间是否大于打卡时间且是在同一天
                            1. 是，则继续执行打卡程序
                            2. 否，将打卡时间置None，goto start
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if isinstance(args[0], Clocked):
            args[0].generate_clocked_time()
            if (datetime.datetime.now() > args[0].clocked_date) and \
                (datetime.date.today().day - args[0].clocked_date.day == 0):
                args[0].logger.info(f"满足设定时间，执行函数, 当前时间：{datetime.datetime.now()} 设定时间：{args[0].clocked_date}")
                return func(*args, **kwargs)
            args[0].clocked_date = None
            args[0].logger.info(f"不满足设定时间，执行函数， 设定时间：{args[0].clocked_date}")
    return wrapped


def check_is_clocked(func):
    """
        check if clocked today or not
        修饰类方法的时候，第一个参数肯定为self，即类的实例
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if isinstance(args[0], Clocked):
            all_files = os.listdir(args[0].screenshot_daily_clocked_path)
            if f"{time.strftime('%Y-%m-%d')}.png" not in all_files:
                args[0].logger.info("没有打过卡，执行打卡程序")
                return func(*args, **kwargs)
            args[0].logger.info("已打卡")
    return wrapped
    

class Clocked:
    clocked_url = r"url/to/your/website"
    chrome_driverpath = "D:\\AutoClocked\\chromedriver_win32\\chromedriver.exe"
    screenshot_daily_clocked_path = os.path.join(os.path.expanduser("~"), "AutoClocked")
    logdir = os.path.join(screenshot_daily_clocked_path, "Logs")
    # screenshot_daily_clocked_path = "E:\\Clocked_Screenshot"
    clocked_date = None
    logger = create_logger(logdir)

    def __init__(self) -> None:
        self.check_dirs()

    def check_dirs(self):
        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)
            self.logger.debug("目录不存在, 已创建")


    def init_chrome_options(self):
        options = ChromeOptions()
        options.add_argument("headless")                # 无头浏览器
        options.add_argument("disable-gpu")             # 禁用gpu
        options.add_argument('log-level=3')             # 设置日志打印级别
        options.add_argument('disable-infobars')        # 禁用浏览器显示被自动化软件调用
        options.add_argument("incognito")               # 隐身模式
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        prefs = {
            "profile.defautl_content_settings.popups":0,
            "download.default_directory": self.screenshot_daily_clocked_path
        }
        options.add_experimental_option("prefs", prefs)
        return options

    @check_is_clocked
    def generate_clocked_time(self):
        if self.clocked_date is None:
            random_min = randint(1, 10)
            self.clocked_date = datetime.datetime(
                year=datetime.date.today().year,
                month=datetime.date.today().month,
                day=datetime.date.today().day,
                hour=8,
                minute=40
            ) + datetime.timedelta(minutes=random_min)
            self.logger.info(f"执行生成打卡时间: {self.clocked_date}")

    @check_is_clocked # 这里后装载，先执行, 功能：未打卡则继续向下执行
    @check_can_clock # 这里先装载，后执行， 功能：看函数
    def clocked_(self):
        options = self.init_chrome_options()
        driver = webdriver.Chrome(executable_path=self.chrome_driverpath, options=options)
        driver.get(self.clocked_url)
        time.sleep(3)
        clocked_file_name = os.path.join(
                self.screenshot_daily_clocked_path,
                f"{time.strftime('%Y-%m-%d')}.png"
            )
        driver.save_screenshot(clocked_file_name)
        driver.close()
        self.logger.info(f"完成打卡，clocked_date: {self.clocked_date}")
        # 将 clocked_date 置None
        self.clocked_date = None


    def START(self):
        scheduler = BackgroundScheduler()
        # 周一到周五， 早上8:30 执行
        scheduler.add_job(self.clocked_, 'interval', seconds=30)
        # scheduler.add_job(self.clocked_, 'cron', day_of_week='mon-fri', hour=8, minute=30)
        scheduler.start()

if __name__=="__main__":
    try:
        clocked = Clocked()
        clocked.START()
        while True:
            time.sleep(1)
    except BaseException as e:
        clocked.logger.error(str(e))