import csv
import math

gameDiff = {}
runsAfterTie = []

#going to be used to clean up the code, unused right now
def getScore(row, awayMax, homeMax):
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

def getScoreDiffMidInning(inning):
    homeScore = 0
    awayScore = 0
    i = 2020
    while i < 2024:
        with open('gl' + str(i) + '.csv', mode='r') as file:
            csvFile = csv.DictReader(file)
            game = 0
            for row in csvFile:
                game += 1
                (homeScore, awayScore) = getScore(row, awayMax = inning-1, homeMax = inning-2)
                if homeScore != None:
                    gameDiff.__setitem__((i, game),(homeScore+awayScore,homeScore-awayScore))
                awayScore = 0
                homeScore = 0

        i += 1

def getScoreDiffTopInning(inning):
    homeScore = 0
    awayScore = 0
    i = 2020
    while i < 2024:
        with open('gl' + str(i) + '.csv', mode='r') as file:
            csvFile = csv.DictReader(file)
            game = 0
            for row in csvFile:
                game += 1
                (homeScore, awayScore) = getScore(row, awayMax = inning-1, homeMax = inning-1)
                if homeScore != None:
                    gameDiff.__setitem__((i, game),(homeScore+awayScore,homeScore-awayScore))
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
                (homeScore, awayScore) = getScore(row, awayMax = len(row['awayinnings']), homeMax = len(row['homeinnings']))
                totalRuns = homeScore + awayScore
                if gameDiff.get((i, game)) != None:
                    if gameDiff.get((i, game))[1] == 0:
                        runsAfterTie.append(totalRuns - gameDiff.get((i, game))[0])
                
                    
        i += 1

inning = input('When would you like to get the score from?\n')
timeOfGame = ''
if float(inning) % 1 == 0:
    getScoreDiffTopInning(int(inning))
    timeOfGame = ' top ' + str(inning) + 'th'
else:
    getScoreDiffMidInning(int(float(inning)-.5))
    timeOfGame = ' mid ' + str(int(float(inning)-.5)) + 'th'
getRunsAfterTie()
over = 0
under = 0
runsAdded = input('How many more runs are you wondering about?\n')
for runs in runsAfterTie:
    if runs > int(runsAdded) - 1:
        over += 1
    else:
        under += 1
print('\nIn the past 4 seasons there was an average of ' + str(round(sum(runsAfterTie)/len(runsAfterTie), 3)) + ' runs scored in games tied in the' + timeOfGame + '.\n')
print(str(over) + ' of ' + str(len(runsAfterTie)) + ' games went over ' + runsAdded + ' runs, or ' + str(round((over/len(runsAfterTie))*100, 3)) + '%.')