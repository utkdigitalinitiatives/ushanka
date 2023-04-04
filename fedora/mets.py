from lxml import etree
import xml.etree.ElementTree as ET


class METSSection:
    def __init__(self, path, hash):
        self.path = path
        self.hash = hash
        self.ns = {
            'mets': 'http://www.loc.gov/METS/',
            'premis': 'http://www.loc.gov/premis/v3'
        }
        self.root = self.__decode(path)
        self.techmd = self.get_techmd()

    @staticmethod
    def __decode(path_to_file):
        with open(path_to_file, 'rb') as xml:
            return etree.parse(xml)

    def get_techmd(self):
        return [techmd for techmd in self.root.xpath(
            f'//mets:xmlData[descendant::premis:objectIdentifierValue="{self.hash}"]',
            namespaces=self.ns
        )][0]

    def get_original_path(self):
        return [value.text.replace('%transferDirectory%objects/', '') for value in self.techmd.xpath('.//premis:originalName', namespaces=self.ns)][0]

    def write_premis(self):
        with open('temp_premis/premis.xml', 'w') as premis:
            for node in self.get_techmd():
                premis.write(etree.tostring(node, encoding='unicode', pretty_print=True))


if __name__ == "__main__":
    x = METSSection("data/METS/METS.0a2f42cd-eede-477d-86a3-8ab84962c8c7.xml", '0e65770d-c706-4067-9c55-1f9380828ca2')
    x.write_premis()