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
Views for managing Quantum network ports.
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


class CreatePort(forms.SelfHandlingForm):
    pass


class DeletePort(forms.SelfHandlingForm):
    pass
    

@login_required
def index(request, tenant_id, network_id):
    pass


@login_required
def detail(request, tenant_id, network_id, port_id):
    pass


@login_required
def attach(request, tenant_id, network_id, port_id):
    pass
    

@login_required
def detach(request, tenant_id, network_id, port_id):
    pass
    
    
@login_required
def extensions(request, tenant_id, network_id, port_id):
    pass
