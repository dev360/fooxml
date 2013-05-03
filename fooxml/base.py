
class XmlFile(object):
    """
    XML File object.. not really a file. sorry :)
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        self._stream = args[0]
        self._handler = args[1] if len(args) > 1 else kwargs.get('handler')

    def parse(self):
        """
        Processes the file
        """
        self._handler.parse(self._stream)



def xml_file(*args, **kwargs):
    """
    Usage:
    >>> import fooxml
    >>> handler = SimpleHandler("")
    >>> xml_file = fooxml.xml_file(open('samples/.xml'), handlers=[fooxml])
    >>>
    """
    return XmlFile(*args, **kwargs)
