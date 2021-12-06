from flask import Flask, render_template
from main import getSLP
from datetime import datetime

app = Flask(__name__)

headings = ("Total SLP", "Last Claimed","Date Refreshed")

fromAPI = getSLP("ronin:71dd7cb6743b94b5bffc2a6d43ccdb6d6dd98912,ronin:b800eea5e1ce4d49ca2db939e9883414f0bd5ff2")

summary = [] #store data from each address
for raw_data in fromAPI:
    row = []


    #claimable slp
    row.append(raw_data["claimable_total"])

    #lastclaimed
    lastclaim = raw_data["update_time"]
    lastclaim /= 1000  # converter doesn't read miliseconds UTX
    row.append(datetime.utcfromtimestamp(lastclaim).strftime('%Y-%m-%d %H:%M:%S'))

    #date
    each_date = raw_data["update_time"]
    each_date /= 1000 #converter doesn't read miliseconds UTX
    row.append(datetime.utcfromtimestamp(each_date).strftime('%Y-%m-%d %H:%M:%S'))

    #store into summary
    summary.append(row)





@app.route("/")
def home():
    return render_template("index.html", headings = headings, summary=summary)


if __name__ == "__main__":
    app.run(debug=True)
