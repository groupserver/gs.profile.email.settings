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
from json import dumps as to_json
from gs.profile.base import ProfilePage
from gs.profile.json import email_info


class Status(ProfilePage):

    def __init__(self, profile, request):
        super(Status, self).__init__(profile, request)

    def __call__(self):
        self.request.response.setHeader(b'Content-Type', b'application/json')
        r = email_info(self.siteInfo, self.userInfo)
        retval = to_json(r)
        return retval
