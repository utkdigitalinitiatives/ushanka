Digital Asset Management of Born Digital Materials
==================================================

Once a SIP has been created with Archivematica, it is ready to be ingested into our digital asset management system.  This document describes its
shape and relationships between the various parts.

The Compound Object
-------------------

The SIP is a compound object, which is a collection of related objects.  The compound object is the top-level object in
the digital assets management system.  Each compound object is prescribed with several datastreams, including:

* MODS:  This metadata file contains basic descriptive information about the compound object, including title, identifier, date, and an abstract.
* RELS-EXT:  This metadata file contains relationships between the compound object and other objects in the digital asset management system.
* DC:  This metadata file contains descriptive information about the compound object, including title, identifier, date, and an abstract. It accompanies the MODS so that the properties are interoperable in our triple store.
* AIP: This datastream contains the AIP, which is a compressed file containing the original SIP and any migrated files important for preservation.
* DIP: This datastream contains the DIP, which is a compressed file containing the derivatives most appropriate for access.
* METS: This datastream contains the METS file, which is a metadata file that describes the structure of the SIP, AIP, and DIP.
* POLICY: This datastream contains the policy file, which is a metadata file that describes the rights and access restrictions for the compound object.

.. mermaid::

    erDiagram
        COMPOUNDOBJECT ||--o{ MODS : has
        COMPOUNDOBJECT ||--o{ RELS-EXT : has
        COMPOUNDOBJECT ||--o{ DC : has
        COMPOUNDOBJECT ||--o{ AIP : has
        COMPOUNDOBJECT ||--o{ DIP : has
        COMPOUNDOBJECT ||--o{ METS : has
        COMPOUNDOBJECT ||--o{ POLICY : has
        COMPOUNDOBJECT }|..|{ DIP-PART : contains

The DIP Parts
-------------

In order to enable any future access to files a part of the original SIP, the compound object is split into many DIP
parts. Each DIP part is a work with its own descriptive metadata, relationships, and access restrictions.  Each DIP part
is prescribed with several datastreams, including:

* MODS:  This metadata file contains basic descriptive information about the DIP part, including title, identifier, date, and an abstract.
* RELS-EXT:  This metadata file contains relationships between the DIP part and other objects in the digital asset management system.
* DC:  This metadata file contains descriptive information about the DIP part, including title, identifier, date, and an abstract. It accompanies the MODS so that the properties are interoperable in our triple store.
* PREMIS: This datastream contains the PREMIS file, which is a metadata file that describes the provenance of the DIP part.
* POLICY: This datastream contains the policy file, which is a metadata file that describes the rights and access restrictions for the DIP part.
* OBJ: This datastream contains the primary file from the DIP that the other files describe.

.. mermaid::

    erDiagram
        COMPOUNDOBJECT }|..|{ DIP-PART : contains
        COMPOUNDOBJECT }|..|{ DIP-PART2 : contains
        DIP-PART ||--o{ MODS : has
        DIP-PART ||--o{ RELS-EXT : has
        DIP-PART ||--o{ DC : has
        DIP-PART ||--o{ PREMIS : has
        DIP-PART ||--o{ POLICY : has
        DIP-PART ||--o{ OBJ : has
