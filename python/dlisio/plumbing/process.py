from .basicobject import BasicObject
from .valuetypes import scalar, vector
from .linkage import obname
from .utils import *

from collections import OrderedDict


class Process(BasicObject):
    """
    Process objects describes a specific process or computation applied to input
    objects to get output objects.

    Attributes
    ----------

    description : str

    trademark_name  : str
        Trademark name refers to the process and its products.

    version : str
        Software version.

    properties : list(str)
        Properties that applies to the output of the process, as a result of
        the process.

    status : str
        Indicated the status of the process. It's typically updated to indicate
        when the process is completed or aborted.

    input_channels : list(Channel)
        Channels that are used directly by this Process.

    output_channels : list(Channel)
        Channels that are produced directly by this Process.

    input_computation : list(Computation)
        Computations that are used directly by this Process.

    output_computation : list(Computation)
        Computations that are produced directly by this Process.

    parameters : list(Parameter)
        Parameters that are used by the Process or that directly affect the
        operation of the Process.

    comments : list(str)
        Comments contains information specific to the particular
        execution of the process.

    See also
    --------

    BasicObject : The basic object that Parameter is derived from


    Notes
    -----

    The Process object reflects the logical record type Process, defined in
    rp66. PROCESS records are listed in Appendix A.2 - Logical Record Types and
    described in detail in Chapter 5.8.5 - Static and Frame Data, Process
    objects.
    """
    attributes = {
        'DESCRIPTION'         : scalar('description'),
        'TRADEMARK-NAME'      : scalar('trademark_name'),
        'VERSION'             : scalar('version'),
        'PROPERTIES'          : vector('properties'),
        'STATUS'              : scalar('status'),
        'INPUT-CHANNELS'      : vector('input_channels'),
        'OUTPUT-CHANNELS'     : vector('output_channels'),
        'INPUT-COMPUTATIONS'  : vector('input_computations'),
        'OUTPUT-COMPUTATIONS' : vector('output_computations'),
        'PARAMETERS'          : vector('parameters'),
        'COMMENTS'            : vector('comments')
    }

    linkage = {
        'description'         : obname('LONG-NAME'),
        'input_channels'      : obname('CHANNEL'),
        'output_channels'     : obname('CHANNEL'),
        'input_computations'  : obname('COMPUTATION'),
        'output_computations' : obname('COMPUTATION'),
        'parameters'          : obname('PARAMETER')
    }

    def __init__(self, obj = None, name = None):
        super().__init__(obj, name = name, type = 'PROCESS')
        self.description         = None
        self.trademark_name      = None
        self.version             = None
        self.properties          = []
        self.status              = None
        self.input_channels      = []
        self.output_channels     = []
        self.input_computations  = []
        self.output_computations = []
        self.parameters          = []
        self.comments            = []

    def describe_attr(self, buf, width, indent, exclude):
        describe_description(buf, self.description, width, indent, exclude)

        d = OrderedDict()
        d['Trademark name'] = self.trademark_name
        d['Status']         = self.status
        d['Version']        = self.version
        d['Comments']       = self.comments
        describe_dict(buf, d, width, indent, exclude)

        d = OrderedDict()
        d['Properties']  = self.properties
        d['Parameters']  = replist(self.parameters, 'name')
        describe_dict(buf, d, width, indent, exclude)

        d = OrderedDict()
        d['Input Channels']      = replist(self.input_channels, 'name')
        d['Output Channels']     = replist(self.output_channels, 'name')
        d['Input Computations']  = replist(self.input_computations, 'name')
        d['Output computations'] = replist(self.output_computations, 'name')
        describe_dict(buf, d, width, indent, exclude)
