# Advent of Code 2022

Advent of Code is a celebration of coding mixed with the holiday spirit. In 2022 we are working towards feeding the reindeer with enough fruit to send them on their way on Christmas day.

> Santa's reindeer typically eat regular reindeer food, but they need a lot of magical energy to deliver presents on Christmas. For that, their favorite snack is a special type of star fruit that only grows deep in the jungle. The Elves have brought you on their annual expedition to the grove where the fruit grows.

> To supply enough magical energy, the expedition needs to retrieve a minimum of fifty stars by December 25th. Although the Elves assure you that the grove has plenty of fruit, you decide to grab any fruit you see along the way, just in case.


## Shared

Commonly used imports throughout the application will make things a little easier moving forward


```python
from functools import reduce
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
        currentElf.append(int(line.strip('\n')))
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

def stageHand(r):
    if r[1] == 'Rock':
        r[1] = win_table[r[0]]
    elif r[1] == 'Paper':
        r[1] = r[0]
    else:
        r[1] = lose_table[r[0]]
    return r

rounds = list(map(stageHand, rounds))
```

Same as before then, we want to simply score each round with the new round setup


```python
scores = list(map(lambda r: scoreRound(r), rounds))
sum(scores)
```




    15442


