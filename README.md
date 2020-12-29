# Log-Calculator: Calculating operations' time of manufacturing equipments.
Log-Calculator was a small project for calculating operation-times automatically. 
This code requires 2 files Equipments' Log file (txt) and maually defined operations list. 
Read them and crating each operations csv file 
Because of security reasons, I can't upload raw files of them. 
But their forms look like below,

#### Log file.txt

...  
Informations about equipments...  
...  
[time]  [Operation name1] [Status]  
[time]  [Operation name2] [Status]  
[time]  [Operation name3] [Status]  
[time]  [Operation name1] [Status]  
...  

#### Maually defined operations list.csv

| Operation name      | Status     | Manually defined code     |
| :------------- | :----------: | -----------: |
|  Operation 1 | Start   | 100    |
| Operation 1   | End | 101 |
| ...   | ... | ... |
| Operation 10   | Start | 1001 |
| Operation 10   | Action | 1002 |
| Operation 10   | End | 1003 |

### Result.csv
| Operation name 1     | Status     | Manually defined code     |
| Manually defined code 1    | Status     | Manually defined code     |
| :------------- | :----------: | -----------: |
|  Operation 1 | Start   | 100    |
| Operation 1   | End | 101 |
| ...   | ... | ... |
| Operation 10   | Start | 1001 |
| Operation 10   | Action | 1002 |
| Operation 10   | End | 1003 |

Read above 2 files and it calculating times
