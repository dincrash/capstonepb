import os
import pathlib
import ruamel.yaml
from pathlib import Path

def remover(p):
    if os.path.exists(p):
        path = pathlib.Path(p)
        path.unlink()

def finder3000():
    export = []
    for path in Path('2').rglob('*.yaml'):
        w1 = 'resource'
        w2 = 'price'
        w3 = '-rs'
        if not w1 in path.name:
            if not w2 in path.name:
                if not w3 in path.name:
                    with open(path, 'r', encoding="utf8") as f:
                        yaml = ruamel.yaml.YAML()
                        out = yaml.load(f)
                    if out:
                        out2 = out['ProductOffering']
                        for element in out2:
                            if 'ARCHIVAL' in element['offerType']:
                                export.append(element['externalId'])
                                export.append(element['code'])
                                print(f'{export}', file=open('1.txt', 'a'))
                                export = []
                            if not 'ARCHIVAL' in element['offerType']:
                                export.append(element['externalId'])
                                export.append(element['code'])
                                print(f'{export}', file=open('2.txt', 'a'))
                                export = []

remover('1.txt')
remover('2.txt')
finder3000()
