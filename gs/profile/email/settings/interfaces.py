# coding=utf-8
from zope.interface import Interface
from zope.schema import ASCII, List
from gs.profile.email.base.emailaddress import EmailAddress

class IGSEmailSettings(Interface):
    
    deliveryAddresses = List(title=u'Addresses For Receiving Email',
        description=u'Addresses at which you will usually receive '
          'email from your groups',
        value_type=EmailAddress(title=u'Email Address', 
          description=u'Email address for receiving mail'),
        unique=True,
        default=[],
        required=True)
    
    otherAddresses = List(title=u'Your Other Addresses',
        description=u'Addresses at which you will not usually receive '
          'email from your groups, but from which you might send '
          'messages to your groups',
        value_type=EmailAddress(title=u'Email Address', 
          description=u'Other email address'),
        unique=True,
        default=[],
        required=False)
    
    unverifiedAddresses = List(title=u'Your Unverified Addresses',
        description=u'Addresses which you have added to your profile, '
          'but which have not been determined to both (a) belong to you '
          'and (b) be currently accepting email',
        value_type=EmailAddress(title=u'Email Address', 
          description=u'Unverified email address'),
        unique=True,
        default=[],
        required=False)
        
class IGSEmailSettingsForm(Interface):
    
    deliveryAddresses = ASCII(title=u'Addresses For Receiving Email',
        description=u'Addresses at which you will usually receive '
          'email from your groups',
        required=True)
    
    otherAddresses = ASCII(title=u'Your Other Addresses',
        description=u'Addresses at which you will not usually receive '
          'email from your groups, but from which you might send '
          'messages to your groups',
        required=False)
    
    newAddress = EmailAddress(title=u'Address',
      description=u'The email address you want to add.')

