# deid-ElSayed.py include patient age de-identification 
# deid.py was editied to run multiple de-identification catagories for now the phone de-identification and age de-identification.
# The phone de-ide code was moved to different script under the title ClassPhone. The patient age de-id script is under the title of ClassAge and the new deid code is called deidclass.py

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


def deid_age(text_path= 'id.text', output_path = 'age.phi'):
    """
    Inputs: 
        - text_path: path to the file containing patient records
        - output_path: path to the output file.
    
    Outputs:
        for each patient note, the output file will start by a line declaring the note in the format of:
            Patient X Note Y
        then for each phone number found, it will have another line in the format of:
            start start end
        where the start is the start position of the detected phone number string, and end is the detected
        end position of the string both relative to the start of the patient note.
        If there is no phone number detected in the patient note, only the first line (Patient X Note Y) is printed
        to the output
    Screen Display:
        For each phone number detected, the following information will be displayed on the screen for debugging purposes 
        (these will not be written to the output file):
            start end phone_number
        where `start` is the start position of the detected phone number string, and `end` is the detected end position of the string
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
                    # pass all to check_for_phone to find any phone numbers in note.
                    check_for_age(patient,note,chunk.strip(), output_file)
                    
                    # initialize the chunk for the next note to be read
                    chunk = ''
                
if __name__== "__main__":
    
    deid_age(sys.argv[1], sys.argv[2])