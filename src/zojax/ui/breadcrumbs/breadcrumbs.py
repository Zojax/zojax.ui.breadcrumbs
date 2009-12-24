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
from zope import interface
from zope.proxy import sameProxiedObjects
from zope.security.proxy import removeSecurityProxy
from zope.component import queryMultiAdapter
from zope.traversing.api import getPath, getParents
from zope.dublincore.interfaces import IDCTimes
from zope.app.component.hooks import getSite
from z3c.breadcrumb.interfaces import IBreadcrumb

from zojax.cache.view import cache


def BreadcrumbsContext(object, instance, *args, **kw):
    contexts = []
    for object in instance.objects:
        times = IDCTimes(object, None)
        if times is not None:
            contexts.append(times.modified)
    return {'context': getPath(instance.context),
            'contexts': tuple(contexts)}


class BreadcrumbsViewlet(object):

    def __init__(self, context, request, view, manager=None):
        context = removeSecurityProxy(context)
        objects = []
        vhr = request.getVirtualHostRoot()
        try:
            parents = [context] + list(getParents(context))
        except:
            site = getSite()
            parents = [site] + list(getParents(site))

        for obj in parents:
            objects.append(obj)
            if sameProxiedObjects(obj, vhr) or isinstance(obj, Exception):
                break

        objects.reverse()
        self.objects = objects

        super(BreadcrumbsViewlet, self).__init__(
            context, request, view, manager)

    def update(self):
        request = self.request

        crumbs = []
        for object in self.objects:
            info = queryMultiAdapter((object, request), IBreadcrumb)
            if info is None:
                continue
            crumbs.append({'name': info.name,
                           'url': info.url,
                           'activeURL': info.activeURL})

        self.crumbs = crumbs

    @cache('portal.breadcrumbs', BreadcrumbsContext)
    def __call__(self):
        return super(BreadcrumbsViewlet, self).__call__()
