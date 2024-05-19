import yaml
from playwright.sync_api import sync_playwright
class Zabbix:
    def __init__(self, browser,system_name):
        self.system_name=system_name
        self.main_url = nil
        self.account = nil
        self.password = nil
        self.load_zabbix_config()

    def load_zabbix_config(self):
        with open("zabbix_config.yaml", 'r') as file:
            playwright_config = yaml.safe_load(file)
            self.main_url = playwright_config[self.system_name]['main_url']
            self.account = playwright_config[self.system_name]['account']
            self.password = playwright_config[self.system_name]['password']
    def login(self):

        login_data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.username,
                "password": self.password
            },
            "id": 1,
            "auth": None
        }
        response = self.session.post(self.url, json=login_data)
        result = response.json()
        if 'result' in result:
            self.auth_token = result['result']
            return True
        else:
            print("Login failed:", result)
            return False

    def homepage_display(self):
        if not self.login():
            return
        # 获取一些首页展示数据，例如主机数量、监控项数量等
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend"
            },
            "id": 2,
            "auth": self.auth_token
        }
        response = self.session.post(self.url, json=data)
        hosts = response.json().get('result', [])
        print("Homepage Display:")
        print(f"Total number of hosts: {len(hosts)}")
        self.systems_list = [host['host'] for host in hosts]
        print("Systems List:", self.systems_list)

    def alert_display(self):
        if not self.login():
            return
        # 获取告警数据
        data = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": "extend",
                "filter": {
                    "value": 1  # 仅获取有告警的触发器
                },
                "selectHosts": ["host"]
            },
            "id": 3,
            "auth": self.auth_token
        }
        response = self.session.post(self.url, json=data)
        alerts = response.json().get('result', [])
        print("Alert Display:")
        for alert in alerts:
            for host in alert['hosts']:
                print(f"Host: {host['host']}, Alert: {alert['description']}")

    def important_host_search(self, keyword):
        if not self.login():
            return
        # 检索重要主机
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "search": {
                    "host": keyword
                }
            },
            "id": 4,
            "auth": self.auth_token
        }
        response = self.session.post(self.url, json=data)
        hosts = response.json().get('result', [])
        print(f"Important Host Search for '{keyword}':")
        for host in hosts:
            print(f"Host ID: {host['hostid']}, Host Name: {host['host']}")

# 使用示例
url = "http://your_zabbix_server/api_jsonrpc.php"
username = "Admin"
password = "zabbix"
zabbix = Zabbix(url, username, password)
zabbix.homepage_display()
zabbix.alert_display()
zabbix.important_host_search("important_keyword")