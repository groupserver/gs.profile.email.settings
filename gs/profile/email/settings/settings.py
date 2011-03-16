#coding=utf-8
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('groupserver')
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.XWFCore.XWFUtils import comma_comma_and
from gs.content.form.form import SiteForm
from gs.profile.email.base.emailuser import EmailUser
from gs.profile.email.verify.emailverificationuser import EmailVerificationUser
from interfaces import IGSEmailSettingsForm

# TODO: Rewrite the status messages for an administrator adding an 
# address.
class ChangeEmailSettingsForm(SiteForm):
    form_fields = form.Fields(IGSEmailSettingsForm)
    label = _(u'Change Email Settings')
    pageTemplateFileName = 'browser/templates/settings.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    verifyMesg = _(u'An email has been sent to <strong>verify</strong> '
                    u'that you control ')
    verifyCheckMesg =\
        _(u'<strong>Check</strong> your inbox for the email. ')    
    def __init__(self, user, request):
        SiteForm.__init__(self, user, request)
        self.userInfo = IGSUserInfo(user)
        self.emailUser = EmailUser(user, self.userInfo)

    def setUpWidgets(self, ignore_request=False): #--=mpj17=-- change to True?
        default_data = \
          {'deliveryAddresses': '\n'.join(self.deliveryAddresses),
           'otherAddresses': '\n'.join(self.otherAddresses)}
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.userInfo.user, 
            self.request, data=default_data,
            ignore_request=False)

    @property
    def deliveryAddresses(self):
        return self.emailUser.get_delivery_addresses()
    
    @property   
    def otherAddresses(self):
        verifiedAddresses = self.emailUser.get_verified_addresses()
        otherAddresses = \
          [ a for a in verifiedAddresses 
            if a not in self.deliveryAddresses ]
        return otherAddresses
    
    @property
    def unverifiedAddresses(self):
        return self.emailUser.get_unverified_addresses()
        
    @form.action(label=_('Change'), failure='handle_failure')
    def handle_change(self, action, data):
        self.status = u''

        d = self.t_to_l(data.get('deliveryAddresses',''))
        o = self.t_to_l(data.get('otherAddresses',''))
        u = self.t_to_l(data.get('unverifiedAddresses',''))

        removeUpdate = self.remove_addresses(d, o, u)
        if removeUpdate.changed:
            self.add_to_status(unicode(removeUpdate))

        deliveryUpdate = self.update_delivery_addresses(d)
        if deliveryUpdate.changed:
            self.add_to_status(unicode(deliveryUpdate))
        
        # Resend the verification message to an address
        if data.get('resendVerificationAddress', None):
            r = self.resend_verification(data['resendVerificationAddress'])
            self.add_to_status(r)

        assert type(self.status) == unicode
        
    def add_to_status(self, msg):
        self.status = u'%s<p>%s</p>' % (self.status, msg)
        
    @form.action(label=_('Add'), failure='handle_failure')
    def handle_add(self, action, data):
        self.status = u''

        address = data['newAddress']
        if address:
            e = markup_address(address)
            
            d = len(self.emailUser.get_delivery_addresses())
            isPreferred = d < 1
            self.emailUser.add_address(address, isPreferred)
            self.send_verification(address)

            m = _(u'The address ') + e + \
                _(u' has been <strong>added</strong> to your '
                    u'profile. ')
            self.add_to_status(m)

            n = self.verifyMesg + e + _('. ') + \
                self.verifyCheckMesg +  _(u'You must follow the '
                    u'instructions in the email before you can '
                    u'use ') + e + _('. ')
            self.add_to_status(n)
        assert type(self.status) == unicode

    def handle_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = _(u'There was an error:')
        else:
            self.status = _(u'<p>There were errors:</p>')

    def t_to_l(self, text):
        """Change a text-field (string) to a list"""
        retval = []
        if text:
            retval = text.strip().split('\n')
        assert type(retval) == list
        return retval

    def resend_verification(self, address):
        self.send_verification(address)
        e = markup_address(address)
        retval = self.verifyMesg + e + _(u'. ') + self.verifyCheckMesg
        assert type(retval) == unicode
        return retval
        
    def send_verification(self, address):
        emailVerificationUser = EmailVerificationUser(self.context, 
                                    self.userInfo, address)
        emailVerificationUser.send_verification_message()
        
    def remove_addresses(self, deliveryAddresses, otherAddresses, unverifiedAddresses):
        # --=mpj17=-- While the UI presents an interface for removing 
        # addresses, it is actually handled through a side-effect. The 
        # UI just removes the address from the list of delivery, other,
        # or unverified addresses. This code trawls through the addresses
        # trying to spot the ones that have been removed.
        retval = RemoveUpdate()
         
        oldVerifiedAddresses = self.emailUser.get_verified_addresses()
        newVerifiedAddresses = deliveryAddresses + otherAddresses
        for address in oldVerifiedAddresses:
            assert address in self.emailUser.get_addresses(), \
              'Address %s does not belong to %s (%s)' %\
              (address, self.emailUser.userInfo.name, 
               self.emailUser.userInfo.id)
            if address not in newVerifiedAddresses:
                self.emailUser.remove_address(address)
                retval.verified.append(address)
        
        oldUnverifiedAddresses = self.emailUser.get_unverified_addresses()
        newUnverifiedAddresses = unverifiedAddresses
        for address in oldUnverifiedAddresses:
            assert address in self.emailUser.get_addresses(), \
              'Address %s does not belong to %s (%s)' %\
              (address, self.emailUser.userInfo.name, 
               self.emailUser.userInfo.id)
            if address not in newUnverifiedAddresses:
                self.emailUser.remove_address(address)
                retval.unverified.append(address)

        return retval

    def update_delivery_addresses(self, addresses):
        retval = DeliveryUpdate()
        
        oldAddresses = self.deliveryAddresses
        newAddresses = addresses
        addedAddresses = \
          [a for a in newAddresses if a not in oldAddresses]
        removedAddresses = \
          [a for a in oldAddresses if a not in newAddresses]

        for address in addedAddresses:
            assert address in self.emailUser.get_addresses(), \
              'Address %s does not belong to %s (%s)' %\
              (address, self.emailUser.userInfo.name, 
               self.emailUser.userInfo.id)
            self.emailUser.set_delivery(address)
            retval.added.append(address)

        for address in removedAddresses:
            self.emailUser.drop_delivery(address)
            retval.removed.append(address)
        
        return retval

def markup_address(address):
    return u'<code class="email">%s</code>' % address

class RemoveUpdate(object):
    verifiedRemoveMessage = _(u'<strong>Removed</strong> the address ')
    unverifiedRemoveMessage = _(u'<strong>Removed</strong> the '
        u'unverified address ')
    def __init__(self):
        self.verified = []
        self.unverified = []
    
    @property
    def changed(self):
        return bool(self.verified) or bool(self.unverified)

    def __unicode__(self):
        retval = u''
        if self.verified:
            e = comma_comma_and([markup_address(a) for a in self.verified])
            retval =  self.verifiedRemoveMessage + e + _(u'. ')
        if self.unverified:
            e = comma_comma_and([markup_address(a) for a in self.unverified])
            retval = retval + self.unverifiedRemoveMessage + e + _(u'. ')
        assert type(retval) == unicode
        return retval

    def __str__(self):
        return unicode(self).encode('utf-8')
    
class DeliveryUpdate(object):
    addedMessageA = _(u'<strong>Added</strong> the address ')
    addedMessageB = _(u' to the list of preferred delivery addresses. ')
    removedMessageB = _(u' to the list of your other addresses. ')
    def __init__(self):
        self.added = []
        self.removed = []

    @property
    def changed(self):
        return bool(self.added) or bool(self.removed)

    def __unicode__(self):
        retval = u''
        if self.added:
            e = comma_comma_and([markup_address(a) for a in self.added])
            retval =  self.addedMessageA + e + self.addedMessageB
        if self.removed:
            e = comma_comma_and([markup_address(a) for a in self.removed])
            # Yes, the retval starts with added message A
            retval += self.addedMessageA + e + self.removedMessageB
        assert type(retval) == unicode
        return retval

    def __str__(self):
        return unicode(self).encode('utf-8')

