# capstonepb
console utility based on argparse
help command
magicgenerator.py -h

create json data based on input parameters, with pytest and unittest(mock)
parammeters

--path_to_save_files Where all files need to save

--clear_path If this flag is on, before the script starts creating new data files all files in path_to_save_files that match file_name will be deleted

--file_count How much json files to generate

--file_name Base file_name. If there is no prefix, the final file name will be file_name.json. With prefix full file name will be file_name_file_prefix.json

--prefix What prefix for file name to use if more than 1 file needs to be generated

--multiprocessing The number of processes used to create files. Divides the “files_count” value equally and starts N processes to create an equal number of files in parallel. Optional argument. Default value: 1.

--data_schema It’s a string with json schema.It could be loaded in two ways:
1) With path to json file with schema 
2) With schema entered to command line. Data Schema must support all protocols that are described in “Data Schema Parse”')

magicgenerator.py --file_count=20 --multiprocessing=2
