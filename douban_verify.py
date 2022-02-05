"""
说明：先输入几次错误的密码，出现滑块缺口验证码
"""
from selenium import webdriver
# 导入鼠标事件类
from selenium.webdriver import ActionChains
import time

# 加速度函数
def get_tracks(distance):

    """
    拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
    匀变速运动基本公式：
    ① v=v0+at
    ② s=v0t+½at²
    """
    # 初速度
    v = 0
    # 单位时间为0.3s来统计轨迹，轨迹即0.3内的位移
    t = 0.3
    # 位置/轨迹列表,列表内的一个元素代表0.3s的位移
    tracks = []
    # 当前的位移
    current = 0
    # 到达mid值开始减速
    mid = distance*4/5
    while current < distance:
        if current < mid:
            # 加速度越小,单位时间内的位移越小,模拟的轨迹就越多越详细
            a = 2
        else:
            a = -3

        # 初速度
        v0 = v
        # 0.3秒内的位移
        s = v0*t+0.5*a*(t**2)
        # 当前的位置
        current += s
        # 添加到轨迹列表
        tracks.append(round(s))
        # 速度已经达到v，该速度作为下次的初速度
        v = v0 + a*t
    return tracks
    # tracks: [第一个0.3秒的移动距离,第二个0.3秒的移动距离,...]

# 1、打开豆瓣官网 - 并将窗口最大化
driver = webdriver.Firefox()
driver.maximize_window()
driver.get('https://www.douban.com')

# 2、切换到iframe子页面
iframe_node = driver.find_element_by_xpath('//div[@class="login"]/iframe')
driver.switch_to.frame(iframe_node)
time.sleep(3)

# 3、密码登录 + 用户名 + 密码 + 登录豆瓣
driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]').click()
driver.find_element_by_xpath('//*[@id="username"]').send_keys('17740464396')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('3570liu')
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]/a').click()
# 增大延时，以防定位不到元素
time.sleep(6)

# 4、切换到新的iframe子页面 - 滑块验证
verify_iframe = driver.find_element_by_xpath('//*[@id="tcaptcha_iframe"]')
driver.switch_to.frame(verify_iframe)

# 5、按住开始滑动位置按钮 - 先移动180个像素
start_node = driver.find_element_by_xpath('//*[@id="tcaptcha_drag_button"]')
ActionChains(driver).click_and_hold(on_element=start_node).perform()

# 移动到距离某个节点多少的距离的位置
ActionChains(driver).move_to_element_with_offset(to_element=start_node, xoffset=180, yoffset=0).perform()

# 6、使用加速度函数移动剩下的距离
tracks = get_tracks(30)
for track in tracks:
    # move_by_offset:鼠标从当前位置,移动多少的距离
    ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()

# 7、延迟释放鼠标: release()
time.sleep(2)
ActionChains(driver).release().perform()