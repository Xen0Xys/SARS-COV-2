import json
import os
import urllib.request
import io

#File index: GlobalData, PaysData
#PaysData index: Date, Oays, Infection, Deces, Guerisons, TauxDeces, TauxGuerison, TauxInfection

def getDataFile():
    print("[INFORMATION]: Updating 'all_data.json' file.")
    print("[INFORMATION]: Copying 'all_data.json' file.")
    try:
        with open("all_data.json", "r") as file:
            content = json.loads(file.read())
            file.close()
    except:
        return 2
    print("[INFORMATION]: Removing 'all_data.json' file.")
    if os.path.exists("all_data.json"):
        os.remove("all_data.json")
    url = 'https://www.data.gouv.fr/fr/datasets/r/a7596877-d7c3-4da6-99c1-2f52d418e881'
    print("[INFORMATION]: Downloading 'all_data.json' file.")
    try:
        raise urllib.request.URLError("")
        urllib.request.urlretrieve(url, 'all_data.json')
        print("[INFORMATION]: Formatting 'all_data.json' file.")
        with io.open("all_data.json", "r", encoding="utf-8") as file:
            content = json.loads(file.read())
            file.close()
        with open("all_data.json", "w") as file:
            file.write(json.dumps(content, indent=4))
            file.close()
    except urllib.request.URLError:
        print("[ERROR]: URL unreachable, restorating data.")
        with open("all_data.json", "w") as file:
            file.write(json.dumps(content, indent=4))
            file.close()
        return 1
    return 0
    
    
def getData():
    print("[INFORMATION]: Getting data from all_data.json file.")
    with open("all_data.json", "r") as file:
        content = json.loads(file.read())
        file.close()
    return content

def getCountryData(_country_name):
    to_return = []
    content = getData()
    for current_dict in content["PaysData"]:
        if current_dict["Pays"] == _country_name:
            to_return.append(current_dict)
    to_return.reverse()
    return to_return

def getSpecifiedCountryData(_countries_list):
    data_dict = {}
    content = getData()
    for country in _countries_list:
        if country == "Global":
            data_dict[country] = content["GlobalData"]
        else:
            data_dict[country] = getCountryData(country)
    return data_dict

def SaveDataAsFile(_data_result):
    if os.path.exists("country_data"):
        file_list = os.listdir("country_data")
        for file in file_list:
            os.remove("country_data/{}".format(file))
    else:
        os.mkdir("country_data")
    for country in _data_result.keys():
        with open("country_data/{}.json".format(country), "w") as file:
            file.write(json.dumps(_data_result[country], indent=4))
            file.close()

def getCountryList():
    content = getData()
    country_list = []
    for data_dict in content["PaysData"]:
        if data_dict["Pays"] not in country_list:
            country_list.append(data_dict["Pays"])
    return country_list

STATUS = getDataFile()
if __name__ == "__main__":
    country_list = ["France", "Italie", "Global", "Espagne"]
    result = getSpecifiedCountryData(country_list)
    SaveDataAsFile(result)
    print(getCountryList())