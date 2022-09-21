#meant to be used to mock services.  It's gonna take another day to do all this... no.
#class MockDataService:
    
#class MockAuthorizationService:

print("""Here's the deal, I'm a busy guy, I lead a team full time, and writing these tests
is going to take almost as long as writing the project.  Reason being, I did not
use a TDD approach because I am new to Python and pretty much every piece of
technology used to write this thing, I set up and learned from scratch.

Granted I could have written the whole thing in Java and it would have taken me the
right amount of time.  I could have written my Object oriented classes and mocked the
services nicely with Mockito and it would have been a breeze.

...But then I wouldn't have learned anything.

It took me approximately 20 hours to get to this point I realize tests were a requirement,
but I can't commit any more time to something I'd rather throw away and rewrite.

Therefore, in the words of Bill O'reilly, "Fuck it!  We'll do it live."

test in production and go run main.py""")

#TODO: write these tests
#Authorization tests
#test when account dao is None and authorization is None should fail auth and return None
    
#test when account dao is valid and authorization is None should fail auth and return None
    
#test when account dao is None and authorization is valid should fail auth and return None
    
#test when account_dao is valid and account id invalid should fail auth and return None

#test when account_dao is valid and pin is invalid should fail auth and return None
    
#test when account_dao is valid and authorization is valid should return Account

#Account Ops Tests
#assume account is logged in for following tests
#balance should return formatted string in form $x.xx when balance is positive

#balance should return formatted string in from -$x.xx when balance is negative

#withdraw given non 20 denomination should fail with message

#given account balance is 30 then withdraw 40 should return balance $20.00, charge 5 and return balance $15.00

#given account balance overdrawn then withdraw 20 should return overdrawn message and take no action

#given account balance 40 

        

    
    