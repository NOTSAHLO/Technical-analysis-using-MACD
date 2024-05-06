import technicalanalysis as ta

if __name__ == "__main__":
    analysis = ta.TechnicalAnalysis('Historyczne ceny CDR.csv')
    analysis.run()
    analysis.buy_sell_algorithm(1000)
    #analysis.print_plot()