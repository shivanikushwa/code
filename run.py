"""
-- Read a input_raw JSON file.
-- Processing Rules:
1. Name Correction: Any empty name fields should be filled with "Unknown".
2. Grade Validation: Convert all grade values to integers. If a conversion fails, set the grade to 0.
3. Metadata Consistency: Ensure the metadata object contains valid data:
   - The processed field should be a boolean.
   - The records field should be an integer. If it's not possible, set it to the count of items in the parent object.
4. Activity Members: For the extraActivities list, ensure each members array has at least one member. If empty, add a placeholder member with {"firstName": "None", "lastName": "None"}.
5. Library Book Availability: Replace any null or string values in available with a boolean. The string "yes" should translate to true; otherwise, false.
6. Empty Collections: If a collection like magazines is empty, add a placeholder object like {"placeholder": "empty"}.

-- Final output should be written to a file.
"""

import json
import string
import math
mapping = {
    "one" : 1,
    "two" : 2,
    "three" : 3,
    "four" : 4,
    "five" : 5,
    "six" : 6,
    "seven" : 7,
    "eight" : 8,
    "nine" : 9,
    "ten" : 10
}

def dictionaries(d, k):
    if (k == "magazines" and bool(d) == False):
        d["placeholder"] = "empty"

    for key in d:
        if (type(d[key]) == list):
            lists(d[key], key)
        elif (type(d[key]) == dict):
            dictionaries(d[key], key)

        if (key == "name" and d[key] == ""):
            d[key] = "Unknown"

        if (type(d[key]) != int and k == "grades"):
            n = d[key]
            if (type(n) == float):
                n = math.floor(n)
            else:
                n = int(n)
            d[key] = n

        if (key == "processed" and d[key] is not True):
            d[key] = True

        if (key == "records" and type(d[key]) != int):
            d[key] = mapping[d[key]]
 
        if (key == "available" and d[key] != "yes"):
            d[key] == False

        if (key == "available" and d[key] == "yes"):
            d[key] = True
        
def lists(l, k): 
    if (k == "members" and len(l) == 0):
        d = {"firstname" : "none", "lastname" : "none"}
        l.append(d)

    for x in l:
        if (type(x) == list):
            lists(x, k)
        elif (type(x) == dict):
            dictionaries(x, k)


file = open("input_raw.json", "r")
x = file.read()
data = json.loads(x)
k = "null"
if (type(data) == list):
    lists(data, k)
else:
    dictionaries(data, k)

print(json.dumps(data, indent=2))

with open("output.json", "w") as file:
    json.dump(data, file, indent=2)
