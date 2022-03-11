import argparse
import json
import random
import re
import string
import time
import os
import configparser
import uuid
from multiprocessing import Pool



# help
# python magicgenerator.py -h


def print_name_address(parser: argparse.Namespace) -> dict:
    config = configparser.ConfigParser()
    config.read('default.ini')
    config.sections()
    default = config['DEFAULT']
    parser.add_argument('--path_to_save_files', nargs='?', const=str('./output'),
                        type=str,
                        default=str('./output'),
                        help='Where all files need to save')
    parser.add_argument('--clear_path', action='store_true', default=False,
                        help='If this flag is on, before the script starts creating new data files, '
                             'all files in path_to_save_files that match file_name will be deleted.')
    parser.add_argument('--file_count', nargs='?', const=int((default["file_count"])), type=int,
                        default=int((default["file_count"])),
                        help='How much json files to generate')
    parser.add_argument('--file_name', nargs='?', const=(default["file_name"]), type=str,
                        default=(default["file_name"]),
                        help='Base file_name. If there is no prefix, the final file name will be file_name.json. '
                             'With prefix full file name will be file_name_file_prefix.json')
    parser.add_argument('--prefix', nargs='?', const=(default["prefix"]), choices=['count', 'random', 'uuid'],
                        default=(default["prefix"]),
                        help='What prefix for file name to use if more than 1 file needs to be generated')
    parser.add_argument('--multiprocessing', nargs='?', const=int((default["multiprocessing"])), type=int,
                        default=1,
                        help='The number of processes used to create files. '
                             'Divides the “files_count” value equally and starts '
                             'N processes to create an equal number of files in parallel. '
                             'Optional argument. Default value: 1.')
    parser.add_argument('--data_schema', nargs='?', const=str(default["data_schema"]), type=str,
                        default=str(default["data_schema"]),
                        help='It’s a string with json schema.It could be loaded in two ways:1) '
                             'With path to json file with schema 2) with schema entered to command line. '
                             'Data Schema must support all protocols that are described in “Data Schema Parse”')
    args = parser.parse_args()
    mydict = vars(args)
    print("params input:" + str(mydict))
    return mydict


def read_json(path):
    pp = str(path['data_schema'])
    if pp.startswith("{"):
        json1_str = pp
    if pp.startswith("."):
        with open(pp, 'r', encoding="CP1251") as f:
            json1_str = f.read()
    json1_data = json.loads(json1_str)
    timestamp = int(time.time())
    jsontype = random.choice(json1_data["type"])
    age = (re.sub('[int:rand(),]', '', json1_data['age']))
    age = age.split()
    age = random.randint(int(age[0]), int(age[1]))
    output = {"date": timestamp, "name": generate_name(), "type": jsontype, "age": age}
    print("generate string for json file" + str(output))
    return output


def generate_name():
    output = str(uuid.uuid4())
    print("generate uuid for json file:" + output)
    return output


def generate_json_file_name(mydict, i):
    complete_name = None
    if mydict["prefix"] == "count":
        complete_name = os.path.join(mydict["path_to_save_files"] + "/" + mydict["file_name"] + "_" + str(i) + ".json")
    if mydict["prefix"] == "random":
        complete_name = os.path.join(
            mydict["path_to_save_files"] + "/" + mydict["file_name"] + "_" + (
                ''.join(random.choice(string.digits) for _ in range(4))) + ".json")
    if mydict["prefix"] == "uuid":
        complete_name = os.path.join(
            mydict["path_to_save_files"] + "/" + mydict["file_name"] + "_" + str(uuid.uuid4()) + ".json")
    return complete_name


def create_file(com):
    out = (str(com["path"]).replace('[', '').replace(']', '').replace('\'', ''))
    print("create file:" + out)
    print("with json data:" + str(com["json"]))
    with open(out, 'w') as f:
        json.dump(com["json"], f, ensure_ascii=False)


def generate_json_output(mydict):
    return read_json(mydict)


def clear_path(mydict):
    for filename in os.listdir(mydict["path_to_save_files"]):
        if filename.startswith(mydict["file_name"]):
            os.remove(mydict["path_to_save_files"] + "/" + filename)
            print("file removed:" + mydict["path_to_save_files"] + "/" + filename)


def cf_multiprocessing(mydict):
    ll = {"path": [], "json": []}
    i = 0
    outdict = []
    while i < mydict["file_count"]:
        ll["path"].append(generate_json_file_name(mydict, i))
        ll["json"].append(read_json(mydict))
        outdict.append(ll)
        i = i + 1
        ll = {"path": [], "json": []}
    if mydict["multiprocessing"] < 0:
        exit(1)
    if mydict["multiprocessing"] <= os.cpu_count():
        print("multiprocessing=" + str(mydict["multiprocessing"]))
        with Pool(mydict["multiprocessing"]) as p:
            p.map(create_file, outdict)
    if mydict["multiprocessing"] > os.cpu_count():
        print("multiprocessing=" + str(mydict["multiprocessing"]))
        with Pool(os.cpu_count()) as p:
            p.map(create_file, outdict)


def main():
    pars = argparse.ArgumentParser(prog='Console Utility (CU)')
    mydict = print_name_address(pars)
    print(mydict)
    if not os.path.exists(mydict["path_to_save_files"]):
        os.makedirs(mydict["path_to_save_files"])
    if mydict["clear_path"] is True:
        clear_path(mydict)
    cf_multiprocessing(mydict)


if __name__ == '__main__':
    main()
