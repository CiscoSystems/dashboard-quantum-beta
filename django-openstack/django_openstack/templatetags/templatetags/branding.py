# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2011 Fourth Paradigm Development, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Template tags for working with django_openstack.
"""

from django import template
from django.conf import settings


register = template.Library()


class SiteBrandingNode(template.Node):
    def render(self, context):
        return settings.SITE_BRANDING


@register.tag
def site_branding(parser, token):
    return SiteBrandingNode()


# TODO(jeffjapan): This is just an assignment tag version of the above, replace
#                  when the dashboard is upgraded to a django version that
#                  supports the @assignment_tag decorator syntax instead.
class SaveBrandingNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = settings.SITE_BRANDING
        return ""


@register.tag
def save_site_branding(parser, token):
    tagname = token.contents.split()
    return SaveBrandingNode(tagname[-1])
