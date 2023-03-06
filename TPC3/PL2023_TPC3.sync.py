#/usr/bin/env python3

import json
import re
from math import ceil

family:list[str] = ["avos","avo","avo","bisavo","bisavo","tataravo","tataravo","pais ","pai","mae","filhos ","filho","filha","netos","neto","neta","esposa","esposo","irmao","irma","irmaos","tio","tia","tios","primo","prima","primos","sobrinho","sobrinha","sobrinhos","sogro","sogra","sogros","cunhado","cunhada","cunhados","padrinho","madrinha","padrinhos","padrasto","madrasta","padrastros","meio irmao","meia irma","meio irmaos"]
years:dict = {}


def read_file(filename:str, encoding:str='utf-8',mode:str='r') -> str:
    with open(filename,mode=mode,encoding=encoding) as f:
        return f.read()

def create_process(line:str,regular_expression:re.Pattern) -> dict:
    return match.groupdict() if (match := regular_expression.match(line)) else None

def create_process_list(data:str,regular_expression:re.Pattern) -> list:
    return [create_process(line.strip(),regular_expression) for line in data.splitlines()]


def clean_processes(process_list:list) -> list:
    listing:list = []
    for process in process_list:
        if process is None:
            continue
        if process['name'] == '':
            continue
        if process['year'] == '':
            continue
        listing.append(process)
    return listing



def secular_match(processes:list[dict]) -> dict:
    sec:dict = {}
    for process in processes:
        year:str = process['year']
        if year not in years.keys():
            years[year] = 1
        else:
            years[year] += 1
        key:str = str(ceil(int(year)/100))
        name:str = process['name']
        person:dict = {'name':name.split(' ')[0],'last_name':name.split(' ')[-1]}
        if key not in sec.keys(): 
            sec[key] = {'last_name':{person['last_name']:1},'name':{person['name']:1}}
        else:
            if person['last_name'] not in sec[key]['last_name'].keys():
                sec[key]['last_name'][person['last_name']] = 1
            else:
                sec[key]['last_name'][person['last_name']] += 1
            if person['name'] not in sec[key]['name'].keys():
                sec[key]['name'][person['name']] = 1
            else:
                sec[key]['name'][person['name']] += 1

    for key in sec.keys():
        sec[key]['last_name'] = list(sorted(sec[key]['last_name'].items(),key=lambda x: x[1],reverse=True))
        sec[key]['name'] = list(sorted(sec[key]['name'].items(),key=lambda x: x[1],reverse=True))

        sec[key]['last_name'] = [f'{name} ({count})' for name,count in sec[key]['last_name']][:5]
        sec[key]['name'] = [f'{name} ({count})' for name,count in sec[key]['name']][:5]

    sec = {key:sec[key] for key in sorted(sec.keys())}

    return sec


def relationship_match(processes:list[dict]) -> dict:
    relation:dict = {}
    for process in processes:
        if process['other'] == '':
            continue
        matches:list = re.findall(r"(?=("+'|'.join(family)+r"))",process['other'])
        if len(matches) > 0:
            for match in matches:
                if match not in relation.keys():
                    relation[match] = 1
                else:
                    relation[match] += 1
    relation = list(sorted(relation.items(),key=lambda x: x[1],reverse=True))
    relation = [f'{name} ({count})' for name,count in relation]
    print(f'Family: {relation}')


def to_json(processes:list[dict]) -> str:
    output:str = json.dumps(processes[:20],indent=4,ensure_ascii=False)
    with open('processes.json','w',encoding='utf-8') as f:
        f.write(output)
    return output


def main():
    #575::1894-11-08::Aarao Pereira Silva::Antonio Pereira Silva::Francisca Campos Silva::RandomStuff::
    #pid::year-month-day::name::father::mother::other::
    regular_expression = re.compile(r'(?P<pid>\d+)::(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})::(?P<name>[a-zA-Z ]*)::(?P<father>[a-zA-Z ]*)::(?P<mother>.[a-zA-Z ]*)::(?P<other>.*)::')
    data = read_file('processos.txt')
    process_list = create_process_list(data,regular_expression)
    process_list = clean_processes(process_list)
    sec = secular_match(process_list)
    for key in years.keys():
        print(f'Year {key}: {years[key]}')
    print()
    for key in sec.keys():
        print(f'Century {key}')
        print(f'Last Names: {sec[key]["last_name"]}')
        print(f'Names: {sec[key]["name"]}')
    print()
    relationship_match(process_list)
    to_json(process_list)

if __name__ == '__main__':
    main()
