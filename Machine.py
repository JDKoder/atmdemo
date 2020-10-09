from decimal import Decimal

#currently machine only tracks the state of how much money it contains, not how many bills
#To improve this we would have the machine track individual bills and feed the withdrawal amount
#to this service and have the machine respond to.  Since the machine only distributes $20, we can
#just track values in that multiple.
class Machine:
    
    def __init__(self):
        self.contents = Decimal(10000)
        
    def __init__(self, initial):
        self.contents = Decimal(initial)
        
    def get_contents(self):
        return self.contents
    
    def can_process(self, ammount_dec):
        """Can the machine dispense the amount requested? True|False"""
        return self.contents > ammount_dec
    
    def pay_out(self, amount_dec):
        """Subtract the amount requested from the contests of the machine."""
        self.contents -= amount_dec;