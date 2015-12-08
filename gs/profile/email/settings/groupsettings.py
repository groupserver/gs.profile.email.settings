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
from collections import Mapping
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope.component import createObject, getMultiAdapter
from gs.core import comma_comma_and
from gs.group.member.email.base.interfaces import IGroupEmailUser
from gs.group.member.email.base import GroupEmailSetting
from gs.profile.base import ProfileContentProvider
from .utils import markup_address
# TODO: Make into an adaptor
# TODO: Move to gs.groups.member.email,
#                  ^^^^^^
#                  GroupS, not group.


class GroupSettingsContentProvider(ProfileContentProvider):
    '''A content provider to list all the group email-settings'''

    def update(self):
        self.groupEmailSettings = GroupSettings(self.userInfo)

    def render(self):
        pageTemplate = ViewPageTemplateFile(self.pageTemplateFileName)
        r = pageTemplate(self)
        return r


class GroupSettings(Mapping):
    '''A mapping to provide the group email settings

:param Products.CustomUser.interfaces.IGSUserInfo userInfo: Information about the user.'''

    def __init__(self, userInfo):
        super(GroupSettings, self).__init__()
        self.userInfo = userInfo
        self.context = self.userInfo.user

    @Lazy
    def folders(self):
        'The folder-IDs (group IDs) for the groups the user is a member of, sorted by ID'
        # --=mpj17=-- Use the folder-IDs rather than the group objects because it uses less
        # memory.
        groupsInfo = createObject('groupserver.GroupsInfo', self.context)
        retval = groupsInfo.get_member_groups_for_user(self.context, self.userInfo.user)
        sorted(retval)
        return retval

    def __len__(self):
        # For the collections.Sized ABC
        return len(self.folders)

    def __iter__(self):
        # For the collections.Itterable ABC
        for folder in self.folders:
            yield self[folder]

    def __contains__(self, key):
        # For the collections.Container ABC
        retval = key in self.folders
        return retval

    def __getitem__(self, key):
        # For the collections.Mapping ABC
        if key not in self:
            raise KeyError(key)
        grp = createObject('groupserver.GroupInfo', key)
        retval = GroupSettingInfo(self.context, grp, self.userInfo)
        return retval


class GroupSettingInfo(object):
    """Information about a user's group email settings.

:param context: The context for the object
:param Products.GSGroup.interfaces.IGSGroupInfo groupInfo: Information about the group.
:param Products.CustomUser.interfaces.IGSUserInfo userInfo: Information about the user."""
    def __init__(self, context, groupInfo, userInfo):
        self.context = context
        self.groupInfo = groupInfo
        self.userInfo = userInfo

    @Lazy
    def groupEmailUser(self):
        retval = getMultiAdapter((self.userInfo, self.groupInfo), IGroupEmailUser,
                                 context=self.context)
        return retval

    @Lazy
    def setting(self):
        '''The delivery setting for the user

:returns: The delivery setting for the user in the group
:rtype: :class:`Setting`'''
        retval = self.groupEmailUser.get_delivery_setting()
        return retval

    @Lazy
    def webOnly(self):
        return self.setting == GroupEmailSetting.webonly

    @Lazy
    def oneEmailPerPost(self):
        return self.setting in (GroupEmailSetting.specific, GroupEmailSetting.default)

    @Lazy
    def digest(self):
        return self.setting == GroupEmailSetting.digest

    @Lazy
    def defaultAddr(self):
        '''True if the messages are sent to the user's default (alias preferred) email addresses.'''
        grpAddrs = self.groupEmailUser.get_specific_email_addresses()
        retval = len(grpAddrs) == 0
        return retval

    @Lazy
    def addresses(self):
        'The address where posts are delivered.'
        addrs = self.groupEmailUser.get_addresses()
        retval = comma_comma_and([markup_address(a) for a in addrs])
        return retval
