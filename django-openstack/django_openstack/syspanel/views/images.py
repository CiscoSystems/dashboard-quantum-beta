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

from django import template
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from glance.common import exception as glance_exception

from django_openstack import api
from django_openstack import forms


LOG = logging.getLogger('django_openstack.sysadmin.views.images')


class DeleteImage(forms.SelfHandlingForm):
    image_id = forms.CharField(required=True)

    def handle(self, request, data):
        image_id = data['image_id']
        try:
            api.image_delete(request, image_id)
        except glance_exception.ClientConnectionError, e:
            LOG.error("Error connecting to glance", exc_info=True)
            messages.error(request,
                           "Error connecting to glance: %s" % e.message)
        except glance_exception.Error, e:
            LOG.error('Error deleting image with id "%s"' % image_id,
                      exc_info=True)
            messages.error(request, "Error deleting image: %s" % e.message)
        return redirect(request.build_absolute_uri())


class ToggleImage(forms.SelfHandlingForm):
    image_id = forms.CharField(required=True)

    def handle(self, request, data):
        image_id = data['image_id']
        try:
            api.image_update(request, image_id, image_meta={'is_public': False})
        except glance_exception.ClientConnectionError, e:
            LOG.error("Error connecting to glance", exc_info=True)
            messages.error(request,
                           "Error connecting to glance: %s" % e.message)
        except glance_exception.Error, e:
            LOG.error('Error updating image with id "%s"' % image_id,
                      exc_info=True)
            messages.error(request, "Error updating image: %s" % e.message)
        return redirect(request.build_absolute_uri())


@login_required
def index(request):
    for f in (DeleteImage, ToggleImage):
        _, handled = f.maybe_handle(request)
        if handled:
            return handled

    # We don't have any way of showing errors for these, so don't bother
    # trying to reuse the forms from above
    delete_form = DeleteImage()
    toggle_form = ToggleImage()

    images = []
    try:
        images = api.image_list_detailed(request)
        if not images:
            messages.info(request, "There are currently no images.")
    except glance_exception.ClientConnectionError, e:
        LOG.error("Error connecting to glance", exc_info=True)
        messages.error(request, "Error connecting to glance: %s" % e.message)
    except glance_exception.Error, e:
        LOG.error("Error retrieving image list", exc_info=True)
        messages.error(request, "Error retrieving image list: %s" % e.message)

    return render_to_response('syspanel_images.html', {
        'delete_form': delete_form,
        'toggle_form': toggle_form,
        'images': images,
    }, context_instance = template.RequestContext(request))


@login_required
def update(request, image_id):
    try:
        image = api.image_get(request, image_id)
    except glance_exception.ClientConnectionError, e:
        LOG.error("Error connecting to glance", exc_info=True)
        messages.error(request, "Error connecting to glance: %s" % e.message)
    except glance_exception.Error, e:
        LOG.error('Error retrieving image with id "%s"' % image_id,
                  exc_info=True)
        messages.error(request,
                       "Error retrieving image %s: %s" % (image_id, e.message))

    if request.method == "POST":
        form = UpdateImageForm(request.POST)
        if form.is_valid():
            image_form = form.clean()
            metadata = {
                'is_public': image_form['is_public'],
                'disk_format': image_form['disk_format'],
                'container_format': image_form['container_format'],
                'name': image_form['name'],
                'location': image_form['location'],
            }
            try:
                # TODO add public flag to properties
                metadata['properties'] = {
                    'kernel_id': int(image_form['kernel_id']),
                    'ramdisk_id': int(image_form['ramdisk_id']),
                    'image_state': image_form['state'],
                    'architecture': image_form['architecture'],
                    'project_id': image_form['project_id'],
                }
                api.image_update(request, image_id, metadata)
                messages.success(request, "Image was successfully updated.")
            except glance_exception.ClientConnectionError, e:
                LOG.error("Error connecting to glance", exc_info=True)
                messages.error(request,
                               "Error connecting to glance: %s" % e.message)
            except glance_exception.Error, e:
                LOG.error('Error updating image with id "%s"' % image_id,
                          exc_info=True)
                messages.error(request, "Error updating image: %s" % e.message)
            except:
                LOG.error('Unspecified Exception in image update',
                          exc_info=True)
                messages.error(request,
                               "Image could not be updated, please try again.")

        else:
            LOG.error('Image "%s" failed to update' % image['name'],
                      exc_info=True)
            messages.error(request,
                           "Image could not be uploaded, please try agian.")
            form = UpdateImageForm(request.POST)
            return render_to_response('django_nova_syspanel/images/image_update.html',{
                'image': image,
                'form': form,
            }, context_instance = template.RequestContext(request))

        return redirect('syspanel_images')
    else:
        form = UpdateImageForm(initial={
                'name': image.get('name', ''),
                'kernel': image['properties'].get('kernel_id', ''),
                'ramdisk': image['properties'].get('ramdisk_id', ''),
                'is_public': image.get('is_public', ''),
                'location': image.get('location', ''),
                'state': image['properties'].get('image_state', ''),
                'architecture': image['properties'].get('architecture', ''),
                'project_id': image['properties'].get('project_id', ''),
                'container_format': image.get('container_format', ''),
                'disk_format': image.get('disk_format', ''),
            })

        return render_to_response('django_nova_syspanel/images/image_update.html',{
            'image': image,
            'form': form,
        }, context_instance = template.RequestContext(request))


@login_required
def upload(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST)
        if form.is_valid():
            image = form.clean()
            metadata = {'is_public': image['is_public'],
                        'disk_format': 'ami',
                        'container_format': 'ami',
                        'name': image['name']}
            try:
                messages.success(request, "Image was successfully uploaded.")
            except:
                # TODO add better error management
                messages.error(request, "Image could not be uploaded, please try again.")

            try:
                api.image_create(request, metadata, image['image_file'])
            except glance_exception.ClientConnectionError, e:
                LOG.error('Error connecting to glance while trying to upload'
                          ' image', exc_info=True)
                messages.error(request,
                               "Error connecting to glance: %s" % e.message)
            except glance_exception.Error, e:
                LOG.error('Glance exception while uploading image',
                          exc_info=True)
                messages.error(request, "Error adding image: %s" % e.message)
        else:
            LOG.error('Image "%s" failed to upload' % image['name'],
                      exc_info=True)
            messages.error(request,
                           "Image could not be uploaded, please try agian.")
            form = UploadImageForm(request.POST)
            return render_to_response('django_nova_syspanel/images/image_upload.html',{
                'form': form,
            }, context_instance = template.RequestContext(request))

        return redirect('syspanel_images')
    else:
        form = UploadImageForm()
        return render_to_response('django_nova_syspanel/images/image_upload.html',{
            'form': form,
        }, context_instance = template.RequestContext(request))
