rankMap = {'2':1, '3':2, '4':3, '5':4, '6':5, '7':6, '8':7, '9':8, 'T':9, 'J':10, 'Q':11, 'K':12, 'A':13}

## breaks string input for hands into a histogram of rank/count, sorted list of cards and
## boolean indicator of whether the hand is a flush
def processHand(hand):
    
    values = []
    suit = ''
    isFlush = True
    valueCount = {}
    sortHand = []

    ## process hand into a list of card values and a boolean representing whether
    ## the hand is a flush
    for card in hand:
        values.append(card[0])
        if(suit == ''):
            suit = card[1]
        if(card[1] != suit):
            isFlush = False

    ## sort the card list
    sortValues = sorted(values, key = rankMap.__getitem__, reverse = True)

    ## tally the number of each value using dictionary
    for card in values:
        valueCount[card] = valueCount.get(card,0) + 1

    ## sort the card values by number in hand and create a histogram or list of lists where
    ## each sublist is [value, number in hand]
    sortCard = sorted(valueCount, key=valueCount.__getitem__, reverse = True)
    for card in sortCard:
        sortHand.append([card, valueCount[card]])

    ## return tuple consisting of histogram, sorted card list and isFlush
    return (sortHand, sortValues, isFlush)

## returns decimal value for h considering it to be a list of base 13 coefficients
def score(h):
    score = 0
    mult = 1
    for i in range(-1,-(len(h)+1),-1):
        if(type(h[i]) == int):
            score += mult*h[i]
        else:
            score += mult*rankMap[h[i]]
        mult *= 13
    return score

## determines whether a hand is a straight
def isStraight(h):
    if((rankMap[h[0]] - rankMap[h[-1]]) == 4):
        return True
    elif((h[0] == 'A') and (h[1] == '5')):
        return True
    else:
        return False
    

## evaluates the handInfo and assigns a score to it based on normal poker rules
def evaluateHand(handInfo):
    hist = handInfo[0]
    hand = handInfo[1]
    isFlush = handInfo[2]

    ## create list [handRank, topCard, 2ndCard, hand] where handRank is number based
    ## on whether 4 of a kind, straight, etc, topCard is value of 4 of kind or high card
    ## in straight, etc. 2ndCard is card in second pair (either of full house or 2 pair)
    ## hand is all 5 cards in hand
    result = []

    if(isFlush):                                       
        if(isStraight(hand)):
            result = [9, hand[0], 0] + hand             ## straight flush
        else:
            result = [6, hand[0], 0] + hand             ## normal flush

    elif(hist[0][1] == 4):                              ## 4 of a kind
        result = [8, hist[0][0]] + hand
        
    elif(hist[0][1] == 3):
        if (hist[1][1] == 2):                           ## full house
            result = [7, hist[0][0], hist[1][0]] + hand
        else:                                           ## 3 of a kind
            result = [4, hist[0][0], 0] + hand
            
    elif(hist[0][1] == 2):
        if(hist[1][1] == 2):                            ## 2 pair
            result = [3, hist[0][0], hist[1][0]] + hand
        else:                                           ## 1 pair
            result = [2, hist[0][0], 0] + hand

    elif(isStraight(hand)):
        result = [5, hand[0], 0] + hand                 ## normal straight

    else:                                               ## highcard
        result = [1, hand[0], 0] + hand

    return score(result)            
        
## loads hands from text file
def load_hands():
    inFile = open("p054_poker.txt", 'r', 0)
    handsList = []
    for line in inFile:
        handsList.append(line)
    print " ", len(handsList), " hands loaded."
    return handsList



handsList = load_hands()

hand1Wins = 0

for hands in handsList:
    hands = hands.split()
    hand1 = hands[0:5]
    hand2 = hands[5:10]

    if(evaluateHand(processHand(hand1)) > evaluateHand(processHand(hand2))):
        hand1Wins += 1

print "Player 1 wins %d times" % hand1Wins
    




