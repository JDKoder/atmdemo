import threading
from threading import Thread, Event
import logging

class SessionTimer(Thread):
    
    def __init__(self, interval, auth_svc):
        Thread.__init__(self)
        self.logger = logging.getLogger("SessionTimer")
        self.logger.debug("initializing session timer: interval[" + str(interval) + "]")
        self.interval_seconds = interval
        self.stopped = Event()
        self.reset = False
        self.auth_svc = auth_svc
        
    def run(self):
        self.logger.debug("session timer countdown started.")
        while not self.stopped.wait(self.interval_seconds):
            self.logger.debug("session interval elapsed")
            if self.reset is False:
                println("Your account has been logged out due to inactivity.")
                self.auth_svc.logout()
                println("Please press enter to continue.")
                self.stopped.set()
        if self.reset:
            self.logger.debug("session timer refreshed")
            self.reset = False
            self.run()
        
    def ref(self, event=None):
        self.logger.debug("refreshing session timer")
        self.reset = True
        #calling set will force the event to cease waiting and exit the run loop
        #since we are setting the reset flag to True, it will run the session timer
        #again recursively.
        self.stopped.set()
        #This call will set the event back to false and start the thread's execution again
        self.stopped.clear()
    
    def kill(self):
        self.stopped.set()