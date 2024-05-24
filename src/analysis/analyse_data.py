import os
import ast
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

class Analyse_Data():
    def __init__(self):
        self.data_total = []
        self.data_round = []
        self.num_simulations = 0
        self.num_rounds = 0
        
    def getDataTotal(self):
        return self.data_total
    
    def getDataRound(self):
        return self.data_round
    
    def getNumSimulations(self):
        return self.num_simulations
    
    def getNumRounds(self):
        return self.num_rounds

    # Receive data with the same agent types in every simulation
    def receiveData(self, data, fname):
        # File exists
        if os.path.exists(f'src/analysis/txts/{fname}.txt'):
            with open(f'src/analysis/txts/{fname}.txt', 'a') as file:
                file.write(str(data) + '\n') # add new line of total rewards
        else: # New file   
            with open(f'src/analysis/txts/{fname}.txt', 'w') as file:
                file.write(str(data) + '\n') # total_rewards
    
    def setDataTotal(self, fname):
        total_rewards = []
        with open(f'src/analysis/txts/{fname}.txt', 'r') as infile:
            for line in infile:
                total_rewards.append(ast.literal_eval(line.strip()))
                self.num_simulations += 1
        self.data_total = total_rewards
    
    def setDataRound(self, fname):
        round_rewards = []
        with open(f'src/analysis/txts/{fname}.txt', 'r') as infile:
            for line in infile:
                round_rewards.append(ast.literal_eval(line.strip()))
                #self.num_simulations += 1
        self.num_rounds = len(round_rewards[0])
        self.data_round = round_rewards
        
    def getAverageByBehavior(self):
        rewards = self.getDataTotal()
        num_simulations = self.getNumSimulations()
        average_rewards = {}
        # average it by num of simulations
        for key in rewards[0].keys():
            average_rewards[key] = sum([rewards[j][key] for j in range(self.getNumSimulations())]) / num_simulations
        return average_rewards # return rewards
    
    def getVarianceByBehavior(self):
        rewards = self.getDataTotal()
        num_simulations = self.getNumSimulations()
        variance_rewards = {}
        for key in rewards[0].keys():
            mean = sum([rewards[j][key] for j in range(num_simulations)]) / num_simulations
            variance_rewards[key] = sum([(rewards[j][key] - mean) ** 2 for j in range(num_simulations)]) / num_simulations
        return variance_rewards
    
    def getStandardDeviationByBehavior(self):
        rewards = self.getDataTotal()
        num_simulations = self.getNumSimulations()
        standard_deviation_rewards = {}
        for key in rewards[0].keys():
            mean = sum([rewards[j][key] for j in range(num_simulations)]) / num_simulations
            standard_deviation_rewards[key] = (sum([(rewards[j][key] - mean) ** 2 for j in range(num_simulations)]) / num_simulations) ** 0.5
        return standard_deviation_rewards
    
    def plotBarData(self):
        for stats_type in ['average_endowment', 'variance_endowment', 'standard_deviation_endowment']:
            if stats_type == 'average_endowment':
                rewards = self.getAverageByBehavior()
            elif stats_type == 'variance_endowment':
                rewards = self.getVarianceByBehavior()
            elif stats_type == 'standard_deviation_endowment':
                rewards = self.getStandardDeviationByBehavior()
            self.drawBarPlot(rewards, stats_type)
        
    def drawBarPlot(self, rewards, stats_type):
        agent_types = list(rewards.keys())
        
        left = list(range(1, len(agent_types) + 1))
        height = [rewards[agent_types[i]] for i in range(len(agent_types))]
        tick_label = agent_types
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(agent_types)))
        
        plt.bar(left, height, tick_label=tick_label, width=0.8, color=colors)

        legend_handles = [mpatches.Patch(color=colors[i], label=agent_types[i]) for i in range(len(agent_types))]
        plt.legend(handles=legend_handles, title="Agent Types")
        
        plt.xlabel(f"Agents")
        plt.ylabel(f"{stats_type}")
        plt.title(f"{stats_type} by each agent type after {self.getNumSimulations()} Simulations")
        
        plt.savefig(f'src/analysis/bar_plots/{stats_type}_with_{self.getNumSimulations()}_sims_bar_plot.png')
        plt.close()
        
    def drawLinePlot(self):        
        for i in range(self.getNumSimulations()):
            x = list(range(1, self.getNumRounds() + 1))
            y = [self.getDataRound()[i][j] for j in range(self.getNumRounds())]
            plt.plot(x, y, label = f"Simulation {i+1}")
 
        plt.xlabel('Rounds')
        plt.ylabel(f"Total reward")
        plt.title(f"Total reward per round ({self.getNumRounds()} rounds)")
        plt.legend()
        
         # Set x-axis ticks to integer values
        plt.xticks(range(1, self.getNumRounds() + 1))
 
        plt.savefig(f'src/analysis/line_plots/{self.getNumSimulations()}_simulations_during_{self.getNumRounds()}_rounds_line_plot.png')
        plt.close()


class Individual_Plot():
    def __init__(self, game, stats):
        self.stats = stats
        self.game = game
        
    def getStats(self):
        return self.stats
    
    def getGame(self):
        return self.game
    
    def callStatsTypePlots(self, stats_type):
        self.drawLinePlot(stats_type)
        self.drawBarPlot(stats_type)
        
    def callBarTypePlots(self):
        self.drawTotalBarPlot(self.getGame().getTotalRewardByBehavior(), "total_rewards")
        if self.getGame().getNumBannedAgentsByBehavior() is not None:
            self.drawTotalBarPlot(self.getGame().getNumBannedAgentsByBehavior(), "num_banned_agents")
    
    def drawLinePlot(self, stats_type):
        stats_list = self.getStats().getStatsType(stats_type)
        agent_types = list(stats_list[0].keys())
        
        for i in range(len(agent_types)):
            x = list(range(1, self.stats.getStatsRound() + 2))
            y = [stats_list[j][agent_types[i]] for j in range(self.stats.getStatsRound() + 1)]
            plt.plot(x, y, label = f"Agent {agent_types[i]}")
 
        plt.xlabel('Rounds')
        plt.ylabel(f"{stats_type}")
        plt.title(f"{stats_type} in {self.stats.getStatsRound() + 1} Rounds")
        plt.legend()
        
         # Set x-axis ticks to integer values
        plt.xticks(range(1, self.stats.getStatsRound() + 2))
 
        plt.savefig(f'src/analysis/individual_game_plots/{stats_type}_line_plot.png')
        plt.close()
        
    def drawBarPlot(self, stats_type):
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
        plt.title(f"{stats_type} in {self.stats.getStatsRound() + 1} Rounds")
        
        plt.savefig(f'src/analysis/individual_game_plots/{stats_type}_bar_plot.png')
        plt.close()
    
    # Draw a bar plot of a stat of each agent type at the end of the game    
    def drawTotalBarPlot(self, rewards, plot_type):
        agent_types = list(rewards.keys())
        
        left = list(range(1, len(agent_types) + 1))
        height = [rewards[agent_types[i]] for i in range(len(agent_types))]
        tick_label = agent_types
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(agent_types)))
        
        plt.bar(left, height, tick_label=tick_label, width=0.8, color=colors)

        legend_handles = [mpatches.Patch(color=colors[i], label=agent_types[i]) for i in range(len(agent_types))]
        plt.legend(handles=legend_handles, title="Agent Types")
        
        plt.ylabel(f"{plot_type}")
        plt.xlabel(f"Agents")
        plt.title(f"{plot_type} by each agent type after {self.stats.getStatsRound() + 1} Rounds")
        
        plt.savefig(f'src/analysis/individual_game_plots/{plot_type}_bar_plot.png')
        plt.close()