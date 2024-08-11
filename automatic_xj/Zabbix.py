import yaml
from playwright.sync_api import sync_playwright
import pytesseract
import cv2
class Zabbix:
    def __init__(self, browser,system_name):
        self.system_name=system_name
        self.main_url = None
        self.account = None
        self.password = None
        self.page=browser.new_page()
        self.load_zabbix_config()
    def load_zabbix_config(self):
        with open("zabbix_config.yaml", 'rb') as file:
            zabbix_config = yaml.safe_load(file)
            self.main_url = zabbix_config['main_url']
            self.account = zabbix_config[self.system_name]['account']
            self.password = zabbix_config[self.system_name]['password']


    def get_text_from_img(self,img):
        '''
        如何由playwright 的img 转换为 str
        :param img:
        :return:
        '''
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        retval, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        blur = cv2.GaussianBlur(threshold, (5, 5), 0)
        contours, hierarchy = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        count = 0
        result=0
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if w > 10 and h > 10:
                roi = blur[y:y + h, x:x + w]
                cv2.imwrite(str(count) + '.jpg', roi)
                text = pytesseract.image_to_string(roi, lang='eng')
                if text!='':
                    result=text
                    result = result.strip()
                count += 1
        return result
    def login(self):
        self.page.goto(self.main_url)
        self.page.wait_for_timeout(2000)  #延迟等待2s
        # textlines=self.page.locator('.el-input__inner')
        account_text=self.page.get_by_role('text')
        print(type(account_text))
        passsword_text=self.page.get_by_role('password')
        captch_img=self.page.locator('#captcha-image')
        captcha_text=self.page.locator('#captcha')
        account_text.fill(self.account)
        passsword_text.fill(self.password)
        #captcha_text.fill(self.get_text_from_img(captch_img))
        captcha_text.fill("xxx")
        bt_login=self.page.get_by_role('button')
        bt_login.click();


# # 使用示例
# url = "http://your_zabbix_server/api_jsonrpc.php"
# username = "Admin"
# password = "zabbix"
# zabbix = Zabbix(url, username, password)
# zabbix.homepage_display()
# zabbix.alert_display()
# zabbix.important_host_search("important_keyword")