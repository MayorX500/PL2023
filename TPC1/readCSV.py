import math

dataset:list[dict] = []

data:dict = {
        "info":{
            "total":0,
            "sick":{
                "total":0,
                "F":0,
                "M":0
            },
            "not_sick":{
                "total":0,
                "F":0,
                "M":0
                }
            }
        }

def read_dataset(filename) -> list[dict]:
    with open(filename, 'r') as f:
        header:list[str] = f.readline().strip().split(',')
        for line in f:
            line = line.strip().split(',')
            dataset.append({header[i]: line[i] for i in range(len(header))})
    data["info"]["total"] = len(dataset)
    return dataset


def dist_by_gender() -> dict:
    sick_dataset = [data for data in dataset if data["temDoença"] == "1"]
    not_sick_dataset = [data for data in dataset if data["temDoença"] == "0"]

    data["info"]["sick"]["total"] = len(sick_dataset)
    data["info"]["not_sick"]["total"] = len(not_sick_dataset)
    data["info"]["sick"]["F"] = len([data for data in sick_dataset if data["sexo"] == "F"])
    data["info"]["not_sick"]["F"] = len([data for data in not_sick_dataset if data["sexo"] == "F"])
    data["info"]["sick"]["M"] = len([data for data in sick_dataset if data["sexo"] == "M"])
    data["info"]["not_sick"]["M"] = len([data for data in not_sick_dataset if data["sexo"] == "M"])
    return data

def ratio_gender() -> dict:
    ratios = {}
    ratios["sick.total"] = round(data["info"]["sick"]["total"] / data["info"]["total"] * 100 ,2)
    ratios["sick.M.total"] = round(data["info"]["sick"]["M"] / data["info"]["total"] * 100 ,2)
    ratios["sick.F.sick"] = round(data["info"]["sick"]["F"] / data["info"]["sick"]["total"] * 100 ,2)
    ratios["sick.M.sick"] = round(data["info"]["sick"]["M"] / data["info"]["sick"]["total"] * 100 ,2)
    ratios["not_sick.total"] = round(data["info"]["not_sick"]["total"] / data["info"]["total"] * 100 ,2)
    ratios["not_sick.M.total"] = round(data["info"]["not_sick"]["M"] / data["info"]["total"] * 100 ,2)
    ratios["not_sick.F.not_sick"] = round(data["info"]["not_sick"]["F"] / data["info"]["not_sick"]["total"] * 100 ,2)
    ratios["not_sick.M.not_sick"] = round(data["info"]["not_sick"]["M"] / data["info"]["not_sick"]["total"] * 100 ,2)
    return ratios

def dist_by_age() -> dict:
    data["info"]["sick"]["age"] = {}

def main():
    global dataset
    read_dataset('PL2023_TPC1.csv')
    dist_by_gender()
    print(ratio_gender())
    print(data)

if __name__ == '__main__':
    main()
