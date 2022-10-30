from flask import Flask, render_template, redirect

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
    return redirect(f"/{ac_id}")

@app.route('/<account_id>')
def check(account_id):
    ac = account.get_account(account_id)

    tr = transaction.get_all_transactions(account_id)
    te, _ = transaction.top_expenses(tr)

    tr = transaction.decorate_transactions(tr)
    tr = transaction.sort_transactions(tr)

    te_labels = ", ".join([t['category'] for t in te])
    te_amount = ", ".join([str(t['amount']) for t in te])
    # te_values = [t[1] for t in te]

    print(te_labels)

    return render_template('homepage.html', account=ac[0], transactions_by_day=tr, te_labels=te_labels, te_amount=te_amount)

if __name__ == '__main__':
    app.run(port=8000, debug=True)