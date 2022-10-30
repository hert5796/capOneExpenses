from unicodedata import category
from db.sdk.capOne import CapOne
from db.sdk.helper import relative_day
from datetime import datetime
from json import loads

class Transaction(CapOne):

    def get_all_transactions(self, account_id, params=None):
        response = self.get_request(
            f"https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data/transactions/accounts/{account_id}/transactions",
            params
        ).text

        return loads(response)["Transactions"]

    def create_transaction(self, account_id, quantity=1):
        response = self.post_request(
            f"https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data/transactions/accounts/{account_id}/create",
            {
                "quantity": quantity
            }
        ).text

        return response

    def decorate_transactions(self, transactions):
        for transaction in transactions:
            transaction['charges'] = format(float(transaction['amount']) * -1, '.2f')
            transaction['datetime'] = datetime.strptime(transaction['timestamp'], "%Y-%m-%d %H:%M:%S")
            transaction['time'] = transaction['datetime'].strftime("%H:%M")
            transaction['relative_day']  = relative_day(transaction['datetime'].date())
            transaction['summary'] = transaction['message'].split(" of ")[0]

        return transactions

    def sort_transactions(self, transactions):
        tr = sorted(transactions, key=lambda x: x['datetime'], reverse=True)

        tr_by_day = {}
        for t in tr:
            day = t['datetime'].strftime("%Y-%m-%d")
            if day not in tr_by_day:
                tr_by_day[day] = []
            tr_by_day[day].append(t)
        
        tr_by_day = sorted(tr_by_day.items(), key=lambda x: x[0], reverse=True)

        return tr_by_day

    def top_expenses(self, transactions, limit=5):
        # Cluster transactions by merchant catergory
        tr_by_merchant = {}
        for t in transactions:
            category = t['merchant']['category']
            if category not in tr_by_merchant:
                tr_by_merchant[category] = []
            tr_by_merchant[category].append(t)
        # Get top limit categories
        top_transactions = sorted(tr_by_merchant.items(), key=lambda x: sum([float(t['amount']) for t in x[1]]), reverse=True)[:limit]
        
        # Get sum of transactions for each category
        top_expenses = []
        for category, transactions in top_transactions:
            top_expenses.append({
                'category': category,
                'amount': sum([float(t['amount']) for t in transactions])
            })

        return top_expenses, top_transactions
        
