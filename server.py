# coding:utf-8
import json
import random
import time
import urllib2



class ServerCli:

    node_list = []
    expectedClientNum = 3

    def __init__(self):
        pass

    @staticmethod
    def bootstrap(address, seeds):
        data = {
            "seeds": seeds
        }
        req = urllib2.Request("http://" + address + "/bootstrap",
                              json.dumps(data),
                              {"Content-Type": "application/json"})
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        return res

    def start_simulation(self):

        assert len(self.node_list) == self.expectedClientNum

        for node in self.node_list:
            seed_list = []
            for peer in self.node_list:
                if node != peer:
                    seed_list.append({"node_id": peer["node_id"], "ip": peer["ip"], "port": peer["port"]})
            print seed_list
            ServerCli.bootstrap(str(node["ip"]) + ":" + str(node["port"]), seed_list)

        print
        "ok"
        time.sleep(1)

        node1_wallet = self.node_list[0]["wallet"]
        node2_wallet = self.node_list[1]["wallet"]
        node3_wallet = self.node_list[2]["wallet"]

        while True:
            # node1 发送给node2 node3
            node1_balance = ServerCli.get_balance("127.0.0.1:5000", node1_wallet)
            node1_balance = node1_balance['balance']
            if node1_balance > 0:
                amount = random.randint(1, node1_balance) / 10
                print
                'send from node1 to node2 with amount:' + str(amount)
                ServerCli.simulate_tx("127.0.0.1:5000", node1_wallet, node2_wallet, amount)
                time.sleep(random.randint(4, 5))

            node1_balance = ServerCli.get_balance("127.0.0.1:5000", node1_wallet)
            node1_balance = node1_balance['balance']
            if node1_balance > 0:
                amount = random.randint(1, node1_balance) / 10
                print
                'send from node1 to node3 with amount:' + str(amount)
                ServerCli.simulate_tx("127.0.0.1:5000", node1_wallet, node3_wallet, amount)
                time.sleep(random.randint(4, 5))

            # node2 发送给node1 node3
            node2_balance = ServerCli.get_balance("127.0.0.1:5001", node2_wallet)
            node2_balance = node2_balance['balance']
            if node2_balance > 0:
                amount = random.randint(1, node2_balance) / 10
                print
                'send from node2 to node1 with amount:' + str(amount)
                ServerCli.simulate_tx("127.0.0.1:5001", node2_wallet, node1_wallet, amount)
                time.sleep(random.randint(4, 5))

            node2_balance = ServerCli.get_balance("127.0.0.1:5001", node2_wallet)
            node2_balance = node2_balance['balance']
            if node2_balance > 0:
                amount = random.randint(1, node2_balance) / 10
                print
                'send from node2 to node3 with amount:' + str(amount)
                ServerCli.simulate_tx("127.0.0.1:5001", node2_wallet, node3_wallet, amount)
                time.sleep(random.randint(4, 5))
            #
            # node3 发送给node1 node2
            node3_balance = ServerCli.get_balance("127.0.0.1:5002", node3_wallet)
            node3_balance = node3_balance['balance']
            if node3_balance > 0:
                amount = random.randint(1, node3_balance) / 10
                print
                'send from node3 to node1 with amount:' + str(amount)
                ServerCli.simulate_tx("127.0.0.1:5002", node3_wallet, node1_wallet, amount)
                time.sleep(random.randint(4, 5))

            node3_balance = ServerCli.get_balance("127.0.0.1:5002", node3_wallet)
            node3_balance = node3_balance['balance']
            if node3_balance > 0:
                amount = random.randint(1, node3_balance) / 10
                print
                'send from node3 to node2 with amount:' + str(amount)
                ServerCli.simulate_tx("127.0.0.1:5002", node3_wallet, node2_wallet, amount)
                time.sleep(random.randint(4, 5))
            time.sleep(5)


    @staticmethod
    def simulate_tx(address, sender, receiver, amount):
        data = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        }

        req = urllib2.Request(url="http://" + address + "/transactions/new",
                              headers={"Content-Type": "application/json"}, data=json.dumps(data))
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        return res


    @staticmethod
    def get_balance(address, wallet_address):
        req = urllib2.Request(url="http://" + address + "/balance?address=" + wallet_address,
                              headers={"Content-Type": "application/json"})

        res_data = urllib2.urlopen(req)
        res = res_data.read()
        return json.loads(res)


    @staticmethod
    def get_node_info(address):
        req = urllib2.Request(url="http://" + address + "/curr_node",
                              headers={"Content-Type": "application/json"})

        res_data = urllib2.urlopen(req)
        res = res_data.read()
        return json.loads(res)