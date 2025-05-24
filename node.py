import math

class Node:
    def __init__(self, id, x, y, demand, readyTime, dueTime, serviceTime,pickuppair, deliverypair):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.readyTime = readyTime
        self.dueTime = dueTime
        self.serviceTime = serviceTime
        self.pickuppair = pickuppair
        self.deliverypair = deliverypair
        # self.serviceStartTime = serviceStartTime
        # self.waitingTime = waitingTime
    
    def __str__(self):
        return (f"Node id: {self.id}; location: ({self.x},{self.y}) demand: {self.demand}; readyTime: {self.readyTime}; dueTime: {self.dueTime}; serviceTime:{self.serviceTime}; pickuppair: {self.pickuppair}; deliverypair: {self.deliverypair}")

    def __eq__(self, other):
        # 当other也是Node实例且属性相同时，返回True
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __hash__(self):
        # 依据属性计算哈希值，保证相等的对象哈希值相同
        return hash(self.id)

    def getDistance(p1, p2):
        """Calculate the eculidean distance between p1 and p2

        Args:
            p1 (Node): node 1
            p2 (Node): node 2

        Returns:
            float: distance btw p1 and p2
        """
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        return math.sqrt(dx ** 2 + dy ** 2)
    
    