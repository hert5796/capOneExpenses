from db.sdk.capOne import CapOne
from json import loads

class Account(CapOne):
    def __init__(self):
        super().__init__()
        self.base = "https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data/accounts"

    # Create list of random accounts 
    # quantity: int - number of accounts to create, capped at 25
    # numTransactions: int - number of transactions to create, capped at 25
    # liveBalance: bool - whether to use live balance or not
    def random_accounts(self, quantity=1, numTransactions=5, liveBalance=False):
        response = self.post_request(self.base + "/create", {
            "quantity": quantity,
            "numTransactions": numTransactions,
            "liveBalance": liveBalance
        }).text
        
        # print(response)
        return response["Accounts"]

    # Get accounts
    def get_accounts(self, params={}):
        response = self.get_request(self.base, params).text

        return loads(response)["Accounts"]

    # Get account by id
    def get_account(self, account_id, params={}):
        response = self.get_request(self.base + f"/{account_id}", params).text

        return loads(response)["Accounts"]


    




