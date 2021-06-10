import json
import requests
from intersight_auth import IntersightAuth

def getRecommendedDriver(Status,InvModel,InvOsVendor,HclOsVersion,InvFirmwareVersion,components,InvProcessor):
    print("Current HCL Status: " + Status)
    print("Current Operating System: " + HclOsVersion )
    print("Current Firmware Version: " + InvFirmwareVersion)
    print("Current Model: " + InvModel)

    componentList = []
    hclComponentInfo = ""

    for fields in components:
        componentList.append([fields[0],fields[1],fields[2],fields[3],fields[4]])
        hclComponentInfo = hclComponentInfo + "{\"Firmwares\":[{\"FirmwareVersion\":\"" + fields[1] + "\"}],\"Model\":\"" + fields[0] + "\"},"

    # Strip off trailing "," from the above loop to avoid breaking JSON format
    hclComponentInfo = hclComponentInfo[:-1]

    ProfileList = "{\"ProfileList\":[{\"OsVendor\":\"" + InvOsVendor + "\",\"OsVersion\":\"" + HclOsVersion + "\",\"ProcessorModel\":\"" + InvProcessor + "\"," \
                      "\"UcsVersion\":\"" + InvFirmwareVersion + "\",\"ServerModel\":\"" + InvModel + "\",\"Products\":[" + hclComponentInfo + "]}]" \
                      ",\"RequestType\":\"GetRecommendedDrivers\"}"

    resource_path = "https://intersight.com/api/v1/hcl/CompatibilityStatuses"

    RESPONSE = requests.post(resource_path,ProfileList,auth=AUTH)

    compatabilityStatuses = RESPONSE.json()["ProfileList"]

    HCLList = []

    for s in compatabilityStatuses:
        for t in (s["Products"]):
            for q in (t["Firmwares"]):
                HCLList.append([q["DriverName"],q["DriverVersion"]])

    #Remove duplicate driver names & version from HCLList
    cleanup = []
    [cleanup.append(x) for x in HCLList if x not in cleanup]
    HCLList = cleanup

    for field in componentList:
        if "Incompatible-Driver" in field[4]:
            print("\n")
            print("Component Status: " + field[4])
            print("Model: " + field[0])
            print("Firmware: " + field[1])
            print("Driver Name: " + field[3])
            print("Current Incompatible Driver Version: " + field[2])
            print("Supported Driver Versions: ")
            for drivers in HCLList:
                if field[3] in drivers:
                    print(drivers[1])

def getComponents(link):
    json_body = {
        "request_method": "GET",
        "resource_path": link
    }

    RESPONSE = requests.request(
        method=json_body['request_method'],
        url=json_body['resource_path'],
        auth=AUTH
    )

    affectedDevice = RESPONSE.json()
    return [affectedDevice['InvModel'], affectedDevice['InvFirmwareVersion'],affectedDevice['InvDriverVersion'],affectedDevice['InvDriverName'],affectedDevice['SoftwareStatus']]


def getHCLStatus():
    components = []
    serverMOID = '60b663a876752d3132542179'

    json_body = {
        "request_method": "GET",
        "resource_path": (
                'https://intersight.com/api/v1/cond/HclStatuses?$filter=(ManagedObject.Moid%20eq%20%27' + serverMOID + '%27)'
        )
    }

    RESPONSE = requests.request(
        method=json_body['request_method'],
        url=json_body['resource_path'],
        auth=AUTH
    )

    hclStatuses = RESPONSE.json()["Results"]

    for r in hclStatuses:
        try:
           Status = r['Status']
           InvModel = r['InvModel']
           InvOsVendor = r['InvOsVendor']
           HclOsVersion = r['HclOsVersion']
           InvProcessor = r['InvProcessor']
           InvFirmwareVersion = r['InvFirmwareVersion']
           for s in r['Details']:
               components.append(getComponents(s['link']))
        except:
           print("")

    getRecommendedDriver(Status,InvModel,InvOsVendor,HclOsVersion,InvFirmwareVersion,components,InvProcessor)

#Configure Intersight API token and start finding all devices affected by a security advisory        
AUTH = IntersightAuth(
    secret_key_filename='SecretKey.txt',
    api_key_id='x/y/z'
    )

getHCLStatus()