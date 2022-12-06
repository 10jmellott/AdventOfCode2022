# Advent of Code 2022

[Advent of Code](https://adventofcode.com/) is a celebration of coding mixed with the holiday spirit. In 2022 we are working towards feeding the reindeer with enough fruit to send them on their way on Christmas day.

> Santa's reindeer typically eat regular reindeer food, but they need a lot of magical energy to deliver presents on Christmas. For that, their favorite snack is a special type of star fruit that only grows deep in the jungle. The Elves have brought you on their annual expedition to the grove where the fruit grows.

> To supply enough magical energy, the expedition needs to retrieve a minimum of fifty stars by December 25th. Although the Elves assure you that the grove has plenty of fruit, you decide to grab any fruit you see along the way, just in case.


## Shared

Commonly used imports throughout the application will make things a little easier moving forward


```python
from functools import reduce
import re
```


```python
def readlinesext(f):
    return list(map(lambda l: l.strip(), f))
def readlinesnl(f):
    return list(map(lambda l: l.strip('\n'), f))
```

# Day 1: Calorie Counting

The elves are beginning a foot expedition through the jungle to begin collecting fruit for the reindeer. The elves are on foot and, as a result, are all bringing a certain amount of food with them. However, some elves are worried they might not have enough food and have asked us to find out who has the most food so we know who to ask just in case.

Open up the sheet with information on how many calories each elf has. 


```python
f = open('data/01.txt', 'r')
```

Parse the data into an array of elves with each elf's itemized list of food items (measured by calories)


```python
elves = list()
currentElf = list()
for line in f:
    if line == '\n':
        elves.append(currentElf)
        currentElf = list()
    else:
        currentElf.append(int(line.strip()))
elves.append(currentElf)
```

Next, we want to tally up each elf's caloric total and order them so we know which elves have the most calories.


```python
calories = list(map(lambda l: reduce(lambda a, b: a+b, l), elves))
calories.sort()
```

The first part asks us which elf has the most calories. Pretty simply in python as the calorie list is already sorted we just want the highest value which is the last item in the list, i.e. index -1.


```python
calories[-1]
```




    67633



That's enough food for a human adult for easily over a month...are they riding on a donkey or something?

The elves realize that if they cannibalize only the elf with the highest calorie count, there's too many elves and we'll end up depleting that elf solely of calories. Instead, they want the total calories for the top three elves with the most calories. As the list is still sorted, we slice out of the array the last three values in the calorie array and sum them together.


```python
sum(calories[-3:])
```




    199628



# Day 2: Rock Paper Scissors

The elves set up camp on the beach and start playing Rock, Paper, Scissors. One elf attempts to help us cheat by providing us with an encrypted strategy guide to help us win.

Read in the encrypted data files & parse it into the rounds. The first value can be A, B, or C representing rock, paper, or scissor. The second value for each round is what we should throw out, X, Y, or Z representing rock, paper, or scissors respectively as well.


```python
f = open('data/02.txt', 'r')
rounds = list(map(lambda l: l.split(), f))
```

To make things easier, let's normalize the data. I don't love magic strings, but this isn't a large project so deal with it.


```python
normalize = {
    'A': 'Rock', 'B': 'Paper', 'C': 'Scissors',
    'X': 'Rock', 'Y': 'Paper', 'Z': 'Scissors'
}
rounds = list(map(lambda l: list(map(lambda r: normalize[r], l)), rounds))
```

Now we want to setup a function to be able to score each round. The scoring rules are fairly complex, but your score for each round is determined as 0 for losing, 3 for a draw, and 6 for a win. Additionally you gain 1, 2, or 3 points depending on whether your hand was a rock, paper, or scissors respectively.


```python
lose_table = {
    'Rock': 'Paper',
    'Paper': 'Scissors',
    'Scissors': 'Rock'
}

score_add = { 'Rock': 1, 'Paper': 2, 'Scissors': 3 }

score_lose = 0
score_draw = 3
score_win = 6

def scoreRound(r):
    score = score_add[r[1]]
    if r[0] == r[1]:
        score += score_draw
    elif lose_table[r[1]] == r[0]:
        score += score_lose
    else:
        score += score_win
    return score
```

Next, we want to actually check each round for the score and tally them


```python
scores = list(map(lambda r: scoreRound(r), rounds))
```

Finally, the first part requests us to find the sum of the scores


```python
sum(scores)
```




    15422



After chatting with the elf who left us to our own devices to figure this thing out, they actually told us that X means we need to lose, Y means we need to draw, and Z means we need to win. So, we need to re-normalize the data a little differently first. We know how the data was normalized the first time, so we can use the existing data without issue.


```python
win_table = {
    'Rock': 'Scissors',
    'Paper': 'Rock',
    'Scissors': 'Paper'
}

def stagehand(r):
    if r[1] == 'Rock':
        r[1] = win_table[r[0]]
    elif r[1] == 'Paper':
        r[1] = r[0]
    else:
        r[1] = lose_table[r[0]]
    return r

rounds = list(map(stagehand, rounds))
```

Same as before then, we want to simply score each round with the new round setup


```python
scores = list(map(lambda r: scoreRound(r), rounds))
sum(scores)
```




    15442



# Day 3: Rucksack Reorganization

An elf messed up packing the backpacks and we need to solve it. To start with we'll take a short-code list of the items in each backpack and figure out which item is at fault in each sack and do a quick sum of the value of each of those items to try and determine how bad it really is.

Alright, keeping things simple let's pull down the input list and try and parse the input.


```python
f = open('data/03.txt', 'r')
def splitcompartments(l):
    middle = int(len(l) / 2)
    return set(l[:middle]), set(l[middle:])
rucksacks = readlinesext(f)
compartments = list(map(splitcompartments, rucksacks))
```

Ok, next order of business now that the shorthand list is parsed is to loop through each rucksack and find the common denominator in each sack. This is pretty easy thanks to pre-converting the sack lists to sets.


```python
overlaps = list(map(lambda s: list(s[0] & s[1])[0], compartments))
```

Now we have the following rules to help prioritize which items to start with:
* Lowercase item types a through z have priorities 1 through 26.
* Uppercase item types A through Z have priorities 27 through 52.


```python
orda = ord('a')
ordA = ord('A')
def scoreitem(i):
    ci = ord(i)
    if ci >= orda:
        return ci - orda + 1
    return ci - ordA + 27
scores = list(map(scoreitem, overlaps))
```

Let's see, roughly, how bad of a shape we're in...


```python
sum(scores)
```




    7701



Alright, now that we know this, another problem has arisen in that the elves are actually supposed to be grouped into sets of three. The elves are already in order, but they don't know what their group identity is, namely which item does every member in the group hold? To get this solved, we need to do some complex slicing.


```python
slices = rucksacks[::3], rucksacks[1::3], rucksacks[2::3]
```

Now that we have the groups more or less figured out, next we need to find each group's badge.


```python
badges = list()
for i in range(len(slices[0])):
    badge = list(set(slices[0][i]) & set(slices[1][i]) & set(slices[2][i]))[0]
    badges.append(badge)
```

Now that we have the badges, scoring them really isn't any different and all we care about is the final total of the badges anyway so we'll do both real quick.


```python
sum(list(map(scoreitem, badges)))
```




    2644



# Day 4: Camp Cleanup

The elves are disturbingly disorganized. For today's puzzle we see that the elves are trying to cleanup the campsite, but they have overlapping segments they expect to clean up. The elves are broken down into pairs but some pairs overlap completely which is silly. So, our first challenge is to figure out how many pairs are completely overlapped.


```python
f = open('data/04.txt', 'r')
pairs = readlinesext(f)
pairs = list(map(lambda p: list(map(lambda e: list(map(int, e.split('-'))), p.split(','))), pairs))
```

Now that we have the pair data parsed, we need a method for detecting when a pair is completely overlapped. As these regions are consecutive, we can pretty easily do some basic math to do boundary detection. Either the smaller of the first must be overlapped completely by the smaller of the second.


```python
def testsuperset(pair):
    p1 = pair[0]
    p2 = pair[1]
    if p1[0] >= p2[0] and p1[1] <= p2[1]:
        return True
    elif p1[0] <= p2[0] and p1[1] >= p2[1]:
        return True
    return False
```

Nothing left but to get the number of supersets...


```python
len(list(filter(testsuperset, pairs)))
```




    456



By now it's probably pretty clear that things are overlapping pretty hard, and supersets are only the worst offenders. Let's drill down and see how many pairs overlap even the smallest bit next. This is pretty simple as we've already tested the superset but basically it boils down simply checking a fixed point rather than both ends of the range for each elf. For the first case we check if the start of the range for the second elf is encapsulated within the range of the first elf, and then visa versa.


```python
def testoverlap(pair):
    p1 = pair[0]
    p2 = pair[1]
    if p1[0] <= p2[0] and p1[1] >= p2[0]:
        return True
    elif p1[0] >= p2[0] and p1[0] <= p2[1]:
        return True
    return False
```

And, like last time, we'll get the number that pass this check.


```python
len(list(filter(testoverlap, pairs)))
```




    808



# Day 5: Supply Stacks

Today's trial leaves us to a set of shipping containers piled into stacks with instructions on how to move the containers to their final arrangement. The first order of business, as usual, is parsing the input in an easier to consume format.


```python
f = open('data/05.txt', 'r')
source = readlinesnl(f)
separationindex = source.index('')
sourcestacks = source[:separationindex-1]
sourceinstructions = source[separationindex+1:]
```

Now that we have the input separated into the stack and instruction segments, let's parse each part one at a time. We can start with the stacks. To make parsing this easier, we'll start by determining the number of stacks we have dictated by length of the string as there's whitespace at the end of each. Next we'll parse this segment given we know the exact placement for each character we can loop through each line and append to the stacks appropriately (starting from the bottom, it is a stack you know).


```python
nstacks = int((len(sourcestacks[0]) + 1) / 4)
stacks = list(map(lambda _: list(), range(nstacks)))
for i in range(nstacks):
    charindex = i * 4 + 1
    for j in range(len(sourcestacks) - 1, -1, -1):
        character = sourcestacks[j][charindex]
        if character != ' ':
            stacks[i].append(sourcestacks[j][charindex])
```

Alright, we've finalized the stack organization, so next is parsing the instructions which is a pretty simple regex.


```python
def parseinstruction(instruction):
    match = re.search("move (\d+) from (\d) to (\d)", instruction)
    return int(match.group(1)), int(match.group(2)), int(match.group(3))
instructions = list(map(parseinstruction, sourceinstructions))
```

So, finally now that we have everything parsed out, let's execute the instructions.


```python
def execute(stacks, instruction):
    for i in range(instruction[0]):
        stacks[instruction[2] - 1].append(stacks[instruction[1] - 1].pop())
for instruction in instructions:
    execute(stacks, instruction)
```

The only ask of this question now is what is to determine the container at the top of each stack.


```python
reduce(lambda a, b: a + b[len(b) - 1], stacks, '')
```




    'TWSGQHNHL'



So, this would have been the answer if the crane moved containers like a stack, one at a time. However, it doesn't and instead actually moves items as 'whole sets'. So moving three would move the top three from the stack and keep them in place. Thankfully we have the tools, so we should be able to do this without too much trouble.

 As we managed the instructions in-place, we'll re-run the stack construction real quick. The instructions, thankfully, should be the same.


```python
nstacks = int((len(sourcestacks[0]) + 1) / 4)
stacks = list(map(lambda _: list(), range(nstacks)))
for i in range(nstacks):
    charindex = i * 4 + 1
    for j in range(len(sourcestacks) - 1, -1, -1):
        character = sourcestacks[j][charindex]
        if character != ' ':
            stacks[i].append(sourcestacks[j][charindex])
```


```python
def execute(stacks, instruction):
    popindex = len(stacks[instruction[1] - 1]) - instruction[0]
    for i in range(instruction[0]):
        stacks[instruction[2] - 1].append(stacks[instruction[1] - 1].pop(popindex))
for instruction in instructions:
    execute(stacks, instruction)
```

Finally, we just want to see the order once more of the top containers of each stack for checking purposes.


```python
reduce(lambda a, b: a + b[len(b) - 1], stacks, '')
```




    'JNRSCDWPP'



# Day 6: Tuning Trouble

We're finally setting out to the star fruit grove, but the elves hand you a faulty communication system. Notably the system can't seem to figure out the start or end of the communication transfer protocol which is silly. So, we'll just do it manually. The input this time is a single line of text so we won't spend any time parsing it for now. Instead we'll just define a method to find the first set of 4 unique characters in the input field.


```python
f = open('data/06.txt', 'r')
packet = readlinesext(f)[0]
def findstart(packet, characters):
    for i in range(characters - 1, len(packet)):
        if len(set(packet[i - characters:i])) == characters:
            return i
findstart(packet, 4)
```




    1850



Well, start of packet is 4 unique items, but a start of message is 14...so only a minor change.


```python
findstart(packet, 14)
```




    2823


