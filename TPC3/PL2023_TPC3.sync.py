#/usr/bin/env python3

import re
from math import ceil


def read_file(filename:str, encoding:str='utf-8',mode:str='r') -> str:
    with open(filename,mode=mode,encoding=encoding) as f:
        return f.read()

def create_process(line:str,regular_expression:re.Pattern) -> dict:
    return match.groupdict() if (match := regular_expression.match(line)) else None

def create_process_list(data:str,regular_expression:re.Pattern) -> list:
    return [create_process(line.strip(),regular_expression) for line in data.splitlines() if create_process(line.strip(),regular_expression) != None ]

def clean_processes(process_list:list) -> list:
    processes:dict = {}
    for process in process_list:
        if process['pid'] not in processes.keys():
            processes[process['pid']] = process
        else:
            for key,value in process.items():
                if value != '':
                    processes[process['pid']][key] = value
    return list(sorted(processes.values(),key=lambda x: int(x['pid'])))

def secular_match(processes:list[dict]) -> dict:
    sec:dict = {}
    for process in processes:
        key:str = str(ceil(int(process['year'])/100))
        name:str = process['name']
        person:dict = re.match(r'^(?P<name>[a-zA-Z]*).* (?P<last_name>[a-zA-Z]*)$',name).groupdict()
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

    return sec

def main():
    #575::1894-11-08::Aarao Pereira Silva::Antonio Pereira Silva::Francisca Campos Silva::RandomStuff::
    #pid::year-month-day::name::father::mother::other::
    #pid must be unique, if not, missing data will be overwritten by the last one
    regular_expression = re.compile(r'(?P<pid>\d+)::(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})::(?P<name>[a-zA-Z ]*)::(?P<father>[a-zA-Z ]*)::(?P<mother>.[a-zA-Z ]*)::(?P<other>.*)::')
    data = read_file('processos.txt')
    process_list = create_process_list(data,regular_expression)
    process_list = clean_processes(process_list)
    sec = secular_match(process_list)
    for key in sec.keys():
        print(f'Century {key}')
        print(f'Last Names: {sec[key]["last_name"]}')
        print(f'Names: {sec[key]["name"]}')

if __name__ == '__main__':
    main()
