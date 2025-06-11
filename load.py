## 从Space-Track.org下载指定NORAD ID的原始TLE数据并保存到TXT文件

import requests
import configparser
from datetime import datetime

class MyError(Exception):
    def __init__(self, resp, message):
        self.resp = resp
        self.message = message
        super().__init__(f"{message}: {resp.status_code} - {resp.text}")

# Space-Track.org API配置
uriBase = "https://www.space-track.org"
requestLogin = "/ajaxauth/login"
requestCmdAction = "/basicspacedata/query" 

# 在这里直接设置要下载的NORAD ID（可以是一个或多个，用逗号分隔）
# NORAD_IDS = "43476, 43477"  # Grace_follow
# configOut = "GraceFo_tle.txt"

NORAD_IDS = "46026"  # Grace_follow
configOut = "Tsinghua.txt"
 
# 从配置文件读取凭证
config = configparser.ConfigParser()
config.read("./load.ini")
configUsr = config.get("configuration", "username")
configPwd = config.get("configuration", "password")
siteCred = {'identity': configUsr, 'password': configPwd}

def download_raw_tle(session, norad_id):
    """下载指定NORAD ID的原始TLE数据"""
    print(f"正在下载NORAD ID {norad_id} 的TLE数据...")
    requestTLE = f"/class/tle/NORAD_CAT_ID/{norad_id}/orderby/EPOCH%20asc/format/tle"
    resp = session.get(uriBase + requestCmdAction + requestTLE)
    if resp.status_code != 200:
        raise MyError(resp, "获取TLE数据失败")
    return resp.text

def save_to_txt(raw_tle, filename, norad_id):
    """将原始TLE保存到TXT文件"""
    print("正在保存数据到TXT文件...")
    
    # 分割原始TLE数据行并移除空行
    lines = [line.strip() for line in raw_tle.split('\n') if line.strip()]
    
    # 重新组织TLE格式
    formatted_tle = []
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            # 添加两行TLE数据
            formatted_tle.append(lines[i])
            formatted_tle.append(lines[i+1])
            # 添加一个空行分隔不同的TLE组
            formatted_tle.append('')
    
    # 移除最后一个多余的空行
    if formatted_tle and formatted_tle[-1] == '':
        formatted_tle = formatted_tle[:-1]
    
    # 写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        # 写入文件头信息
        f.write(f"TLE数据 (原始数据，未处理)\n")
        f.write(f"下载时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"数据来源: Space-Track.org\n")
        f.write(f"NORAD ID: {norad_id}\n")
        f.write("="*50 + "\n\n")
        
        # 写入TLE数据
        f.write('\n'.join(formatted_tle))
    
    print(f"数据已保存到 {filename}")


def main():
    try:
        with requests.Session() as session:
            # 登录Space-Track
            resp = session.post(uriBase + requestLogin, data=siteCred)
            if resp.status_code != 200:
                raise MyError(resp, "登录失败")
            
            # 下载TLE数据
            raw_tle = download_raw_tle(session, NORAD_IDS)
            
            # 保存到TXT文件
            save_to_txt(raw_tle, configOut, NORAD_IDS)
            
    except Exception as e:
        print(f"程序出错: {str(e)}")
    finally:
        print("程序执行完毕")

if __name__ == "__main__":
    main()