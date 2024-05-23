import matplotlib.pyplot as plt

class Graph_Stats:
    def __init__(self, stats):
        self.stats = stats
        
    def getStats(self):
        return self.stats
    
    def draw_lines_graph(self, stats_type):
        plt.clf()
        stats_list = self.getStats().getStatsType(stats_type)
        agent_types = list(stats_list[0].keys())
        
        for i in range(len(agent_types)):
            x = list(range(1, self.stats.getStatsRound() + 2))
            y = [stats_list[j][agent_types[i]] for j in range(self.stats.getStatsRound() + 1)]
            plt.plot(x, y, label = f"Agent {agent_types[i]}")
 
        # naming the x axis
        plt.xlabel('Rounds')
        # naming the y axis
        plt.ylabel(f"{stats_type}")
        # giving a title to my graph
        plt.title(f"Graph of {stats_type} in {self.stats.getStatsRound() + 1} Rounds")
 
        # show a legend on the plot
        plt.legend()
        
         # Set x-axis ticks to integer values
        plt.xticks(range(1, self.stats.getStatsRound() + 2))
 
        # function to save the plot
        plt.savefig(f'graphs/{stats_type}.png')
        plt.close()