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

import logging

from django import utils
from django.conf import settings
from django.contrib import messages
from django.forms import widgets
from django.utils import dates
from django.utils import safestring
from django.utils import formats

from django.forms import *

LOG = logging.getLogger('django_quantum.forms')

class SelfHandlingForm(Form):
    method = CharField(required=True, widget=HiddenInput)

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        initial['method'] = self.__class__.__name__
        kwargs['initial'] = initial
        super(SelfHandlingForm, self).__init__(*args, **kwargs)

    @classmethod
    def maybe_handle(cls, request, *args, **kwargs):
        if cls.__name__ != request.POST.get('method'):
            return cls(*args, **kwargs), None

        try:
            if request.FILES:
                form = cls(request.POST, request.FILES, *args, **kwargs)
            else:
                form = cls(request.POST, *args, **kwargs)

            if not form.is_valid():
                return form, None

            data = form.clean()

            return form, form.handle(request, data)
        except Exception as e:
            LOG.error('Nonspecific error while handling form', exc_info=True)
            messages.error(request, 'Unexpected error: %s' % e.message)
            return form, None
