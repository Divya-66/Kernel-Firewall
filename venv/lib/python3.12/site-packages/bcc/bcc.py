# -*- coding: utf-8 -*-
"""Main module."""

import numpy as np
import traitlets as tl
import traittypes as tt

try:
    import numba
    from numba.types import float64, float32
    jit = numba.njit(nogil=True, fastmath=True)

    def guvec(sigs, layout, func):
        return numba.guvectorize(
            sigs, layout, nopython=1, fastmath=1)(func)  # nogil not supported

except ImportError:
    import numpy
    import pytest
    float64 = float32 = numpy.empty((1, 1, 1, 1, 1, 1, 1))
    jit = lambda f: None

    def guvec(sigs, layout, func):
        return None


# numba closure-based versions


@jit
def _numba_get_bin_indices(value, ndim, lower, width):
    tmp = value.copy()
    tmp -= lower
    tmp /= width
    indices = tmp.astype(np.int64)
    tmp -= indices + 0.5
    corner_indices = indices - (tmp < 0)
    parity = 0.25 * ndim < np.sum(np.sign(tmp) * tmp)
    indices = corner_indices if parity else indices
    return indices, parity


def _kernel_bcc_indexer(sizes, lower, upper):
    sizes = np.asarray(sizes)
    lower = np.asarray(lower)
    upper = np.asarray(upper)
    ndim = len(sizes)
    width = (upper - lower) / sizes
    sizes = sizes + 2

    @jit
    def func(value, res):
        assert value.ndim == 1
        indices, parity = _numba_get_bin_indices(value, ndim, lower, width)
        indices += 1
        nside_prod = np.ones(ndim, dtype=np.int64)
        nside_prod[1:] = np.cumprod(sizes[:-1])
        index = np.sum(nside_prod * indices)
        res[0] = np.left_shift(index, 1) + parity

    return func


def gu_bcc_indexer(*args, **kw):
    func = _kernel_bcc_indexer(*args, **kw)
    return guvec([(float64[:], float64[:])], '(n)->()', func)


def numba_bcc_indexer(*args, **kw):
    func0 = _kernel_bcc_indexer(*args, **kw)

    @jit
    def func(value):
        res = np.empty(1, dtype=np.int64)
        func0(value, res)
        return res[0]

    return func


##################### crappy Traitlets stuff #####################


class PositiveInt(tl.Int):
    def info(self):
        return u'a positive integer'

    def validate(self, obj, proposal):
        super().validate(obj, proposal)
        if proposal <= 0:
            self.error(obj, proposal)
        return proposal


class PositiveFloat(tl.Float):
    def info(self):
        return u'a positive float'

    def validate(self, obj, proposal):
        super().validate(obj, proposal)
        if proposal <= 0.0:
            self.error(obj, proposal)
        return proposal


class BCC(tl.HasTraits):
    """BCC lattice maps voronoi cells to bin ids
        DOES THE GEOMETRIC WINDOW DEFINE THE GRID, OR
                 1:N contiguous
        option 1: all idx in range(0, len(binner)) valid
        option 2: all points in [lower, upper] have valid indices
        ARE THESE MUTUALLY EXCLUSIVE????
    """
    ndim = PositiveInt()
    sizes = tt.Array(dtype='u8')  # (upper-lower)/width
    nside = tt.Array(dtype='u8')  # 1 + sizes + 1 (for boundary)
    lower = tt.Array(dtype='f8')
    upper = tt.Array(dtype='f8')
    width = tt.Array(dtype='f8')

    def get_bin_index(self, value):
        indices, parity = self._get_bin_indices(value)
        indices += 1
        index = np.sum(self._nside_prod() * indices, axis=-1)
        return np.left_shift(index, 1) + parity

    def get_bin_center(self, index):
        index = np.asarray(index, dtype='i8')
        parity = np.bitwise_and(index, 1)
        indices = np.mod(
            np.right_shift(index, 1)[..., np.newaxis] // self._nside_prod(),
            self.nside)
        indices -= 1
        return self._get_bin_center_from_indices(indices, parity)

    def __len__(self):
        return np.prod(self.nside)

    if 1:  # 'HIDDEN METHODS'

        def _get_bin_indices(self, value):
            value = np.asarray(value)
            tmp = value.copy()
            tmp -= self.lower
            tmp /= self.width
            indices = tmp.astype('i8')
            tmp -= indices + 0.5
            corner_indices = indices - (tmp < 0)
            parity = 0.25 * self.ndim < np.sum(np.sign(tmp) * tmp, axis=-1)
            indices = np.where(parity[..., np.newaxis], corner_indices,
                               indices)
            return indices, parity

        def _nside_prod(self):
            _nside_prod = np.ones(self.ndim, dtype='i8')
            _nside_prod[1:] = np.cumprod(self.nside[:-1])
            return _nside_prod

        def _get_bin_center_from_indices(self, indices, parity):
            cen = (self.lower + self.width / 2 + self.width * indices +
                   np.where(parity[..., np.newaxis], self.width / 2.0, 0.0))
            return cen

        @tl.default('ndim')
        def _default_ndim(self):
            if len(self.sizes.shape) is not 1 or self.sizes.shape[0] < 3:
                raise tl.TraitError('sizes must have shape (ndim>=3,)')
            return self.sizes.shape[0]

        @tl.default('sizes')
        def _default_sizes(self):
            raise tl.TraitError('sizes must be specified')

        @tl.default('lower')
        def _default_lower(self):
            return np.zeros((self.ndim, ))

        @tl.default('upper')
        def _default_upper(self):
            return np.ones((self.ndim, ))

        @tl.default('width')
        def _default_width(self):
            return (self.upper - self.lower) / self.sizes

        @tl.default('nside')
        def _default_nside(self):
            return self.sizes + 2

        @tl.validate('sizes')
        def _validate_sizes(self, proposal):
            return proposal['value']

        @tl.validate('nside')
        def _validate_nside(self, proposal):
            if not np.all(proposal['value'] == self.sizes + 2):
                raise tl.TraitError('bad nside, should be sizes + 2')
            return proposal['value']

        @tl.validate('lower')
        def _validate_lower(self, proposal):
            lower = proposal['value']
            if (self.sizes.shape != lower.shape):
                err = 'sizes and lower must have same shape. '
                err += 'sizes.shape: %s, lower.shape: %s' % (self.sizes.shape,
                                                             lower.shape)
                raise tl.TraitError(err)
            with self.hold_trait_notifications():
                if np.any(lower >= self.upper):
                    raise tl.TraitError('lower >= upper!')
            return lower

        @tl.validate('upper')
        def _validate_upper(self, proposal):
            upper = proposal['value']
            if (self.sizes.shape != upper.shape):
                err = 'sizes and upper must have same shape. '
                err += 'sizes.shape: %s, upper.shape: %s' % (self.sizes.shape,
                                                             upper.shape)
                raise tl.TraitError(err)
            with self.hold_trait_notifications():
                if np.any(self.lower >= upper):
                    raise tl.TraitError('lower >= upper!')
            return upper


class _Cubic:
    pass
