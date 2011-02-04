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
        allAddresses = self.emailUser.get_addresses()
        verifiedAddresses = self.emailUser.get_verified_addresses()
        unverifiedAddresses = \
          [ a for a in allAddresses if a not in verifiedAddresses ]
        return unverifiedAddresses
        
    @form.action(label=_('Change'), failure='handle_change_action_failure')
    def handle_change(self, action, data):
        deliveryAddresses = data.get('deliveryAddresses','').strip().split('\n')
        self.update_delivery_addresses(deliveryAddresses)
    
    def handle_change_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = _(u'There was an error:')
        else:
            self.status = _(u'<p>There were errors:</p>')
        
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
