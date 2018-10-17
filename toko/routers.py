from rest_framework.routers import Route, DynamicRoute, SimpleRouter

class AppRouter(SimpleRouter):

    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Creation route.
        Route(
            url=r'^{prefix}/new{trailing_slash}$',
            mapping={
                'get': 'new',
                'post': 'create'
            },
            name='{basename}-new',
            detail=False,
            initkwargs={'suffix': 'New'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Editing route.
        Route(
            url=r'^{prefix}/{lookup}/edit{trailing_slash}$',
            mapping={
                'get': 'edit',
                'put': 'update',
                'patch': 'partial_update',
            },
            name='{basename}-edit',
            detail=True,
            initkwargs={'suffix': 'Edit'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]
