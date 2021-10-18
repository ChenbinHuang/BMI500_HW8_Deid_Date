# Week 8 Assignment: de-id of DateYear in medical records
I have chosen to find and deidentify DateYear information in the given medical records.
The edited deid.py and resulting accuracy statistics (stats.txt) can be found under python directory.

Examining "DateYear" category.


==========================

Num of true positives = 46

Num of false positives = 2188

Num of false negatives = 0

Sensitivity/Recall = 1.0

PPV/Specificity = 0.914

==========================

# Prerequisites
## Python
* Python 3.5.2
## Perl
* Perl 5, Version 28, Subversion 0 (v5.28.0)
# Running insturctions
## Python Code
### De-identification
1- Change to the python directory

2- run ```python deid.py id.text phone.phi```

In which:

* ```id.text``` contains Patient Notes.
* ```phone.phi``` is the output file that will be created.
### Stats
1- change to the python directory

2- run ```python stats.py id.deid id-phi.phrase phone.phi ```

In which:

* ```id.deid``` is the gold standard that is category-blind.
* ```id-phi.phrase``` is the gold standard with the categories included.
* ```phone.phi``` is the test file that the stats is run on.
