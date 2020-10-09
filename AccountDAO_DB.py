import logging
from datetime import datetime, timezone
import pymongo
from pymongo import MongoClient

class AccountMongoDBService:
    
    def __init__(self):
        self.logger = logging.getLogger("AccountMongoDBService")
        self.logger.debug("Initialized logger for AccountMongoDBService")
        cluster = MongoClient("mongodb+srv://takeoff:6XlEMRScrF8ODBny@atmdemo.rkqze.mongodb.net/bank?retryWrites=true&w=majority")
        db = cluster["bank"]
        self.accounts_dao = db["account"]
        self.acct_history_dao = db["account_history"]
        
    def find_one_account(self, params):
        self.logger.debug("Entering find_one_account")
        self.logger.info("finding account with params" + str(params));
        self.logger.debug("Exiting find_one_account")
        return self.accounts_dao.find_one(params)
    
    def find_account_hist_by_account_id(self, account_id):
        self.logger.debug("Entering find_account_hist_by_account_id")
        self.logger.info("finding account history by account id: " + str(account_id))
        self.logger.debug("Exiting find_account_hist_by_account_id")
        return self.acct_history_dao.find({"account_id":account_id}).sort("created_date", pymongo.DESCENDING)
    
    def save_transaction(self, account_id, balance):
        """persist the user's balance after a transactions"""
        self.logger.debug("Entering save_transaction")
        self.logger.info("Saving account balance [" + str(balance) + "] for account [" + str(account_id) +"]")  
        deposite_success = False
        try:
            post1 = self.accounts_dao.update({"account_id":account_id}, {"$set":{"balance":balance}})
            deposite_success = True
        except:
            self.logger.error("An error occurred during save_transaction.  Last command failed.")
        return deposite_success
        self.logger.debug("update complete with response: " + str(post1))
        self.logger.debug("Exiting save_transaction")
        
    #update the user's history
    def update_history(self, account_id, amount, balance):
        self.logger.debug("Entering update_history")
        #construct a string representation of the current utc date time
        created_date = datetime.now(timezone.utc)
        current_time_str = created_date.strftime("%Y-%m-%d %H:%M:%S")
        self.logger.debug("splitting current_time_str on space: " + current_time_str)
        datetime_arr = current_time_str.split(" ")
        self.logger.debug("datetime_arr: " + str(datetime_arr))
        self.logger.info("Inserting to account_history for account " + str(account_id))
        payload = {"account_id":account_id,
                    "date":datetime_arr[0],
                    "time":datetime_arr[1],
                    "amount":amount,
                    "balance":balance,
                    "created_date":created_date}
        self.logger.debug("insert payload: " + str(payload))
        insert = self.acct_history_dao.insert(payload)
        self.logger.debug("account_history insert complete with response" + str(insert))
        self.logger.debug("Exiting update_history")
