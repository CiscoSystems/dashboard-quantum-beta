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
from django.utils import simplejson
from django.utils.translation import ugettext as _

from django_quantum import forms

from django_openstack import api

from quantum.client import Client

import warnings


LOG = logging.getLogger('django_quantum.dash')

quantum = Client(settings.QUANTUM_URL, settings.QUANTUM_PORT, False, settings.QUANTUM_TENANT, 'json')

class CreateNetwork(forms.SelfHandlingForm):
    name = forms.CharField(required=True, label="Network Name")
    
    def handle(self, request, data):
        network_name = data['name']

        try:
            LOG.info('Creating network %s ' % network_name)
            send_data = {'network': {'net-name': '%s' % network_name}}
            quantum.create_network(send_data)
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
    network = forms.CharField(widget=forms.HiddenInput())

    def handle(self, request, data):
        try:
            LOG.info('Deleting network %s ' % data['network'])
            quantum.delete_network(data['network'])
        except Exception, e:
            messages.error(request,
                           'Unable to delete network %s: %s' %
                           (data['network'], e.message,))
        else:
            msg = 'Network %s has been deleted.' % data['network']
            LOG.info(msg)
            messages.success(request, msg)

        return shortcuts.redirect(request.build_absolute_uri())
    

class RenameNetwork(forms.SelfHandlingForm):
    network = forms.CharField(widget=forms.HiddenInput())
    new_name = forms.CharField(required=True)
    
    def handle(self, request, data):
        try:
            LOG.info('Renaming network %s to %s' % (data['network'], data['new_name']))
            send_data = {'network': {'net-name': '%s' % data['new_name']}}
            quantum.update_network(data['network'], send_data)
        except Exception, e:
            messages.error(request,
                           'Unable to rename network %s: %s' %
                           (data['network'], e.message,))
        else:
            msg = 'Network %s has been renamed to %s.' % (data['network'], data['new_name'])
            LOG.info(msg)
            messages.success(request, msg)

        return shortcuts.redirect(request.build_absolute_uri())


class CreatePort(forms.SelfHandlingForm):
    network = forms.CharField(widget=forms.HiddenInput())
    ports_num = forms.IntegerField(required=True, label="Number of Ports")
    
    def handle(self, request, data):
        try:
            LOG.info('Creating %s ports on network %s' % (data['ports_num'], data['network']))
            for i in range(0, data['ports_num']):
                quantum.create_port(data['network'])
        except Exception, e:
            messages.error(request,
                           'Unable to create ports on network %s: %s' %
                           (data['network'], e.message,))
        else:
            msg = '%s ports created on network %s.' % (data['ports_num'], data['network'])
            LOG.info(msg)
            messages.success(request, msg)
        return shortcuts.redirect(request.build_absolute_uri())
       
        
class DeletePort(forms.SelfHandlingForm):
    network = forms.CharField(widget=forms.HiddenInput())
    port = forms.CharField(widget=forms.HiddenInput())
    
    def handle(self, request, data):
        try:
            LOG.info('Deleting %s ports on network %s' % (data['port'], data['network']))
            quantum.delete_port(data['network'], data['port'])
        except Exception, e:
            messages.error(request,
                           'Unable to delete port %s: %s' %
                           (data['port'], e.message,))
        else:
            msg = 'Port %s deleted from network %s.' % (data['port'], data['network'])
            LOG.info(msg)
            messages.success(request, msg)
        return shortcuts.redirect(request.build_absolute_uri())


class AttachPort(forms.SelfHandlingForm):
    network = forms.CharField(widget=forms.HiddenInput())
    port = forms.CharField(widget=forms.HiddenInput())
    vif = forms.CharField(required=True, label="Select VIF to connect")
    
    def handle(self, request, data):
        try:
            LOG.info('Attaching %s port to VIF %s' % (data['port'], data['vif']))
            body = {'port': {'attachment-id': '%s' % data['vif']}}
            quantum.attach_resource(data['network'], data['port'], body)
        except Exception, e:
            messages.error(request,
                           'Unable to attach port %s to VIF %s: %s' %
                           (data['port'], data['vif'], e.message,))
        else:
            msg = 'Port %s connect to VIF %s.' % (data['port'], data['vif'])
            LOG.info(msg)
            messages.success(request, msg)
        return shortcuts.redirect(request.build_absolute_uri())
        

class DetachPort(forms.SelfHandlingForm):
    network = forms.CharField(widget=forms.HiddenInput())
    port = forms.CharField(widget=forms.HiddenInput())
    
    def handle(self, request, data):
        try:
            LOG.info('Detaching port %s' % data['port'])
            quantum.detach_resource(data['network'], data['port'])
        except Exception, e:
            messages.error(request,
                           'Unable to detach port %s: %s' %
                           (data['port'], e.message,))
        else:
            msg = 'Port %s detached.' % (data['port'])
            LOG.info(msg)
            messages.success(request, msg)
        return shortcuts.redirect(request.build_absolute_uri())
        
    
class TogglePort(forms.SelfHandlingForm):
    network = forms.CharField(widget=forms.HiddenInput())
    port = forms.CharField(widget=forms.HiddenInput())
    state = forms.CharField(widget=forms.HiddenInput())
    
    def handle(self, request, data):
        try:
            LOG.info('Toggling port state to %s' % data['state'])
            body = {'port': {'port-state': '%s' % data['state']}}
            quantum.set_port_state(data['network'], data['port'], body)
        except Exception, e:
            messages.error(request,
                           'Unable to set port state to %s: %s' %
                           (data['state'], e.message,))
        else:
            msg = 'Port %s state set to %s.' % (data['port'],data['state'])
            LOG.info(msg)
            messages.success(request, msg)
        return shortcuts.redirect(request.build_absolute_uri())
        
@login_required
def index(request, tenant_id):
    delete_form, delete_handled = DeleteNetwork.maybe_handle(request)
    network_form, create_handled = CreateNetwork.maybe_handle(request)
    rename_form, rename_handled = RenameNetwork.maybe_handle(request)
    
    networks = []
    instances = []
    
    try:
        networks_list = quantum.list_networks()
        details = []
        for network in networks_list['networks']:
            
            # Get all ports statistics for the network
            total = 0
            available = 0
            used = 0
            ports = quantum.list_ports(network['id'])
            for port in ports['ports']:
                total += 1
                # Get port details
                port_details = quantum.list_port_details(network['id'], port['id'])
                # Get port attachment
                port_attachment = quantum.list_port_attachments(network['id'], port['id'])
                if port_attachment['attachment'] == None:
                    available += 1
                else:
                    used += 1
            # Get network details like name and id
            details = quantum.list_network_details(network['id'])
            networks.append({
                'name' : details['network']['name'], 
                'id' : network['id'],
                'total' : total,
                'available' : available,
                'used' : used,
                'tenant' : tenant_id
            })
    
    except Exception, e:
        messages.error(request, 'Unable to get network list: %s' % e.message)

    return shortcuts.render_to_response('dash_networks.html', {
        'networks': networks,
        'network_form' : network_form,
        'delete_form' : delete_form,
        'rename_form' : rename_form,
    }, context_instance=template.RequestContext(request))


@login_required
def detail(request, tenant_id, network_id):
    create_port_form, create_handled  = CreatePort.maybe_handle(request)
    delete_port_form, delete_handled  = DeletePort.maybe_handle(request)
    attach_port_form, attach_handled  = AttachPort.maybe_handle(request)
    detach_port_form, detach_handled  = DetachPort.maybe_handle(request)
    toggle_port_form, port_toggle_handled = TogglePort.maybe_handle(request)
    
    network = {}
    network_ports = []
    
    try:
        network_details = quantum.list_network_details(network_id)
        network['name'] = network_details['network']['name']
        network['id'] = network_id
        # Get all ports on this network
        ports = quantum.list_ports(network_id)
        for port in ports['ports']:
            port_details = quantum.list_port_details(network_id, port['id'])
            # Get port attachments
            port_attachment = quantum.list_port_attachments(network_id, port['id'])
            # Find instance the attachment belongs to
            # Get all instances
            instances = api.server_list(request)
            connected_instance = None
            # Get virtual interface ids by instance
            for instance in instances:
                for vif in instance.virtual_interfaces:
                    if str(vif['id']) == str(port_attachment):
                        connected_instance = instance
                        break
            network_ports.append({
                'id' : port_details['port']['id'],
                'state' : port_details['port']['state'],
                'attachment' : port_attachment['attachment'],
                'instance' : instance
            })
        network['ports'] = network_ports
        
    except Exception, e:
        messages.error(request, 'Unable to get network details: %s' % e.message)

    return shortcuts.render_to_response('dash_networks_detail.html', {
        'network': network,
        'tenant' : tenant_id,
        'create_port_form' : create_port_form,
        'delete_port_form' : delete_port_form,
        'attach_port_form' : attach_port_form,
        'detach_port_form' : detach_port_form,
        'toggle_port_form' : toggle_port_form
    }, context_instance=template.RequestContext(request))


@login_required
def vif_ids(request):
    vifs = []
    attached_vifs = []
    
    try:
        # Get a list of all networks
        networks_list = quantum.list_networks()
        for network in networks_list['networks']:
            ports = quantum.list_ports(network['id'])
            # Get port attachments
            for port in ports['ports']:
                port_attachment = quantum.list_port_attachments(network['id'], port['id'])
                if port_attachment['attachment']:
                    attached_vifs.append(port_attachment['attachment'].encode('ascii'))
            # Get all instances
            instances = api.server_list(request)
            # Get virtual interface ids by instance
            for instance in instances:
                instance_vifs = instance.virtual_interfaces
                for vif in instance_vifs:
                    # Check if this VIF is already connected to any port
                    if str(vif['id']) in attached_vifs:
                        vifs.append({
                            'id' : vif['id'],
                            'instance' : instance.id,
                            'instance_name' : instance.name,
                            'available' : False,
                            'network_id' : vif['network']['id'],
                            'network_name' : vif['network']['label']
                        })
                    else:
                        vifs.append({
                            'id' : vif['id'],
                            'instance' : instance.id,
                            'instance_name' : instance.name,
                            'available' : True,
                            'network_id' : vif['network']['id'],
                            'network_name' : vif['network']['label']
                        })
        return http.HttpResponse(simplejson.dumps(vifs), mimetype='application/json')
    except Exception, e:
        messages.error(request, 'Unable to get virtual interfaces: %s' % e.message)
        return http.HttpResponse('Unable to get virtual interfaces: %s' % e.message, mimetype='application/json')
