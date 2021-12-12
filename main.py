import requests
from datetime import datetime


def getSLP(roninAdd):
    response = requests.get("https://game-api.axie.technology/slp/" + roninAdd)
    return response.json()


if __name__ == '__main__':
    roninAdd = "ronin:71dd7cb6743b94b5bffc2a6d43ccdb6d6dd98912"
    jsonFile = getSLP(roninAdd)

    claimable = jsonFile[0]["claimable_total"]
    total = jsonFile[0]["total"]
    lastDateClaimed = jsonFile[0]["last_claimed_item_at"]  # in UNIX timecode

    lastDateDatetime = datetime.fromtimestamp(lastDateClaimed)
    todayDatetime = datetime.now()
    difference = todayDatetime-lastDateDatetime
    print(difference.days, "days")
    lastDateUpdate = jsonFile[0]["update_time"]  # in UNIX timecode
    lastDateUpdate /= 1000
    print("Total Claimable: " + str(claimable))
    print("Total: " + str(total))
    print("Last Date Claimed: " + datetime.utcfromtimestamp(lastDateClaimed).strftime('%Y-%m-%d %H:%M:%S'))
    print("Last Date Site Refreshed: " + datetime.utcfromtimestamp(lastDateUpdate).strftime('%Y-%m-%d %H:%M:%S'))
