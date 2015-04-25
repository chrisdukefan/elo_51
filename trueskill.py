import pandas
import numpy as np
import datetime
# initial parameters for trueskill: mean = 25, variance = (25/3)^2, beta^2 = (25/3)^2/4, tao^2 = (25/3)^2/10000
def score_trueskill(hp1,hp2,csv): # define a new function that takes in hyperparameter values and returns the percent of games correctly predicted
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
            w_tskillmean = ID[winner][0]
            w_tskillvar = ID[winner][1]
            if (ID[winner][2] - game_date).days == 1: w_date = 1 
            else: w_date = 0
            w_games = ID[winner][3]
        else: 
            w_tskillmean = 25
            w_tskillvar = (25/3)^2
            w_date = 0
            w_games = 0
        if loser in ID.keys():
            l_tskillmean = ID[loser][0]
            l_tskillvar = ID[loser][1]
            if (ID[loser][2] - game_date).days == 1: l_date = 1
            else: l_date = 0
            l_games = ID[loser][3]
        else: 
            l_tskillmean = 25
            l_tskillvar = (25/3)^2
            l_date = 0
            l_games = 0
        # if hm_i == 1: w_tskill = w_tskill+hp3 + hp4*w_date; l_elo = l_elo + hp4*l_date
        # else: l_elo = l_elo +hp3 + hp4*l_date; w_elo = w_elo + hp4*l_date;
        if w_tskillmean>l_tskillmean: outcomes.append(1)
        if l_tskillmean>w_tskillmean: outcomes.append(0)
        c = sqrt(2*hp1 + w_tskillvar + l_tskillvar)
        w_new_tskillmean = w_tskillmean + w_tskillvar/c # (w_elo+np.log(pd+1)*(2.2/((w_elo-l_elo)*.001+2.2))*hp1*(1-(1/(1+10**((l_elo-w_elo)/400)))))
        l_new_tskillmean = # (l_elo+np.log(pd+1)*(2.2/((w_elo-l_elo)*.001+2.2))*hp1*(0-(1/(1+10**((w_elo-l_elo)/400)))))
        ID[winner]=(w_new_tskillmean,w_new_tskillvar,game_date,w_games + 1);
        ID[loser]=(l_new_tskillmean,l_new_tskillvar,game_date,l_games + 1)
    print (sum(outcomes)/float(len(outcomes)))
    print(ID)
score_trueskill((25/3)^2/4,(25/3)^2/10000,'games2015.csv') # run the function on the 2015 data with the given hyperparameters