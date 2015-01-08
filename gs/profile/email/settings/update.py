# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import absolute_import, unicode_literals
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('groupserver')
from gs.core import comma_comma_and, to_ascii
from .utils import markup_address


class RemoveUpdate(object):
    verifiedRemoveMessage = _('<strong>Removed</strong> the address ')
    unverifiedRemoveMessage = _('<strong>Removed</strong> the unverified '
                                'address ')
    profileMessage = _(' from your profile.')

    def __init__(self):
        self.verified = []
        self.unverified = []

    @property
    def changed(self):
        return bool(self.verified) or bool(self.unverified)

    def __unicode__(self):
        retval = ''
        if self.verified:
            e = comma_comma_and([markup_address(a) for a in self.verified])
            retval = self.verifiedRemoveMessage + e + self.profileMessage
        if self.unverified:
            e = comma_comma_and([markup_address(a)
                                 for a in self.unverified])
            retval = retval + self.unverifiedRemoveMessage + e + \
                self.profileMessage
        return retval

    def __str__(self):
        retval = to_ascii(unicode(self))
        return retval


class DeliveryUpdate(object):
    addedMessageA = _('<strong>Added</strong> the address ')
    addedMessageB = _(' to the list of preferred delivery addresses. ')
    removedMessageB = _(' to the list of your extra addresses. ')

    def __init__(self):
        self.added = []
        self.removed = []

    @property
    def changed(self):
        return bool(self.added) or bool(self.removed)

    def __unicode__(self):
        retval = ''
        if self.added:
            e = comma_comma_and([markup_address(a) for a in self.added])
            retval = self.addedMessageA + e + self.addedMessageB
        if self.removed:
            e = comma_comma_and([markup_address(a) for a in self.removed])
            # Yes, the retval starts with added message A
            retval += self.addedMessageA + e + self.removedMessageB
        return retval

    def __str__(self):
        retval = to_ascii(unicode(self))
        return retval
