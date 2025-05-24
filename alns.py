import random, time
from instance import Instance
from solution import Solution
from destroy import Destroy
from repair import Repair
from parameters import Parameters
import copy
import math

class ALNS:
    """
    Class that models the ALNS algorithm. 

    Parameters
    ----------
    instance : Instance
        The problem instance that we want to solve.
    
    """

    def __init__(self, instance):
        
        self.instance = instance
        self.randomGen = random.Random(Parameters.randomSeed) # for reproducibility
        self.avgCusRmved = Parameters.avgCusRmved
        self.maxStringLen = Parameters.maxStringLen
        self.temper=Parameters.initial_temper


    def execute(self):
        starttime = time.time()
        self.constructInitialSolution()
        endtime = time.time()
        cpuTime = round(endtime - starttime, 3)

        print(f"Terminated! CPU times {cpuTime} seconds, cost : {self.currentSolution.distance}")

        self.tempSolution = copy.deepcopy(self.currentSolution)
        self.bestSolution = copy.deepcopy(self.currentSolution)
        totalIter = Parameters.itertimes
        c = math.pow(Parameters.final_temper / Parameters.initial_temper, 1/totalIter)
        starttime = time.time()
        cnt_time = [0, 0, 0]
        cnt_usage = [0, 0, 0]
        for cnt in range(totalIter):
            removaln = self.randomGen.randint(1, int(0.1 * self.instance.numNodes - 1))
            chooseDestroy = self.randomGen.randint(1, 9)
            finalDestroy = -1
            if chooseDestroy <= 3:
                finalDestroy = 1
            elif chooseDestroy <= 6:
                finalDestroy = 2
            else:
                finalDestroy = 3
            #finalDestroy=3
            curDTime1 = time.time()
            repairSolution = self.destroyAndRepair(destroyOptNo=finalDestroy, repairOptNo=1, removaln=removaln)
            curDTime2 = time.time()
            cnt_time[finalDestroy - 1] += round(curDTime2 - curDTime1, 3)
            cnt_usage[finalDestroy - 1] += 1
            
            self.ifAccept(repairSolution, cnt, finalDestroy, 1)
            self.temper*=c
            #print(self.currentSolution.checkFeasibility())
            if cnt < totalIter * Parameters.fleetminratio:
                self.executeFleetMin(cnt)

        
        endtime = time.time()
        cpuTimeIteration = round(endtime - starttime, 3)
        self.currentSolution.checkFeasibility()
        
        print(f"Iteration Time: {cpuTimeIteration}")
        print(f"Destroy Running Time : {cnt_time}")
        print(f"Destroy Count Usage : {cnt_usage}")
        self.CPUTime = cpuTimeIteration
    
    def constructInitialSolution(self):
        """Construct the initial solution
        """
        self.currentSolution = Solution(self.instance, list(), list(), self.instance.customers.copy())
        # 1. based on Solomon's time-oriented Nearest Neighbur Heuristic
        # self.currentSolution.executeTimeNN()
        # 2. based on each route per pair of customer ...
        self.currentSolution.executeNaive()
        # 3. based on C-W saving Heuristic (seems very efficient!)
        # self.currentSolution.executeCWsaving(self.randomGen)


    def display(self, isbest = True):
        """Display the current Solution.

        Args:
            isbest (bool, optional): _description_. Defaults to True.
        """
        if isbest:
            print(self.bestSolution)
        else:
            print(self.currentSolution)
                
    
    def executeFleetMin(self, iterNum = 0):
        """Fleet Minimization Procedure: Remove entire route and 
        check if all customers it served can be inserted to other routes

        Args:
            iterNum (int, optional): Current Iteration Number. Defaults to 0.
        """
        # self.tempSolution = copy.deepcopy(self.currentSolution)
        self.tempSolution = self.currentSolution.copy()
        for route in self.tempSolution.routes:
            if len(route.nodes)==2:
                print('There is a route without customer')
        destroySolution = Destroy(self.instance, self.tempSolution)
        destroySolution.executeEntireRouteRemoval(self.randomGen)
        originalFleetSize = len(destroySolution.solution.routes)
        tempSolution2 = destroySolution.solution.copy() # This is very important!
        repairSolution = Repair(self.instance, tempSolution2)
        repairSolution.executeMultiGreedyInsertion(self.randomGen)
        if len(repairSolution.solution.routes) <= originalFleetSize:
            self.currentSolution = repairSolution.solution
            print(f"Found Shorter Route!!! Obj: {repairSolution.solution.distance}, IterNum : {iterNum} , trucks: {len(repairSolution.solution.routes)} complete! ")

    
    def destroyAndRepair(self, destroyOptNo, repairOptNo, removaln):
        """To conduct a full Destroy and Repair Procedure ... 

        Args:
            destroyOptNo (_type_): _description_
            repairOptNo (_type_): _description_
            removaln (_type_): _description_

        Returns:
            _type_: _description_
        """
        # depict the destroy and repair process ... 
        self.tempSolution = copy.deepcopy(self.currentSolution)
        destroySolution = Destroy(self.instance, self.tempSolution)
        if destroyOptNo == 1:
            destroySolution.executeRandomRemoval(removaln, self.randomGen)
        elif destroyOptNo == 2:
            destroySolution.executeStringRemoval(self.avgCusRmved, self.maxStringLen, self.randomGen)
        elif destroyOptNo == 3:
            destroySolution.executeSplitStringRemoval(self.avgCusRmved, self.maxStringLen, self.randomGen)
            # strangly, this seems not that ... efficient ... ?? 
        
        tempSolution2 = destroySolution.solution.copy() # This is very important! 
        repairSolution = Repair(self.instance, tempSolution2)
        
        if repairOptNo == 1:
            repairSolution.executeMultiGreedyInsertion(self.randomGen)

        return repairSolution
    
    
    def ifAccept(self, repairSolution, iterNum = 0, chooseDestroy = 0, chooseRepair = 0):
        """check if this repaired solution should be accepted

        Args:
            repairSolution (Class Repair): the repaired solution.
            iterNum (int, optional): iteration number. Defaults to 0.
        """
        if repairSolution.solution.distance < self.currentSolution.distance-self.temper*math.log(random.random())\
                or len(repairSolution.solution.routes) < len(self.currentSolution.routes):
            if len(repairSolution.solution.routes) > len(self.currentSolution.routes):
                return
            self.currentSolution = repairSolution.solution
        if self.bestSolution.distance - repairSolution.solution.distance > 0 or len(self.bestSolution.routes) > len(repairSolution.solution.routes):
            if len(repairSolution.solution.routes) > len(self.bestSolution.routes):
                return
            self.bestSolution = repairSolution.solution
            print(f"Found!! Obj: {repairSolution.solution.distance}, IterNum : {iterNum} , trucks: {len(repairSolution.solution.routes)}, DesOpt: {chooseDestroy}, RepOpt: {chooseRepair},", end = " ")
            
            if self.instance.withBKS:
                print(f"Gap to BKS : { round((repairSolution.solution.distance - self.instance.BKSDistance) * 100 / self.instance.BKSDistance, 2)}%, BKS Trucks {self.instance.BKSTrucks}")
            else:
                print("")
                

    def returnBrief(self):
        """Reture Brief to mian function 
        """
        if self.instance.withBKS:
            return [self.bestSolution.distance, len(self.bestSolution.routes), self.CPUTime, round((self.bestSolution.distance - self.instance.BKSDistance) * 100 / self.instance.BKSDistance, 3),  self.instance.BKSTrucks]
        else:
            return [self.bestSolution.distance, len(self.bestSolution.routes), self.CPUTime]

if __name__ == "__main__":
    import os
    from datetime import datetime

    def get_timestamped_filename(prefix="results", extension=".md"):
        """
        Generate a time-stampled filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 获取当前时间
        return f"{prefix}_{timestamp}{extension}"

    folder = "./benchmark/Solomon/"
    category = "Solomon"
    
    # os.makedirs("./Logger", exist_ok=True)
    # file_path = os.path.join("./Logger", get_timestamped_filename())
    # file_exists = os.path.exists(file_path)
    # for inst in instList[1:]:
    
    for inst in ['r205.txt']:
        fileName = folder + inst
        curInstance = Instance.readInstance(fileName)
        curInstance.updateBKS(category, inst.split(".")[0] ) # Update Best Known Solution ... 
        alns_solver = ALNS(curInstance)