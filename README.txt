This part of the code deals with requesting verification for, 
and verifying, email addresses.

The code for unverifying email addresses (i.e. disabling them after 
bouncing) is currently in Products.XWFMailingListManager.bounceaudit
but should probably be moved here. 

The main code will be in gs.profile.email.base. It will include
checks for whether an email address is or is not verified. The
bounce-logging code could maybe be moved there, too.
