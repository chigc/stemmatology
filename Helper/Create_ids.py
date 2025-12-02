import requests
import xml.etree.ElementTree as ET
import csv

# Query the XML data
url = "https://gams-staging.uni-graz.at/archive/objects/query:chigc.ms-datatable/methods/sdef:Query/getXML"
response = requests.get(url)
response.raise_for_status()

# Parse XML
root = ET.fromstring(response.content)
print("XML data fetched and parsed successfully")
print(f"Root tag: {root.tag}")
print(f"Root attributes: {root.attrib}")

# Detect namespace from root tag if present
namespaces = {}
if '}' in root.tag:
    namespace = root.tag.split('}')[0].strip('{')
    namespaces = {'ns': namespace}
    print(f"Detected namespace: {namespace}")
else:
    namespaces = {"ns": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}

# Try to find result elements
print("\nSearching for result elements...")
results = root.findall('.//result')  # Try without namespace first

if not results and namespaces:
    # Try with namespace
    results = root.findall('.//ns:result', namespaces)

if not results:
    # Try other common patterns
    for pattern in ['./ns:results/ns:result', './/ns:result', './results/result', './/result']:
        try:
            if 'ns:' in pattern and namespaces:
                results = root.findall(pattern, namespaces)
            else:
                results = root.findall(pattern.replace('ns:', ''))
            if results:
                print(f"Found {len(results)} results using pattern: {pattern}")
                break
        except Exception as e:
            continue

print(f"Found {len(results)} result elements")

# Extract data from XML
rows = []
IDlist = []
def century_from_year(year):
    return (year - 1) // 100 + 1
for item in results:
    row_data = {}

    for child in item:
        # Remove namespace from tag name
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        row_data[tag] = child.text
    if row_data:
        rows.append(row_data)
    notafter = row_data.get("notafter")
    if notafter is None or notafter == "":
        notafter = row_data.get("notbefore", "N/A")
    newID = [row_data.get("sigla", "N/A"),row_data.get("graphversion", "N/A"), row_data.get("msgroup", "N/A"),notafter] 
    IDlist.append(newID)   

IDlistclean = []
for ID in IDlist:
    print(ID)
    IDentry = str(ID[0]) + "_" + str(ID[1]).replace("None", "0") + "_" + str(ID[2]).replace("None", "0") + "_" + str(century_from_year(int(ID[3])))
    print(IDentry)
    IDlistclean.append(IDentry)
# Write to CSV
with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["first_part", "full_string"])  # header
    
    for item in IDlistclean:
        first_part = item.split("_", 1)[0]  # split only at first "_"
        writer.writerow([first_part, item])