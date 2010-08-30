from django import template

from kita_gallery.apps.gallery.views.management import can_upload

register = template.Library()

def _is_quoted(string):
    return string[0] == '"' and string[-1] == '"'

class HasObjectPermNode(template.Node):
    def __init__(self, user, perm, obj, varname):
        self.user = template.Variable(user)
        self.perm = perm
        self.obj = template.Variable(obj)
        self.varname = varname

    def render(self, context):
        user = self.user.resolve(context)
        obj = self.obj.resolve(context)

        if user.is_authenticated():
            context[self.varname] = user.has_perm(self.perm, obj)
        else:
            context[self.varname] = False

        return ''

@register.tag('has_obj_perm')
def do_has_obj_perm(parser, token):
    """
    Usage {% has_obj_perm user "gallery.change_collection" collection_obj as has_perm %}
    """

    try:
        tokens = token.split_contents()
        tag_name = tokens[0]
        args = tokens[1:]
    except (ValueError, IndexError):
        raise template.TemplateSyntaxError('%r tag requires arguments.' % tag_name)

    if _is_quoted(args[0]) or not _is_quoted(args[1]) or _is_quoted(args[2]) \
        or args[3] != 'as' or _is_quoted(args[4]):
        raise template.TemplateSyntaxError('%r tag had invalid argument.' % tag_name)

    return HasObjectPermNode(args[0], args[1][1:-1], args[2], args[4])

class CanUploadNode(template.Node):
    def __init__(self, user, varname):
        self.user = template.Variable(user)
        self.varname = varname

    def render(self, context):
        user = self.user.resolve(context)

        if user.is_authenticated():
            context[self.varname] = can_upload(user) is not None
        else:
            context[self.varname] = False

        return ''

@register.tag('can_upload')
def do_can_upload(parser, token):
    """
    Usage {% can_upload user as has_upload_permission %}
    """

    try:
        tokens = token.split_contents()
        tag_name = tokens[0]
        args = tokens[1:]
    except (ValueError, IndexError):
        raise template.TemplateSyntaxError('%r tag requires arguments.' % tag_name)

    if _is_quoted(args[0]) or args[1] != 'as' or _is_quoted(args[2]):
        raise template.TemplateSyntaxError('%r tag had invalid argument.' % tag_name)

    return CanUploadNode(args[0], args[2])
