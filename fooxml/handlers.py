from xml.sax import make_parser
from xml.sax.handler import ContentHandler


class LXMLHandler(object):
    """
    The LXMLHandler uses the lxml.etree.iterparse
    strategy to parse xml
    """
    def __init__(self, element, **kwargs):
        self._element = element
        self._base_key = None
        self._accumulator = {}
        self._callback = kwargs.get('callback', None)
        self._nodes = []

    @property
    def current_key(self):
        return '/'.join(self._nodes)

    def iter(self, event, element):
        """
        Iterates over the etree
        """
        if event == 'start':
            self._nodes.append(element.tag)

        if self.is_start(event, element):
            if self._base_key == None:
                self._base_key = self.current_key

            self._accumulator = {}

        if event == 'start':
            self._accumulator[self.current_key] = element.text

            for attr in element.attrib:
                self._accumulator[self.current_key + "@" + attr] = element.attrib[attr]

        if self.is_end(event, element):
            if self._callback:
                self._callback(self.obj)

        if event == 'end':
            self._nodes.pop()

    @property
    def obj(self):
        """
        Builds out the object
        """
        obj = {}
        for key in self._accumulator:
            if self._base_key and key.startswith(self._base_key):
                attr = key[len(self._base_key)+1:]

                # Only pick the first level attributes
                # for right now
                if '/' not in attr:
                    obj[attr] = self._accumulator[key]

        # print self._accumulator
        return obj

    def is_start(self, event, element):
        """
        Determines if this is the start of element
        """
        return event == 'start' and element.tag == self._element

    def is_end(self, event, element):
        """
        Determines if this is the end of element
        """
        return event == 'end' and element.tag == self._element

    def parse(self, stream):
        """
        Parse implementation
        """
        from lxml import etree
        for e, el in etree.iterparse(stream, events=('start', 'end')):
            self.iter(e, el)


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



