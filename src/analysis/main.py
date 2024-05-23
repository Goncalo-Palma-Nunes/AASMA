from analyse_data import Analyse_Data

if __name__ == "__main__":
    analyse = Analyse_Data()
    # Comment the line below if the set up is different between the runs
    analyse.setDataTotal("total_rewards")
    analyse.setDataRound("round_rewards")
    analyse.plotBarData()
    analyse.drawLinePlot()  