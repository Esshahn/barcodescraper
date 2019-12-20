#
# OPEN EAN GTIN Database scraper script
# 
# not for production use
# takes a vendor id and a barcode range
# retrieves data from https://opengtindb.org/
# reformats data to proper JSON
# strips useless data (e.g. formatting strings)
# converts number as strings to real numbers
# stores valid barcodes in valid.json
# stores invalid barcodes in invalid.json
# stores valid barcode and information as separate JSON file in folder "barcodes"


import json, requests, os, sys

def get_as_dict(ean,user_id):

    link = f'http://opengtindb.org/?ean={ean}&cmd=query&queryid={user_id}'
    f = requests.get(link).text.splitlines()
    lines = {"barcode": ean}

    for i in f:
        if "=" in i:
            line = i.split("=")
            
            try:
                value = int(line[1])
            except ValueError:
                value = line[1]
            
            lines[line[0]] = value

    return lines



def load_JSON_as_dict(filename):
    # load JSON

    with open(sys.path[0] + '/' + filename, "a+") as json_file:
        try:
            json_data =  json.load(json_file)
        except ValueError:
            json_data = "{}"
    
    return json.loads(json_data)



def write_as_json_file(dict):
    filename = "barcodes/" + str(dict["barcode"]) + ".json"
    with open(filename, 'w') as json_file:
        json.dump(dict, json_file)



def update_file(filename, dict):
    with open(filename, 'w') as json_file:
        json.dump(dict, json_file)



def scraper(start, amount, vendor_id, user_id):

    barcodes_valid = load_JSON_as_dict("valid.json")
    barcodes_invalid = load_JSON_as_dict("invalid.json")

    for id in range(start,start+amount):
        vendor = vendor_id * 10000000 # REWE
        barcode = get_as_dict(vendor + id, user_id)
        
        print (barcode)
        
        if barcode["error"] is 0:
            write_as_json_file(barcode)
            barcodes_valid.update( {barcode["barcode"] : barcode["error"]} )
        else:
            barcodes_invalid.update( {barcode["barcode"] : barcode["error"]} )

    update_file("valid.json",barcodes_valid)
    update_file("invalid.json",barcodes_invalid)



## -------------- main -------------- ##

vendors = {"REWE": 438884}
user_id = 765690123382645678008

scraper(4014862+5, 4, vendors["REWE"], user_id)



