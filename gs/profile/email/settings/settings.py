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

    def setUpWidgets(self, ignore_request=False):
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
        deliveryAddrs = self.t_to_l(data.get('deliveryAddresses',''))
        otherAddrs = self.t_to_l(data.get('otherAddresses',''))
        unverifiedAddrs = self.t_to_l(data.get('unverifiedAddresses',''))
        #r = self.update_addresses(deliveryAddrs, otherAddrs, 
        #            unverifiedAddrs)
        #if r:
        #    self.status = u'<p>%s</p>' % r
        
        if data.get('resendVerificationAddress', None):
            r = self.resend_verification(data['resendVerificationAddress'])
            self.status = u'%s\n<p>%s</p>' % (self.status, r)
        assert type(self.status) == unicode
            
    @form.action(label=_('Add'), failure='handle_failure')
    def handle_add(self, action, data):
        address = data['newAddress']
        isPreferred = len(self.emailUser.get_delivery_addresses()) < 1
        self.emailUser.add_address(address, isPreferred)
        self.send_verification(address)
        # TODO: Rewrite for an admin adding an address.
        e = u'<code class="email">%s</code>' % address
        m = _(u'The address ') + e + _(u' has been <strong>added</strong> '
            u'to your profile. ')
        n = self.verifyMesg + e + _('. ') + self.verifyCheckMesg + \
            _(u'You must follow the instructions in the email before '
                u'you can use ') + e + _('. ')
        self.status = u'<p>%s</p> <p>%s</p>' % (m, n)
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
        e = u'<code class="email">%s</code>' % address
        retval = self.verifyMesg + e + _(u'. ') + self.verifyCheckMesg
        assert type(retval) == unicode
        return retval
        
    def send_verification(self, address):
        emailVerificationUser = EmailVerificationUser(self.context, 
                                    self.userInfo, address)
        emailVerificationUser.send_verification_message()
    
    def update_addresses(self, deliveryAddresses, otherAddresses, unverifiedAddresses):
        # Perform two types of address update: remove some addresses,
        # and handle any different delivery addresses.
        #self.remove_addresses(deliveryAddresses, otherAddresses, 
        #            unverifiedAddresses)
        # retval = self.update_delivery_addresses(deliveryAddresses)
        retval = u''
        assert type(retval) == unicode
        return retval
    
    def remove_addresses(self, deliveryAddresses, otherAddresses, unverifiedAddresses):
        # --=mpj17=-- While the UI presents an interfacefor removing 
        # addresses, it is actually handled through a side-effect. The 
        # UI just removes the address from the list of delivery, other,
        # or unverified addresses. This code trawls through the addresses
        # trying to spot the ones that have been removed.
 
        oldVerifiedAddresses = self.emailUser.get_verified_addresses()
        newVerifiedAddresses = deliveryAddresses + otherAddresses
        for address in oldVerifiedAddresses:
            assert address in self.emailUser.get_addresses(), \
              'Address %s does not belong to %s (%s)' %\
              (address, self.emailUser.userInfo.name, 
               self.emailUser.userInfo.id)
            if address not in newVerifiedAddresses:
                self.emailUser.remove_address(address)
                r.append(u'<code class="email">%s</code>' % address)
        
        oldUnverifiedAddresses = self.emailUser.get_unverified_addresses()
        newUnverifiedAddresses = unverifiedAddresses
        for address in oldUnverifiedAddresses:
            assert address in self.emailUser.get_addresses(), \
              'Address %s does not belong to %s (%s)' %\
              (address, self.emailUser.userInfo.name, 
               self.emailUser.userInfo.id)
            if address not in newUnverifiedAddresses:
                self.emailUser.remove_address(address)
            
    def update_delivery_addresses(self, addresses):
        oldAddresses = self.deliveryAddresses
        newAddresses = addresses
        addedAddresses = \
          [a for a in newAddresses if a not in oldAddresses]
        removedAddresses = \
          [a for a in oldAddresses if a not in newAddresses]
        
        retval = u''
        r = []
        for address in addedAddresses:
            assert address in self.emailUser.get_addresses(), \
              'Address %s does not belong to %s (%s)' %\
              (address, self.emailUser.userInfo.name, 
               self.emailUser.userInfo.id)
            self.emailUser.set_delivery(address)
            r.append(address)
        if r:
            s = [u'<code class="email">%s</code>' % a for a in r]
            retval = _(u'<strong>Added</strong> ') + comma_comma_and(s) + \
                _(u' to the list of preferred delivery addresses. ')
            
        r = []
        for address in removedAddresses:
            self.emailUser.drop_delivery(address)
            r.append(address)
        if r:
            s = [u'<code class="email">%s</code>' % a for a in r]
            retval = retval + _(u'<strong>Added</strong> ') + \
                comma_comma_and(s) + \
                _(u' to the list of other addresses.')
        
        return retval

