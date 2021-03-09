import requests
from urllib.parse import quote
import magic


class FedoraObject:
    def __init__(
        self, fedora_url="http://localhost:8080", auth=("fedoraAdmin", "fedoraAdmin")
    ):
        self.fedora_url = fedora_url
        self.auth = auth

    def __ingest(
        self,
        namespace,
        label,
        state="A",
    ):
        """@todo: Right now this is private, but this should be public if create_digital_object goes to another class.
        """
        r = requests.post(
            f"{self.fedora_url}/fedora/objects/new?namespace={namespace}&label={label}&state={state}",
            auth=self.auth,
        )
        if r.status_code == 201:
            return r.content.decode("utf-8")
        else:
            raise Exception(
                f"Request to ingest object with label `{label}` failed with {r.status_code}."
            )

    def add_relationship(self, pid, subject, predicate, obj, is_literal="true"):
        """Add a relationship to a digital object.

        Args:
            pid (str): The persistent identifier to the object where you want to add the relationship.
            subject (str): The subject of the relationship.  This should refer to the pid (for external relationships) or the dsid (for internal relationships). For
            predicate (str): The predicate of the new relationship.
            obj (str): The object of the new relationship.  Can refer to a graph or a literal.
            is_literal (str): This defaults to "true" but can also be "false." It specifies whether the object is a graph or a literal.

        Returns:
            int: The status code of the post request.json

        Examples:
            >>> FedoraObject().add_relationship(pid="test:6", subject="info:fedora/test:6", predicate="info:fedora/fedora-system:def/relations-external#isMemberOfCollection", obj="info:fedora/islandora:test", is_literal="false",)
            200

        """
        r = requests.post(
            f"{self.fedora_url}/fedora/objects/{pid}/relationships/new?subject={quote(subject, safe='')}&predicate={quote(predicate, safe='')}&object={quote(obj, safe='')}&isLiteral={is_literal}",
            auth=self.auth,
        )
        if r.status_code == 200:
            return r.status_code
        else:
            raise Exception(
                f"Unable to add relationship on {pid} with subject={subject}, predicate={predicate}, and object={obj}, and isLiteral as {is_literal}.  Returned {r.status_code}."
            )

    def change_versioning(self, pid, dsid, versionable="false"):
        """Change versioning of a datastream.

        Args:
             pid (str): The persistent identifier of the object to which the dsid belongs.
             dsid (str): The datastream id of the datastream you want to modify.
             versionable (str): Defaults to "false".  "false" or "true" on whether a datastream is versioned.

        Returns:
            int: The status code of the request.

        Examples:
            >>> FedoraObject().change_versioning("test:1", "RELS-EXT", "true")
            200

        """
        r = requests.put(
            f"{self.fedora_url}/fedora/objects/{pid}/datastreams/{dsid}?versionable={versionable}",
            auth=self.auth,
        )
        if r.status_code == 200:
            return r.status_code
        else:
            raise Exception(
                f"Unable to change versioning of the {dsid} datastream on {pid} to {versionable}.  Returned {r.status_code}."
            )

    def add_managed_datastream(
        self,
        pid,
        dsid,
        file,
        versionable="true",
        datastream_state="A",
        checksum_type="DEFAULT",
    ):
        """Adds an internally managed datastream.

        This is not a one to one vesion of addDatastream.  It has been stripped down to fit one use case: internally
        managed content.  I'll add other methods if other use cases arise.

        Args:
            pid (str): The persistent identifier to the object when you want to add a file.
            dsid (str): The datastream id to assign your new file.
            file (str): The path to your file.
            versionable (str): Defaults to "true".  Specifies whether the datastream should have versioning ("true" or "false").
            datastream_state (str): Specify whether the datastream is active, inactive, or deleted.
            checksum_type (str): The checksum type to use.  Defaults to "DEFAULT". See API docs for options.

        Returns:
            int: The http status code of the request.

        Examples:
            >>> FedoraObject().add_managed_datastream("test:10", "AIP", "my_aip.7z")
            201

        """
        if checksum_type not in (
            "DEFAULT",
            "DISABLED",
            "MD5",
            "SHA-1",
            "SHA-256",
            "SHA-385",
            "SHA-512",
        ):
            raise Exception(
                f"\nInvalid checksum type specified for {pid} when adding the {dsid} datastream with {file}"
                f"content.\nMust be one of: DEFAULT, DISABLED, MD5, SHA-1, SHA-256, SHA-385, SHA-512."
            )
        mime = magic.Magic(mime=True)
        upload_file = {
            "file": (file, open(file, "rb"), mime.from_file(file), {"Expires": "0"})
        }
        r = requests.post(
            f"{self.fedora_url}/fedora/objects/{pid}/datastreams/{dsid}/?controlGroup=M&dsLabel={dsid}&versionable={versionable}&dsState={datastream_state}&checksumType={checksum_type}",
            auth=self.auth,
            files=upload_file,
        )
        if r.status_code == 201:
            return r.status_code
        else:
            raise Exception(
                f"\nFailed to create {dsid} datastream on {pid} with {file} as content. Fedora returned this"
                f"status code: {r.status_code}."
            )

    def create_digital_object(
        self, object_namespace, object_label, collection, object_state="A"
    ):
        """@todo: This is temporary code.  Ultimately, this will likely come out and go to its own class and method.
        """
        # Ingest a new object
        pid = self.__ingest(object_namespace, object_label, object_state)
        # Add that object to a collection
        self.add_relationship(
            pid,
            f"info:fedora/{pid}",
            "info:fedora/fedora-system:def/relations-external#isMemberOfCollection",
            f"info:fedora/{collection}",
            is_literal="false",
        )
        # Give it a content model
        self.add_relationship(
            pid,
            f"info:fedora/{pid}",
            "info:fedora/fedora-system:def/model#hasModel",
            "info:fedora/islandora:binaryObjectCModel",
            is_literal="false",
        )
        # Version relationships
        self.change_versioning(pid, "RELS-EXT", "true")
        # Add the AIP
        # Add technical metadata about the AIP
        # Add the DIP
        # Give it metadata
        # Transform DublinCore
        return f"Successfully created {pid}."


if __name__ == "__main__":
    # x = FedoraObject().create_digital_object(
    #     "test", "Mark's New Test", "islandora:test"
    # )
    x = FedoraObject().add_managed_datastream(
        "test:10",
        "AIP",
        file="Chronicling_COVID-19-20210215T185151Z-001-2aaa349a-12a2-4338-90d1-5097bb989acc.7z",
    )
