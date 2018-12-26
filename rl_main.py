from feed.bt_data import BTCSVBasicData
from rl.agent.base import *
from rl.agent.dqn_agent import DQNAgent
from rl.env.cerebro_ext import RLExtCerebro

episode = 5
data_path = "./test_data/stock/000002.csv"

network_config_path = "./config/stock_mlp_baseline.cls"


if __name__ == "__main__":
    agent = DQNAgent(network_config_path)

    for i in range(episode):
        print("#####################EPISODE " + str(i) + "###########################")

        cerebro = RLExtCerebro()

        # Add a agent
        cerebro.addagent(agent)

        # Add a strategy
        cerebro.addstrategy(RLCommonStrategy)

        print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())

        # Create a Data Feed
        data = BTCSVBasicData(
            dataname=data_path,
            reverse=False)

        # Add the Data Feed to Cerebro
        cerebro.adddata(data)

        # Add a FixedSize sizer according to the stake
        cerebro.addsizer(bt.sizers.FixedSize, stake=100)

        # Set the commission - 0.1% ... divide by 100 to remove the %
        cerebro.broker.setcommission(commission=0.001)

        # Set our desired cash start
        cerebro.broker.setcash(100000.0)

        cerebro.run()

        print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

        # cerebro.plot()
