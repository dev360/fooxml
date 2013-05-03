from StringIO import StringIO
import unittest

import fooxml


class LXMLHandlerTest(unittest.TestCase):

    def test_parse(self):
        """ Testing the routes """

        objs = []

        def callback(obj):
            objs.append(obj)

        handler = fooxml.LXMLHandler("AttributeLink", callback=callback)
        xml_file = fooxml.xml_file("../samples/SampleAttributeLink.xml", handler)
        xml_file.parse()

        assert len(objs) > 1
        assert type(objs[0]) == dict
        assert objs[0]['AttributeLinkID'] == 'ML0000001057'
        assert objs[0]['ObjectID'] == 'MN0000833164'
        assert objs[0]['PropertyAttributeID'] == 'MA0000000239'
        assert objs[0]['ValueAttributeID'] == '            '
        assert objs[0]['Value'] == 'JoVonn'
        assert objs[0]['Weight'] == '5'
        assert objs[0]['Rank'] == '0'
        assert objs[0]['SortOrder'] == '2'
        assert objs[0]['p_BaseObjectID'] == 'MN0000833164'
        assert objs[0]['Action'] == 'A'


    def test_parse_ampersand(self):
        """
        Test parsing of ampersand characters
        """
        # From http://www.w3schools.com/xml/simple.xml
        xml_fragment = """<?xml version="1.0" encoding="ISO-8859-1"?>
        <!-- Edited by XMLSpy? -->
        <breakfast_menu>
            <food>
                <name>Belgian Waffles &amp; Beer</name>
                <price>$5.95</price>
                <description>two of our famous Belgian Waffles with plenty of real maple syrup</description>
                <calories>650</calories>
            </food>
            <food>
                <name>Strawberry Belgian Waffles</name>
                <price>$7.95</price>
                <description>light Belgian waffles covered with strawberries and whipped cream</description>
                <calories>900</calories>
            </food>
        </breakfast_menu>
        """
        stream = StringIO(xml_fragment)
        stream.seek(0)

        objs = []
        def callback(obj):
            objs.append(obj)

        handler = fooxml.LXMLHandler("food", callback=callback)
        xml_file = fooxml.xml_file(stream, handler)
        xml_file.parse()

        assert len(objs) > 1
        assert type(objs[0]) == dict
        assert objs[0]['name'] == 'Belgian Waffles & Beer'



