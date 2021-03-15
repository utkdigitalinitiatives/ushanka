from dataclasses import dataclass
import requests


@dataclass
class MetadataBuilder:
    label: str
    original_metadata: dict
    pid: str

    @staticmethod
    def __lookup_rights(rights):
        valid_rights = {
            "Copyright Not Evaluated": "http://rightsstatements.org/vocab/CNE/1.0/",
            "Copyright Undetermined": "http://rightsstatements.org/vocab/UND/1.0/",
            "No Known Copyright": "http://rightsstatements.org/vocab/NKC/1.0/",
            "No Copyright - United States": "http://rightsstatements.org/vocab/NoC-US/1.0/",
            "No Copyright - Other Known Legal Restrictions": "http://rightsstatements.org/vocab/NoC-OKLR/1.0/",
            "No Copyright - Non-Commercial Use Only": "http://rightsstatements.org/vocab/NoC-NC/1.0/",
            "No Copyright - Contractual Restrictions": "http://rightsstatements.org/vocab/NoC-CR/1.0/",
            "In Copyright": "http://rightsstatements.org/vocab/InC/1.0/",
            "In Copyright - EU Orphan Work": "http://rightsstatements.org/vocab/InC-OW-EU/1.0/",
            "In Copyright - Educational Use Permitted": "http://rightsstatements.org/vocab/InC-EDU/1.0/",
            "In Copyright - Non-Commercial Use Permitted": "http://rightsstatements.org/vocab/InC-NC/1.0/",
            "In Copyright - Rights-holder(s) Unlocatable or Unidentifiable": "http://rightsstatements.org/vocab/InC-RUU/1.0/",
        }
        if rights in valid_rights:
            return rights, valid_rights[rights]
        else:
            return (
                "Copyright Not Evaluated",
                "http://rightsstatements.org/vocab/CNE/1.0/",
            )

    def __check_title(self, title):
        if title == "":
            return self.label
        else:
            return title

    def build_mods(self):
        rights = self.__lookup_rights(self.original_metadata["rights"])
        title = self.__check_title(self.original_metadata["title"])
        mods_record = f"""<?xml version="1.0"?>\n<mods xmlns="http://www.loc.gov/mods/v3" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-5.xsd">\n\t<titleInfo><title>{title}</title></titleInfo>\n\t<abstract>{self.original_metadata['abstract']}</abstract>\n\t<originInfo>\n\t\t<dateCreated>{self.original_metadata['date']}</dateCreated>\n\t\t<publisher>{self.original_metadata['publisher']}</publisher>\n\t</originInfo>\n\t<language>\n\t\t<languageTerm authority="iso639-2b" type="text">{self.original_metadata['language']}</languageTerm>\n\t</language>\n\t<accessCondition type="use and reproduction" xlink:href="{rights[1]}">{rights[0]}</accessCondition>\n<identifier type="pid">{self.pid}</identifier></mods>"""
        with open("temp/MODS.xml", "w") as metadata:
            metadata.write(mods_record)

    def build_dc(self):
        title = self.__check_title(self.original_metadata["title"])
        dc_record = f"""<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">\n\t<dc:title>{title}</dc:title>\n\t<dc:description>{self.original_metadata['abstract']}</dc:description>\n\t<dc:date>{self.original_metadata['date']}</dc:date>\n\t<dc:rights>{self.original_metadata['rights']}</dc:rights>\n\t<dc:identifier>{self.original_metadata['identifier']}</dc:identifier></oai_dc:dc>"""
        with open("temp/DC.xml", "w") as metadata:
            metadata.write(dc_record)


class GSearchConnection:
    def __init__(
        self, pid, url="http://localhost:8080", auth=("fedoraAdmin", "fedoraAdmin")
    ):
        self.url = (
            f"{url}/fedoragsearch/rest?operation=updateIndex&action=fromPid&value={pid}"
        )
        self.auth = auth

    def update(self):
        r = requests.post(self.url, auth=self.auth)
        return r.status_code


if __name__ == "__main__":
    print(GSearchConnection("test:4").update())
