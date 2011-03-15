#coding=utf-8
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('groupserver')
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CustomUserFolder.interfaces import IGSUserInfo
from gs.content.form.form import SiteForm
from gs.profile.email.base.emailuser import EmailUser
from interfaces import IGSEmailSettingsForm

class ChangeEmailSettingsForm(SiteForm):
    form_fields = form.Fields(IGSEmailSettingsForm)
    label = _(u'Change Email Settings')
    pageTemplateFileName = 'browser/templates/settings.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    
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
        deliveryAddresses = data.get('deliveryAddresses','') and \
          data['deliveryAddresses'].strip().split('\n') or [] 
        otherAddresses = data.get('otherAddresses','') and \
          data['otherAddresses'].strip().split('\n') or []
        unverifiedAddresses = data.get('unverifiedAddresses','') and \
          data['unverifiedAddresses'].strip().split('\n') or []
        self.update_addresses(deliveryAddresses, otherAddresses, unverifiedAddresses)

        self.status = _(u' ')
        assert self.status
    
    @form.action(label=_('Add'), failure='handle_failure')
    def handle_add(self, action, data):
        address = data['newAddress']
        isPreferred = len(self.emailUser.get_delivery_addresses()) < 1
        self.emailUser.add_address(address, isPreferred)
        
        # TODO: Rewrite for an admin adding an address.
        e = u'<code class="email">%s</code>' % address
        m = _(u'The address ') + e + _(u' has been <strong>added</strong> '
            u'to your profile. ')
        n = _(u'An email has been sent to <strong>verify</strong> '
            u'that you control ') + e + _('. ') + \
            _(u'<strong>Check</strong> your inbox for the email. '
            u'You must follow the instructions in the email before '
            u'you can use ') + e + _('. ')
        self.status = u'<p>%s</p> <p>%s</p>' % (m, n)
        assert self.status

    def handle_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = _(u'There was an error:')
        else:
            self.status = _(u'<p>There were errors:</p>')
    
    def update_addresses(self, deliveryAddresses, otherAddresses, unverifiedAddresses):
        oldVerifiedAddresses = self.emailUser.get_verified_addresses()
        newVerifiedAddresses = deliveryAddresses + otherAddresses
        for address in oldVerifiedAddresses:
            assert address in self.emailUser.get_addresses(), \
              'Address %s does not belong to %s (%s)' %\
              (address, self.emailUser.userInfo.name, 
               self.emailUser.userInfo.id)
            if address not in newVerifiedAddresses:
                self.emailUser.remove_address(address)
        
        oldUnverifiedAddresses = self.emailUser.get_unverified_addresses()
        newUnverifiedAddresses = unverifiedAddresses
        for address in oldUnverifiedAddresses:
            assert address in self.emailUser.get_addresses(), \
              'Address %s does not belong to %s (%s)' %\
              (address, self.emailUser.userInfo.name, 
               self.emailUser.userInfo.id)
            if address not in newUnverifiedAddresses:
                self.emailUser.remove_address(address)
        
        self.update_delivery_addresses(deliveryAddresses)
    
    def update_delivery_addresses(self, addresses):
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
        for address in removedAddresses:
            self.emailUser.drop_delivery(address)

