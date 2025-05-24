from instance import Instance
from solution import Solution
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

class Visualizer:
    
    def __init__(self, instance, solution):
        self.instance = instance
        self.solution = solution
        
    def show(self):
        for idx, node in enumerate(self.instance.allNodes):
            if idx == 0:
                plt.scatter(node.x, node.y, c='red', label='Depot', marker='s', s=50)  # depot用方形
            else:
                plt.scatter(node.x, node.y, c='black', label='Depot', marker='o', s=50)  # depot用方形
        
        colors = [hsv_to_rgb([i / len(self.solution.routes), 1, 1]) for i in range(len(self.solution.routes))]
        
        for ri, route in enumerate(self.solution.routes):
            curNodes = route.nodes
            for idx in range(1, len(curNodes)):
                plt.plot([curNodes[idx - 1].x, curNodes[idx].x], [curNodes[idx - 1].y, curNodes[idx].y], color=colors[ri], linewidth=2, label=f'Route {idx + 1}')
        plt.title(f'Visualizaton of {self.instance.name}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.axis('equal')  # 坐标轴等比例显示
        plt.show()