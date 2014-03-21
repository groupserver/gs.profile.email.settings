# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('groupserver')
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.profile.base import ProfileForm
from gs.profile.email.base.emailuser import EmailUser
from gs.profile.email.verify.emailverificationuser import EmailVerificationUser
from .interfaces import IGSEmailSettingsForm
from .groupsettings import GroupEmailSettings
from .update import RemoveUpdate, DeliveryUpdate
from .utils import markup_address

# TODO: Rewrite the status messages for an administrator adding an
# address.


class ChangeEmailSettingsForm(ProfileForm):
    form_fields = form.Fields(IGSEmailSettingsForm)
    label = _('Change Email Settings')
    pageTemplateFileName = 'browser/templates/settings.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    verifyMesg = _('An email has been sent to <strong>verify</strong> '
                    'that you control ')
    verifyCheckMesg =\
        _('<strong>Check</strong> your inbox (and Spam folder) for the '
            'email. ')

    def __init__(self, user, request):
        super(ChangeEmailSettingsForm, self).__init__(user, request)
        # These caches will be cleared when the form submits, so we
        #   do them in the non-@Lazy way.
        self.__otherAddresses = self.__deliveryAddresses = None
        self.__unverifiedAddresses = None

    @Lazy
    def emailUser(self):
        retval = EmailUser(self.context, self.userInfo)
        return retval

    @Lazy
    def groupSettings(self):
        retval = GroupEmailSettings(self.userInfo)
        return retval

    def setUpWidgets(self, ignore_request=False):  # FIXME: change to True?
        default_data = \
          {'deliveryAddresses': '\n'.join(self.deliveryAddresses),
           'otherAddresses': '\n'.join(self.otherAddresses)}
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.userInfo.user,
            self.request, data=default_data,
            ignore_request=False)

    @property
    def deliveryAddresses(self):
        if self.__deliveryAddresses is None:
            self.__deliveryAddresses = self.emailUser.get_delivery_addresses()
        return self.__deliveryAddresses

    @property
    def otherAddresses(self):
        if self.__otherAddresses is None:
            verifiedAddresses = self.emailUser.get_verified_addresses()
            self.__otherAddresses = \
              [a for a in verifiedAddresses if a not in self.deliveryAddresses]
        return self.__otherAddresses

    @property
    def unverifiedAddresses(self):
        if self.__unverifiedAddresses is None:
            self.__unverifiedAddresses = \
                self.emailUser.get_unverified_addresses()
        return self.__unverifiedAddresses

    @property
    def showOtherAddresses(self):
        retval = (len(self.deliveryAddresses) > 1) or self.otherAddresses
        return retval

    @form.action(label=_('Change'), failure='handle_failure')
    def handle_change(self, action, data):
        self.status = ''

        d = self.t_to_l(data.get('deliveryAddresses', ''))
        o = self.t_to_l(data.get('otherAddresses', ''))
        u = self.t_to_l(data.get('unverifiedAddresses', ''))
        d, o = self.fix_delivery(d, o)

        removeUpdate = self.remove_addresses(d, o, u)
        if removeUpdate.changed:
            self.add_to_status(unicode(removeUpdate))

        deliveryUpdate = self.update_delivery_addresses(d)
        if deliveryUpdate.changed:
            self.add_to_status(unicode(deliveryUpdate))

        self.__otherAddresses = self.__deliveryAddresses = None
        self.__unverifiedAddresses = None

        # Resend the verification message to an address
        if data.get('resendVerificationAddress', None):
            r = self.resend_verification(data['resendVerificationAddress'])
            self.add_to_status(r)

        assert type(self.status) == unicode

    def fix_delivery(self, deliveryAddresses, otherAddresses):
        newDelivery = deliveryAddresses
        newOther = otherAddresses
        if ((len(newDelivery) < 1) and (len(newOther) > 0)):
            newDelivery.append(newOther.pop())
        return (newDelivery, newOther)

    def add_to_status(self, msg):
        self.status = '%s<p>%s</p>' % (self.status, msg)

    @form.action(label=_('Add'), failure='handle_failure')
    def handle_add(self, action, data):
        self.status = ''

        address = data['newAddress']
        if address:
            e = markup_address(address)

            d = len(self.emailUser.get_delivery_addresses())
            isPreferred = d < 1
            self.emailUser.add_address(address, isPreferred)
            self.send_verification(address)

            m = _('The address ') + e + \
                _(' has been <strong>added</strong> to your '
                    'profile. ')
            self.add_to_status(m)

            n = self.verifyMesg + e + _('. ') + \
                self.verifyCheckMesg + _('You must follow the '
                    'instructions in the email before you can '
                    'use ') + e + _('. ')
            self.add_to_status(n)
        assert type(self.status) == unicode

    def handle_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = _('There was an error:')
        else:
            self.status = _('<p>There were errors:</p>')

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
        retval = self.verifyMesg + e + _('. ') + self.verifyCheckMesg
        assert type(retval) == unicode
        return retval

    def send_verification(self, address):
        emailVerificationUser = EmailVerificationUser(self.context,
                                    self.userInfo, address)
        emailVerificationUser.send_verification(self.request)

    def remove_addresses(self, deliveryAddresses, otherAddresses,
                            unverifiedAddresses):
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
