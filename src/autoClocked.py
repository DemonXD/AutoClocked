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


import os
import time
from random import randint
from selenium import webdriver
# 实现规避检测
from selenium.webdriver import ChromeOptions
from apscheduler.schedulers.background import BackgroundScheduler

clocked_url = r"http://erp.careerintlinc.com/sitepages/aportal/default.aspx"
edge_driverpath = "C:\\Users\\ci24924\\Desktop\\edgedriver_win64\\msedgedriver.exe"
chrome_driverpath = "C:\\Users\\ci24924\\Desktop\\chromedriver_win32\\chromedriver.exe"
screenshot_daily_clocked_path = "E:\\Clocked_Screenshot"

options = ChromeOptions()
options.add_argument("headless") # 无头浏览器
options.add_argument("disable-gpu") # 禁用gpu
options.add_argument('log-level=3') # 设置日志打印级别
options.add_argument('disable-infobars') # 禁用浏览器显示被自动化软件调用
options.add_argument("incognito") # 隐身模式
options.add_experimental_option("excludeSwitches", ["enable-automation"])
prefs = {"profile.defautl_content_settings.popups":0, "download.default_directory": screenshot_daily_clocked_path}
options.add_experimental_option("prefs", prefs)

global clocked_date
clocked_date = None

def check_is_clocked():
    """
        check if clocked today or not
    """
    pass

def generate_clocked_time():
    global clocked_date
    clocked_date = randint

def clocked_():
    global clocked_date
    driver = webdriver.Chrome(executable_path=chrome_driverpath, options=options)
    driver.get(clocked_url)
    time.sleep(3)
    clocked_file_name = os.path.join(
            screenshot_daily_clocked_path,
            f"{time.strftime('%Y-%m-%dT%H-%M-%SZ')}.png"
        )
    # clocked_file_name.replace("\\", "\\\\")
    driver.save_screenshot(clocked_file_name)
    driver.close()


def main():
    scheduler = BackgroundScheduler()
    # 周一到周五， 早上8:30 执行
    scheduler.add_job(clocked_, 'cron', day_of_week='mon-fri', hour=8, minute=30)
    scheduler.start()

if __name__=="__main__":
    try:
        inter = randint(10, 20)
        main(inter)
        while True:
            time.sleep(10)
    except BaseException as e:
        with open(f"{screenshot_daily_clocked_path}\\error.log", "a+") as f:
            f.write(str(e) + "\n")