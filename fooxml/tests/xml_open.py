import unittest

import fooxml


class XmlOpenTest(unittest.TestCase):

    def test_process(self):
        """ Testing the routes """

        objs = []

        def callback(obj):
            objs.append(obj)

        handler = fooxml.SimpleHandler("AttributeLink", callback=callback)
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

