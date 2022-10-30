from flask import Flask, render_template
from datetime import datetime, timedelta
from db.sdk.account import Account
from db.sdk.transaction import Transaction
from json import dumps

app = Flask(__name__)

account, transaction = Account(), Transaction()


# 01073771 # Melisa Jacobs
# 77058457 # Domingo Kiehn
# 37401495 # Karlene Raynor
# 34841425 # Danielle Blick
# 71594276 # Beulah Kris
# 81251951 # Sidney Wisozk
# 58135773 # Wade Konopelski
# 73347905 # Pearle Berge
# 39419128 # Ray Kautzer
# 50433494
# 66883520
# 03001220
# 70928271
# 27709054
# 00181767

@app.route('/')
def default():
    ac_id = "01073771"
    ac = account.get_account(ac_id)
    tr = transaction.get_all_transactions(ac_id)

    def relative_day(date):
        day_map = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

        if date == datetime.today().date():
            return "Today"
        elif date == datetime.today().date() - timedelta(days=1):
            return "Yesterday"
        else:
            return day_map[date.weekday()] + ", " + date.strftime("%d %b %Y")


    def decorate(transaction):
        transaction['charges'] = format(float(transaction['amount']) * -1, '.2f')
        transaction['datetime'] = datetime.strptime(transaction['timestamp'], "%Y-%m-%d %H:%M:%S")
        transaction['time'] = transaction['datetime'].strftime("%H:%M")
        transaction['relative_day']  = relative_day(transaction['datetime'].date())
        transaction['summary'] = transaction['message'].split(" of ")[0]

        return transaction
    tr = map(decorate, tr)
    tr = sorted(tr, key=lambda x: x['datetime'], reverse=True)

    # cluster transactions by day
    tr_by_day = {}
    for t in tr:
        day = t['datetime'].strftime("%Y-%m-%d")
        if day not in tr_by_day:
            tr_by_day[day] = []
        tr_by_day[day].append(t)
    
    # list transaction clusters by day
    tr_by_day = sorted(tr_by_day.items(), key=lambda x: x[0], reverse=True)

    return render_template('homepage.html', account=ac[0], transactions_by_day=tr_by_day)

if __name__ == '__main__':
    app.run(port=8000, debug=True)