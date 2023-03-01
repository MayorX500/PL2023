#/usr/bin/env python3

import re


def read_file(filename:str, encoding:str='utf-8',mode:str='r') -> str:
    with open(filename,mode=mode,encoding=encoding) as f:
        return f.read()

def create_process(line:str,regular_expression:re.Pattern) -> dict:
    return match.groupdict() if (match := regular_expression.match(line)) else {}

def create_process_list(data:str,regular_expression:re.Pattern) -> list:
    return [create_process(line.strip(),regular_expression) for line in  data.splitlines()]

def clean_processes(process_list:list) -> list:
    processes:dict = {}
    for process in process_list:
        if process == {}:
            continue
        if process['pid'] not in processes:
            processes[process['pid']] = process
        else:
            if process['name'] != '':
                processes[process['pid']]['name'] = process['name']
            if process['father'] != '':
                processes[process['pid']]['father'] = process['father']
            if process['mother'] != '':
                processes[process['pid']]['mother'] = process['mother']
            if process['other'] != '':
                processes[process['pid']]['other'] = process['other']
    return list(sorted(processes.values(),key=lambda x: int(x['pid'])))

def main():

    #575::1894-11-08::Aarao Pereira Silva::Antonio Pereira Silva::Francisca Campos Silva::RandomStuff::
    #pid::year-month-day::name::father::mother::other::
    #pid must be unique
    regular_expression = re.compile(r'(?P<pid>\d+)::(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})::(?P<name>[a-zA-Z ]*)::(?P<father>[a-zA-Z ]*)::(?P<mother>.[a-zA-Z ]*)::(?P<other>.*)::')
    data = read_file('processos_small.txt')
    process_list = create_process_list(data,regular_expression)
    process_list = clean_processes(process_list)
    print(process_list)
    
if __name__ == '__main__':
    main()