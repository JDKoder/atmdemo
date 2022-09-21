#import logging
import logging

#authorization that maintains state of the user's authorization status.
#methods are provided to attempt authorization

#This class is meant to support only 1 active account at a time.
class Authorization:
    
    authorized = False
    active_account = {}
    account_dao_svc = None
    
    def __init__(self, account_dao):
        self.logger = logging.getLogger("Authorization")
        self.logger.debug("Initialized logger for Authorization")
        self.authorized = False
        self.active_account = {}
        self.account_dao_svc = account_dao 

    def is_authorized(self):
        return self.authorized
    
    def get_active_account(self):
        return self.active_account
    
    def refresh(self, account_id):
        self.logger.debug("Entering refresh");
        if self.authorized and account_id == self.active_account.get("account_id"):
            authorization = {"account_id": self.active_account.get("account_id"),
                             "pin": self.active_account.get("pin")}
            self.active_account = self.account_dao_svc.find_one_account(authorization)
        else:
            self.logger.warn("Process called refresh without authorization.  This shouldn't happen.")
        self.logger.debug("Exiting refresh");

    def logout(self):
        """Verifies if the user is already logged in.
        If so, we clear the authorized flag and set the active_account back
        to an empty value.
        """
        self.logger.debug("Entering logout")
        if self.authorized:
            print("Account", self.active_account.get("account_id"), "logged out.")
            self.logger.info("Account " + self.active_account.get("account_id") + " logged out.")
            self.authorized = False
            self.active_account = {}
        else:
            self.logger.info("No account is authorized - No action taken in logout.")
            print("No account is currently authorized");
        self.logger.debug("exiting logout")

    def attempt_auth(self, authorization):
        """Takes an authorization dict with expected account_id and pin keys.
        makes a call to the DAO to retrieve account information.  Stores it in
        local variable and marks authorized as True.
        """        
        self.logger.debug("Entering attempt_auth")
        valid_args = True
        account = None
        #Authorization is expected to contain a dict of account_id and pin
        if None in (self.account_dao_svc, authorization):
            self.logger.error(str("Invalid Arguments account_dao:["
                                  + str(self.account_dao_svc) + "]; authorization:["
                                  + str(authorization) + "]"))
            valid_args = False
        if valid_args == True and None in (authorization.get("account_id"),
                    authorization.get("pin")):
            message = str("Invalid authorization parameters: account_id[" +
                          str(authorization.get("account_id")) + "]; pin[" +
                          str(authorization.get("pin")), "]")
            self.logger.error(message)
            valid_args = False
        if valid_args:
            account = self.account_dao_svc.find_one_account(authorization)
        
        if account is None or len(account) == 0 or not valid_args:
            self.logger.info("Authorization failed.")
            print("Authorization failed.")
            if self.authorized:
                self.logger.info("User attempted authentication while already logged in with arguments: "
                                 + str(authorization))
                print ("Please logout before attempting to sign in to another account.")
        else:
            self.authorized = True
            self.active_account = account
            print(authorization.get("account_id"), "successfully authorized.")
            self.logger.info("Successfully authorized: " + str(account))
        self.logger.debug("Exiting attempt_auth")
        