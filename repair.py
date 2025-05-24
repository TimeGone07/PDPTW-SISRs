import sys

from parameters import Parameters
from route import Route
class Repair:
    
    def __init__(self, instance, solution):
        self.instance = instance
        self.solution = solution 
    
    def executeMultiGreedyInsertion(self, randomGen):
        sortByRules = randomGen.randint(1, 7)
        tempArray = []
        if sortByRules == 1:
            sorted(self.solution.notServed, key = lambda node: node.demand, reverse = True)
            # sort by demand, from high to low
            
        elif sortByRules == 2:
            sorted(self.solution.notServed, key = lambda node: (node.x - self.instance.depot.x )**2 + (node.y - self.instance.depot.y)**2, reverse = True)
            # sort by distance, from high to low
            
        elif sortByRules == 3:
            sorted(self.solution.notServed, key = lambda node: (node.x - self.instance.depot.x )**2 + (node.y - self.instance.depot.y)**2, reverse = False)
            # sort by distance, from low to high
            
        elif sortByRules == 4:
            sorted(self.solution.notServed, key = lambda node: node.dueTime - node.readyTime, reverse = False)
        elif sortByRules == 5:
            sorted(self.solution.notServed, key = lambda node: node.readyTime, reverse = False)
        elif sortByRules == 7:
            sorted(self.solution.notServed, key = lambda node: node.dueTime, reverse = True)
        else:
            randomGen.shuffle(self.solution.notServed)
            # random shuffle
            # print("H4")
            # for node in self.solution.notServed:
            #     print(node)

        tempArray = self.solution.notServed.copy()
        
        while True:
            cus = self.solution.notServed[0]
            if cus.pickuppair==0:
                pickup=cus
                delivery=self.instance.getpairnode(cus)
            else:
                pickup = self.instance.getpairnode(cus)
                delivery = cus
            #print("repair id:", pickup.id,delivery.id)
            curMinIncrement = sys.maxsize
            curBest = None
            curBestRouteIdx = None
            for idx, potentialRoute in enumerate(self.solution.routes):
                #获取所有可行位置
                iters=potentialRoute.getalliters(pickup,delivery)
                if not iters:
                    continue
                #afterInsert, costIncrement = potentialRoute.greedyInsert(cus)
                #迭代所有位置
                for iter in iters:
                    if randomGen.random() < 1-Parameters.blinkrate:
                        #pre, succ, cost = iter
                        if iter[2] < curMinIncrement:
                            curMinIncrement = iter[2]
                            curBest = iter
                            curBestRouteIdx = idx

            if curBest == None:
                # means cannot find a way to insert ... 
                nodeList = [self.instance.depot, pickup, delivery, self.instance.depot]
                newRoute = Route(self.instance, nodeList, set(nodeList))
                self.solution.routes.append(newRoute)
                self.solution.distance += (self.instance.distMatrix[0][pickup.id]+self.instance.distMatrix[pickup.id][delivery.id] + self.instance.distMatrix[delivery.id][0])
            else:
                self.solution.routes[curBestRouteIdx].insertcustomer(pickup, delivery,curBest[0],curBest[1])
                self.solution.distance += curMinIncrement
            # print(cus in self.solution.notServed)
            self.solution.notServed.remove(pickup)
            self.solution.served.append(pickup)
            self.solution.notServed.remove(delivery)
            self.solution.served.append(delivery)
            if not self.solution.notServed:
                break


    
    def executeGreedyInsertion(self, randomGen):

        while len(self.solution.notServed) > 0:
            
            cus = randomGen.choice(self.solution.notServed)
            # random select the customer ... 
            curMinIncrement = sys.maxsize
            curBestRoute = None 
            curBestRouteIdx = None
            
            for idx, potentialRoute in enumerate(self.solution.routes):
                afterInsert, costIncrement = potentialRoute.greedyInsert(cus)
                if randomGen.random() < 0.99:
                    if afterInsert:
                        if costIncrement < curMinIncrement:
                            curMinIncrement = costIncrement
                            curBestRoute = afterInsert
                            curBestRouteIdx = idx

            if curBestRoute == None:
                # means cannot find a way to insert ... 
                nodeList = [self.instance.depot, cus, self.instance.depot]
                newRoute = Route(self.instance, nodeList, set(nodeList))
                self.solution.routes.append(newRoute)
                self.solution.distance += (self.instance.distMatrix[0][cus.id] + self.instance.distMatrix[cus.id][0])
            else:
                self.solution.routes[curBestRouteIdx] = Route(self.instance, curBestRoute, set(curBestRoute))
                self.solution.distance += curMinIncrement

            self.solution.notServed.remove(cus)
            self.solution.served.append(cus)


# if __name__ == "__main__":