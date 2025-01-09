# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AttentionHighlight(Component):
    """An AttentionHighlight component.
AttentionHighlight is a component that displays tokens and highlights related words
based on attention weights when hovering over a token.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- attentionMatrix (list of list of numberss; optional):
    Matrix of attention weights. Should be a 2D array where
    attentionMatrix[i][j] represents the attention weight from token i
    to token j. Values should be between 0 and 1.

- tokens (list of strings; optional):
    Array of tokens to display."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_text_components'
    _type = 'AttentionHighlight'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, tokens=Component.UNDEFINED, attentionMatrix=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'attentionMatrix', 'tokens']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'attentionMatrix', 'tokens']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AttentionHighlight, self).__init__(**args)
