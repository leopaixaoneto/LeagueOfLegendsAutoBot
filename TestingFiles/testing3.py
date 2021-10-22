import json

finalData = []

with open('./TestingFiles/champions.json') as json_file:
    data = json.load(json_file)
    count = 0
    match = None

    while(len(finalData) < len(data['champions'])):
        match = None
        for champ in data['champions']:
            if(int(champ['id']) == (count+1)):
                match = champ

        if(not match is None):
            finalData.append(match)
        count += 1

    print(finalData)
    print(len(finalData))
    print(len(data['champions']))
