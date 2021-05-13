import bitmath
import xmltodict


class METSFile:
    """A class to represent an Archivematica METS file.

    attributes:
        contents (OrderedDict): The contents of a METS file as an OrderedDict.
        administrative_metadata (list): All the administrative metadata in a METS file as a list.
        original_files (list): A list of AdministrativeMetadata objects for the original files.
        total_size (int): The total size of the original files in a METS file.
        pretty_total_size (str): The total size formatted to the unit that makes the most sense.

    """

    def __init__(self, contents):
        self.contents = xmltodict.parse(contents)
        self.administrative_metadata = self.__get_all_administrative_metadata()
        self.original_files = self.__find_original_files()
        self.total_size = sum([int(original.size) for original in self.original_files])
        self.pretty_total_size = bitmath.Byte(bytes=int(self.total_size)).best_prefix()

    def __get_all_administrative_metadata(self):
        return [section for section in self.contents["mets:mets"]["mets:amdSec"]]

    def __find_original_files(self):
        original_files = []
        for file_group in self.contents["mets:mets"]["mets:fileSec"]["mets:fileGrp"]:
            if file_group["@USE"] == "original":
                for filename in file_group["mets:file"]:
                    try:
                        admsec = filename["@ADMID"]
                        name = filename["mets:FLocat"]["@xlink:href"].split("/")[-1]
                        path = filename["mets:FLocat"]["@xlink:href"]
                        current = AdministrativeMetadata(
                            admsec, name, path, self.administrative_metadata
                        )
                        original_files.append(current)
                    except KeyError:
                        pass
        return original_files


class AdministrativeMetadata:
    """Class for working with Administrative Metadata from Archivematica.

    Attributes:
        id (str): The identifier of the administrative metadata section.
        name (str): The name of the file.
        path (str): The path to the file.
        original_metadata (OrderedDict): The original metadata as an ordered dict.
        size (str): The size of the file in bytes.
        best_size (str): The size of the file formatted to be most human readable.

    """
    def __init__(self, amdid, name, path_to_file, all_data):
        self.id = amdid
        self.name = name
        self.path = path_to_file
        self.original_metadata = self.__find_admin_metadata(all_data)
        self.size = self.__get_size_in_bytes()
        self.best_size = self.__get_best_size()

    def __find_admin_metadata(self, all):
        for section in all:
            if section["@ID"] == self.id:
                return section

    def get_pronom_link(self):
        format_registry = self.get_format_registry()
        if format_registry[0] == "PRONOM":
            return f"http://nationalarchives.gov.uk/PRONOM/{format_registry[1]}"
        else:
            return ""

    def __get_size_in_bytes(self):
        return self.original_metadata["mets:techMD"]["mets:mdWrap"]["mets:xmlData"][
            "premis:object"
        ]["premis:objectCharacteristics"]["premis:size"]

    def __get_best_size(self):
        return bitmath.Byte(bytes=int(self.size)).best_prefix()

    def get_format_registry(self):
        """Gets registry name and key as a tuple."""
        format = self.original_metadata["mets:techMD"]["mets:mdWrap"]["mets:xmlData"][
            "premis:object"
        ]["premis:objectCharacteristics"]["premis:format"]
        return (
            format["premis:formatRegistry"]["premis:formatRegistryName"],
            format["premis:formatRegistry"]["premis:formatRegistryKey"],
        )

    def get_format_designation(self):
        format = self.original_metadata["mets:techMD"]["mets:mdWrap"]["mets:xmlData"][
            "premis:object"
        ]["premis:objectCharacteristics"]["premis:format"]
        return (
            format["premis:formatDesignation"]["premis:formatName"],
            format["premis:formatDesignation"]["premis:formatVersion"],
        )

    def get_last_modified(self):
        return self.original_metadata["mets:techMD"]["mets:mdWrap"]["mets:xmlData"][
            "premis:object"
        ]["premis:objectCharacteristics"]["premis:creatingApplication"][
            "premis:dateCreatedByApplication"
        ]

    def get_checksum(self):
        fixity = self.original_metadata["mets:techMD"]["mets:mdWrap"]["mets:xmlData"][
            "premis:object"
        ]["premis:objectCharacteristics"]["premis:fixity"]
        return fixity["premis:messageDigestAlgorithm"], fixity["premis:messageDigest"]


if __name__ == "__main__":
    with open("full_mets.xml", "rb") as my_mets:
        mets = METSFile(my_mets)
        print(mets.pretty_total_size)