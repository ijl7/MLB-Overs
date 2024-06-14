import csv
import math

gameDiff = {}
runsAfterTie = []

#going to be used to clean up the code, unused right now
def getAnyScore(row, awayMax, homeMax):
    homeScore = 0
    awayScore = 0

    awayInning = 0
    homeInning = 0

    if awayMax > len(row['awayinnings']) or homeMax > len(row['homeinnings']):
        return (None,None)

    while awayInning < awayMax:
        awayinningRuns = row['awayinnings'][awayInning]
        if awayinningRuns != '(':
            awayScore += int(awayinningRuns)
            awayInning += 1
        else:
            awayScore += int(row['awayinnings'][awayInning+1:awayInning+3])
            awayInning += 4
    
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

    return (homeScore, awayScore)

def getScoreDiffMid8th():
    homeScore = 0
    awayScore = 0
    i = 2020
    while i < 2024:
        with open('gl' + str(i) + '.csv', mode='r') as file:
            csvFile = csv.DictReader(file)
            game = 0
            for row in csvFile:
                game += 1
                (homeScore, awayScore) = getAnyScore(row, awayMax = min(8,len(row['awayinnings'])-1), homeMax = min(7, len(row['homeinnings'])-2))
                if homeScore != None:
                    gameDiff.__setitem__(game,(homeScore+awayScore,homeScore-awayScore))
                awayScore = 0
                homeScore = 0

        i += 1
        
def getRunsAfterTie():
    i = 2020
    while i < 2024:
        with open('gl' + str(i) + '.csv', mode='r') as file:
            csvFile = csv.DictReader(file)
            game = 0
            for row in csvFile:
                totalRuns = 0
                awayScore = 0
                homeScore = 0
                game += 1
                (homeScore, awayScore) = getAnyScore(row, awayMax = len(row['awayinnings']), homeMax = len(row['homeinnings']))
                totalRuns = homeScore + awayScore
                if gameDiff.get(game) != None:
                    if gameDiff.get(game)[1] == 0:
                        runsAfterTie.append(totalRuns - gameDiff.get(game)[0])
                
                    
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
print('\nIn the past 4 seasons there was an average of ' + str(round(sum(runsAfterTie)/len(runsAfterTie), 3)) + ' runs scored in games not tied in the mid 8th.\n')
print(str(over) + ' of ' + str(len(runsAfterTie)) + ' games went over, or ' + str(round((over/len(runsAfterTie))*100, 3)) + '%.')