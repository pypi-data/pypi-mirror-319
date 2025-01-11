# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class interactive_graph(Component):
    """An interactive_graph component.


Keyword arguments:

- id (string; required)

- chartType (a value equal to: 'categorical', 'continuous'; optional)

- data (list of dicts; required)

    `data` is a list of dicts with keys:

    - x (string | number; required)

    - y (number; required)

- height (number; default 500)

- smoothingFactor (number; optional)

- smoothingType (string; default "bellcurve")

- width (number; default 500)

- xLabel (string; default "X Axis Label")

- yLabel (string; default "Y Axis Label")"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'i2dgraph'
    _type = 'interactive_graph'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, width=Component.UNDEFINED, height=Component.UNDEFINED, xLabel=Component.UNDEFINED, yLabel=Component.UNDEFINED, data=Component.REQUIRED, chartType=Component.UNDEFINED, smoothingType=Component.UNDEFINED, smoothingFactor=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'chartType', 'data', 'height', 'smoothingFactor', 'smoothingType', 'width', 'xLabel', 'yLabel']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'chartType', 'data', 'height', 'smoothingFactor', 'smoothingType', 'width', 'xLabel', 'yLabel']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(interactive_graph, self).__init__(**args)
