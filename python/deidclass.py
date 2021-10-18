# deidclass.py was editied to include all the different catagories in PHI, which after the development of the de-identification catagories can be helpful. 
# The Telephone code was moved to different script under the title ClassPhone. The patient age de-id script is under the title of ClassAge.
# The same age de-identification code was also saved under deid-retta-elsayed for easier access. 

import re
import sys
from deid_retta_elsayed import deid_age
from ClassPhone import deid_phone
# The following function ask the user to choose a number corsponded to the catagory/class of data to de-identfy. After the number was chosen the result either the
# ClassPhone or the ClassAge or both will run and record the data to age.phi. 
def instructions():
    print(
        'Options:\n',
        '1. Phone\n',
        '2. Age\n',
        '3. Location(underDEV)\n',
        '4. DateYear(underDEV)\n',
        '5. Date(underDEV)\n',
        '6. HCPName(underDEV)\n',
        '7. PTName(underDEV)\n',
        '8. RelativeProxyName(underDEV)\n',
        '9. PTNameInitial(underDEV)\n',
        '10. Age(underDEV)\n',
        '11. Other(underDEV)\n',
        '12. All(underDEV)\n',
        'select the PHI category to de-identify?'
    )
    x = input('')
    return x

if __name__== "__main__":
    x = instructions()
    print(x)

    if x == '1':
        deid_phone(sys.argv[1], sys.argv[2])
    if x == '2':
        deid_age(sys.argv[1], sys.argv[2])
    if x == '12':
        deid_phone(sys.argv[1], sys.argv[2])
        deid_age(sys.argv[1], sys.argv[2])
    

    