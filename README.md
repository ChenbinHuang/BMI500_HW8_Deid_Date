# de-id Edited: 
Few changes have been done to the original deid.py
- First, the deid.py was changed to deidclass.py which when running this line ```python deidclass.py id.text age-retta-elsayed.phi``` it will promote you to choose an option for deidentification catagory including: 
 1. Phone
 2. Age
 3. Location(underDEV)
 4. DateYear(underDEV)
 5. Date(underDEV)
 6. HCPName(underDEV)
 7. PTName(underDEV)
 8. RelativeProxyName(underDEV)
 9. PTNameInitial(underDEV)
 10. Age(underDEV)
 11. Other(underDEV)
 12. All(underDEV)
 select the PHI category to de-identify?
 Here you can entre the number. For this code phone (1), age(2) are working to de-id both type 12. 

 - Second, the de-id of the phone was moved to a script under the title of ClassPhone. 
 - Third, the developed de-id for the patient age is under age-retta-elsayed.py. For this script, Regular expression or Regex wasn't used. Instead, age indicators such as phrases including years old, yrs, yo, age, etc... were used to identify the age in a chunk. 


# de-id
Perl and Python code for de-identifying electronic medical records
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
