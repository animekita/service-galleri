from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from forms import EditCollectionForm, CreateCollectionForm, \
     EditPhotographerForm, CreatePhotographerForm,\
     UploadImagesToForm, PictureForm
from models import Collection, Photographer, Picture

def list_collections(request,
                     template_name='gallery/list_collections.html'):

    return render_to_response(template_name,
                              {'collections' : Collection.objects.all(), },
                              context_instance=RequestContext(request))


def view_collection(request,
                    collection_id,
                    page=1,
                    template_name='gallery/view_collection.html'):

    collection = get_object_or_404(Collection, pk=collection_id)

    paginator = Paginator(collection.picture_set.all(), 12)

    try:
        page = paginator.page(int(page))
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    return render_to_response(template_name,
                              {'collection' : collection,
                               'paginator' : paginator,
                               'page' : page},
                              context_instance=RequestContext(request))

def view_picture(request,
                 picture_id,
                 template_name='gallery/view_picture.html'):

    import wingdbstub
    picture = get_object_or_404(Picture, pk=picture_id)

    collection = picture.collection

    pictures = collection.picture_set.all().values_list('pk')
    pictures = [values[0] for values in pictures]

    picture_position = pictures.index(picture.pk) + 1
    picture_count = len(pictures)

    if picture_position < picture_count:
        next_picture = pictures[picture_position]
    else:
        next_picture = None

    if picture_position > 1:
        prev_picture = pictures[picture_position-2]
    else:
        prev_picture = None

    # very ugly hack / workaround, we can't do this in the template
    breadcrumb = 'billede %s af %s' % (picture_position, picture_count)

    return render_to_response(template_name,
                              {'picture': picture,
                               'collection': collection,
                               'picture_position': picture_position,
                               'picture_count': picture_count,
                               'next_picture': next_picture,
                               'prev_picture': prev_picture,
                               'breadcrumb' : breadcrumb},
                              context_instance=RequestContext(request))


@login_required
def create_collection(request,
                      template_name='gallery/management/create_collection.html'):

    if request.method == 'POST':
        form = CreateCollectionForm(request.POST)

        if form.is_valid():
            collection = form.save()

            request.user.message_set.create(message=_(u'Event created'))
            return HttpResponseRedirect(reverse('gallery_create_collection'))

    else:
        form = CreateCollectionForm()

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))

def create_photographer(request,
                        template_name='gallery/management/create_photographer.html'):

    if request.method == 'POST':
        form = PhotographerForm(request.POST)

        if form.is_valid():
            photographer = form.save()

            request.user.message_set.create(message=_(u'Photographer created'))
            return HttpResponseRedirect(reverse('gallery_create_photographer'))

    else:
        form = PhotographerForm()

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required
def edit_collection(request,
                 collection_id,
                 template_name='gallery/management/edit_collection.html'):

    collection = get_object_or_404(Collection, pk=collection_id)

    if request.method == 'POST':
        form = EditCollectionForm(request.POST, instance=collection)

        if form.is_valid():
            form.save()

            url = reverse('gallery_view_collection', args=[collection.pk,])

            request.user.message_set.create(message=_(u'Collection edited'))
            return HttpResponseRedirect(url)

    else:
        form = EditCollectionForm(instance=collection)

    return render_to_response(template_name,
                              {'form': form,
                               'collection': collection},
                              context_instance=RequestContext(request))

@login_required
def edit_photographer(request,
                 photographer_id,
                 template_name='gallery/management/edit_photographer.html'):

    photographer = get_object_or_404(Photographer, pk=photographer_id)

    if request.method == 'POST':
        form = EditPhotographerForm(request.POST, instance=photographer)

        if form.is_valid():
            form.save()

            url = reverse('gallery_view_photographer', args=[photographer.pk,])

            request.user.message_set.create(message=_(u'Photographer edited'))
            return HttpResponseRedirect(url)

    else:
        form = EditPhotographerForm(instance=photographer)

    return render_to_response(template_name,
                              {'form': form,
                               'photographer': photographer},
                              context_instance=RequestContext(request))

@login_required
def edit_picture(request,
                 picture_id,
                 template_name='gallery/management/edit_image.html'):

    picture = get_object_or_404(Picture, pk=picture_id)

    if request.method == 'POST':
        form = PictureForm(request.POST, instance=picture)

        if form.is_valid():
            form.save()

            request.user.message_set.create(message=_(u'Picture edited'))
            return HttpResponseRedirect(reverse('gallery_edit_picture', args=picture.pk))

    else:
        form = PictureForm(instance=picture)

    return render_to_response(template_name,
                              {'form': form,
                               'picture': picture},
                              context_instance=RequestContext(request))

@login_required
def upload_images_step1(request,
                        template_name='gallery/management/upload_images_step1.html'):

    if request.method == 'POST':
        form = UploadImagesToForm(request.POST)

        if form.is_valid():
            url = reverse('gallery_upload_images_step2',
                          args=[form.cleaned_data['collection'].pk,
                                form.cleaned_data['photographer'].pk])

            return HttpResponseRedirect(url)

    else:
        form = UploadImagesToForm()

    return render_to_response(template_name,
                              {'form' : form},
                              context_instance=RequestContext(request))


@login_required
def upload_images_step2(request, collection_id, photographer_id,
                        template_name='gallery/management/upload_images_step2.html'):

    collection = get_object_or_404(Collection, pk=collection_id)
    photographer = get_object_or_404(Photographer, pk=photographer_id)

    return render_to_response(template_name,
                              {'collection' : collection,
                               'photographer' : photographer},
                              context_instance=RequestContext(request))

@csrf_exempt
def upload_images_callback(request, collection_id, photographer_id):

    collection = get_object_or_404(Collection, pk=collection_id)
    photographer = get_object_or_404(Photographer, pk=photographer_id)

    Picture.objects.create(original=request.FILES['Filedata'],
                           photographer=photographer,
                           collection=collection)

    return HttpResponse('1')
