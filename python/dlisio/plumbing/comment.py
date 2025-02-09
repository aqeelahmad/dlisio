from .basicobject import BasicObject
from .valuetypes import vector
from .utils import describe_array

class Comment(BasicObject):
    """
    Comment objects contains arbitrary messages that may be interesting for the
    consumer e.g. a drilling report.

    Attributes
    ----------

    text : list(str)
        Textual comments

    See also
    --------

    BasicObject : The basic object that Comment is derived from

    Notes
    -----

    The Comment object reflects the logical record type COMMENT, described in
    rp66. COMMENT objects are defined in Appendix A.2 - Logical Record Types,
    described in detail in Chapter 6.1.2 - Transient Data, Comment objects.
    """
    attributes = { 'TEXT' : vector('text') }

    def __init__(self, obj = None, name = None):
        super().__init__(obj, name = name, type = 'COMMENT')
        self.text = []

    def describe_attr(self, buf, width, indent, exclude):
        describe_array(buf, self.text, width, indent)
