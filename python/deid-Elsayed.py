# deid-ElSayed.py include patient age de-identification 
# The Telephone code was moved to different script under the title ClassPhone. The patient age de-id script is under the title of ClassAge.

import re
import sys

# Age indicators that follow ages
age_pre = ("age")
# Age indicators that precede ages
age_post = ('year','YEAR', "y/o",'YO', "Y/O",'YR','yr', "y\.o\.", 'yo', 'y', 'y.o.','y.o','years','YEARS',"years old", "year-old", "-year-old", "years-old", "-years-old", "years of age", "yrs of age")

def check_for_age(patient,note,chunk, output_handle):
    """
    Inputs:u
        - patient: Patient Number, will be printed in each occurance of personal information found
        - note: Note Number, will be printed in each occurance of personal information found
        - chunk: one whole record of a patient
        - output_handle: an opened file handle. The results will be written to this file.
            to avoid the time intensive operation of opening and closing the file multiple times
            during the de-identification process, the file is opened beforehand and the handle is passed
            to this function. 
    Logic:
        Search the entire chunk for phone number occurances. Find the location of these occurances 
        relative to the start of the chunk, and output these to the output_handle file. 
        If there are no occurances, only output Patient X Note Y (X and Y are passed in as inputs) in one line.
        Use the precompiled regular expression to find phones.
    """
    output_handle.write('Patient {}\tNote {}\n'.format(patient,note))
    list_of_words = chunk.split()
    offset=27
# the following is a for loop to look for some age indicators/key words in the texts to determine the patient age. Some of these indicators can be before "age_pre" or after "age_post"
    for x in age_pre:
        if x in list_of_words:
            number_of_words = len(x.split())
            if number_of_words == '1':
                prev_word = list_of_words[list_of_words.index(x) + 1]
                if prev_word.isnumeric():
                    print(patient, note,prev_word)
                    #print((x.start()-offset),x.end()-offset, x.group())
                    output_handle.write(prev_word+'\n')
            # To avoid the difficulty to implement strings with space such as "year old" the following lines were implemented: 
            if number_of_words == '2':
                prev_word = list_of_words[list_of_words.index(x.split()[1]) + 2]
                if prev_word.isnumeric():
                    print(patient, note,prev_word)
                    #print((x.start()-offset),x.end()-offset, x.group())
                    output_handle.write(prev_word+'\n')

    for x in age_post:
        if x in list_of_words:
            post_word = list_of_words[list_of_words.index(x) - 1]
            if post_word.isnumeric():
                print(patient, note,post_word)
                #print((x.start()-offset),x.end()-offset, x.group())
                output_handle.write(post_word+'\n')


def deid_age(text_path='id.text', output_path='age.phi'):
    """
    Inputs: 
        - text_path: path to the file containing patient records
        - output_path: path to the output file.
    
    Outputs:
        for each patient note, the output file will start by a line declaring the note in the format of:
            Patient X Note Y
        then for every patient age found, it will have another line with the patient age.
        If patient age is not detected in the chunk, only the first line (Patient X Note Y) is printed to the output.
    Screen Display:
        Each patient's age detected will be displayed on the screen 
    
    """
    start_of_record_pattern = '^start_of_record=(\d+)\|\|\|\|(\d+)\|\|\|\|$'
    end_of_record_pattern = '\|\|\|\|END_OF_RECORD$'
    with open(output_path,'w+') as output_file:
        with open(text_path) as text:
            chunk = ''
            for line in text:
                record_start = re.findall(start_of_record_pattern,line,flags=re.IGNORECASE)
                if len(record_start):
                    patient, note = record_start[0]
                chunk += line

                record_end = re.findall(end_of_record_pattern, line,flags=re.IGNORECASE)
                if len(record_end):
                    check_for_age(patient,note,chunk.strip(), output_file)
                    chunk = ''
                    
if __name__== "__main__":
        
    
    
    deid_age(sys.argv[1], sys.argv[2]) 