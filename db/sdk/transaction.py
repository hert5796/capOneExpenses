from urllib import request
from db.sdk.capOne import CapOne
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

        print(response)
        # return loads(response)["Transactions"]
