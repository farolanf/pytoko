
def get_upload_path(subdir, parent_attr=None):
    """
    Get upload path in the form of user_{id}/{subdir}/{filename}
    """

    def get_path(obj, filename):
        """
        Get user from the parent object if parent_attr is specified,
        otherwise assume user object is on the object itself.
        """
        user = None

        if parent_attr:
            if hasattr(obj, parent_attr):
                user = getattr(obj, parent_attr).user
        else:
            user = obj.user

        if not user:
            return '%s/%s' % (subdir, filename)

        return '%s_%s/%s/%s' % ('user', user.id, subdir, filename)
        
    return get_path