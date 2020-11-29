import pandas as pd

dane = pd.read_excel('analiza.xlsx', columns=['a', 'b', 'c'])


MAX = 460 # zakladana kwota kampanii

print(dane)

konwersje = dane.a
