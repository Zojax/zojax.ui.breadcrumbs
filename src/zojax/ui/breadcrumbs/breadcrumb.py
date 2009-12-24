##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
"""

$Id$
"""
from zope import interface, component
from zope.i18nmessageid import MessageFactory
from zope.traversing.browser import absoluteURL
from zope.traversing.interfaces import IContainmentRoot
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.dublincore.interfaces import IDCDescriptiveProperties
from z3c.breadcrumb.interfaces import IBreadcrumb

_ = MessageFactory('zojax.ui.breadcrumbs')


class GenericBreadcrumb(object):
    interface.implements(IBreadcrumb)
    component.adapts(interface.Interface, IBrowserRequest)

    activeURL = True

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def name(self):
        dc = IDCDescriptiveProperties(self.context, None)
        if dc is not None:
            name = dc.title
        else:
            name = getattr(self.context, 'title', '')
        if not name:
            name = getattr(self.context, '__name__', '')
        if not name and IContainmentRoot.providedBy(self.context):
            name = _('top')
        return name

    @property
    def url(self):
        return '%s/'%absoluteURL(self.context, self.request)
