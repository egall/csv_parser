import sys, os

CSV_DIR="/home/egall/scratch/csvs"

"""
process_line() -- processes each line of the input file and writes the result in output file
inputs:
        filename - full path of file being read
        fume_cd - the code for the fumigation method used
        prodno_list - list of pesticide product numbers for this file/dataset
        acres_treated_list - the list of acres treated (row idx in the csv)
        line - the line of the input file we are processing
        results_fp - pointer to file where results will be stored
outputs:
        None
"""
def process_line(filename, fume_cd, prodno_list, acres_treated_list, line, results_fp):
    # tokenize the line by splitting on commas
    buffer_dist_ft = line.split(',')
    # gpa is gallons per acre
    gpa = buffer_dist_ft.pop(0)
    # idx will be used to index into the column values to get the appropriate buffer distance
    idx = 0
    # Run through each column in the row
    for acres_treated in acres_treated_list:
        if (idx >= len(buffer_dist_ft)):
            print("Something funny in {0}, stopping reading at index {1} of gallons per acre row {2}".format(filename, idx, gpa))
            continue
        buff_dist = buffer_dist_ft[idx]
        idx += 1
        # Since we need an entry for each prodno we loop through here
        for prodno in prodno_list:
            wrline = "{0},{1},{2},{3},{4}\n".format(prodno, fume_cd, gpa, acres_treated, buff_dist)
            results_fp.write(bytes(wrline, 'UTF-8'))
    
    


"""
read_file() -- reads in a file line by line and processes info
inputs:  
        filename - full path of file to read
        results_fp - pointer to file where results will be stored
outputs: 
         None
"""
def read_file(filename, results_fp):
    line_count = 0
    fume_cd = ""
    prodno_list = []
    acres_treated_list = []
    with open(filename, "r+") as fp:
        for line in fp:
            # strip off newline
            line = line.rstrip()
            # first line is fume_cd
            if (line_count == 0):
                if not line.isdigit():
                    print("WARNING: Read invalid fume_cd", line)
                else:
                    fume_cd = line
            # second line is the list of product numbers
            elif (line_count == 1):
                prodno_list = line.split('\t')
            # third line is the column values (acres treated)
            elif (line_count == 2):
                acres_treated_list = line.split(',')
            else:
                process_line(filename, fume_cd, prodno_list, acres_treated_list, line, results_fp)
            line_count += 1
    
    

"""
open_dir() -- collects all of the files in a directory
inputs:
        dirname - full path to dir
        results_fp - pointer to file where results will be stored
outputs:
        None
"""
def open_dir(dirname, results_fp):
    # enumerate through each file in dir
    for filename in os.listdir(dirname):
        # don't need to process hidden files
        if (filename[0] != '.'):
            full_file_path = dirname + '/' + filename
            read_file(full_file_path, results_fp)

"""
init_csv_parse() -- opens and closes csv file to write, calls open_dir() which handles .csv parsing
inputs:
        dirname - Full path to directory
outputs:
        None
"""
def init_csv_parse(dirname):
    results_fp = open("results.csv", "wb+")
    open_dir(dirname, results_fp)
    results_fp.close()
        
    

if __name__ == "__main__":
    init_csv_parse(CSV_DIR)
