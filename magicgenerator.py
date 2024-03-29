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
# python3 magicgenerator.py -h


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
    print("params input:" + str(vars(args)))
    return vars(args)


def read_json(path):
    # print("path:" + path)
    pp = str(path)
    if pp.startswith("{"):
        json1_str = pp
    if pp.startswith("."):
        with open(pp, 'r', encoding="CP1251") as f:
            json1_str = f.read()
    json1_data = json.loads(json1_str)
    output = {}
    for i in json1_data:
        # type timestamp, str and int.
        if json1_data[i].startswith('timestamp'):
            if json1_data[i].startswith('timestamp'):
                output.update({i: int(time.time())})
            if json1_data[i].startswith('timestamp:r'):
                print("error: timestamp:rand()")
                exit(1)
        if json1_data[i].startswith("str:"):
            if json1_data[i].startswith('str:'):
                output.update({i: re.sub('str:', '', (json1_data[i]))})
            if json1_data[i].startswith('str:rand('):
                print("error: str:rand()")
                exit(1)
            if json1_data[i] == 'str:rand':
                output.update({i: generate_name()})
            if json1_data[i].startswith("str:["):
                output.update({i: random.choice(eval(re.sub('str:', '', (json1_data[i]))))})

        if json1_data[i].startswith("int:"):
            if json1_data[i].startswith("int:rand("):
                out = (re.sub('[int:rand(),]', '', json1_data['age']))
                out = out.split()
                out = random.randint(int(out[0]), int(out[1]))
                output.update({i: out})
            elif json1_data[i] == 'int:rand':
                output.update({i: random.randint(0, 10000)})
            elif json1_data[i] == 'int:':
                output.update({i: None})
            else:
                print("error: int rand or rand(1,20),could not be converted to int type")
                exit(1)

    print("generate string for json file" + str(output))
    return output


def generate_name():
    output = str(uuid.uuid4())
    print("generate uuid for json file:" + output)
    return output


def generate_json_file_name(paths, filename, prefix, i):
    complete_name = None
    if prefix == "count":
        complete_name = os.path.join(paths, filename + "_" + str(i) + ".json")
    if prefix == "random":
        complete_name = os.path.join(
            paths, filename + "_" + (
                ''.join(random.choice(string.digits) for _ in range(4))) + ".json")
    if prefix == "uuid":
        complete_name = os.path.join(
            paths, filename + "_" + str(uuid.uuid4()) + ".json")
    return complete_name


def create_file(com):
    out = (str(com["path"]).replace('[', '').replace(']', '').replace('\'', ''))
    print("create file:" + out)
    print("with json data:" + str(com["json"]))
    with open(out, 'w') as f:
        json.dump(com["json"], f, ensure_ascii=False)


def clear_path(paths, filenames):
    for filename in os.listdir(paths):
        if filename.startswith(filenames):
            os.remove(os.path.join(paths, filename))
            print("file removed:" + os.path.join(paths, filename))


def cf_multiprocessing(filecount, path, filename, prefix, dataschema, multiprocessing):
    ll = {"path": [], "json": []}
    i = 0
    outdict = []
    while i < filecount:
        ll["path"].append(
            generate_json_file_name(path, filename, prefix, i))
        ll["json"].append(read_json(dataschema))
        outdict.append(ll)
        i = i + 1
        ll = {"path": [], "json": []}
    if multiprocessing < 0:
        exit(1)
    if multiprocessing <= os.cpu_count():
        print("multiprocessing=" + str(multiprocessing))
        with Pool(multiprocessing) as p:
            p.map(create_file, outdict)
    if multiprocessing > os.cpu_count():
        print("multiprocessing=" + str(multiprocessing))
        with Pool(os.cpu_count()) as p:
            p.map(create_file, outdict)


def main():
    pars = argparse.ArgumentParser(prog='Console Utility (CU)')
    input_param = print_name_address(pars)
    path = input_param["path_to_save_files"]
    filename = input_param["file_name"]
    clearpath = input_param["clear_path"]
    filecount = input_param["file_count"]
    prefix = input_param["prefix"]
    dataschema = input_param['data_schema']
    multiprocessing = input_param["multiprocessing"]
    print(input_param)
    if not os.path.exists(path):
        os.makedirs(path)
    if clearpath is True:
        clear_path(path, filename)
    cf_multiprocessing(filecount, path, filename, prefix, dataschema, multiprocessing)


if __name__ == '__main__':
    main()
