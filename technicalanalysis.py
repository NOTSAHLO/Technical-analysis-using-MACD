import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class TechnicalAnalysis:

    def __init__(self, data_file):
        self.data = self.load_data(data_file)
        self.macd = np.zeros(1200)
        self.signal = np.zeros(1000)
        self.figure, (self.macd_signal_plot, self.data_plot) = plt.subplots(2)
        self.x = range(1, 1001)

    def load_data(self, data_file):
        df = pd.read_csv(data_file, usecols=['Ostatnio'], decimal=',')
        df['Ostatnio'] = df['Ostatnio'].replace('[^0-9\.]+', '', regex=True).astype(float)
        return list(df.iloc)

    def eman(self, data, index, N):
        # Nominator
        alpha = 2/(N + 1)
        nominator = 0
        for i in range(0, N):
            nominator = nominator + data[index+i] * (1 - alpha)**i
        # Denominator
        denominator = 0
        for i in range(0, N):
            denominator = denominator + (1 - alpha)**i
        ema = nominator/denominator
        return ema

    def count_macd(self):
        for i in range(0, 1200):
            self.macd[i] = self.eman(self.data, i, 12) - self.eman(self.data, i, 26)

    def count_signal(self):
        for i in range(0, 1000):
            self.signal[i] = self.eman(self.macd, i, 9)

    def prepare_data_for_plot(self):
        self.data = self.data[:1000]
        self.data.reverse()
        self.macd = list(self.macd)
        self.macd = self.macd[:1000]
        self.macd.reverse()
        self.signal = list(self.signal)
        self.signal.reverse()

    def plot_data(self):
        self.macd_signal_plot.plot(self.x, self.macd, label='MACD')
        self.macd_signal_plot.plot(self.x, self.signal, label='SIGNAL')
        self.data_plot.plot(self.x, self.data, label='Action Price')
        self.macd_signal_plot.set_xlabel('Day')
        self.macd_signal_plot.set_ylabel('MACD / SIGNAL Value')
        self.macd_signal_plot.set_title('MACD / SIGNAL Chart from last 1000 days')
        self.macd_signal_plot.legend()
        self.data_plot.set_xlabel('Day')
        self.data_plot.set_ylabel('Action Price [zł]')
        self.data_plot.set_title('Action Price Chart from last 1000 days')
        self.data_plot.legend()
        manager = plt.get_current_fig_manager()
        manager.set_window_title('Wykresy MACD/SIGNAL oraz Danych wejściowych')
        self.figure.set_size_inches(14, 10)
        plt.show()

    def run(self):
        self.count_macd()
        self.count_signal()

    def print_plot(self):
        self.prepare_data_for_plot()
        self.plot_data()

    def buy_sell_algorithm(self, funds):
        money = funds
        actions = 0
        for i in range(0, 1000):
            # first day has no comparison to the previous day, so we neither buy nor sell
            if i > 0:
                # CROSSING FROM THE BOTTOM
                if (self.macd[i] > self.signal[i]) and (self.macd[i - 1] < self.signal[i - 1]):
                    # buying if we have money
                    if money != 0:
                        actions = money / float(self.data[i])
                        money = 0
                        #print("Bought on day ", i, " for ", float(self.data[i]))
                # CROSSING FROM THE TOP
                elif (self.macd[i] < self.signal[i]) and (self.macd[i - 1] > self.signal[i - 1]):
                    # selling if we have something to sell
                    if actions != 0:
                        money = actions * float(self.data[i])
                        actions = 0
                        #print("Sold on day ", i, " for ", float(self.data[i]))
        if money == 0:
            money = actions*self.data[999]
        print("Money after investing: ", float(money))
