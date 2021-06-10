class DateModel:
    """Class for building DateModels for use in other ArchivesSpace classes.

    Attributes:
        valid_labels (tuple): A sequence of valid labels.
        valid_types (tuple): A sequence of valid types.
        valid_certainties (tuple): A sequence of valid certainties.
    """

    def __init__(self):
        self.valid_labels = (
            "agent_relation",
            "broadcast",
            "copyright",
            "creation",
            "deaccession",
            "digitized",
            "event",
            "existence",
            "issued",
            "modified",
            "other",
            "publication",
            "record_keeping",
            "usage",
        )
        self.valid_types = ("bulk", "inclusive", "range", "single")
        self.valid_certainties = ("approximate", "inferred", "questionable")

    @staticmethod
    def __check_for_a_value(beginning, ending, expression):
        values = {}
        if beginning == "" and ending == "" and expression == "":
            raise Exception("Bad date. Must have a begin, end, or expression value.")
        if beginning != "":
            values["begin"] = beginning
        if ending != "":
            values["end"] = ending
        if expression != "":
            values["expression"] = expression
        return values

    def __test_type(self, date_type):
        if date_type not in self.valid_types:
            raise Exception(f"{date_type} is not a valid date type.")
        return

    def __test_label(self, date_label):
        if date_label not in self.valid_labels:
            raise Exception(f"{date_label} is not a valid date label.")
        return

    def __test_certainty(self, certainty):
        if certainty not in self.valid_certainties:
            raise Exception(f"{certainty} is not a valid date certainty.")
        return

    def create(self, date_type, label, certainty="", begin="", end="", expression=""):
        """Creates a new DateModel for use in other classes.

        Schema is found here: https://github.com/archivesspace/archivesspace/blob/82c4603fe22bf0fd06043974478d4caf26e1c646/common/schemas/date.rb

        Args:
            date_type (str): The type of date.  Must be a value in DateModel.valid_types.
            label (str): The label for the date.  Must be a value in DateModel.valid_labels.
            certainty (str): A certainty value for the date.  Optional, but must be in DateModel.valid_certainties if used.
            begin (str): A beginning value.  Must have one or more of begin, end, or expression.
            end (str): An ending value. Must have one or more of begin, end, or expression.
            expression (str): A more open value type to express a date. Must have one or more of begin, end, or expression.

        Returns:
            dict: A dict representing your date.

        Examples:
            >>> DateModel().create(date_type="single", label="creation", begin="2002-03-14"))
            {'jsonmodel_type': 'date', 'date_type': 'single', 'label': 'creation', 'era': 'ce', 'calendar': 'gregorian',
            'begin': '2002-03-14'}

        """
        date_values = self.__check_for_a_value(begin, end, expression)
        self.__test_label(label)
        self.__test_type(date_type)
        model = {
            "jsonmodel_type": "date",
            "date_type": date_type,
            "label": label,
            "era": "ce",
            "calendar": "gregorian",
        }
        if certainty != "":
            self.__test_certainty(certainty)
            model["certainty"] = certainty
        for key, value in date_values.items():
            model[key] = value
        return model


class Extent:
    """Class for building Extent models for use with other ArchivesSpace classes.

    Attributes:
        valid_portions (tuple): A sequence of valid portion strings.
        valid_extent_type (tuple): A sequence of valid extent types.
    """

    def __init__(self):
        self.valid_portions = ("whole", "part")
        self.valid_extent_type = (
            "cassettes",
            "cubic feet",
            "gigabytes",
            "megabytes",
            "terrabytes",
            "leaves",
            "linear feet",
            "photographic prints",
            "photographic slides",
            "reels",
            "sheets",
            "volumes",
            "boxes",
            "files",
        )

    def create(
        self,
        number,
        type_of_unit,
        portion,
        container_summary="",
        physical_details="",
        dimensions="",
    ):
        """Creates extent information following the ArchivesSpace schema.

        Schema described here: https://github.com/archivesspace/archivesspace/blob/82c4603fe22bf0fd06043974478d4caf26e1c646/common/schemas/extent.rb

        Args:
            number (str): A numeric value for indicating the number of units in the extent statement, e.g, 5, 11.5, 245. Used in conjunction with Extent Type to provide a structured extent statement.
            type_of_unit (str): A term indicating the type of unit used to measure the extent of materials described.
            portion (str): Used to specify whether an extent statement relates to the whole or part of a given described.

        Returns:
            dict: The appropriate extent information following the ArchivesSpace schema.

        Examples:
            >>> Extent().create(number="35", type_of_unit="cassettes", portion="whole")
            {"jsonmodel_type": "extent", "portion": "whole", "number": "35", "extent_type": "cassettes",}

        """
        if portion in self.valid_portions and type_of_unit in self.valid_extent_type:
            model = {
                "jsonmodel_type": "extent",
                "portion": portion,
                "number": number,
                "extent_type": type_of_unit,
            }
            if container_summary != "":
                model["container_summary"] = container_summary
            if physical_details != "":
                model["physical_details"] = physical_details
            if dimensions != "":
                model["dimensions"] = dimensions
            return model

        else:
            raise Exception("Invalid extent information.")


class FileVersion:
    """Class for building FileVersion models to use with other classes that need them."""

    @staticmethod
    def add(uri, published=True, is_representative=True, show_attribute="new"):
        return {
            "jsonmodel_type": "file_version",
            "is_representative": is_representative,
            "file_uri": uri,
            "xlink_actuate_attribute": "onRequest",
            "xlink_show_attribute": show_attribute,
            "publish": published,
        }


class LanguageOfMaterials:
    """Class for building Language of Materials models to use with other classes that need them.

    Currently, this is only used to bypass problems from ArchivesSpace. It's messy, bad, and encompasses multiple
    ArchivesSpace models unlike other classes in this package.
    """

    def add(self, languages=["eng"]):
        return [self.__append_language(language) for language in languages]

    @staticmethod
    def __append_language(language):
        return {
            "jsonmodel_type": "lang_material",
            "language_and_script": {
                "language": language,
                "jsonmodel_type": "language_and_script",
            },
        }


class ExternalIdentifer:
    """Class for buidling External Identifiers in ArchivesSpae."""

    @staticmethod
    def add(id, source):
        """Adds and external identifier.

        Args:
            id (str): The external identifier you are referencing.
            source (str): Where the external identifier comes from.

        Examples:
            >>> ExternalIdentifer.add("209519", "Archivists Toolkit Database::RESOURCE_COMPONENT")
            {"jsonmodel_type": "external_id", "external_id": "209519", "source": "Archivists Toolkit Database::RESOURCE_COMPONENT"}
            >>> ExternalIdentifer.add("borndigital:8", "islandora")
            {"jsonmodel_type": "external_id", "external_id": "borndigital:8", "source": "Islandora 7"}

        """
        return {
            "jsonmodel_type": "external_id",
            "external_id": id,
            "source": source,
        }
