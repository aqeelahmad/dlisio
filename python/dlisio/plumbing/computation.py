from .basicobject import BasicObject
from .valuetypes import scalar, vector, reverse, skip
from .linkage import obname, objref
from .utils import *

import logging
import numpy as np


class Computation(BasicObject):
    """
    Results of computations that are more appropriately expressed as static
    information rather than as channels.

    The computation value(s) may be scalars or an array. In
    the later case, the structure of the array is defined in the dimension
    attribute. The zones attribute specifies which zones the computations is
    defined. If there are no zones the computation is defined everywhere.

    The axis attribute, if present, defines axis labels for multidimensional
    value(s).

    Attributes
    ----------

    long_name : str or Longname
        Descriptive name of the computation

    properties : list(str)
        Property indicators that summarizes the characteristics of the
        computation and the processing that has occurred to produce it

    dimension : list(int)
        Array structure of a single value

    axis : list(Axis)
        Coordinate axes of the values

    zones : list(Zone)
        Mutually disjoint zones over which the value of the current
        computation is constant

    source
        The immediate source of the Computation

    values

    See also
    --------

    BasicObject : The basic object that Computation is derived from

    Notes
    -----

    The Computation object reflects the logical record type COMPUTATION,
    defined in rp66.  COMPUTATION objects are listed in Appendix A.2 - Logical
    Record Types, and described in detail in Chapter 5.8.6 - Static and Frame
    Data, COMPUTATION objects.
    """

    attributes = {
        'LONG-NAME' : scalar('long_name'),
        'PROPERTIES': vector('properties'),
        'DIMENSION' : reverse('dimension'),
        'AXIS'      : reverse('axis'),
        'ZONES'     : vector('zones'),
        'SOURCE'    : scalar('source'),
        'VALUES'    : skip()
    }

    linkage = {
        'long-name' : obname('LONG-NAME'),
        'axis'      : obname('AXIS'),
        'zones'     : obname('ZONE'),
        'source'    : objref
    }

    def __init__(self, obj = None, name = None):
        super().__init__(obj, name = name, type = 'COMPUTATION')
        self.long_name   = None
        self.properties  = []
        self.dimension   = []
        self.axis        = []
        self.zones       = []
        self.source = None

    @property
    def values(self):
        """ Computation values

        Computation value(s) may be scalar or array's. The size/dimensionallity
        of each value is defined in the dimensions attribute.

        Each value may or may not be zoned, i.e. it is only defined in a
        certain zone. If this is the case the first zone, computation.zones[0],
        will correspond to the first value, computation.values[0] and so on.
        If there is no zones, there should only be one value, which is said to
        be unzoned, i.e. it is defined everywere.

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

        >>> computation.values[0]
        [10, 20, 30]

        Zone (if any) where that parameter value is valid:

        >>> computation.zones[0]
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
        d['Sample dimensions']   = self.dimension
        d['Axis labels']         = self.axis
        d['Zones']               = self.zones
        d['Property indicators'] = self.properties
        d['Source object']       = self.source
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
