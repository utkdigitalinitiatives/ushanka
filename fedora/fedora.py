import requests
from urllib.parse import quote


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

    def create_digital_object(self, object_namespace, object_label, collection, object_state="A"):
        # Ingest a new object
        pid = self.__ingest(object_namespace, object_label, object_state)
        # Add that object to a collection
        self.add_relationship(pid, f"info:fedora/{pid}", "info:fedora/fedora-system:def/relations-external#isMemberOfCollection", f"info:fedora/{collection}", is_literal="false")
        # Give it a content model
        self.add_relationship(pid, f"info:fedora/{pid}", "info:fedora/fedora-system:def/model#hasModel", "info:fedora/islandora:binaryObjectCModel", is_literal="false")
        # Version relationships
        # Add the AIP
        # Add the DIP
        # Give it metadata
        # Transform DublinCore
        return


if __name__ == "__main__":
    x = FedoraObject().create_digital_object("test", "Mark's New Test", "islandora:test")
