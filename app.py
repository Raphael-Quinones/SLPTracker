from flask import Flask, render_template, request
from main import getSLP
from datetime import datetime

app = Flask(__name__)

summary = []  # store data from each address
addresses = [] # check if address's already there to avoid duplicates
@app.route("/",methods=["POST", "GET"])
def home():
    headings = ("Name", "Total SLP", "Last Claimed", "Date Refreshed")
    name = request.form["name"]
    address = request.form["ronin_add"]


    if address in addresses:

        return render_template("index.html", headings = headings, summary=summary)
    else:
        fromAPI = getSLP(address)
        for raw_data in fromAPI:
            row = []

            # name
            row.append(name)

            # claimable slp
            row.append(raw_data["claimable_total"])

            # lastclaimed
            lastclaim = raw_data["update_time"]
            lastclaim /= 1000  # converter doesn't read miliseconds UTX
            row.append(datetime.utcfromtimestamp(lastclaim).strftime('%Y-%m-%d %H:%M:%S'))

            # date
            each_date = raw_data["update_time"]
            each_date /= 1000  # converter doesn't read miliseconds UTX
            row.append(datetime.utcfromtimestamp(each_date).strftime('%Y-%m-%d %H:%M:%S'))

            # store into summary
            summary.append(row)

            # store address for duplicate checking
            addresses.append(address)

    return render_template("index.html", headings = headings, summary=summary)




if __name__ == "__main__":
    app.run(debug=True)
