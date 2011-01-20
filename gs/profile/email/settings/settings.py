#coding=utf-8
from zope.formlib import form
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
        
    @form.action(label=_(u'Change'), failure='handle_set_action_failure')
    def handle_set(self, action, data):
        self.status = _(u'Something changed!')
        assert type(self.status == unicode)
    
    def handle_set_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = _(u'There was an error:')
        else:
            self.status = _(u'<p>There were errors:</p>')
        
        