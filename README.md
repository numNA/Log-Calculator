# Log-Calculator: Calculating operations' time of manufacturing equipments.
Log-Calculator was a small project for calculating operation-times automatically. 
This code requires 2 files Equipments' Log file (txt) and maually defined operations list. 
Read them and crating each operations csv file 
Because of security reasons, I can't upload raw files of them. 
But their forms look like below.

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

| Operation name 1 & Code (Status: Start)      | ...     | Operation name 10 & Code (Status: Start)     |
| Operation name 1 & Code (Status: End)      | ...     | Operation name 10 & Code (Status: End)     |
| Mean of Operating times in Log file (Operation 1)          | ...     | Mean of Operating times in Log file (Operation 1)        |
|:==============|-----------------|----------------:|
| 1st Operation 1's time | ...   | 1st Operation 10's time    |
| 2nd Operation 1's time   | ... | 2nd Operation 10's time |
| ...   | ... | ... |
| nth Operation 1's time   | ... | nth Operation 10's time |
| ...   | ... | ... |
| blank   | ... | (n+m)th Operation 10's time |

### new


|              | Header 1        | Header 2                       || Header 3                       ||
|              | Subheader 1     | Subheader 2.1  | Subheader 2.2  | Subheader 3.1  | Subheader 3.2  |
|==============|-----------------|----------------|----------------|----------------|----------------|
| Row Header 1 | 3row, 3col span                                 ||| Colspan only                   ||
| Row Header 2 |       ^                                         ||| Rowspan only   | Cell           |
| Row Header 3 |       ^                                         |||       ^        | Cell           |
| Row Header 4 |  Row            |  Each cell     |:   Centered   :| Right-aligned :|: Left-aligned  |
:              :  with multiple  :  has room for  :   multi-line   :    multi-line  :  multi-line    :
:              :  lines.         :  more text.    :      text.     :         text.  :  text.         :
|--------------|-----------------|----------------|----------------|----------------|----------------|
[Caption Text]
