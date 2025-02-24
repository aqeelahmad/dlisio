from .basicobject import BasicObject
from .valuetypes import scalar, vector, reverse, skip
from .linkage import obname
from .utils import *

import logging
import numpy as np
from collections import OrderedDict


class Parameter(BasicObject):
    """Parameter

    A parameter object describes a parameter used in the acquisition and
    processing of data.  The parameter value(s) may be scalars or an array. In
    the later case, the structure of the array is defined in the dimension
    attribute. The zones attribute specifies which zones the parameter is
    defined. If there are no zones the parameter is defined everywhere.

    The axis attribute, if present, defines axis labels for multidimensional
    value(s).

    Attributes
    ----------

    long_name : Longname
        Descriptive name of the channel.

    dimension : list(int)
        Dimensions of the parameter values

    axis : list(Axis)
        Coordinate axes of the parameter values

    zones : list(Zone)
        Mutually disjoint intervals where the parameter values is constant

    values


    See also
    --------

    BasicObject : The basic object that Parameter is derived from

    Notes
    -----

    The Parameter object reflects the logical record type PARAMETER, described
    in rp66. PARAMETER objects are defined in Appendix A.2 - Logical Record
    Types, described in detail in Chapter 5.8.2 - Static and Frame Data,
    PARAMETER objects.
    """
    attributes = {
        'LONG-NAME' : scalar('long_name'),
        'DIMENSION' : reverse('dimension'),
        'AXIS'      : reverse('axis'),
        'ZONES'     : vector('zones'),
        'VALUES'    : skip(),
    }

    linkage = {
        'long_name' : obname("LONG-NAME"),
        'axis'      : obname("AXIS"),
        'zones'     : obname("ZONE")
    }

    def __init__(self, obj = None, name = None):
        super().__init__(obj, name = name, type = 'PARAMETER')
        self.long_name = None
        self.dimension = []
        self.axis      = []
        self.zones     = []

    @property
    def values(self):
        """ Parameter values

        Parameter value(s) may be scalar or array's. The size/dimensionallity
        of each value is defined in the dimensions attribute.

        Each value may or may not be zoned, i.e. it is only defined in a
        certain zone. If this is the case the first zone, parameter.zones[0],
        will correspond to the first value, parameter.values[0] and so on.  If
        there is no zones, there should only be one value, which is said to be
        unzoned, i.e. it is defined everywere.

        Raises
        ------

        ValueError
            Unable to structure the values based on the information available.

        Returns
        -------

        values : structured np.ndarray

        Notes
        -----

        If dlisio is unable to structure the values due to insufficient or
        contradictory information in the object, an ValueError is raised.  The
        raw array can still be accessed through attic, but note that in this
        case, the semantic meaning of the array is undefined.

        Examples
        --------

        First value:

        >>> parameter.values[0]
        [10, 20, 30]

        Zone (if any) where that parameter value is valid:

        >>> parameter.zones[0]
        Zone('ZONE-A')
        """
        try:
            values = self.attic['VALUES']
        except KeyError:
            return np.empty(0)

        shape = validshape(values, self.dimension, samplecount=len(self.zones))
        return sampling(values, shape)

    def describe_attr(self, buf, width, indent, exclude):
        describe_description(buf, self.long_name, width, indent, exclude)

        d = OrderedDict()
        d['Sample dimensions'] = self.dimension
        d['Axis labels']       = self.axis
        d['Zones']             = self.zones

        describe_dict(buf, d, width, indent, exclude)

        describe_sampled_attrs(
                buf,
                self.attic,
                self.dimension,
                'VALUES',
                None,
                width,
                indent,
                exclude
        )
