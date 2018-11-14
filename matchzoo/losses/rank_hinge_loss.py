import numpy as np

from keras import layers, backend as K


class RankHingeLoss(object):
    def __init__(self, num_neg=1, margin=1.0):
        self._num_neg = num_neg
        self._margin = margin

    def __call__(self, y_true: np.array, y_pred: np.array) -> np.array:
        """
        Calculate rank hinge loss.

        Support user defined :attr:`margin` and :attr:`neg_num`.

        :param y_true: Label.
        :param y_pred: Predicted result.
        :return: Hinge loss computed by user-defined margin.
        """

        y_pos = layers.Lambda(lambda a: a[::(self._num_neg + 1), :],
                              output_shape=(1,))(y_pred)
        y_neg = []
        for neg_idx in range(self._num_neg):
            y_neg.append(
                layers.Lambda(
                    lambda a: a[(neg_idx + 1)::(self._num_neg + 1), :],
                    output_shape=(1,))(y_pred))
        y_neg = K.mean(K.concatenate(y_neg, axis=-1), axis=-1, keepdims=True)
        loss = K.maximum(0., self._margin + y_neg - y_pos)
        return K.mean(loss)
