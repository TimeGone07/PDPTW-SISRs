import random

from route import Route
import operator
class Solution:
    
    def __init__(self, instance, routes, served, notServed):
        self.instance = instance
        self.routes = routes
        self.served = served
        self.notServed = notServed
        self.distance = self.computeDistance()
    
    def computeDistance(self):
        distance = 0
        for route in self.routes:
            distance += route.distance
        return distance
    
    def executeForwardSlack(self):
        self.served = []
        self.notServed = []
        for i in range(len(self.routes)):
            self.routes[i].forgePushForward()
            self.served += self.routes[i].nodes[1: -1]
    
    def executeNaive(self):
        """Naive initial solution construction, forge a route for each customer. 100 customer, 50 routes.
        """
        while True:
            customer = random.choice(self.notServed)
            cuspair = self.instance.getpairnode(customer)
            if customer.pickuppair==0:
                nodeList = [self.instance.depot, customer, cuspair, self.instance.depot]
            else:
                nodeList = [self.instance.depot, cuspair, customer, self.instance.depot]
            newRoute = Route(self.instance, nodeList, set(nodeList))
            self.served.append(customer)
            self.served.append(cuspair)
            self.notServed.remove(customer)
            self.notServed.remove(cuspair)
            self.routes.append(newRoute)
            self.distance += newRoute.distance
            if not self.notServed:
                break

    def executeTimeNN(self):
        """Time-oriented NN in Solomon 1987, inital solution construction
        """
        sigma_1, sigma_2, sigma_3 = 1/3, 1/3, 1/3
        # determine the weight
        lastCusIdx = -1
        customers = self.instance.allNodes
        while len(self.notServed) > 0:
            # print(len(self.routes))
            if lastCusIdx == -1:
                # if have no route ... 
                # need to compare with the depot, choose the 'closest' one
                
                closeDist = []
                for nextCus in self.notServed:
                    closeDist.append(sigma_1 * self.instance.distMatrix[0][nextCus.id] + 
                                    sigma_2 * customers[nextCus.id].readyTime + 
                                    sigma_3 * (customers[nextCus.id].dueTime - self.instance.distMatrix[0][nextCus.id]))
                
                # find the minimum index of closeDist
                min_index, min_value = min(enumerate(closeDist), key = operator.itemgetter(1))
                choseCus = self.notServed[min_index]
                nodeList = [self.instance.depot, choseCus, self.instance.depot]
                newRoute = Route(self.instance, nodeList, set(nodeList))
                self.served.append(choseCus)
                self.notServed.pop(min_index)
                self.routes.append(newRoute)
                lastCusIdx = choseCus.id

                # update served customers / not-served customers
                # update routes of current solution
                # update last visited customer
            else:
                # have existing customers, which means existing routes
                # check every route and find the closest customer
                lastRoute = self.routes[-1]
                lastCustomer = lastRoute.nodes[-2]
                # store the close distance and target route ... 
                nxtCus = None; nxtRate = float('inf'); nxtCusIdx = -1
                for nextIdx, nextCus in enumerate(self.notServed):
                    # check feasibility
                    if lastRoute.serviceStartTime[-2] + lastCustomer.serviceTime + self.instance.distMatrix[lastCustomer.id][nextCus.id] > nextCus.dueTime:
                        continue
                    if lastRoute.load + nextCus.demand > self.instance.capacity:
                        continue
                    curRate = sigma_1 * self.instance.distMatrix[lastCustomer.id][nextCus.id] + \
                            sigma_2 * (customers[nextCus.id].readyTime - (customers[lastCustomer.id].readyTime + customers[lastCustomer.id].serviceTime)) + \
                            sigma_3 * (customers[nextCus.id].dueTime - (customers[lastCustomer.id].readyTime + customers[lastCustomer.id].serviceTime + self.instance.distMatrix[lastCustomer.id][nextCus.id]))
                    if curRate < nxtRate:
                        nxtCus = nextCus
                        nxtRate = curRate
                        nxtCusIdx = nextIdx
                if nxtCus != None:
                    # find feasible customer! Just Insert it!
                    lastCusIdx = nxtCus.id
                    self.routes[-1].nodes.insert(-1, nxtCus)
                    self.routes[-1].nodesSet.add(nxtCus)
                    self.routes[-1].load += nxtCus.demand
                    self.routes[-1].serviceStartTime.insert(-1, max(nxtCus.readyTime, self.instance.distMatrix[lastCustomer.id][nxtCus.id] + lastRoute.serviceStartTime[-2] + lastCustomer.serviceTime))
                    self.routes[-1].waitingTime.insert(-1, max(0, nxtCus.readyTime - (self.instance.distMatrix[lastCustomer.id][nxtCus.id] + lastRoute.serviceStartTime[-2] + lastCustomer.serviceTime)))
                    self.routes[-1].distance += (self.instance.distMatrix[lastCustomer.id][nxtCus.id] + self.instance.distMatrix[nxtCus.id][0] - self.instance.distMatrix[lastCustomer.id][0])
                    self.served.append(nxtCus)
                    self.notServed.pop(nxtCusIdx)
                    lastRoute = self.routes[-1]
                else:
                    lastCusIdx = -1
        
        for route in self.routes:
            route.calculateTime()
            route.forgePushForward()
            self.distance += route.distance
    
    def executeCWsaving(self, randomGen):
        
        randomGen.shuffle(self.notServed)
        for v_id in range(self.instance.numVehicle):
            # iter num of vehicles ... 
            routeList = [self.instance.depot]
            prevServiceStartTime = 0
            currLoad = 0
            while self.notServed:
                nextCustomer = None
                bestScore = float('inf')
                prevNode = routeList[-1]
                currArrivalTime = 0
                for customer in self.notServed:
                    arriveTime = prevServiceStartTime + prevNode.serviceTime + self.instance.distMatrix[prevNode.id][customer.id]
                    if arriveTime > customer.dueTime or currLoad + customer.demand > self.instance.capacity:
                        # break time window or weight constraint ... 
                        continue 
                    actualServiceStartTime = max(customer.readyTime, arriveTime)
                    if actualServiceStartTime + self.instance.distMatrix[customer.id][0] + customer.serviceTime > self.instance.depot.dueTime:
                        # IMPORTANT FIX: If all satistied but fail to reach depot before due time ... 
                        continue
                    currCustomerScore = self.instance.distMatrix[prevNode.id][customer.id] + max(0, customer.readyTime - arriveTime)
                    if currCustomerScore < bestScore:
                        bestScore = currCustomerScore
                        nextCustomer = customer
                        currArrivalTime = arriveTime
                if nextCustomer == None:
                    # no feasible customer ...
                    break
                routeList.append(nextCustomer)
                currLoad += nextCustomer.demand
                prevServiceStartTime = max(currArrivalTime, nextCustomer.readyTime)
                self.notServed.remove(nextCustomer)
                self.served.append(nextCustomer)
            routeList.append(self.instance.depot)
            if len(routeList) > 2:
                self.routes.append(Route(self.instance, routeList, set(routeList)))
                self.distance += self.routes[-1].distance

    def removeCustomer(self, customer):
        # remove customer from Solution ...
        for i in range(len(self.routes)):
            if customer in self.routes[i].nodesSet:
                #executed = True
                if len(self.routes[i].nodes) == 3:
                    self.routes.remove(self.routes[i])
                    self.distance -= (self.instance.distMatrix[customer.id][0] + self.instance.distMatrix[0][customer.id])
                    # delete the entire route ...
                    break
                # print(f"length of nodes before: {len(self.routes[i].nodes)}")
                self.routes[i].removeCustomer(customer)
                # self.routes[i].forgePushForward()
                break

        self.served.remove(customer)
        self.notServed.append(customer)

    def removeRouteString(self, routeIdx, rmvds):
        """Remove a string of customers from route with routeIdx via customerIdx

        Args:
            routeIdx (_type_): _description_
            rmvdIdxes (_type_): _description_
        """

        #rmvdLen = len(rmvds)
        #prevDist = self.routes[routeIdx].computeDistance()
        # print(f"routeIdx : {routeIdx}, rmvdIdxes: {rmvdIdxes}")

        # for node in self.routes[routeIdx].nodes:
        #     print(node)
        # print(f"Run Remove Route String, Original : {[node.id for node in self.routes[routeIdx].nodes]}")
        for cus in rmvds:
            self.routes[routeIdx].removeCustomer(cus)
            self.served.remove(cus)
            self.notServed.append(cus)
        #     print(f"Removed: {self.routes[routeIdx].nodes[index].id}", end = ",")
        # print("")
        
        #self.routes[routeIdx].removeCustomerByIndex(rmvds)
        #self.distance += (self.routes[routeIdx].distance - prevDist)

    def keepRouteString(self, routeIdx, keptIdxes):
        """Remove customers except those index in keptIdxes

        Args:
            routeIdx (_type_): _description_
            keptIdxes (_type_): _description_
        """
        setKept = set(keptIdxes)
        rmvdIdxes = [k for k in range(1, len(self.routes[routeIdx].nodes) - 1) if k not in setKept]
        prevDist = self.routes[routeIdx].computeDistance()
        # print(f"Run Keep Route String, Original : {[node.id for node in self.routes[routeIdx].nodes]}")
        for index in rmvdIdxes:
            self.served.remove(self.routes[routeIdx].nodes[index])
            self.notServed.append(self.routes[routeIdx].nodes[index])
        #     print(f"Removed: {self.routes[routeIdx].nodes[index].id}", end = ",")
        # print("")
        self.routes[routeIdx].removeCustomerByIndex(rmvdIdxes)
        self.distance += (self.routes[routeIdx].distance - prevDist)

    def removeRoute(self, routeIdx):
        """remove route from solution and update ... 

        Args:
            routeIdx (_type_): _description_
        """
        self.distance -= self.routes[routeIdx].distance
        for customer in self.routes[routeIdx].nodesSet:
            if customer.id != 0:
                self.served.remove(customer)
                self.notServed.append(customer)
                # remove from set 
        self.routes.pop(routeIdx)
    
    def __str__(self):
        # num_route = len(self.routes)
        cnt_customers = 0
        cost = 0
        visited = [0 for _ in range(self.instance.numNodes)]
        phase1 = f"Truck used: {len(self.routes)}\n"
        for idx, route in enumerate(self.routes):
            phase1 += f"Truck {idx}\n"
            cnt_customers += (len(self.routes[idx].nodes) - 2)
            nodes = route.nodes
            cost += route.distance
            for j, node in enumerate(nodes):
                phase1 += (str(node) + "waitingTime: " + str(route.waitingTime[j]) + "; serviceStartTime: " + str(route.serviceStartTime[j]) + "; forwardTimeSlack:" + str(route.forwardTimeSlack[j]) + "\n")
                if node.id != 0:
                    visited[node.id] += 1
        
        phase1 += f"Cost: {cost}, Customers {cnt_customers}, check {self.distance}\n"
        for i in range(1, self.instance.numNodes):
            if visited[i] > 1:
                phase1 += f"Customer {i} visited {visited[i]} times\n"
            elif visited[i] < 1:
                phase1 += f"Customer {i} is not visited.\n"
                
        return (phase1)

    def checkFeasibility(self):
        """check feasibility of the solution
        """
        visited = [0 for _ in range(self.instance.numNodes)]
        isFeas = True
        for idx, route in enumerate(self.routes):
            if route.nodes[0].id != 0 or route.nodes[-1].id != 0:
                print(f"FATAL: route {idx} start/end != depot!")
                isFeas = False
                break
            curLoad = 0
            for j, node in enumerate(route.nodes):
                if node.id != 0:
                    visited[node.id] += 1
                curLoad += node.demand
                if curLoad > self.instance.capacity:
                    print(f"FATAL: route {idx} exceed capacity!")
                    isFeas = False
        for i in range(1, len(visited)):
            if visited[i] > 1:
                print(f"Cus {i} is visited multiple times!")
                isFeas = False
            elif visited[i] < 1:
                print(f"Cus {i} is not visited!")
                isFeas = False

        if isFeas:
            print("Success!! Pass Feasibility Check!")
        else:
            print("Fail!! Check reasons above!")
        return isFeas
    
    def copy(self):
        """
        Method that creates a copy of the solution and returns it
        """
        # need a deep copy of routes because routes are modifiable
        routesCopy = list()
        for route in self.routes:
            routesCopy.append(route.copy())
        newCopy = Solution(self.instance, routesCopy, self.served.copy(), self.notServed.copy())
        newCopy.computeDistance()
        return newCopy

