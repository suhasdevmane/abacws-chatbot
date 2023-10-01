from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.extras.infixowl import Class, Ontology, Property, min, only, some

CPR = Namespace("http://purl.org/cpr/0.75#")
INF = Namespace("http://www.loa-cnr.it/ontologies/InformationObjects.owl#")
EDNS = Namespace("http://www.loa-cnr.it/ontologies/ExtendedDnS.owl#")
DOLCE = Namespace("http://www.loa-cnr.it/ontologies/DOLCE-Lite.owl#")
REL = Namespace("http://www.geneontology.org/owl#")
GALEN = Namespace("http://www.co-ode.org/ontologies/galen#")
TIME = Namespace("http://www.w3.org/2006/time#")
CYC = Namespace("http://sw.cyc.com/2006/07/27/cyc/")


def infixowl_example():
    g = Graph()
    g.bind("cpr", CPR, override=False)
    g.bind("ro", REL, override=False)
    g.bind("inf", INF, override=False)
    g.bind("edns", EDNS, override=False)
    g.bind("dol", DOLCE, override=False)
    g.bind("time", TIME, override=False)
    g.bind("galen", GALEN, override=False)

    Class.factoryGraph = g
    Property.factoryGraph = g
    Ontology.factoryGraph = g

    cprOntology = Ontology(URIRef("http://purl.org/cpr/owl"))  # noqa: N806
    cprOntology.imports = [
        URIRef("http://obo.sourceforge.net/relationship/relationship.owl"),
        URIRef(DOLCE),
        URIRef(EDNS),
        URIRef("http://www.w3.org/2006/time#"),
    ]
    cprOntology.comment = [
        Literal(
            """This OWL ontology was generated by Fuxi 0.85b.dev-r107
               (with newly added Infix OWL syntax library).  It imports the
               OBO relationship ontology, DOLCE, and OWL time. It formally
               defines a focused, core set of archetypes [Jung, C.]
               replicated in various patient record terminology. This core is
               defined in RDF and follows the normalization principles
               of "rigorous formal ontologies" [Rector, A.]."""
        )
    ]
    cprOntology.setVersion(Literal("0.75"))

    # Relations
    # represented-by
    representationOf = Property(  # noqa: N806
        CPR["representation-of"],
        inverseOf=Property(CPR["represented-by"]),
        comment=[
            Literal(
                """Patient records stand in the cpr:representation-of relation
                   with patients"""
            )
        ],
    )
    representedBy = Property(  # noqa: F841, N806
        CPR["represented-by"], inverseOf=representationOf
    )
    # description-of
    descrOf = Property(  # noqa: N806
        CPR["description-of"],
        comment=[
            Literal(
                """Clinical descriptions stand in the cpr:description-of
                   relation with various clinical phenomenon"""
            )
        ],
        domain=[Class(CPR["clinical-description"])],
    )
    # cpr:interpreted-by
    interpretedBy = Property(  # noqa: F841, N806
        CPR["interpreted-by"],
        comment=[
            Literal(
                """Signs and symptoms are interpreted by rational physical
                   objects (people)"""
            )
        ],
        domain=[Class(CPR["medical-sign"]) | Class(CPR["symptom"])],
        range=[Class(CPR.person)],
    )
    # cpr:realized-by
    realizedBy = Property(  # noqa: N806
        CPR["realized-by"],
        comment=[
            Literal(
                """The epistemological relation in which screening acts and
                   the problems they realize stand to each other"""
            )
        ],
        inverseOf=Property(CPR["realizes"]),
        domain=[Class(CPR["medical-problem"])],
        range=[Class(CPR["screening-act"])],
    )
    # cpr:realizes
    realizes = Property(CPR["realizes"], inverseOf=realizedBy)  # noqa: F841

    # Classes
    # cpr:person
    person = Class(CPR.person)
    person.comment = [
        Literal(
            """A class which directly corresponds with the “Person” class in
               both GALEN and Cyc"""
        )
    ]
    person.subClassOf = [Class(EDNS["rational-physical-object"])]
    person.equivalentClass = [Class(GALEN.Person), Class(CYC.Person)]

    # cpr:patient
    patient = Class(CPR.patient)
    patient.comment = [
        Literal(
            """A class which directly corresponds with the “Patient”
               and “MedicalPatient” classes in GALEN / Cyc"""
        )
    ]
    # patient.equivalentClass = [Class(GALEN.Patient),Class(CYC.MedicalPatient)]
    patient.subClassOf = [CPR["represented-by"] @ some @ Class(CPR["patient-record"])]
    person += patient

    # cpr:clinician
    clinician = Class(CPR.person)
    clinician.comment = [
        Literal(
            """A person who plays the clinician role (typically Nurse,
               Physician / Doctor, etc.)"""
        )
    ]
    person += clinician

    # bytes
    bytes = Class(CPR.bytes)
    bytes.comment = [
        Literal(
            """The collection of physical objects which constitute a stream of
               bytes in memory, disk, etc."""
        )
    ]
    bytes.subClassOf = [DOLCE["non-agentive-physical-object"]]

    # cpr:patient-record
    patientRecord = Class(CPR["patient-record"])  # noqa: N806
    patientRecord.comment = [
        Literal(
            """a class (a representational artifact [REFTERM]) depicting
               relevant clinical information about a specific patient and is
               primarily comprised of one or more
               cpr:clinical-descriptions."""
        )
    ]
    patientRecord.seeAlso = [URIRef("")]
    patientRecord.subClassOf = [
        bytes,
        # Class(CYC.InformationBearingThing),
        CPR["representation-of"] @ only @ patient,
        REL.OBO_REL_has_proper_part @ some @ Class(CPR["clinical-description"]),
    ]

    # cpr:medical-problem
    problem = Class(
        CPR["medical-problem"],
        subClassOf=[
            Class(DOLCE.quality),
            realizedBy @ only @ Class(CPR["screening-act"]),
        ],
    )
    problem.comment = [
        Literal(
            """.. problems that clearly require the intervention of a health
                  care professional. These include acute problems requiring
                  hospitalization and chronic problems requiring long-term
                  management."""
        )
    ]

    # cpr:clinical-description
    clinDescr = Class(CPR["clinical-description"])  # noqa: N806
    clinDescr.disjointWith = [CPR["patient-record"]]
    clinDescr.comment = [
        Literal(
            """A class which corresponds (at least syntactically) with the HL7
               RIM Act Class, insofar as its members consist of clinical
               recordings (representational artifacts) of natural phenomena
               of clinical significance"""
        )
    ]
    clinDescr.subClassOf = [
        bytes,
        # Class(CYC.InformationBearingThing),
        DOLCE["has-quality"] @ some @ Class(TIME.TemporalEntity),
        descrOf @ min @ Literal(1),
    ]

    # cpr:medical-sign
    sign = Class(
        CPR["medical-sign"],
        subClassOf=[
            problem,
            Property(CPR["interpreted-by"]) @ only @ clinician,
            Property(CPR["interpreted-by"]) @ some @ clinician,
        ],
        disjointWith=[CPR.symptom],
    )
    sign.comment = [
        Literal(
            """A cpr:medical-problem which are specifically interpreted by a
               clinician. As such, this class is informally defined as an
               objective indication of a quality typically detected by a
               physician during a physical examination of a patient."""
        )
    ]

    symptom = Class(
        CPR["symptom"],
        subClassOf=[
            problem,
            Property(CPR["interpreted-by"]) @ only @ patient,
            Property(CPR["interpreted-by"]) @ some @ patient,
        ],
        disjointWith=[sign],
    )
    symptom.comment = [
        Literal(
            """(Medicine) any sensation or change in bodily function that is
               experienced by a patient and is associated with a particular
               disease."""
        )
    ]

    # clinical-act heriarchy
    clinicalAct = Class(  # noqa: N806
        CPR["clinical-act"], subClassOf=[Class(EDNS.activity)]
    )

    therapy = Class(CPR["therapeutic-act"], subClassOf=[clinicalAct])
    therapy += Class(CPR["physical-therapy"], disjointWith=[CPR["medical-therapy"]])
    therapy += Class(
        CPR["psychological-therapy"],
        disjointWith=[CPR["medical-therapy"], CPR["physical-therapy"]],
    )

    medicalTherapy = Class(  # noqa: N806
        CPR["medical-therapy"],
        disjointWith=[CPR["physical-therapy"], CPR["psychological-therapy"]],
    )
    therapy += medicalTherapy
    medicalTherapy += Class(CPR["substance-administration"])  # noqa: N806

    diagnosticAct = Class(CPR["diagnostic-act"], subClassOf=[clinicalAct])  # noqa: N806
    diagnosticAct.disjointWith = [CPR["therapeutic-act"]]

    screeningAct = Class(CPR["screening-act"])  # noqa: N806
    screeningAct += Class(CPR["laboratory-test"])  # noqa: N806

    diagnosticAct += screeningAct  # noqa: N806

    screeningAct += Class(  # noqa: N806
        CPR["medical-history-screening-act"],
        disjointWith=[CPR["clinical-examination"], CPR["laboratory-test"]],
    )

    screeningAct += Class(  # noqa: N806
        CPR["clinical-examination"],
        disjointWith=[CPR["laboratory-test"], CPR["medical-history-screening-act"]],
    )

    device = Class(  # noqa: F841
        CPR["medical-device"], subClassOf=[Class(GALEN.Device)]
    )

    print(g.serialize(format="turtle"))


if __name__ == "__main__":
    infixowl_example()
