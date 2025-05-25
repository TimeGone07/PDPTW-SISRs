from node import Node
import numpy as np
import pandas as pd

class Instance:
    """_summary_
    class that represent an instance, such as C101
    """
    def __init__(self, name, capacity, depot, customers,distMatrix):
        """_summary_

        Args:
            name (str): name of instance
            numVehicle (int): number of vehicles
            capacity (int): capacity of vehicles
            depot (Node): depot info of instance
            customers (list of Node): customers info of instance
        """
        self.name = name
        self.numVehicle = int(len(customers)/2)
        self.capacity = capacity
        self.depot = depot
        self.customers = customers 
        self.distMatrix = distMatrix  # distance matrix
        # save all nodes 
        self.allNodes = [depot] + customers
        self.numNodes = len(self.allNodes)
        self.withBKS = False # Indicate no Best Known Solution found ... 
        # compute distance matrix
        self.adjDistMatrix = np.argsort(self.distMatrix, axis=1).tolist() # matrix for string removal

    def updateBKS(self, category, instID):
        """Update Best Known Solutions (if any...)

        Args:
            category (_str_): the category of dataset, like "Solomon" or "Gehring&Homberge"
            instID (_str_): the instance ID of dataset, like "c101" or "C2_2_4"
        """
        filePath = "./SOTA/" + category + ".xlsx"
        try:
            df = pd.read_excel(filePath)
            best_solution = df[df["Instance"] == instID]
            if not best_solution.empty:
                self.withBKS = True
                self.BKSTrucks = int(best_solution.iloc[0]["Vehicles"])
                self.BKSDistance = round(float(best_solution.iloc[0]["Distance"]), 2)
                print(self.BKSTrucks, self.BKSDistance)
        except Exception:
            print(f"Fatal: Fail to load Best Known Solution! {category}, {instID} is not found!")
    
    def readInstance(fileName):
        with open(fileName, 'r') as f:
            lines = f.readlines()
        #numVehicle = 0
        capacity = 0 
        depot = None 
        customers = []
        distMatrix = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("NAME"):
                # read vehicle data
                i += 9  # jump the headlines
                capacity = int(lines[i].split( )[1])
                i += 1
            elif line.startswith("NODES"):
                # read customers data
                i += 1  # jump the headlines
                while i < len(lines) and lines[i].strip():
                    if lines[i].startswith("EDGES"):
                        break
                    data = list(map(float, lines[i].split()))
                    if depot == None:
                        depot = Node(
                            id =int(data[0]),
                            x = data[1],
                            y = data[2],
                            demand = int(data[3]),
                            readyTime = int(data[4]),
                            dueTime = int(data[5]),
                            serviceTime = int(data[6]),
                            pickuppair= int(data[7]),
                            deliverypair= int(data[8])
                        )
                    else:
                        customers.append(Node(
                            id=int(data[0]),
                            x=data[1],
                            y=data[2],
                            demand=int(data[3]),
                            readyTime=int(data[4]),
                            dueTime=int(data[5]),
                            serviceTime=int(data[6]),
                            pickuppair=int(data[7]),
                            deliverypair=int(data[8])
                        ))
                    i += 1
            elif line.startswith("EDGES"):
                i+=1
                while i < len(lines) and lines[i].strip():
                    if lines[i].startswith("EOF"):
                        break
                    distMatrix.append(list(map(int, lines[i].split())))
                    i+=1
            else:
                i += 1

        print(f"Complete Read Instance : {fileName}")
        return Instance(fileName, capacity, depot, customers, distMatrix)

    def getpairnode(self,cus):
        if cus.pickuppair == 0:
            #print(cus.id,cus.deliverypair)
            #print(self.customers[cus.deliverypair-1])
            return self.customers[cus.deliverypair-1]
        elif cus.deliverypair == 0:
            #print(cus.id, cus.pickuppair)
            #print(self.customers[cus.pickuppair-1])
            return self.customers[cus.pickuppair-1]
        else:
            print("Fatal: Fail to get pair node!")
    
if __name__ == "__main__":
    # only for test ... 
    folder = "./Instances/n100/"
    inst = "bar-n100-1.txt"
    category = "n100"
    fileName = folder + inst
    curInstance = Instance.readInstance(fileName)
    curInstance.updateBKS(category, inst.split(".")[0] ) # Update Best Known Solution ... 