# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals, print_function
from zope.cachedescriptors.property import Lazy
from gs.content.form.api.json import EndpointMixin
from gs.profile.base import ProfileForm
from gs.profile.email.base.emailuser import EmailUser


class AddressForm(EndpointMixin, ProfileForm):
    '''An abstract base-class for forms that deal with email addresses.'''

    def __init__(self, profile, request):
        super(AddressForm, self).__init__(profile, request)

    @Lazy
    def emailUser(self):
        '''The gs.profile.email.base.EmailUser for the current user'''
        retval = EmailUser(self.context, self.userInfo)
        return retval

    def handle_failure(self, action, data, errors):
        retval = self.build_error_response(action, data, errors)
        return retval
