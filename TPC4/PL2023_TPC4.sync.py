#!/usr/bin/env python3

import json
import re
import numpy as np


def to_json(path:str ,data:list[dict]) -> str:
    output:str = json.dumps(data,indent=4,ensure_ascii=False)
    with open(path,'w',encoding='utf-8') as f:
        f.write(output)
    return output

def from_json(path:str) -> list[dict]:
    output:list[dict] = []
    with open(path,'r',encoding='utf-8') as f:
        output = json.load(f)
    return output

def create_header(line:str) -> list[dict]:
    header_list:list[str] = re.split(r',\s*(?![^{}]*\})', line)[:3]
    grades_group:tuple = None
    try:
        grades_group = re.search(r'{(?P<min>\d*),?(?P<max>\d*)}', line).groupdict()
        functions = re.findall(r'::[a-zA-Z]*', line)
        functions = [function[2:] for function in functions]
        if grades_group['max'] == '':
            grades_group['max'] = grades_group['min']
        grades_group['function'] = functions
        n_grades:list = [f"Nota_{i}" for i in range(1,int(grades_group['max'])+1)]
        n_grades += grades_group['function']
        header_list += n_grades
    except AttributeError as none:
        # print(none)
        pass
    return header_list


def from_csv(path:str) -> list[dict]:
    output:list[dict] = []
    functions:bool = True
    with open(path,'r',encoding='utf-8') as f:
        header:list[dict] = create_header(f.readline().strip())
        for line in f:
            output.append(dict(zip(header,re.split(r',\s*(?![^{}]*\})', line.strip()))))
        for student in output:
            if len(student.keys()) > 3:
                functions = False
            student['Notas'] = []
            for key in header:
                if key not in student.keys():
                    student[key] = None
                if key.startswith('Nota_'):
                    student['Notas'].append(int(student[key])) if student[key] != '' else None
                    student.pop(key)

    remove_list:bool = False
    for func in header:
        match func:
            case 'nothing':
                for student in output:
                    student.pop('nothing')
            case 'sum':
                remove_list = True
                for student in output:
                    student['Notas_sum'] = sum(student['Notas'])
                    student.pop('sum')
            case 'media':
                remove_list = True
                for student in output:
                    student['Notas_media'] = sum(student['Notas'])/len(student['Notas'])
                    student.pop('media')
            case 'max':
                remove_list = True
                for student in output:
                    student['Notas_max'] = max(student['Notas'])
                    student.pop('max')
            case 'min':
                remove_list = True
                for student in output:
                    student['Notas_min'] = min(student['Notas'])
                    student.pop('min')
            case 'std':
                remove_list = True
                for student in output:
                    student['Notas_std'] = np.std(student['Notas'])
                    student.pop('std')
            case _:
                pass

    try:
        if functions or remove_list:
            for student in output:
                student.pop('Notas')
    except KeyError as none:
        # print(none)
        pass

    return output


def main():
    try:
        for i in range(1,100):
            to_json(f'alunos{i}.json',from_csv(f'alunos{i}.csv'))
    except FileNotFoundError as none:
        #print(none)
        pass

if __name__ == '__main__':
    main()
