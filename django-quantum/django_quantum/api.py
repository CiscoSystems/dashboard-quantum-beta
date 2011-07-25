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
Api wrapper around the quantum client.
"""
import logging

from quantum.client import Client
from django.conf import settings

class Api(Client):
    """ Wrapper around the base quantum client with some default values"""
    def __init__(self, host=settings.QUANTUM_URL, port=settings.QUANTUM_PORT, use_ssl=False, tenant=settings.QUANTUM_TENANT, format='json'):
        Client.__init__(self, host, port, use_ssl, tenant, format)
