import pandas  # used for importing the .csv files
import operator
import numpy as np # used for natural logs
import datetime # used for dates
hp_test = {} # set up a dictionary to hold the results of our optimization
for hp1 in range(2,3): # range to iterate over for the first hyperparameter, the scale 'k'
    for hp2 in (400,100): # range for the spread hyperparameter
        for hp3 in (1,2): # range for the effect homecourt advantage
            for hp4 in (0,-1): # range for the effect of playing in a back to back
                data = pandas.read_csv('games2012.csv') # read in csv
                ID = {} # set up a dictionary that will be the place of storage for teams and their ratings
                outcomes = [] # set up an array that will contain whether we correctly predicted the game or not
                for idx, row in data.iterrows(): # for each game....
                    if data.loc[idx,'PTS']>data.loc[idx,'PTS.1']: # check who won the game, this is the case where the away team won
                        winner = data.loc[idx,'Visitor/Neutral']; loser = data.loc[idx,'Home/Neutral']; # get the names of the winner and loser
                        pd = data.loc[idx,'PTS'] - data.loc[idx,'PTS.1']; hm_i = 0 #get the point differential and signal whether home team won
                    else: # do the same in the case where the home team won
                        winner = data.loc[idx,'Home/Neutral']; loser = data.loc[idx,'Visitor/Neutral'];
                        pd = data.loc[idx,'PTS.1'] - data.loc[idx,'PTS'];hm_i = 1
                    game_date = datetime.datetime.strptime(data.loc[idx]["Date"],"%a, %b %d, %Y") # get the date of the game
                    if winner in ID.keys(): # if the team has already played a game
                        w_elo = ID[winner][0] # get their ranking
                        if (ID[winner][1] - game_date).days == 1: w_date = 1 # check whether they are playing in a back-to-back game
                        else: w_date = 0 
                        w_games = ID[winner][2] # see how many previous games they've played
                    else: # else initialize a new team
                        w_elo = 1500
                        w_date = 0
                        w_games = 0
                    if loser in ID.keys(): #do the same for the losing team
                        l_elo = ID[loser][0]
                        if (ID[loser][1] - game_date).days == 1: l_date = 1
                        else: l_date = 0
                        l_games = ID[loser][2]
                    else: 
                        l_elo = 1500
                        l_date = 0
                        l_games = 0
                    if hm_i == 1: w_elo = w_elo+hp3 + hp4*w_date; l_elo = l_elo + hp4*l_date # adjust the teams' elo rating for homecourt advantage and back to back
                    else: l_elo = l_elo +hp3 + hp4*l_date; w_elo = w_elo + hp4*l_date;
                    if w_elo>l_elo: outcomes.append(1) # if the model correctly predicted the game, add a one to the outcome vector
                    if l_elo>w_elo: outcomes.append(0) # else add a zero
                    w_new_elo = (w_elo+np.log(pd+1)*(2.2/((w_elo-l_elo)*.001+2.2))*hp1*(1-(1/(1+10**((l_elo-w_elo)/400))))) # update the winner's elo
                    l_new_elo = (l_elo+np.log(pd+1)*(2.2/((w_elo-l_elo)*.001+2.2))*hp1*(0-(1/(1+10**((w_elo-l_elo)/400))))) # update the loser's elo
                    ID[winner]=(w_new_elo,game_date,w_games + 1) # update the dictionary of teams to include a key of the team's name, and a value of (their elo score, the date of their last game, how many games they've played so far)
                    ID[loser]=(l_new_elo,game_date,l_games + 1) # do the same for the losing team
                hp_test[(hp1,hp2,hp3,hp4)] = (sum(outcomes)/float(len(outcomes))) # update the dictionary of results to include a key of all their hyperparameters and a value of the percent of games correctly predicted
print (sorted(hp_test.items(), key=operator.itemgetter(1),reverse=True)) # print out the dictionary in order form most accurate to least accurate
print (sorted(ID.items()))