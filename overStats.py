import csv
import math


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
                while awayInning < len(row['awayinnings'])-1:
                    awayinningRuns = row['awayinnings'][awayInning]
                    if awayinningRuns != '(':
                        awayScore += int(awayinningRuns)
                        awayInning += 1
                    else:
                        awayScore += int(row['awayinnings'][awayInning+1:awayInning+3])
                        awayInning += 4
                homeInning = 0
                while homeInning < len(row['homeinnings'])-2:
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
                print(awayScore-homeScore)
                awayScore = 0
                homeScore = 0
                
        i += 1
                #homeScore8th = row[]
                #return (game, diff)


getScoreDiffMid8th()