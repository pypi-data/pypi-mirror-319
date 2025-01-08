import IP2Location
import os

def get_ip_info(ip_address):
    try:
        database = IP2Location.IP2Location(os.path.join("data", "IP2LOCATION-LITE-DB3.BIN"))
        rec = database.get_all(ip_address)
        return rec
    except Exception as e:
        print("未找到该IP地址对应的地理信息" + str(e))


if __name__ == "__main__": 
    ip = "8.8.8.8"
    print(get_ip_info(ip))