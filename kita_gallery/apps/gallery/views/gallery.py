from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from kita_gallery.apps.gallery.models import Collection, Photographer, Picture

def list_collections(request,
                     template_name='gallery/list_collections.html'):

    return render_to_response(template_name,
                              {'collections' : Collection.objects.all(), },
                              context_instance=RequestContext(request))

def view_collection(request,
                    collection_slug,
                    page_number=1,
                    collection_class=Collection,
                    template_name='gallery/view_collection.html'):

    collection = get_object_or_404(collection_class, slug=collection_slug)

    paginator = Paginator(collection.picture_set.all(), 12)

    try:
        page = paginator.page(int(page_number))
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    return render_to_response(template_name,
                              {'collection' : collection,
                               'paginator' : paginator,
                               'page' : page,},
                              context_instance=RequestContext(request))

def view_photographer(request,
                      collection_slug,
                      page_number=1,
                      collection_class=Photographer,
                      template_name='gallery/view_photographer.html'):

    return view_collection(request, collection_slug, page_number,
                           collection_class, template_name)

def view_collection_picture(request,
                 picture_id,
                 collection_slug,
                 collection_class=Collection,
                 template_name='gallery/view_collection_picture.html'):

    picture = get_object_or_404(Picture, pk=picture_id)
    collection = get_object_or_404(collection_class, slug=collection_slug)

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

def view_photographer_picture(request,
                              picture_id,
                              collection_slug,
                              collection_class=Photographer,
                              template_name='gallery/view_photographer_picture.html'):

    return view_collection_picture(request,
                                   picture_id,
                                   collection_slug,
                                   collection_class,
                                   template_name)
