
def get_upload_path(subdir, parent_attr=None):
    """
    Get upload path in the form of user_{id}/{subdir}/{filename}
    """

    def get_path(obj, filename):
        """
        Get user from the parent object if parent_attr is specified,
        otherwise assume user object is on the object itself.

        Throws error if parent_attr doesn't exist.
        
        Ignore if user doesn't exist.
        """
        user = None

        if parent_attr:
            parent = getattr(obj, parent_attr)
            user = getattr(parent, 'user', None)
        else:
            user = getattr(obj, 'user', None)

        if not user:
            return '%s/%s' % (subdir, filename)

        return '%s_%s/%s/%s' % ('user', user.id, subdir, filename)
        
    return get_path