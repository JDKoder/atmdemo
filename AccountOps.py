import logging
from decimal import Decimal, ROUND_DOWN
from bson import Decimal128

class AccountOperations:
    
    account_data_svc = None
    authorization_svc = None
    machine = None


    def __init__(self, account_data_svc, authorization_svc, machine_svc):
        self.logger = logging.getLogger("AccountOperations")
        self.logger.debug("Initialized logger for AccountOperations")
        self.account_data_svc = account_data_svc
        self.authorization_svc = authorization_svc
        self.machine = machine_svc

    def pretty_money(self, amount_dec):
        isNeg = ""
        if amount_dec < 0:
            isNeg = "-"
            amount_dec = -amount_dec
        return isNeg + "$" + str(amount_dec.quantize(Decimal('.01'), rounding=ROUND_DOWN))


    def balance(self, args=None):
        self.logger.debug("Entering balance")
        acct = self.authorization_svc.get_active_account()
        self.logger.debug("Found account:" + str(acct))
        if acct is not None and "balance" in acct:
            balance_str = self.pretty_money(Decimal(str(acct.get("balance"))))
            self.logger.debug("printing account balance:" + balance_str)            
            print("Current balance: " + balance_str)        
        else:
            print("balance not found.")
            self.logger.debug("balance not found on acct.")
        self.logger.debug("Exiting balance")


    def withdraw(self, args):
        self.logger.debug("Entering withdraw")
        if len(args) > 1 and args[1].replace('.','',1).isdigit():
            self.logger.debug("valid input")
            withdraw_dec = Decimal(args[1])
            pretty_withdraw = self.pretty_money(withdraw_dec)
            if not (withdraw_dec % 20 == Decimal("0")):
                print("Please enter withdrawal amount as a multiple of 20.")
                return
            account = self.authorization_svc.get_active_account()
            aid = account.get("account_id")
            acct_bal = Decimal(str(account.get("balance")))
            overdrawn = acct_bal < 20
            self.logger.info("account overdrawn: " + str(overdrawn))
            if overdrawn:
                print("Your account is overdrawn! You may not make withdrawals at this time.")
                return
            elif not self.machine.can_process(20):
                print ("Unable to process your withdrawal at this time.")
                return
            elif not self.machine.can_process(withdraw_dec):
                self.logger.info("The machine cannot fulfill the requested withdrawal amount:" + pretty_withdraw)
                print ("Unable to dispense full amount requested at this time.")
                withdraw_dec = self.machine.get_contents()
                self.logger.info("Adjusted withdrawal amount to machine's available contents: " + pretty_withdraw)
            elif acct_bal - withdraw_dec < 20:
                self.logger.info("Account has become overdrawn.")
                overdrawn = True
            final_balance = acct_bal - withdraw_dec
            pretty_final = self.pretty_money(final_balance)
            final_balance_dec128 = Decimal128(str(final_balance))
            pretty_withdraw = self.pretty_money(-withdraw_dec)
            withdraw_dec128 = Decimal128(str(-withdraw_dec))
            if self.account_data_svc.save_transaction(aid, final_balance_dec128):
                self.logger.info("Withdrawal successful for account: " + str(aid))
                self.machine.pay_out(withdraw_dec)
                self.account_data_svc.update_history(aid, pretty_withdraw, pretty_final)
                self.authorization_svc.refresh(aid)
                account = self.authorization_svc.get_active_account()
            if overdrawn:
                self.logger.info("Charging overdraft fee of $5")
                acct_bal = Decimal(str(account.get("balance"))) - 5
                pretty_final = self.pretty_money(acct_bal)
                print("You have been charged an overdraft fee of $5. Current balance:", pretty_final)
                #apply the fee to acct_bal
                
                final_balance_dec128 = Decimal128(str(acct_bal))
                self.account_data_svc.save_transaction(aid, final_balance_dec128)
                self.account_data_svc.update_history(aid, self.pretty_money(Decimal("-5")), pretty_final)
                self.authorization_svc.refresh(aid)
        else:
            self.logger.debug("invalid input")
            print("Expected a non negative decimal value.")
        self.logger.debug("Exiting withdraw")


    def deposite(self, args):
        self.logger.debug("Entering desposite")
        ##if the number is negative or not in decimal format then give error and prompt again.
        if len(args) > 1 and args[1].replace('.','',1).isdigit():
            deposite_dec = Decimal(args[1])
            account = self.authorization_svc.get_active_account()
            acct_bal = Decimal(str(account.get("balance")))
            final_balance_dec = acct_bal + deposite_dec
            final_balance_pretty = self.pretty_money(final_balance_dec)
            final_balance_dec128 = Decimal128(str(final_balance_dec))
            aid = account.get("account_id")
            #if user save is succesful we save the user's history and refresh the active account
            if self.account_data_svc.save_transaction(aid, final_balance_dec128):
                self.logger.info("Deposite succesful for account: " + str(aid))
                self.authorization_svc.refresh(aid)
                self.balance()
                deposite_pretty = self.pretty_money(deposite_dec)
                self.account_data_svc.update_history(aid, deposite_pretty, final_balance_pretty)
        else:
            print("Expected a non negative decimal value in non-scientific format")
        self.logger.debug("Exiting desposite")


    def history(self, args=None):
        self.logger.debug("Entering history")
        acct = self.authorization_svc.get_active_account()
        self.logger.debug("Found account:" + str(acct))
        if acct is not None and "account_id" in acct:
            print("Date".ljust(15) + "Time".ljust(15) + "Amount".ljust(15) + "Balance After Transaction".ljust(26))
            account_id = acct.get("account_id")
            acct_hist = self.account_data_svc.find_account_hist_by_account_id(account_id)
            for h in acct_hist:
                self.logger.debug("account_history current iteration:" + str(h))
                h
                print(h.get("date").ljust(15) + h.get("time").ljust(15) + str(h.get("amount")).ljust(15) + str(h.get("balance")).ljust(26))
        else:
            print("Something went wrong.  Please discontinue use of this ATM.")
            self.logger.error("account_id attribute was not found in account" + str(acct))
        self.logger.debug("Exiting history")