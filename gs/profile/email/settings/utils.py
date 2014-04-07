# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def markup_address(address):
    r = '<code class="email">{0}</code>'
    retval = r.format(address)
    return retval
