# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('groupserver')
from Products.XWFCore.XWFUtils import comma_comma_and
from utils import markup_address


class RemoveUpdate(object):
    verifiedRemoveMessage = _(u'<strong>Removed</strong> the address ')
    unverifiedRemoveMessage = _(u'<strong>Removed</strong> the '
        u'unverified address ')
    profileMessage = _(u' from your profile.')

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
            retval = self.verifiedRemoveMessage + e + self.profileMessage
        if self.unverified:
            e = comma_comma_and([markup_address(a) for a in self.unverified])
            retval = retval + self.unverifiedRemoveMessage + e + \
                        self.profileMessage
        assert type(retval) == unicode
        return retval

    def __str__(self):
        return unicode(self).encode('utf-8')


class DeliveryUpdate(object):
    addedMessageA = _(u'<strong>Added</strong> the address ')
    addedMessageB = _(u' to the list of preferred delivery addresses. ')
    removedMessageB = _(u' to the list of your extra addresses. ')

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
            retval = self.addedMessageA + e + self.addedMessageB
        if self.removed:
            e = comma_comma_and([markup_address(a) for a in self.removed])
            # Yes, the retval starts with added message A
            retval += self.addedMessageA + e + self.removedMessageB
        assert type(retval) == unicode
        return retval

    def __str__(self):
        return unicode(self).encode('utf-8')
