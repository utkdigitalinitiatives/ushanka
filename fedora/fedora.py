import requests
from urllib.parse import quote
import magic
import os
from fedora.metadata import MetadataBuilder, GSearchConnection


class FedoraObject:
    def __init__(
        self, fedora_url="http://localhost:8080", auth=("fedoraAdmin", "fedoraAdmin")
    ):
        self.fedora_url = fedora_url
        self.auth = auth

    def ingest(
        self,
        namespace,
        label,
        state="A",
    ):
        """Creates a new object in Fedora and returns a persistent identifier.

        Args:
            namespace (str): The namespace of the new persistent identifier.
            label (str): The label of the new digital object.
            state (str): The state of the new object. Must be "A" or "I".

        Returns:
            str: The persistent identifier of the new object.

        Examples:
            >>> FedoraObject().ingest("test", "My new digital object", "islandora:test")
            "test:1"

        """
        if state not in ("A", "I"):
            raise Exception(
                f"\nState specified for new digital object based on label: {label} is not valid."
                f"\nMust be 'A' or 'I'."
            )
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
            subject (str): The subject of the relationship.  This should refer to the pid (for external relationships)
            or the dsid (for internal relationships). For
            predicate (str): The predicate of the new relationship.
            obj (str): The object of the new relationship.  Can refer to a graph or a literal.
            is_literal (str): This defaults to "true" but can also be "false." It specifies whether the object is a graph or a literal.

        Returns:
            int: The status code of the post request.

        Examples:
            >>> FedoraObject().add_relationship(pid="test:6", subject="info:fedora/test:6",
            ... predicate="info:fedora/fedora-system:def/relations-external#isMemberOfCollection",
            ... obj="info:fedora/islandora:test", is_literal="false",)
            200

        """
        r = requests.post(
            f"{self.fedora_url}/fedora/objects/{pid}/relationships/new?subject={quote(subject, safe='')}"
            f"&predicate={quote(predicate, safe='')}&object={quote(obj, safe='')}&isLiteral={is_literal}",
            auth=self.auth,
        )
        if r.status_code == 200:
            return r.status_code
        else:
            raise Exception(
                f"Unable to add relationship on {pid} with subject={subject}, predicate={predicate}, and object={obj}, "
                f"and isLiteral as {is_literal}.  Returned {r.status_code}."
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
                f"Unable to change versioning of the {dsid} datastream on {pid} to {versionable}.  Returned "
                f"{r.status_code}."
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
            f"{self.fedora_url}/fedora/objects/{pid}/datastreams/{dsid}/?controlGroup=M&dsLabel={dsid}&versionable="
            f"{versionable}&dsState={datastream_state}&checksumType={checksum_type}",
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


class BornDigitalObject(FedoraObject):
    def __init__(
        self,
        path,
        namespace,
        label,
        collection,
        state,
        desriptive_metadata,
        fedora="http://localhost:8080",
        auth=("fedoraAdmin", "fedoraAdmin"),
    ):
        self.path = path
        self.namespace = namespace
        self.label = label
        self.collection = collection
        self.state = state
        self.original_metadata = desriptive_metadata
        super().__init__(fedora, auth)

    def add_to_collection(self, pid):
        """Adds the object to a collection in Fedora."""
        return self.add_relationship(
            pid,
            f"info:fedora/{pid}",
            "info:fedora/fedora-system:def/relations-external#isMemberOfCollection",
            f"info:fedora/{self.collection}",
            is_literal="false",
        )

    def assign_binary_content_model(self, pid):
        """Assigns binary content model to digital object."""
        return self.add_relationship(
            pid,
            f"info:fedora/{pid}",
            "info:fedora/fedora-system:def/model#hasModel",
            "info:fedora/islandora:binaryObjectCModel",
            is_literal="false",
        )

    def add_archival_information_package(self, pid):
        """Adds the AIP to the OBJ datastream."""
        # TODO: This will change.  For now, the idea is to assume that the OBJ is in an AIP directory on disk. This is
        #       for demo purposes only. This will change once we know where the AIP will come from.
        aip = ""
        for path, directories, files in os.walk(f"{self.path}/AIP"):
            aip = self.add_managed_datastream(pid, "OBJ", f"{self.path}/AIP/{files[0]}")
        if aip == "":
            raise Exception(
                f"\nFailed to create OBJ on {pid}. No file was found in {self.path}/AIP/."
            )
        return aip

    def add_dissemination_information_package(self, pid):
        """Adds the DIP to a datastream called DIP."""
        dip = ""
        for path, directories, files in os.walk(f"{self.path}/DIP"):
            dip = self.add_managed_datastream(pid, "DIP", f"{self.path}/DIP/{files[0]}")
        if dip == "":
            raise Exception(
                f"\nFailed to create OBJ on {pid}. No file was found in {self.path}/AIP/."
            )
        return dip

    def add_technical_metadata(self):
        return

    def add_mods_metadata(self, pid):
        """Adds a MODS datastream."""
        MetadataBuilder(self.label, self.original_metadata, pid).build_mods()
        response = self.add_managed_datastream(pid, "MODS", "temp/MODS.xml")
        if response == "":
            raise Exception(f"\nFailed to create MODS on {pid}.")
        GSearchConnection(pid).update()
        return

    def add_a_thumbnail(self, pid):
        """Adds a thumbnail"""
        self.add_managed_datastream(pid, "TN", f"{self.path}/TN.jpg")
        return

    def new(self):
        pid = self.ingest(self.namespace, self.label, self.state)
        self.add_to_collection(pid)
        self.assign_binary_content_model(pid)
        self.change_versioning(pid, "RELS-EXT", "true")
        self.add_archival_information_package(pid)
        self.add_mods_metadata(pid)
        self.add_dissemination_information_package(pid)
        self.add_a_thumbnail(pid)
        return pid


if __name__ == "__main__":
    sample_metadata = {
        "title": "Chronocling Covid",
        "abstract": "This test deposit includes objects submitted as part of the Chronicling Covid-19 project.",
        "publisher": "University of Tennessee",
        "date": "2020",
        "language": "English",
        "rights": "Copyright Not Evaluated",
    }
    print(
        BornDigitalObject(
            "data/object_1", "test", "Testing", "islandora:test", "A", sample_metadata
        ).new()
    )
