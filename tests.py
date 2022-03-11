from unittest import mock

from magicgenerator import read_json, cf_multiprocessing, clear_path, create_file, generate_json_file_name
from unittest.mock import Mock
import pytest
import json
import os
import time

DATA_SCHEM_FORTEST = "{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": " \
                     "\"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 15)\"}"


@pytest.mark.parametrize("a, expected_result, expected_str",
                         [({'data_schema': "./schema.json"}, 100, 'partner'),
                          ({'data_schema': DATA_SCHEM_FORTEST}, 100, 'partner')])
def test_datatype(a, expected_result, expected_str):
    assert type(read_json(a)['age']) is type(expected_result)
    assert type(read_json(a)['date']) is type(expected_result)
    assert type(read_json(a)['name']) is type(expected_str)
    assert type(read_json(a)['type']) is type(expected_str)


def test_dataschema():
    with mock.patch('random.choice', mock.Mock(return_value='client')):
        assert "client" == read_json({'data_schema': "./schema.json"})['type']


def test_temporaryfiles(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "schema.json"
    m = Mock()
    print(m.main(p))


def test_clearpath():
    output = "./output"
    if not os.path.exists(output):
        os.makedirs(output)
    mydict = {"path_to_save_files": "./output", "file_name": "super_data777"}
    out = mydict["path_to_save_files"] + "/" + mydict["file_name"]
    with open(out, 'w', encoding="cp1251") as f:
        json.dump(mydict, f, ensure_ascii=False)
    clear_path(mydict)
    assert os.path.isfile(out) is False


def test_savedfiles():
    output = "./output"
    if not os.path.exists(output):
        os.makedirs(output)
    ll = {"path": "./output/super_data888", "json": "create file super_data888"}
    create_file(ll)
    assert os.path.isfile(ll["path"]) is True


def test_countfiles_multiprocessing():
    output = "./output"
    if not os.path.exists(output):
        os.makedirs(output)
    count_files = 10
    mydict = {"multiprocessing": 1, "data_schema": "./schema.json", "path_to_save_files": "./output",
              "file_name": "super_data999", "file_count": count_files, "prefix": "count"}
    cf_multiprocessing(mydict)
    i = 0
    for filename in os.listdir("./output"):
        if filename.startswith("super_data999"):
            i = i + 1
    assert i == count_files


def test_generate_json_file_name():
    # test generate json name for files
    i = 1
    prefix = "count"
    mydict = {"prefix": prefix, "path_to_save_files": "./output", "file_name": "test"}
    assert generate_json_file_name(mydict, i) == "./output/test_1.json"
