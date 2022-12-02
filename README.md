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


