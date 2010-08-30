from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlquote
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
from django.conf import settings
from django.utils.importlib import import_module

from kita_gallery.apps.gallery.forms import \
     EditCollectionForm, CreateCollectionForm, \
     EditPhotographerForm, CreatePhotographerForm,\
     UploadImagesToForm, LimitedEditPhotographerForm

from kita_gallery.apps.gallery.models import Collection, Photographer, Picture

def permission_denied(request):
    from django.contrib.auth import REDIRECT_FIELD_NAME
    login_url = settings.LOGIN_URL
    path = urlquote(request.get_full_path())
    tup = login_url, REDIRECT_FIELD_NAME, path
    return HttpResponseRedirect('%s?%s=%s' % tup)

def can_upload(user):
    if user.has_perm('gallery.add_picture'):
        return Photographer.objects.all()
    elif Photographer.objects.filter(user=user).exists():
        return Photographer.objects.filter(user=user)
    else:
        return None

def can_upload_as(user, photographer):
    photographers = can_upload(user)

    return photographers is not None and photographer in photographers

@login_required
@permission_required('gallery.add_collection')
def create_collection(request,
                      template_name='gallery/management/create_collection.html'):

    if request.method == 'POST':
        form = CreateCollectionForm(request.POST)

        if form.is_valid():
            collection = form.save()

            request.user.message_set.create(message=_(u'Event created'))
            return HttpResponseRedirect(reverse('gallery_view_collection',
                                                args=[collection.slug]))

    else:
        form = CreateCollectionForm()

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required
@permission_required('gallery.add_photographer')
def create_photographer(request,
                        template_name='gallery/management/create_photographer.html'):

    if request.method == 'POST':
        form = CreatePhotographerForm(request.POST)

        if form.is_valid():
            photographer = form.save()

            request.user.message_set.create(message=_(u'Photographer created'))
            return HttpResponseRedirect(reverse('gallery_view_photographer',
                                                args=[photographer.slug]))

    else:
        form = CreatePhotographerForm()

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required
@permission_required('gallery.change_collection')
def edit_collection(request,
                 collection_slug,
                 template_name='gallery/management/edit_collection.html'):

    collection = get_object_or_404(Collection, slug=collection_slug)

    if request.method == 'POST':
        form = EditCollectionForm(request.POST, instance=collection)

        if form.is_valid():
            form.save()

            url = reverse('gallery_view_collection', args=[collection.slug,])

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
                 photographer_slug,
                 template_name='gallery/management/edit_photographer.html'):

    photographer = get_object_or_404(Photographer, slug=photographer_slug)

    if not request.user.has_perm('gallery.change_photographer', photographer):
        return permission_denied(request)

    form_class = LimitedEditPhotographerForm

    if request.user.has_perm('gallery.add_photographer'):
        form_class = EditPhotographerForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=photographer)

        if form.is_valid():
            form.save()

            url = reverse('gallery_view_photographer', args=[photographer.slug,])

            request.user.message_set.create(message=_(u'Photographer edited'))
            return HttpResponseRedirect(url)

    else:
        form = form_class(instance=photographer)

    return render_to_response(template_name,
                              {'form': form,
                               'photographer': photographer},
                              context_instance=RequestContext(request))

@login_required
def upload_images_step1(request,
                        collection_slug,
                        template_name='gallery/management/upload_images_step1.html'):

    collection = get_object_or_404(Collection, slug=collection_slug)

    photographers = can_upload(request.user)

    if photographers is None:
        return permission_denied(request)

    if len(photographers) == 1:
        url = reverse('gallery_upload_images_step2',
                      args=[collection.slug, photographers[0].slug])
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = UploadImagesToForm(photographers, request.POST)

        if form.is_valid():
            url = reverse('gallery_upload_images_step2',
                          args=[collection.slug,
                                form.cleaned_data['photographer'].slug])

            return HttpResponseRedirect(url)

    else:
        form = UploadImagesToForm(photographers)

    return render_to_response(template_name,
                              {'form' : form,
                               'collection' : collection},
                              context_instance=RequestContext(request))


@login_required
def upload_images_step2(request,
                        collection_slug,
                        photographer_slug,
                        template_name='gallery/management/upload_images_step2.html'):

    collection = get_object_or_404(Collection, slug=collection_slug)
    photographer = get_object_or_404(Photographer, slug=photographer_slug)

    if not can_upload_as(request.user, photographer):
        return permission_denied(request)

    return render_to_response(template_name,
                              {'collection' : collection,
                               'photographer' : photographer,
                               'sessionid' : request.COOKIES['sessionid']},
                              context_instance=RequestContext(request))

@csrf_exempt
def upload_images_callback(request, collection_slug, photographer_slug):
    collection = get_object_or_404(Collection, slug=collection_slug)
    photographer = get_object_or_404(Photographer, slug=photographer_slug)

    sessionid = request.POST.get('sessionid', None)

    if sessionid is None:
        return HttpResponse('0')

    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore(sessionid)

    try:
        user_id = session[SESSION_KEY]
        backend_path = session[BACKEND_SESSION_KEY]

        backend = load_backend(backend_path)
        user = backend.get_user(user_id) or None
    except KeyError:
        return HttpResponse('0')

    if not user.is_authenticated() or \
       not can_upload_as(user, photographer):
        return HttpResponse('0')

    Picture.objects.create(original=request.FILES['Filedata'],
                           photographer=photographer,
                           collection=collection)

    return HttpResponse('1')