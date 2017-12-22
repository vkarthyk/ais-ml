# structureForGrephi.csv
- This file is to import into Grephi, a software that could draw graphics
- The format matches the Basic format of Grephi input.
- for each row, the first element represents the father, and every other element in this row is his direct child node
- example: 
```
A | B | C | D
B | E |
```
- means we have a tree like this
```angular2html
A-->B--->E
 |
 -->C 
 |
 -->D

```
# fieldTree.pkl
- This is the pickle dump version of the same tree, created by dataParsing/main --> factory.goFindSomeoneDoThisJob( JobType.SaveFieldTree)
- You can load this file by calling dataParsing/main --> factory.goFindSomeoneDoThisJob( JobType.LoadFieldTree)
It will be stored inside the factory.
- Then call other functions to operate this tree
