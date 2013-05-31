# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.XWFCore.XWFUtils import comma_comma_and
from utils import markup_address
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
        retval = [GroupEmailSetting(g, u) for g in grps]
        assert type(retval) == list
        return retval

    def __len__(self):
        return len(self.groupEmailSettings)

    def __getitem__(self, key):
        return self.groupEmailSettings[key]

    def __iter__(self):
        return iter(self.groupEmailSettings)


class GroupEmailSetting(object):
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

    def __init__(self, groupInfo, userInfo):
        assert groupInfo
        assert userInfo
        self.groupInfo = groupInfo
        user = userInfo.user
        self.setting = user.get_deliverySettingsByKey(groupInfo.id)
        assert self.setting in range(0, 4)

        self.webOnly = self.setting == 0
        self.email = self.setting in (1, 2)
        self.digest = self.setting == 3

        grpAddrs = user.get_specificEmailAddressesByKey(groupInfo.id)
        self.default = len(grpAddrs) == 0

        addrs = user.get_deliveryEmailAddressesByKey(groupInfo.id)
        self.addresses = comma_comma_and([markup_address(a) for a in addrs])

        assert self.groupInfo
        assert self.groupInfo == groupInfo
        assert type(self.setting) == int

        assert type(self.addresses) in (str, unicode)
