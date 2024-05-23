import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

class Graph_Stats:
    def __init__(self, stats):
        self.stats = stats
        
    def getStats(self):
        return self.stats
    
    def draw_line_plot(self, stats_type):
        plt.clf()
        stats_list = self.getStats().getStatsType(stats_type)
        agent_types = list(stats_list[0].keys())
        
        for i in range(len(agent_types)):
            x = list(range(1, self.stats.getStatsRound() + 2))
            y = [stats_list[j][agent_types[i]] for j in range(self.stats.getStatsRound() + 1)]
            plt.plot(x, y, label = f"Agent {agent_types[i]}")
 
        plt.xlabel('Rounds')
        plt.ylabel(f"{stats_type}")
        plt.title(f"Graph of {stats_type} in {self.stats.getStatsRound() + 1} Rounds")
        plt.legend()
        
         # Set x-axis ticks to integer values
        plt.xticks(range(1, self.stats.getStatsRound() + 2))
 
        plt.savefig(f'graphs/{stats_type}_line_plot.png')
        plt.close()
        
    def draw_bar_plot(self, stats_type):
        stats_list = self.getStats().getStatsType(stats_type)
        agent_types = list(stats_list[0].keys())
        left = []
        height = []
        tick_label = []
        
        bar_width = 0.2
        offset = np.linspace(-bar_width * len(agent_types) / 2, bar_width * len(agent_types) / 2, len(agent_types))
        for i in range(len(agent_types)):
            left.extend(range(1, self.stats.getStatsRound() + 2) + offset[i])
            height.extend([stats_list[j][agent_types[i]] for j in range(self.stats.getStatsRound() + 1)])
            tick_label.extend([f"r{round_number}" for round_number in range(1, self.stats.getStatsRound() + 2)])
            
        # Generate a list of colors using a colormap
        colors = plt.cm.viridis(np.linspace(0, 1, len(agent_types)))
        bar_colors = np.repeat(colors, self.stats.getStatsRound() + 1, axis=0)

        plt.bar(left, height, tick_label=tick_label, width=bar_width, color=bar_colors)

        legend_handles = [mpatches.Patch(color=colors[i], label=agent_types[i]) for i in range(len(agent_types))]
        plt.legend(handles=legend_handles, title="Agent Types")
        
        plt.ylabel(f"{stats_type}")
        plt.xlabel(f"Rounds")
        plt.title(f"Graph of {stats_type} in {self.stats.getStatsRound() + 1} Rounds")
        
        plt.savefig(f'graphs/{stats_type}_bar_plot.png')
        plt.close()