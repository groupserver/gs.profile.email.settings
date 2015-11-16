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
from zope.component import createObject, getMultiAdapter
from gs.core import comma_comma_and
from gs.group.member.email.base.interfaces import IGroupEmailUser
from gs.group.member.email.base import GroupEmailSetting
from .utils import markup_address
# TODO: Make a content provider
# TODO: Remove depricated code
# TODO: Make into an adaptor
# TODO: Move to gs.groups.member.email,
#                  ^^^^^^
#                  GroupS, not group.


class GroupEmailSettings(object):

    def __init__(self, userInfo):
        self.userInfo = userInfo
        self.context = self.userInfo.user
        self.__groupEmailSettings = None

    @Lazy
    def groupsInfo(self):
        retval = createObject('groupserver.GroupsInfo', self.context)
        return retval

    @Lazy
    def groupEmailSettings(self):
        folders = self.groupsInfo.get_member_groups_for_user(self.context,
                                                             self.userInfo.user)
        grps = [createObject('groupserver.GroupInfo', g) for g in folders]
        u = self.userInfo
        retval = [GroupEmailSettingInfo(self.context, g, u) for g in grps]
        assert type(retval) == list
        return retval

    def __len__(self):
        return len(self.groupEmailSettings)

    def __getitem__(self, key):
        return self.groupEmailSettings[key]

    def __iter__(self):
        return iter(self.groupEmailSettings)


class GroupEmailSettingInfo(object):
    """Information about a user's group email settings.

    ATTRIBUTES
      group:      Information about the group.
      setting:    The delivery setting for the user, as an integer.
                    0. No email delivery (Web only)
                    1. One email per post to the default address.
                    2. One email per post to a specific address.
                    3. Daily digest of topics.
      default:    True if the messages are sent to the user's default (alias
                  preferred) email addresses.
      addresses:  The address where posts are delivered.
    """

    def __init__(self, context, groupInfo, userInfo):
        self.groupInfo = groupInfo
        groupEmailUser = getMultiAdapter((userInfo, groupInfo), IGroupEmailUser,
                                         context=context)
        self.setting = groupEmailUser.get_delivery_setting()

        self.webOnly = self.setting == GroupEmailSetting.webonly
        self.email = self.setting in (GroupEmailSetting.specific, GroupEmailSetting.default)
        self.digest = self.setting == GroupEmailSetting.digest

        grpAddrs = groupEmailUser.get_specific_email_addresses()
        self.default = len(grpAddrs) == 0

        addrs = groupEmailUser.get_addresses()
        self.addresses = comma_comma_and([markup_address(a) for a in addrs])

        assert self.groupInfo
        assert self.groupInfo == groupInfo
