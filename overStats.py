import csv
import math

gameDiff = []
runsAfterTie = []

#going to be used to clean up the code, unused right now
def getAnyScore(row, awayMax, homeMax):
    homeScore = 0
    awayScore = 0

    awayInning = 0
    while awayInning < awayMax:
        awayinningRuns = row['awayinnings'][awayInning]
        if awayinningRuns != '(':
            awayScore += int(awayinningRuns)
            awayInning += 1
        else:
            awayScore += int(row['awayinnings'][awayInning+1:awayInning+3])
            awayInning += 4
    homeInning = 0
    while homeInning < homeMax:
        homeInningRuns = row['homeinnings'][homeInning]
        if homeInningRuns != '(' and homeInningRuns != 'x':
            homeScore += int(homeInningRuns)
            homeInning += 1
        else:
            if homeInningRuns == '(':
                homeScore += int(row['homeinnings'][homeInning+1:homeInning+3])
                homeInning += 4
            else:
                homeScore += 0
                homeInning += 1

    return homeScore + awayScore

def getScoreDiffMid8th():
    homeScore = 0
    awayScore = 0
    i = 2020
    while i < 2021:
        with open('gl' + str(i) + '.csv', mode='r') as file:
            csvFile = csv.DictReader(file)
            game = 0
            for row in csvFile:
                game += 1
                awayInning = 0
                awayMax = 8
                homeMax = 7
                while awayInning < int(min(awayMax, len(row['awayinnings'][awayInning]))):
                    awayinningRuns = row['awayinnings'][awayInning]
                    if awayinningRuns != '(':
                        awayScore += int(awayinningRuns)
                        awayInning += 1
                    else:
                        awayScore += int(row['awayinnings'][awayInning+1:awayInning+3])
                        awayMax += 2
                        awayInning += 4
                homeInning = 0
                while homeInning < int(min(homeMax, len(row['homeinnings'])-1)):
                    homeInningRuns = row['homeinnings'][homeInning]
                    if homeInningRuns != '(' and homeInningRuns != 'x':
                        homeScore += int(homeInningRuns)
                        homeInning += 1
                    else:
                        if homeInningRuns == '(':
                            homeScore += int(row['homeinnings'][homeInning+1:homeInning+3])
                            homeMax += 2
                            homeInning += 4
                        else:
                            homeScore += 0
                            homeInning += 1
                gameDiff.append((game,homeScore+awayScore,homeScore-awayScore))
                awayScore = 0
                homeScore = 0

        i += 1
        
def getRunsAfterTie():
    i = 2020
    while i < 2021:
        with open('gl' + str(i) + '.csv', mode='r') as file:
            csvFile = csv.DictReader(file)
            game = 0
            for row in csvFile:
                totalRuns = 0
                awayScore = 0
                homeScore = 0
                game += 1
                if gameDiff[game-1][2] == 0:
                    awayInning = 0
                    while awayInning < len(row['awayinnings']):
                        awayinningRuns = row['awayinnings'][awayInning]
                        if awayinningRuns != '(':
                            awayScore += int(awayinningRuns)
                            awayInning += 1
                        else:
                            awayScore += int(row['awayinnings'][awayInning+1:awayInning+3])
                            awayInning += 4
                    homeInning = 0
                    while homeInning < len(row['homeinnings']):
                        homeInningRuns = row['homeinnings'][homeInning]
                        if homeInningRuns != '(' and homeInningRuns != 'x':
                            homeScore += int(homeInningRuns)
                            homeInning += 1
                        else:
                            if homeInningRuns == '(':
                                homeScore += int(row['homeinnings'][homeInning+1:homeInning+3])
                                homeInning += 4
                            else:
                                homeScore += 0
                                homeInning += 1
                    totalRuns = homeScore + awayScore
                    runsAfterTie.append(totalRuns - gameDiff[game-1][1])

        i += 1

getScoreDiffMid8th()
getRunsAfterTie()
over = 0
under = 0
for runs in runsAfterTie:
    if runs > 1:
        over += 1
    else:
        under += 1
print('\nIn 2020 there was an average of ' + str(round(sum(runsAfterTie)/len(runsAfterTie), 3)) + ' runs scored in games tied in the mid 8th.\n')
print(str(over) + ' of ' + str(len(runsAfterTie)) + ' games went over, or ' + str(round((over/len(runsAfterTie))*100, 3)) + '%.')