import logging
from AccountDAO_DB import AccountMongoDBService
from authorization import Authorization
from AccountOps import AccountOperations
from Machine import Machine
from SessionTimer import SessionTimer

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', filename='runtime.log', level=logging.DEBUG)
logger = logging.getLogger("main")

#All service initializations
machine = Machine("10000")
data_svc = AccountMongoDBService()
auth_svc = Authorization(data_svc)
ops_svc = AccountOperations(data_svc, auth_svc, machine)

def call(func, args):
        func(args)

def start():
    
    SESSION_INTERVAL = 120 #session length resets to 2 minutes whenever input is received.
    session_timer = None
    """entrypoint to atm demo.  Initializes services and begins the main program loop"""   

    #Main loop
    logger.debug("Entering main loop")
    while True:
        #The user's session should only be tracked after they are authorized.
        #If the user has just authorized for the first time, the session_timer is initialized.
        #At the beginning of the loop, if the user is authorized we can refresh the timer.
        #The session timer runs in a separate thread so even if the user is idle, they will be
        #notified of the logout without running any command.
        if auth_svc.is_authorized():
            if session_timer is not None and session_timer.is_alive():
                session_timer.ref()
            else:
                session_timer = SessionTimer(SESSION_INTERVAL, auth_svc)
                session_timer.start()
        
        #prompt the user for a command and split the input so we have all arguments
        user_args = input("Please enter a command: ")
        logger.debug("user entered args at prompt " + user_args)
        args = str(user_args).split()
        
        #To allow the user to enter commands more easily, make it case insensitive.
        #If the user entered nothing, force it to empty string.
        cmd = "" if len(args) == 0 else args[0].lower();
        logger.debug("command parsed to" + cmd)
       
        if "end" == cmd:
            logger.debug("End command received, breaking out of main loop")
            break
        elif "authorize" == cmd:
            logger.info(str("authorizing with input" + str(args)))
            if len(args) == 3:
                auth_svc.attempt_auth({"account_id":args[1], "pin":args[2]})
            else:
                print("Please enter the command in the format: authorize <account number> <pin>")
        elif "logout" == cmd:
            #call logout on authorization
            auth_svc.logout()
        else:
            #process commands that require authorization
            if auth_svc.is_authorized():
                commands = {
                    "deposite": ops_svc.deposite,
                    "withdraw": ops_svc.withdraw,
                    "balance": ops_svc.balance,
                    "history": ops_svc.history
                    }
                if cmd in commands:
                    call(commands.get(cmd), args)
        logger.debug("Exited main program loop.")
    
    print("The application is now terminating.")

if __name__=='__main__':
    logger.debug("Application Started.")
    start()
    logger.debug("Application terminated.")