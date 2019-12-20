# barcodescraper
scrapes barcode information from open ean database

 not for production use
- takes a vendor id and a barcode range
- retrieves data from https://opengtindb.org/
- reformats data to proper JSON
- strips useless data (e.g. formatting strings)
- converts number as strings to real numbers
- stores valid barcodes in valid.json
- stores invalid barcodes in invalid.json
- stores valid barcode and information as separate JSON file in folder "barcodes"
