#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
Nichole Etienne 
BMI 500 Lab -Deidentification 
The purpose of this code is deidentify the protected health information of the categorty AGE. 
'''
# import statements 
import re
import sys

# Age indicators: 
age_indicators = ["year old", "y\. o\.", "y\.o\.", "yo", "y", "years old", "year-old", "-year-old", "years-old", "-years-old", "years of age", "yrs of age", "s/p"];

# phrases that preceed age: 
preceeding_phrase = ["age", "he is", "she is", "patient is"];

#Age is considered PHI when it is >89 
#Thus the  Regular expression for age is between 89 and 125 (89< age < 125), digits : 2 or 3 
#SN: The oldest woman in my country was 123, 125 seems fair. 
# The digits can be followed by white space, numbers, a comma (,) or a period(.)
structure_age ='[\s]\d{2,3}[\s,.]' 
regex_age = re.compile(structure_age)


#modified from example given in lecture 
def check_for_age(patient,note,chunk, output_handle):
    """
    Inputs:
        - patient: Patient Number, will be printed in each occurance of personal information found
        - note: Note Number, will be printed in each occurance of personal information found
        - chunk: one whole record of a patient
        - output_handle: an opened file handle. The results will be written to this file.
            to avoid the time intensive operation of opening and closing the file multiple times
            during the de-identification process, the file is opened beforehand and the handle is passed
            to this function. 
    Logic:
        Search the entire chunk for age occurances. Find the location of these occurances 
        relative to the start of the chunk, and output these to the output_handle file. 
        If there are no occurances, only output Patient X Note Y (X and Y are passed in as inputs) in one line.
        Use the precompiled regular expression to find ages.
    """
    #offset for start and end positions 
    offset = 25+len(patient)+len(note)

    # For every new note, the first line should be the Patient (X) and the Note (Y) followed by all patient personal information positions
    output_handle.write('Patient {}\tNote {}\n'.format(patient,note))

    # search the whole chunk, and find every position that matches the regular expression
    # for each one write the results: "Start Start END"
    # Also for debugging purposes display on the screen (and don't write to file) 
    # the start, end and the actual personal information that we found
    for match in regex_age.finditer(chunk):
        #conditional statement to see if the digit  found is between the range of 89 to 125
        if int(match.group()[:-1])<125 and int(match.group()[:-1])>89:
            #loops with conditional statement to see if the suffixes exists after the digit when the digit is considered a PHI 
            for suffix in age_indicators:
                for i in re.finditer(match.group()[1:-1]+' '+suffix+' ',chunk):#match.group()[1:-1] ignores the space before age and after age
                    if i.start()==match.start()+1:
                        # debug print, 'end=" "' stops print() from adding a new line
                        print(patient, note,end=' ')
                        print((match.start()+1-offset),match.end()-1-offset, match.group())

                        # create the string that we want to write to file ('start start end')    
                        result = str(match.start()+1-offset) + ' ' + str(match.start()+1-offset) +' '+ str(match.end()-1-offset) 
            
                        # write the result to one line of output
                        output_handle.write(result+'\n')
                        
            #loops with conditional statement to see if the prefixes exists before the digit when the digit is considered a PHI           
            for prefix in age_indicators:
                for i in re.finditer(prefix+match.group()[1:-1],chunk):#match.group()[1:-1] spaces before and after the age are not considered. 
                    if i.end()==match.end()-1:
                        # debug print, 'end=" "' stops print() from adding a new line
                        print(patient, note,end=' ')
                        print((match.start()+1-offset),match.end()-1-offset, match.group())

                        # create the string that we want to write to file ('start start end')    
                        result = str(match.start()+1-offset) + ' ' + str(match.start()+1-offset) +' '+ str(match.end()-1-offset) 
            
                        # write the result to one line of output
                        output_handle.write(result+'\n')
                        
            
    

        
        
        
        
        
        
        
        
        
        
   #modified from that given during class lecture          
def deid_age(text_path= 'id.text', output_path = 'age-Etienne-Nichole.phi'):
    """
    Inputs: 
        - text_path: path to the file containing patient records
        - output_path: path to the output file.
    
    Outputs:
        for each patient note, the output file will start by a line declaring the note in the format of:
            Patient X Note Y
        then for each age found, it will have another line in the format of:
            start start end
        where the start is the start position of the detected age string, and end is the detected
        end position of the string both relative to the start of the patient note.
        If there is no age  detected in the patient note, only the first line (Patient X Note Y) is printed
        to the output
    Screen Display:
        For each age  detected, the following information will be displayed on the screen for debugging purposes 
        (these will not be written to the output file):
            start end age
        where `start` is the start position of the detected age string, and `end` is the detected end position of the string
        both relative to the start of patient note.
    
    """
    # start of each note has the patter: START_OF_RECORD=PATIENT||||NOTE||||
    # where PATIENT is the patient number and NOTE is the note number.
    start_of_record_pattern = '^start_of_record=(\d+)\|\|\|\|(\d+)\|\|\|\|$'

    # end of each note has the patter: ||||END_OF_RECORD
    end_of_record_pattern = '\|\|\|\|END_OF_RECORD$'

    # open the output file just once to save time on the time intensive IO
    with open(output_path,'w+') as output_file:
        with open(text_path) as text:
            # initilize an empty chunk. Go through the input file line by line
            # whenever we see the start_of_record pattern, note patient and note numbers and start 
            # adding everything to the 'chunk' until we see the end_of_record.
            chunk = ''
            for line in text:
                record_start = re.findall(start_of_record_pattern,line,flags=re.IGNORECASE)
                if len(record_start):
                    patient, note = record_start[0]
                chunk += line

                # check to see if we have seen the end of one note
                record_end = re.findall(end_of_record_pattern, line,flags=re.IGNORECASE)

                if len(record_end):
                    # Now we have a full patient note stored in `chunk`, along with patient numerb and note number
                    # pass all to check_for_age to find any ages in note.
                    check_for_age(patient,note,chunk.strip(), output_file)
                    
                    # initialize the chunk for the next note to be read
                    chunk = ''
                
if __name__== "__main__":
        
    
    
    deid_age(sys.argv[1], sys.argv[2])

