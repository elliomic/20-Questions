traits = [] #remaining potential traits
allTraits = [] #all traits
traitType = dict() #determines if traits are adjectives or parts
items = dict() #remaining potential items (items, 0/1 traits)
allItems = dict() #all items

#filling in traits, allTraits, and traitType
traitFile = open("traits.txt", "r")
for line in traitFile:
    traits.append(line.split(" | ")[0].strip())
    allTraits.append(line.split(" | ")[0].strip())
    traitType[line.split(" | ")[0].strip()] = line.split(" | ")[1].strip()
traitFile.close()

#filling in items and allItems
itemFile = open("items.txt", "r")
for line in itemFile:
    items[line.split(" | ")[0]] = line.strip().split(" | ")[1].split(", ")
    allItems[line.split(" | ")[0]] = line.strip().split(" | ")[1].split(", ")
itemFile.close()

gameWon = False
answers = dict() #(trait, 1 or 0)
askedQuestions = [] #list of already-used traits
guess = [] #list of already-used items

#calculating the best question to ask
while not gameWon:
    yesNoSplit = dict()
    for trait in traits:
        ones = 0.0
        zeroes = 0.0
        for key in items:
            if traits.index(trait) < len(items[key]):
                if items[key][traits.index(trait)] == "1":
                    ones += 1
                elif items[key][traits.index(trait)] == "0":
                    zeroes += 1
        if (ones + zeroes) != 0:
            yesNoSplit[trait] = abs((ones / (ones + zeroes)) - .5)
    lowest = traits[0]
##    print traits
    for trait in yesNoSplit:
##        print "trait: " + trait
##        print "split: ", yesNoSplit[trait]
##        print "lowest: ", yesNoSplit[lowest]
        if yesNoSplit[trait] <= yesNoSplit[lowest] and trait not in askedQuestions:
            lowest = trait

#asking the question
    while True:
        if traitType[lowest] == '1':
            answers[lowest] = raw_input("is it " + lowest + "?\n")
        elif traitType[lowest] == '2':
            answers[lowest] = raw_input("does it have " + lowest + "?\n")
        if answers[lowest] == '1' or answers[lowest] == '0' or answers[lowest] == '2':
            break
        else:
            if answers[lowest].lower() == 'yes' or answers[lowest].lower() == 'y':
                answers[lowest] = '1'
                break
            elif answers[lowest].lower() == 'no' or answers[lowest].lower() == 'n':
                answers[lowest] = '0'
                break
            elif answers[lowest].lower() == 'maybe' or answers[lowest].lower() == 'm' or answers[lowest].lower() == 'sometimes' or answers[lowest].lower() == 's' or answers[lowest].lower() == 'unknown' or answers[lowest].lower() == 'u':
                answers[lowest] = '2'
                break
    askedQuestions.append(lowest)
##    print askedQuestions

#ruling out
    badkeys = []
    for key in items:
        if allTraits.index(lowest) < len(items[key]):
            if (items[key][allTraits.index(lowest)] == '0' and answers[lowest] == '1') or (items[key][allTraits.index(lowest)] == '1' and answers[lowest] == '0'):
                badkeys.append(key)
    for key in badkeys:
        del items[key]
##        print items

    moreInformationAvailable = False
    for key in items:
        for trait in traits:
            if items[key][allTraits.index(trait)] == '2':
                moreInformationAvailable = True

    traits.remove(lowest)

#deciding whether to guess, and guessing
    if len(items) == 1 or not moreInformationAvailable:
        for key in items:
            guess.append(key)
            while not gameWon:
                myGuess = raw_input("were you thinking of " + key + "?\n")
                if myGuess == "1" or myGuess == "yes" or myGuess == "y":
                    gameWon = True
                    print "i win!"
                    sortedAnswers = []
                    for trait in allTraits:
                        if trait in answers:
                            sortedAnswers.append(answers[trait])
                        else:
                            sortedAnswers.append("2")
                    for i in range(len(allItems[key])-1):
                        sortedAnswers[i] = allItems[key][i]
                    allItems[key] = sortedAnswers
                    itemFile = open("items.txt", "w")
                    for key in allItems:
                        itemFile.write(key + " | " + str(allItems[key]).strip("[").strip("]").replace("'", "") + "\n")
                    itemFile.close()
                    break
                elif myGuess == '0' or myGuess == 'no' or myGuess == 'n':
                    break
        break

    elif len(items) == 0:
        break

#asking for new item
if not gameWon:
    traitFile = open("traits.txt", "a")
    newTraits = []
    while True:
        newItem = raw_input("i give up. what were you thinking of?\n").lower()
        if newItem != "":
            break

#makes list of traits of new item, not including the new trait
    sortedAnswers = []
    for trait in allTraits:
        if trait in answers:
            sortedAnswers.append(answers[trait])
        else:
            sortedAnswers.append("2")

#asking for new trait
    for key in items:
        newTrait = ""
        while newTrait == "":
            rawInput = raw_input("what makes " + newItem + " different from " + key + "?\n").lower()
            if 'has ' in rawInput:
                newTraitType = '2' #2's are part traits, 1's are adjective traits
                (x, y, newTrait) = rawInput.partition('has ')
            elif 'have ' in rawInput:
                newTraitType = '2'
                (x, y, newTrait) = rawInput.partition('have ')
            elif 'is ' in rawInput:
                newTraitType = '1'
                (x, y, newTrait) = rawInput.partition('is ')
            elif 'are ' in rawInput:
                newTraitType = '1'
                (x, y, newTrait) = rawInput.partition('are ')
            else:
                print "sorry, i don't understand. what is " + newItem + " or what does " + newItem + " have?"
            if newTrait in allTraits:
                sortedAnswers[allTraits.index(newTrait)] = '1'
                while len(allItems[key]) < len(sortedAnswers):
                    allItems[key].append('2')
                allItems[key][allTraits.index(newTrait)] = '0'
                break
            elif newTrait != "":
                traitFile.write(newTrait + " | " + newTraitType + "\n")
                newTraits.append(newTrait)
                break
    traitFile.close()

#filling in 1 on the new trait on the new item, 0 on the new trait on the wrong item, and 2's in between
    for trait in newTraits:
        sortedAnswers.append('1')
        for i in range(1, len(sortedAnswers) - len(allItems[guess[0]])):
            allItems[guess[0]].append('2')
        allItems[guess[0]].append('0')
    
    if newItem in allItems:
        for i in range(len(allItems[newItem])-1):
            if sortedAnswers[i] == '2':
                sortedAnswers[i] = allItems[newItem][i]
        allItems[newItem] = sortedAnswers
    else:
        allItems[newItem] = sortedAnswers
    
    supplementalQuestionsAsked = 0
    if len(guess) > 0 and '2' in allItems[guess[0]]:
        while True:
            supplementalQuestionsAsked += 1 #keeping track of the number of supplemental questions asked
            print "thanks! now teach me something:"
            if traitType[allTraits[allItems[guess[0]].index('2')]] == '2':
                info = raw_input("does " + guess[0] + " have " + allTraits[allItems[guess[0]].index('2')] + "?\n")
            elif traitType[allTraits[allItems[guess[0]].index('2')]] == '1':
                info = raw_input("is " + guess[0] + " " + allTraits[allItems[guess[0]].index('2')] + "?\n")
            if info == '1' or info == 'yes' or info == 'y':
                allItems[guess[0]][allItems[guess[0]].index('2')] = '1'
                break
            elif info == '0' or info == 'no' or info == 'n':
                allItems[guess[0]][allItems[guess[0]].index('2')] = '0'
                break
            elif info == '2' or info == 'maybe' or info == 'm' or info == 'sometimes' or info == 's' or info == 'unknown' or info == 'u':
               allItems[guess[0]][allItems[guess[0]].index('2')] = '2'
               break
    if '2' in allItems[newItem]:
        while True:
            if supplementalQuestionsAsked == 0:
                print "thanks! now teach me something:"
            else:
                print "thanks! one more:"
            if traitType[allTraits[allItems[newItem].index('2')]] == '2':
                info = raw_input("does " + newItem + " have " + allTraits[allItems[newItem].index('2')] + "?\n")
            elif traitType[allTraits[allItems[newItem].index('2')]] == '1':
                info = raw_input("is " + newItem + " " + allTraits[allItems[newItem].index('2')] + "?\n")
            if info == '1' or info == 'yes' or info == 'y':
                allItems[newItem][allItems[newItem].index('2')] = '1'
                break
            elif info == '0' or info == 'no' or info == 'n':
                allItems[newItem][allItems[newItem].index('2')] = '0'
                break
            elif info == '2' or info == 'maybe' or info == 'm' or info == 'sometimes' or info == 's' or info == 'unknown' or info == 'u':
                allItems[newItem][allItems[newItem].index('2')] = '2'
                break
    
    for key in allItems:
        while len(allItems[key]) < len(sortedAnswers):
            allItems[key].append('2')
    
    itemFile = open("items.txt", "w")
    for key in allItems:
        itemFile.write(key + " | " + str(allItems[key]).strip("[").strip("]").replace("'", "") + "\n")
    itemFile.close()
    
print 'thanks! play again!'
