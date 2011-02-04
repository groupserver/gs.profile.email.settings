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
        
    @form.action(label=_('Change'), failure='handle_set_action_failure')
    def handle_set(self, action, data):
        deliveryAddresses = data.get('deliveryAddresses','')
        otherAddresses = data.get('otherAddresses','')
        self.status = _(u'Delivery addresses now: %s.\nOther addresses now: %s') %\
          (deliveryAddresses, otherAddresses)
        assert type(self.status == unicode)
    
    def handle_set_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = _(u'There was an error:')
        else:
            self.status = _(u'<p>There were errors:</p>')
        
        