from flask import Flask, render_template, request, redirect, url_for
from main import getSLP
from datetime import datetime

app = Flask(__name__)

summary = []  # store data from each address
addresses = [] # check if address's already there to avoid duplicates
@app.route("/",methods=["POST", "GET"])
def home():
    headings = ("Name", "Total SLP", "Average" ,"Last Claimed", "Days Past Claiming", "Date Data Gathered")
    name = request.form.get('nm', False)
    address = request.form.get("ronin_add", False)
    delete_name = request.form.get("delete_name", False)


    # delete name in table
    for i in range(len(summary)):
        if summary[i][0] == delete_name:
            summary.pop(i)   # remove whole row
            addresses.pop(i) #remove address from listed address
            delete_name = None
            break


    # catch errors
    try:
        fromAPI = getSLP(address)
        #test function
        fromAPI[0]["claimable_total"]
    except:
        return render_template("index.html", headings=headings, summary=summary)





    if address in addresses:# avoid duplicates
        return render_template("index.html", headings = headings, summary=summary)
    else:
        if address == False:
            return render_template("index.html", headings=headings, summary=summary)
        else:
            for raw_data in fromAPI:
                row = []

                # name
                row.append(name)

                # claimable slp
                claimable = raw_data["claimable_total"]
                row.append(claimable)

                #Average SLP per day
                lastclaim = raw_data["last_claimed_item_at"]
                lastDateDatetime = datetime.fromtimestamp(lastclaim)
                todayDatetime = datetime.now()
                difference = todayDatetime - lastDateDatetime


                average = round(claimable/int(difference.days))

                row.append(average)



                # lastclaimed
                lastclaim = raw_data["last_claimed_item_at"]
                row.append(datetime.utcfromtimestamp(lastclaim).strftime('%b %-d, %Y'))



                # days from last claim date
                lastDateDatetime = datetime.fromtimestamp(lastclaim)
                todayDatetime = datetime.now()
                difference = todayDatetime - lastDateDatetime

                row.append(difference.days)


                # date
                each_date = raw_data["update_time"]
                each_date /= 1000  # converter doesn't read miliseconds UTX
                row.append(datetime.utcfromtimestamp(each_date).strftime('%b %-d, %Y'))

                # store into summary
                summary.append(row)

                # store address for duplicate checking
                addresses.append(address)
    return render_template("index.html", headings = headings, summary=summary)




if __name__ == "__main__":
    app.run(debug=True)
