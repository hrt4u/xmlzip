import copy
import random
import string
from zipfile import ZipFile

from lxml import etree

from timer import Timer


class XmlGenerator(object):

    _template = None
    _xml_per_zip_amount = 100
    _zip_amount = 50

    def __init__(self):
        super().__init__()

    def _get_random_string(self, length=100):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    @property
    def template(self):
        if self._template is None:
            self._template = self.create_template()
        return self._template

    def create_template(self):
        root = etree.Element("root")
        var1 = etree.Element("var", name='id')
        var2 = etree.Element("var", name='level')
        objects = etree.Element("objects")
        root.append(var1)
        root.append(var2)
        root.append(objects)
        # print(etree.tostring(root))
        return root

    def get_template(self):
        return copy.deepcopy(x.template)

    def generate_xml(self, count=None):
        for _ in range(count or self._xml_per_zip_amount):
            objects_count = random.randint(1, 10)
            xml = self.get_template()
            xml[0].set('value', self._get_random_string())
            xml[1].set('value', str(random.randint(1, 10)))
            for i in range(objects_count):
                xml[2].append(etree.Element(
                    "object", name=self._get_random_string()))
            yield etree.tostring(xml)

    def generate_zip(self, count=random.randint(1, 10)):
        with ZipFile('output/{0}.zip'.format(count), 'w') as myzip:
            for xml_string in self.generate_xml():
                myzip.writestr(
                    self._get_random_string(length=14) + '.xml', xml_string)

    def process(self):
        with Timer():
            for i in range(self._zip_amount):
                self.generate_zip(count=i+1)


if __name__ == "__main__":
    x = XmlGenerator()
    x.process()
