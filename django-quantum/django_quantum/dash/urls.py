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

from django.conf.urls.defaults import *

NETWORKS = r'^(?P<tenant_id>[^/]+)/networks/(?P<network_id>[^/]+)/%s$'
PORTS = r'^(?P<tenant_id>[^/]+)/networks/(?P<network_id>)/ports/(?P<port_id>[^/]+)/%s$'

urlpatterns = patterns('django_quantum.dash.views.networks',
    url(r'^(?P<tenant_id>[^/]+)/networks/$', 'index', name='dash_networks'),
    url(NETWORKS % 'detail', 'detail', name='dash_networks_detail'),
)


urlpatterns += patterns('django_quantum.dash.views.ports',
    url(r'^(?P<tenant_id>[^/]+)/networks/(?P<network_id>)/ports/$', 'index', name='dash_ports'),
    url(PORTS % 'detail', 'detail', name='dash_ports_detail'),
    url(PORTS % 'attach', 'attach', name='dash_ports_attach'),
    url(PORTS % 'detach', 'detach', name='dash_ports_detach'),
    url(PORTS % 'extensions', 'extensions', name='dash_ports_extensions'),
)
