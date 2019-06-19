import configparser


config = configparser.ConfigParser()

config['BlueRing'] = {
    "ipv6_enabled": "True",
    "udp_enabled": "True",
    "proxy_type": "0",
    "proxy_host": "None",
    "proxy_port": "0",
    "start_port": "0",
    "end_port": "0",
    "tcp_port": "0",
    "savedata_type": "0",
    "savedata_data": "None",
    "bootstrap_node" : "198.199.98.108", # US bootstrap node (nodes.tox.chat)
    "bootstrap_port" : "33445",
    "bootstrap_key" : "BEF0CFB37AF874BD17B9A8F9FE64C75521DB95A37D33C5BDB00E9CF58659C04F",
                    }

with open('BlueRing.ini', 'w') as confFile:
    config.write(confFile)