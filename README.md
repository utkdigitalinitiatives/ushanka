# Ushanka

This is a fail-fast application to help us think about how to model AIPs and DIPs from Archivematica in Fedora, what
our workflow for deposit may look like, and how to make our DIP discoverable in ArchivesSpace.

Technical information is available on [readthedocs](https://ushanka.readthedocs.io/en/latest/).

## What is this supposed to do?

Ushanka gets AIPs and DIPs from Archivematica and a storage service and deposits it in Fedora.

![Ushanka Overview](imgs/ushanka.svg)

Currently, it does not delete the package in Archivematica.  While this would be easy to do, I wanted to first focus on
thinking about the steps up through storage and what should go into Fedora.

## What does the final object look like?

Right now, I've modelled this as a traditional Binary Object.

Arguably, we should separate the AIP and DIP and treat the parts of the DIPs as single objects.

![An Ushanka Fedora Object](imgs/ushanka_object.svg)

Currently, the object has no TN or TECHMD datastreams.  Its RDF looks like this.

```turtle
@prefix ns0: <info:fedora/fedora-system:def/relations-external#> .
@prefix ns1: <info:fedora/fedora-system:def/model#> .

<info:fedora/test:27>
  ns0:isMemberOfCollection <info:fedora/islandora:test> ;
  ns1:hasModel <info:fedora/islandora:binaryObjectCModel> .
```