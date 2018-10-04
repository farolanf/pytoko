
def inject_test_methods(cls):
    """
    Create test methods on the derived class based on permission config.
    
    This is so test error reporting points to the derived class.
    """
    for action in cls.can:
        method = getattr(cls, 'can_%s' % action)
        setattr(cls, 'test_can_%s' % action, method)

    for action in cls.cannot:
        method = getattr(cls, 'cannot_%s' % action)
        setattr(cls, 'test_cannot_%s' % action, method)
