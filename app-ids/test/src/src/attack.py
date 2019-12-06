import paho.mqtt.client as mqtt 
import threading 
import time

class Attack(object):

    def __init__(self):
        self.calc_flag = False
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        calc_thread = threading.Thread(target=self.calc)
        calc_thread.start()
        self.client.connect("test.mosquitto.org")
        print("Starting loop")
        self.client.loop_forever()

    def on_connect(self,client,userdata,flags,msg):
        print("Connected successfully to the broker")
        self.client.subscribe("ATTACK")
        

    def on_subscribe(self,sclient, userdata, mid, granted_qos):
        print("Subscribed to the broker successfully with granted qos {0}".format(granted_qos ))

    def on_message(self,client,userdata,msg):
        print("Message received")
        self.calc_flag = 2
    def calc(self):
        print("Starting calc")
        while self.calc_flag != 2:
            time.sleep(1)
            print("Testing")
        while True:
            self.calc_flag = self.calc_flag * self.calc_flag
            print(self.calc_flag)
    def on_log(client,userdata,level,buff):
        print(buff)         
if __name__ == "__main__":
    a = Attack()

