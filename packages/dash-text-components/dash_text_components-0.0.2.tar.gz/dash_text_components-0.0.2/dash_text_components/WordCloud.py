# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class WordCloud(Component):
    """A WordCloud component.
WordCloud is a component that displays words with sizes proportional 
to their frequencies or weights.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- clickedWord (string; optional):
    The word that was clicked in the cloud.

- style (dict; optional):
    Custom CSS styles to apply to the WordCloud container.

- words (list of dicts; optional):
    Array of word objects, each containing text and weight. Example:
    [{ text: \"hello\", weight: 5 }, { text: \"world\", weight: 3 }].

    `words` is a list of dicts with keys:

    - text (string; required)

    - weight (number; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_text_components'
    _type = 'WordCloud'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, words=Component.UNDEFINED, clickedWord=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'clickedWord', 'style', 'words']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'clickedWord', 'style', 'words']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(WordCloud, self).__init__(**args)
