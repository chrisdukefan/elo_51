import pandas
import numpy as np
import datetime
import matplotlib.pyplot as plt
elo_spd = []
pt_spd = []
avg = []
def spread_elo(hp1,hp2,hp3,hp4,csvs): # define a new function that takes in hyperparameter values and returns the percent of games correctly predicted
    for csv in csvs:
        data = pandas.read_csv(csv)
        elo_spd = []
        pt_spd = []
        ID = {}
        outcomes = []
        for idx, row in data.iterrows():
            if data.loc[idx,'PTS']>data.loc[idx,'PTS.1']:
            winner = data.loc[idx,'Visitor/Neutral']; loser = data.loc[idx,'Home/Neutral'];
        pd = data.loc[idx,'PTS'] - data.loc[idx,'PTS.1']; hm_i = 0
        else:
            winner = data.loc[idx,'Home/Neutral']; loser = data.loc[idx,'Visitor/Neutral'];
        pd = data.loc[idx,'PTS.1'] - data.loc[idx,'PTS'];hm_i = 1
        game_date = datetime.datetime.strptime(data.loc[idx]["Date"],"%a, %b %d, %Y")
        if winner in ID.keys():
            w_elo = ID[winner][0]
        if (ID[winner][1] - game_date).days == 1: w_date = 1 
        else: w_date = 0
        w_games = ID[winner][2]
        else: 
            w_elo = 1500
        w_date = 0
        w_games = 0
        if loser in ID.keys():
            l_elo = ID[loser][0]
        if (ID[loser][1] - game_date).days == 1: l_date = 1
        else: l_date = 0
        l_games = ID[loser][2]
        else: 
          l_elo = 1500
        l_date = 0
        l_games = 0
        if hm_i == 1: w_elo_g = w_elo+hp3 + hp4*w_date; l_elo_g = l_elo + hp4*l_date
        else: l_elo_g = l_elo +hp3 + hp4*l_date; w_elo_g = w_elo + hp4*l_date;
        dif = w_elo_g - l_elo_g
        if dif>0: pt_spd.append(pd); elo_spd.append(dif)
        else: pt_spd.append(-pd);elo_spd.append(-dif)
        avg.append(dif/pd)
        if w_elo_g>l_elo_g: outcomes.append(1)
        if l_elo_g>w_elo_g: outcomes.append(0)
        w_new_elo = (w_elo+np.log(pd+1)*(2.2/((w_elo-l_elo)*.001+2.2))*hp1*(1-(1/(1+10**((l_elo_g-w_elo_g)/400)))))
        l_new_elo = (l_elo+np.log(pd+1)*(2.2/((w_elo-l_elo)*.001+2.2))*hp1*(0-(1/(1+10**((w_elo_g-l_elo_g)/400)))))
        ID[winner]=(w_new_elo,game_date,w_games + 1);
        ID[loser]=(l_new_elo,game_date,l_games + 1)
    return np.polyfit(elo_spd,pt_spd,1)
spread_elo(4,700,5,-.5,['games2015.csv'])# run the function on the 2015 data with the given hyperparameters


print (spread_elo(4,700,5,-.5,['games2015.csv']))

import pandas
import numpy as np
import datetime
import matplotlib.pyplot as plt

def vs_the_spread(hp1,hp2,hp3,hp4,csv, b, m): # define a new function that takes in hyperparameter values and returns the percent of games correctly predicted
  elo_spd = []
pt_spd = []
right = []
wrong = []
data = pandas.read_csv(csv)
ID = {}
outcomes = []
for idx, row in data.iterrows():
  if data.loc[idx,'PTS']>data.loc[idx,'PTS.1']:
  winner = data.loc[idx,'Visitor/Neutral']; loser = data.loc[idx,'Home/Neutral'];
pd = data.loc[idx,'PTS'] - data.loc[idx,'PTS.1']; hm_i = 0
else:
  winner = data.loc[idx,'Home/Neutral']; loser = data.loc[idx,'Visitor/Neutral'];
pd = data.loc[idx,'PTS.1'] - data.loc[idx,'PTS'];hm_i = 1
game_date = datetime.datetime.strptime(data.loc[idx]["Date"],"%a, %b %d, %Y")
if winner in ID.keys():
  w_elo = ID[winner][0]
if (ID[winner][1] - game_date).days == 1: w_date = 1 
else: w_date = 0
w_games = ID[winner][2]
else: 
  w_elo = 1500
w_date = 0
w_games = 0
if loser in ID.keys():
  l_elo = ID[loser][0]
if (ID[loser][1] - game_date).days == 1: l_date = 1
else: l_date = 0
l_games = ID[loser][2]
else: 
  l_elo = 1500
l_date = 0
l_games = 0
if hm_i == 1: w_elo_g = w_elo+hp3 + hp4*w_date; l_elo_g = l_elo + hp4*l_date; pred = (w_elo_g-l_elo_g)*b+m
else: l_elo_g = l_elo +hp3 + hp4*l_date; w_elo_g = w_elo + hp4*l_date; pred = (l_elo_g-w_elo_g)*b+m
dif = w_elo_g - l_elo_g
if (pred - data.loc[idx,'lineavg'])*(pd - data.loc[idx,'lineavg']) > 0: right.append(1)
else: wrong.append(1)
if dif>0: pt_spd.append(pd); elo_spd.append(dif)
else: pt_spd.append(-pd);elo_spd.append(-dif)
if w_elo_g>l_elo_g: outcomes.append(1)
if l_elo_g>w_elo_g: outcomes.append(0)
w_new_elo = (w_elo+np.log(pd+1)*(2.2/((w_elo-l_elo)*.001+2.2))*hp1*(1-(1/(1+10**((l_elo_g-w_elo_g)/400)))))
l_new_elo = (l_elo+np.log(pd+1)*(2.2/((w_elo-l_elo)*.001+2.2))*hp1*(0-(1/(1+10**((w_elo_g-l_elo_g)/400)))))
ID[winner]=(w_new_elo,game_date,w_games + 1);
ID[loser]=(l_new_elo,game_date,l_games + 1)
return (len(right),len(wrong))
train = spread_elo(4,700,5,-.5,['games2003.csv','games2004.csv','games2005.csv','games2006.csv','games2007.csv','games2008.csv','games2009.csv','games2010.csv','games2011.csv','games2012.csv','games2013.csv','games2014.csv'])
b = train[0]
m = train[1]
print(vs_the_spread(4,700,5,-.5,'games2009.csv',b,m))# run the function on the 2015 data with the given hyperparameters

