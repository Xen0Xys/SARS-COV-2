import json
import os
import urllib.request
import io

#File index: GlobalData, PaysData
#PaysData index: Date, Oays, Infection, Deces, Guerisons, TauxDeces, TauxGuerison, TauxInfection

def getDataFile():
    # Get live info from french gouvernement data site
    print("[INFORMATION]: Updating 'all_data.json' file.")
    print("[INFORMATION]: Copying 'all_data.json' file in RAM.")
    try:
        with open("all_data.json", "r") as file:
            content = json.loads(file.read())
            file.close()
    except FileNotFoundError:
        pass
    print("[INFORMATION]: Removing 'all_data.json' file.")
    if os.path.exists("all_data.json"):
        os.remove("all_data.json")
    url = 'https://www.data.gouv.fr/fr/datasets/r/a7596877-d7c3-4da6-99c1-2f52d418e881'
    print("[INFORMATION]: Downloading 'all_data.json' file.")
    try:
        raise urllib.request.URLError("") #Line use to speed up launch time code or simulate no-wifi launch
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
        try:
            with open("all_data.json", "w") as file:
                file.write(json.dumps(content, indent=4))
                file.close()
            return 1
        except UnboundLocalError:
            os.remove("all_data.json")
            return 2
    return 0
    
def getData():
    # Get data file content
    print("[INFORMATION]: Getting data from all_data.json file.")
    with open("all_data.json", "r") as file:
        content = json.loads(file.read())
        file.close()
    return content

def getCountryData(_country_name):
    # Get data to all designated country from data file
    to_return = []
    content = getData()
    for current_dict in content["PaysData"]:
        if current_dict["Pays"] == _country_name:
            to_return.append(current_dict)
    to_return.reverse()
    return to_return

def getSpecifiedCountryData(_countries_list):
    # Get data to designated country from data file
    data_dict = {}
    content = getData()
    for country in _countries_list:
        if country == "Global":
            data_dict[country] = content["GlobalData"]
        else:
            data_dict[country] = getCountryData(country)
    return data_dict

def SaveDataAsFile(_data_result):
    # Save country data as file
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
    # Get country list from data file
    content = getData()
    country_list = []
    for data_dict in content["PaysData"]:
        if data_dict["Pays"] not in country_list:
            country_list.append(data_dict["Pays"])
    country_list.sort()
    return country_list

STATUS = getDataFile() # Status download code: 0 = OK; 1 = Download error; 2 = Copy error
if __name__ == "__main__":
    country_list = ["France", "Italie", "Global", "Espagne"]
    result = getSpecifiedCountryData(country_list)
    SaveDataAsFile(result)
    print(getCountryList())