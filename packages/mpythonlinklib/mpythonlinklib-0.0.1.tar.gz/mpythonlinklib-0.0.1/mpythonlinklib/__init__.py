import socket

class hardware_control():
    def __init__(self,ip,port,car_type):
        self.address = (ip,port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.car = car_type
        
    #发送消息
    def send_msg_to_car(self,message):
        self.socket.sendto(bytes(str(message),"utf-8"), self.address)
    
    #设置速度
    def set_speed(self,Lspeed,Rspeed):
        message = {'key':1,'args':[int(Lspeed),int(Rspeed)]}
        self.send_msg_to_car(message)
        
    #停止
    def stop(self):
        message = {'key':2}
        self.send_msg_to_car(message)
        
    #根据距离移动
    def move_by_distance(self,speed,distance):
        message = {'key':3,'args':[int(speed),int(distance)]}
        self.send_msg_to_car(message)
    
    #根据时间移动
    def move_by_time(self,Lspeed,Rspeed,time):
        message = {'key':4,'args':[int(Lspeed),int(Rspeed),int(time)]}
        self.send_msg_to_car(message)
        
    #设置板载三颗RGB
    def set_rgb(self,rgb_type,rgb_list):
        if rgb_type == "all":
            message = {'key':13,'args':[int(rgb_list[0]),int(rgb_list[1]),int(rgb_list[2])]}
        else:
            message = {'key':14,'args':[int(rgb_type),int(rgb_list[0]),int(rgb_list[1]),int(rgb_list[2])]}
        self.send_msg_to_car(message)