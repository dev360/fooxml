from xml.sax import make_parser
from xml.sax.handler import ContentHandler


class LXMLHandler(object):
    """
    The LXMLHandler uses the lxml.etree.iterparse
    strategy to parse xml
    """
    def iter(self, event, element):
        """
        Iterates over the etree
        """
        pass

    def parse(self, stream):
        """
        Parse implementation
        """
        pass



class SaxHandler(ContentHandler):
    """
    The BaseHandler accumulates xml attributes into
    an object and wraps the sax parser. The foo in fooxml.
    """
    def __init__(self, element, **kwargs):
        # _value is the current value
        # _obj is the currently accumulated obj
        # _nodes is the hierarchy of nodes
        # _callback is the callback for when an element finishes
        self._values = []
        self._accumulator = {}
        self._nodes = []
        self._callback = kwargs.get('callback', None)
        self._stripchars = kwargs.get('stripchars', False)
        self._elements = [element,]

    def valid_attribute(attr):
        """
        Gets whether to accumulate an attribute or not
        """
        # TODO: Override this later
        return True

    def startDocument(self, *args):
        pass

    def startElement(self, name, attrs):
        #
        # Set key to none if you are at the root element
        #
        self._nodes.append(name)
        self._accumulator[name] = {}
        self._values = []

        for attr in [a for a in attrs.keys()]:
            self._accumulator[name]['@{0}'.format(attr)] = attrs.get(attr)

    def characters(self, data):
        self._values.append(data)

    def endElement(self, name):
        # The element has come to an end, lets
        # print it and wipe it out.
        parent = self._nodes[len(self._nodes)-2]

        # Only collect the value if we're inside of an object
        # that we're supposed to collect.
        # basically, to determine that, one of the nodes
        # would be part of the self.elements collection,
        # so I take the intersection of these sets.

        elements = set(self._elements)
        nodes = set(self._nodes)
        is_needed = len(elements & nodes) >= 1

        if is_needed:
            self._accumulator[parent][name] = ''.join(self._values)

        if name in self._elements:
            self._accumulator[name]["value"] = ''.join(self._values)

        if name in self._elements:
            if self._callback:
                self._callback(self._accumulator[name])

        self._nodes.pop()

    def parse(self, stream):
        """
        Parses the actual file
        """
        parser = make_parser()
        parser.setContentHandler(self)
        parser.parse(stream)



class SimpleHandler(SaxHandler):
    """
    Simple handler accumulates all the data of an element into
    a simple dict. Its ideal when you don't care to control
    exactly which attributes get accumulated into the object.

    XML schema:
        <Persons>
            <Person id="123">
                <FirstName>Christian</FirstName>
                <LastName>Toivola</LastName>
            </Person>
            ...
        </Persons>

    >>> import xmlfoo
    >>> persons = []
    >>> def callback(person):
    ...     persons.append(person)
    >>> handler = SimpleHandler("Persons/Person", callback=callback)
    >>> xml_file = xmlfoo.xml_file("persons.xml", handler)
    >>> xml_file.parse()
    >>> persons[0]["@id"]
    123
    >>> persons[0]["FirstName"]
    Christian
    >>> persons[0]["LastName"]
    Toivola
    """
    pass



