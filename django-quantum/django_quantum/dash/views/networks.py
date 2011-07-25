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
Views for managing Quantum networks.
"""
import logging

from django import http
from django import shortcuts
from django import template
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from django_quantum import forms

from quantum.client import Client

LOG = logging.getLogger('django_quantum.dash')

quantum = Client(settings.QUANTUM_URL, settings.QUANTUM_PORT, False, settings.QUANTUM_TENANT, 'json')

class CreateNetwork(forms.SelfHandlingForm):
    name = forms.CharField(required=True)

    def handle(self, request, data):
        network_name = data['name']

        try:
            quantum.create_network(request, network_name)
        except Exception, e:
            messages.error(request,
                           'Unable to create network %s: %s' %
                           (network_name, e.message,))
        else:
            msg = 'Network %s has been created.' % network_name
            LOG.info(msg)
            messages.success(request, msg)

        return shortcuts.redirect(request.build_absolute_uri())


class DeleteNetwork(forms.SelfHandlingForm):
    network_id = forms.CharField(required=True)

    def handle(self, request, data):
        try:
            quantum.delete_network(network_id)
        except Exception, e:
            messages.error(request,
                           'Unable to delete network %s: %s' %
                           (network_id, e.message,))
        else:
            msg = 'Network %s has been deleted.' % network_id
            LOG.info(msg)
            messages.success(request, msg)

        return shortcuts.redirect(request.build_absolute_uri())
    

@login_required
def index(request, tenant_id):
    networks = []
    
    try:
        networks_list = quantum.list_networks()
        details = []
        for network in networks_list['networks']:
            details = quantum.list_network_details(network['id'])
            networks.append({'name' : details['networks']['network']['name'], 
                           'id' : network['id']})
    except Exception, e:
        messages.error(request, 'Unable to get network list: %s' % e.message)

    return shortcuts.render_to_response('dash_networks.html', {
        'networks': networks,
    }, context_instance=template.RequestContext(request))


@login_required
def detail(request, tenant_id, network_id):
    network = []
    
    try:
        network = quantum.list_network_details(network_id)
    except Exception, e:
        messages.error(request, 'Unable to get network details: %s' % e.message)

    return shortcuts.render_to_response('dash_networks_detail.html', {
        'network': network,
    }, context_instance=template.RequestContext(request))
