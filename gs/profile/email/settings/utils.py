# -*- coding: utf-8 -*-


def markup_address(address):
    r = u'<code class="email">{0}</code>'
    retval = r.format(address)
    return retval
