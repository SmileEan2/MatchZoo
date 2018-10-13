"""An implementation of MultiPerspectiveLayer for Bimpm model."""

from keras import layers
from keras import backend as K
from keras.engine.topology import Layer


class MultiPerspectiveLayer(Layer):
    """
    A keras implementation of Bimpm multi-perspective layer.

    For detailed information, see Bilateral Multi-Perspective
    Matching for Natural Language Sentences, section 3.2.
    """

    def __init__(
        self,
        output_dim: int,
        strategies: dict={'full': True,
                          'maxpooling': True,
                          'attentive': True,
                          'max-attentive': True},
        **kwargs
    ):
        """
        Class initialization.

        :param output_dim: dimensionality of output space.
        """
        self._output_dim = output_dim
        self._strategies = strategies
        super(MultiPerspectiveLayer, self).__init__(**kwargs)

        @classmethod
        def list_available_strategies(cls) -> list:
            """List available strategies for multi-perspective matching."""
            return ['full', 'maxpooling', 'attentive', 'max-attentive']

        @property
        def num_perspectives(self):
            return sum(self._strategies.values())

        def build(self, input_shape: list):
            """Input shape."""
            if self._strategies.get('full'):
                self.full = self.add_weight(name='pool',
                                            shape=(
                                                input_shape[0][1], self.output_dim),
                                            initializer='uniform',
                                            trainable=True)
            if self._strategies.get('maxpooling'):
                self.maxp = self.add_weight(name='maxpooling',
                                            shape=(
                                                input_shape[0][1], self._output_dim),
                                            initializer='uniform',
                                            trainable=True)
            if self._strategies.get('attentive'):
                self.atte = self.add_weight(name='attentive',
                                            shape=(
                                                input_shape[0][1], self._output_dim),
                                            initializer='uniform',
                                            trainable=True)
            if self._strategies.get('max-attentive'):
                self.maxa = self.add_weight(name='max-attentive',
                                            shape=(
                                                input_shape[0][1], self._output_dim),
                                            initializer='uniform',
                                            trainable=True)
            super(MultiPerspectiveLayer, self).build(input_shape)

    def call(self, x: list):
        out = [] # out is a l by d dimensional matrix, l is number of active perspectives.

        # seq_left is the sequence of vectors of current sentence at all time steps.
        # seq_right is the sequence of vectors of the other sentence at all time steps.
        seq_left, seq_right = x
        if self._strategies.get('full'):
            # each forward & backward contextual embedding compare
            # with the last step of the last time step of the other sentence.
            pass
        if self._strategies.get('maxpooling'):
            # each contextual embedding compare with each contextual embedding.
            # retain the maximum of each dimension.
            pass
        if self._strategies.get('attentive'):
            # each contextual embedding compare with each contextual embedding.
            # retain sum of weighted mean of each dimension.
            pass
        if self._strategies.get('max-attentive'):
            # each contextual embedding compare with each contextual embedding.
            # retain max of weighted mean of each dimension.
            pass 

        return out

    def compute_output_shape(self, input_shape: list):
        shape_a, shape_b = input_shape
        return [(shape_a[0], self._output_dim), shape_b[:-1]]
