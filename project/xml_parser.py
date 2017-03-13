import os
import csv
from zipfile import ZipFile
import multiprocessing
import itertools

from lxml import etree

from timer import Timer


class XmlParser(object):

    _zip_archives = None

    def __init__(self):
        super().__init__()

    @property
    def zip_archives(self):
        if self._zip_archives is None:
            self._zip_archives = self.get_zip_archives()
        return self._zip_archives

    def get_zip_archives(self):
        return [f for f in os.listdir("output/") if f.endswith(".zip")]

    def zip_parse(self, zip_archive):
        results1 = []
        results2 = []
        with ZipFile("output/" + zip_archive) as zip_file:
            for xml_file in zip_file.namelist():
                with zip_file.open(xml_file) as xml:
                    root = etree.fromstring(xml.read())
                    results1.append(
                        [root[0].get('value'), root[1].get('value')])
                    for object_ in root[2]:
                        results2.append(
                            [root[0].get('value'), object_.get('name')])
        return results1, results2

    def write_csv_file(self, file, rows):
        with open(file, 'w', newline='') as csvfile:
            spamwriter = csv.writer(
                csvfile, delimiter=',',
                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerows(rows)

    def process(self):
        results1 = [['id', 'level']]
        results2 = [['id', 'object_name']]
        pool = multiprocessing.Pool(multiprocessing.cpu_count() * 2)
        results = list(zip(*pool.map(self.zip_parse, self.zip_archives)))
        print(len(results))
        results1 = list(itertools.chain.from_iterable(results[0]))
        results2 = list(itertools.chain.from_iterable(results[1]))
        print(len(results1), len(results2))
        pool.close()
        pool.join()
        self.write_csv_file('results/results1.csv', results1)
        self.write_csv_file('results/results2.csv', results2)


if __name__ == '__main__':
    x = XmlParser()
    x.process()
