class PhotographerPermissionBackend:
    supports_object_permissions = True
    supports_anonymous_user = False

    def authenticate(self, token=None):
        return None

    def get_user(self, user_id):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        if obj is None:
            return False

        module, action_klass = perm.split('.')

        if module != 'gallery':
            return False

        action, klass = action_klass.split('_')

        if action == 'change' and klass == 'photographer':
            return obj.user is not None and obj.user == user_obj
