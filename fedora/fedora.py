import requests
from urllib.parse import quote


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
        r = requests.post(
            f"{self.fedora_url}/fedora/objects/new?namespace={namespace}&label={label}&state={state}",
            auth=self.auth,
        )
        if r.status_code == 201:
            return r.content
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
                f"Unable to add relationship on {pid} with subject={subject}, predicate={predicate}, and object={obj}, and isLiteral as {is_literal}.  Returned {r.status_code}"
            )

    def create_digital_object(self):
        # Ingest a new object
        # Add that object to a collection
        # Give it a content model
        # Version relationships
        # Add the AIP
        # Add the DIP
        # Give it metadata
        # Transform DublinCore
        return


if __name__ == "__main__":
    # x = FedoraObject().ingest(namespace="test", label="This is a test")
    x = FedoraObject().add_relationship(
        pid="test:6",
        subject="info:fedora/test:6",
        predicate="info:fedora/fedora-system:def/relations-external#isMemberOfCollection",
        obj="info:fedora/islandora:test",
        is_literal="false",
    )
