from analyse_data import Analyse_Data

if __name__ == "__main__":
    analyse = Analyse_Data()
    # Comment the 2 lines below if the set up is different between the runs
    #analyse.setDataTotal("total_rewards")
    #analyse.plotBarData()
    analyse.setDataRound("cumulative_endowment")
    analyse.drawLinePlot("cumulative_endowment")
    stats_type = ['average_endowment_per_round', 'max_endowment_per_round', 'median_endowment_per_round', 'min_endowment_per_round', 'variance_endowment_per_round', 'standard_deviation_endowment_per_round']
    for stat in stats_type:
        analyse.setDataRound(stat)
        analyse.drawLinePlot(stat)