# ADMBw-Regelwerk — Prompt-Pack

> MDG-Version 2026.05 · 318 Stereotype · 44 abstrakt · Quelle `NAFv4-ADMBw-MDG-2026.05.xml` · ohne Zeitstempel

Dieses Dokument ist selbsttragend: Es enthält das vollständige ADMBw-Regelwerk (NAFv4) für die Modellierung aus Prosa. Keine weiteren Dateien nötig.

## Auftrag

Du bist Modellierungsassistent für Architekturmodelle nach der Methode Architektur der Bundeswehr (ADMBw, NAFv4). Übersetze den gelieferten Prosa-Text in ein regelkonformes Modell: Elemente mit Stereotyp, Beziehungen mit Quell- und Zieltyp.

## Eiserne Regeln

1. Keinen Stereotyp erfinden — nur Namen aus dem Katalog unten.
2. Abstrakte Stereotype (🔒) nie instanziieren. Immer einen konkreten Subtyp wählen (Abschnitt „Abstrakte Stereotype“).
3. Jede Beziehung gegen eine Topologie-Regel prüfen: Quelle = client/source/end[0], Ziel = supplier/target/end[1]. Zeilen mit nur „Weitere Rollen“ sind keine Kanten-Regel.
4. Nennt eine Regel einen abstrakten Endpunkt, sind alle seine konkreten Subtypen zulässig.
5. Schreibvarianten vor dem Namensvergleich normalisieren (Abschnitt „Aliases“).
6. Jede Aussage mit der Regelzeile belegen — keine ungeprüften ✓-Behauptungen.

## Ausgabeformat

- **Elemente:** Prosa-Stelle | Elementname | Stereotyp | Metaklasse
- **Beziehungen:** Quelle | Stereotyp | Ziel | erlaubt durch (Regelzeile)
- **Offene Punkte:** was der Prosa-Text nicht hergibt

---

## 1. Stereotyp-Katalog

318 Modell-Stereotype. 🔒 = abstrakt, nicht instanziierbar.

| Stereotype | Metatype | AppliesTo | 🔒 | Beschreibung |
|---|---|---|---|---|
| AchievedEffect | AchievedEffect | Dependency | – | A tuple that exists between an ActualState (e.g., observed/measured during testing) of an element that attempts to achieve a DesiredEffect a … |
| Achiever | Achiever | Object | 🔒 ja | An ActualResource, ActualProject or ActualEnterprisePhase that can deliver a DesiredEffect. |
| ActivityPerformableUnderCondition | ActivityPerformableUnderCondition | Dependency | – | The ActualCondition under which an Activity is performed. |
| ActivitySupportsService | ActivitySupportsService | Realisation | – | Relation states that a process is necessary for the implementation of a service. |
| ActsUpon | ActsUpon | Dependency | – | Asserts that something (subject) is acted upon by an OperationalActivity (activity). |
| ActualCondition | ActualCondition | Object | – | An individual describing an actual situation with respect to circumstances under which an OperationalActivity, Function or ServiceFunction c … |
| ActualConditionToActualResource | ActualConditionToActualResource | Dependency | – | A relationship that expresses that a actual resource is an actual situation. |
| ActualEnduringTask | ActualEnduringTask | Object | – | An actual undertaking recognized by an enterprise as being essential to achieving its goals - i.e. |
| ActualEnterprisePhase | ActualEnterprisePhase | Object | – | The ActualState that describes the phase of an Enterprise endeavor. |
| ActualEnvironment | ActualEnvironment | Object | – | The ActualState that describes the circumstances of an Environment. |
| ActualLocation | ActualLocation | Object | – | The ActualState that describes a physical location, for example using text to provide an address, Geo-coordinates, etc. |
| ActualMeasurement | ActualMeasurement | Slot | – | An actual value that is applied to a Measurement. |
| ActualMeasurementSet | ActualMeasurementSet | Object | – | A set of ActualMeasurements. |
| ActualMeasurementSetAppliesFor | ActualMeasurementSetAppiesFor | Dependency | – | A relationship that expresses which actual measurement applies for an element. |
| ActualOrganization | ActualOrganization | Object | – | An actual formal or informal organizational unit, e.g. "Driving and Vehicle Licensing Agency", "UAF team Alpha". |
| ActualOrganizationalResource | ActualOrganizationalResource | Object | 🔒 ja | Abstract element for an ActualOrganization, ActualPerson or ActualPost. |
| ActualOrganizationRole | ActualOrganizationRole | Slot | – | An ActualOrganizationalResource that is applied to a ResourceRole. |
| ActualPerson | ActualPerson | Object | – | An individual human being. |
| ActualPost | ActualPost | Object | – | An actual, specific post, an instance of a Post "type" - e.g., "President of the United States of America." where the Post would be presiden … |
| ActualProject | ActualProject | Object | – | A time-limited endeavor to provide a specific set of ActualResource that meet specific Capability needs. |
| ActualProjectConsults | ActualProjectConsults | Dependency | – | A relation that expresses that a project consults an OrganizationalResource. |
| ActualProjectDependency | ActualProjectDependency | Dependency | – | Relationship that is a dependency of a actualproject on a actualproject. |
| ActualProjectInforms | ActualProjectInforms | Dependency | – | A relation that expresses that a project informs an OrganizationalResource. |
| ActualProjectMilestone | ActualProjectMilestone | Object | – | An event with a start date in a ActualProject from which progress is measured. |
| ActualProjectMilestoneRole | ActualProjectMilestoneRole | Slot | – | An ActualProjectMilestone that is applied to a ProjectMilestoneRole. |
| ActualPropertySet | ActualPropertySet | Object | – | A set or collection of Actual properties. |
| ActualResource | ActualResource | Object | – | Role in an Organisation, where the role carries the authority to undertake a function - through the ActualOrganizationalResource given the r … |
| ActualResourceNeededByActualProjectMilestone | ActualResourceNeededByActualProjectMilestone | Dependency | – | A relationship that expresses that an actual resource is needed by actual project milestones. |
| ActualResourceRelationship | ActualResourceRelationship | InformationFlow | – | An actual resource flow existing between ActualResources (i.e. flow of data, people, materiel, or energy). |
| ActualResourceRole | ActualResourceRole | Slot | – | An instance of a ResourcePerformer. |
| ActualResourceToActualProjectMilestone | ActualResourceToActualProjectMilestone | Dependency | – | A relationship that expresses that an actual resource is mapped to actual project milestones. |
| ActualResponsibleResource | ActualResponsibleResource | Object | 🔒 ja | An abstract type grouping responsible OrganizationalResources. |
| ActualService | ActualService | Object | – | An individual ServiceSpecification. |
| ActualServiceSpecificationRole | – | Slot | – | An instance of a ServiceSpecification in context of a ServiceSpecification. |
| ActualState | ActualState | Object | 🔒 ja | Abstract element that applies temporal extent to a set of elements realized as Instance Specifications. |
| AffectedActivity | AffectedActivity | Dependency | – | A relationship that expresses which resource is affected by a operational activity. |
| AffectedFunctions | AffectedFunctions | Dependency | – | A relationship that expresses which function is affected by a resource. |
| AffectedResource | AffectedResource | Dependency | – | A relationship that expresses which operational activity is affected by a resource. |
| Alias | Alias | Note | – | A metamodel Artifact used to define an alternative name for an element. |
| AlignsWithGoal | AlignsWithGoal | Dependency | – | A relationship that expresses that an element is aligned with a goal. |
| ArbitraryConnector | ArbitraryConnector | Dependency | – | Represents a visual indication of a connection used in high level operational concept diagrams. |
| ArchitecturalDescription | ArchitecturalDescription | Package | – | An Architecture Description is a work product used to express the Architecture of some System Of Interest. |
| ArchitecturalReference | ArchitecturalReference | Dependency | – | A tuple that specifies that one architectural description refers to another. |
| ArchitecturalSequence | ArchitecturalSequence | Dependency | – | A relationship that specifies that one architectural description is the successor of another. |
| Architecture | Architecture | Class | 🔒 ja | An abstract type that represents a generic architecture. Subtypes are OperationalArchitecture and ResourceArchitecture. |
| ArchitectureForProject | ArchitectureForProject | Dependency | – | A relationship that expresses that a architectural description belongs to a actual project. |
| ArchitectureMetadata | ArchitectureMetadata | Note | – | Information associated with an ArchitecturalDescription, that supplements the standard set of tags used to summarize the Architecture. |
| Asset | Asset | Class | 🔒 ja | Asset as applied to Security views, an abstract type that indicates the types of elements that can be considered as a subject for security a … |
| AssetRole | AssetRole | Part | 🔒 ja | AssetRole as applied to Security views, an abstract element that indicates the type of elements that can be considered as a subject for secu … |
| BoundaryCondition | BoundaryCondition | Dependency | – | A relationship that expresses which environment is relevant to an resource exchange. |
| BusinessProcess | BusinessProcess | Activity | 🔒 ja | An abstract type that represents a behavior or process (i.e. a Function or OperationalActivity) that can be performed by a Performer. |
| BWRequirement | – | Requirement | 🔒 ja | Abstract base class for requirements. |
| Capability | Capability | Class | – | A high level specification of the enterprise's ability to execute a specified course of action. |
| CapabilityConfiguration | CapabilityConfiguration | Class | – | A composite structure representing the physical and human resources (and their interactions) in an enterprise, assembled to meet a capabilit … |
| CapabilityDependency | CapabilityDependency | Dependency | – | A tuple that asserts that one Capability is dependent from another. |
| CapabilityForTask | CapabilityForTask | Abstraction | – | A tuple that asserts that a Capability is required in order for an Enterprise to conduct a phase of an EnduringTask. |
| CapabilityGeneralization | CapabilityGeneralization | Generalization | – | A CapabilityGeneralization is a taxonomic relationship between a more general Capability and a more specific Capability. |
| CapabilityRole | CapabilityRole | Part | – | A high level specification of the enterprise's ability to execute a specified course of action. |
| CapabilityRoleDependency | CapabilityRoleDependency | Dependency | – | A tuple that asserts that one CapabilityRole is dependent from another. |
| CapableElement | CapableElement | – | 🔒 ja | An abstract type that represents a structural element that can perform behaviors (i.e. OperationalActivity). |
| Checks | Checks | Dependency | – | Relation that shows that an acceptance criterion (FitCriterion) is valid for a functional or non-functional requirement. |
| Classification | Classification | Class | – | Classification according to STANAG 1059. |
| Classified | Classified | Dependency | – | Relationship that indicates which classification an element has. |
| Command | Command | InformationFlow | – | A type of ResourceExchange that asserts that one OrganizationalResource commands another. |
| Competence | Competence | Class | – | A specific set of abilities defined by knowledge, skills and aptitude. |
| CompetenceForRole | CompetenceForRole | Dependency | – | A tuple used to associate an organizational role with a specific set of required competencies. |
| CompliesViewpoint | CompliesViewpoint | Dependency | – | Relationship that expresses that a view has been created according to the specifications of a viewpoint. |
| ConceptItem | ConceptItem | – | 🔒 ja | Abstract, an item which may feature in a HighLevelOperationalConcept. |
| ConceptRole | ConceptRole | Part | – | Usage of a ConceptItem in the context of a HighLevelOperationalConcept. |
| Concern | Concern | Class | – | Interest in an EnterprisePhase (EnterprisePhase is synonym for System in ISO 42010) relevant to one or more of its stakeholders. |
| ConcernForActualEnterprisePhase | ConcernForActualEnterprisePhase | Dependency | – | A relationship that expresses which concerns are covered by an actual enterprise phase. |
| ConcernForView | ConcernForView | Dependency | – | A relationship that expresses which concerns are covered by view. |
| ConcernForViewpoint | ConcernForViewpoint | Dependency | – | A relationship that expresses which concerns are covered by viewpoint. |
| Condition | Condition | Class, DataType | – | A type that defines the Location, Environment and/or GeoPoliticalExtent. |
| ConflictsWith | ConflictsWith | Dependency | – | Relation that represents a conflict between two requirements. |
| ConformsTo | ConformsTo | Dependency | – | A relationship that expresses that an UAFElement conforms to a standard. |
| ConsumedBy | ConsumedBy | Dependency | – | Asserts that a service is consumed by a node. It is not required to know what provides the service. |
| Consumes | Consumes | Abstraction | – | A tuple that asserts that a service in someway contributes or assists in the execution of an OperationalActivity. |
| Control | Control | InformationFlow | – | A type of ResourceExchange that asserts that one PhysicalResource controls another PhysicalResource (i.e. |
| DataElement | DataElement | Class | – | A formalized representation of data that is managed by or exchanged between resources. |
| DataElementStoredIn | DataElementStoredIn | Dependency | – | Relation says that a data is stored in software. |
| DataModel | DataModel | Package | – | A structural specification of data types, showing relationships between them that is devoid of implementation detail. |
| DataRole | DataRole | Part | – | A usage of DataElement that exists in the context of an ResourceAsset. |
| Definition | Definition | Note | – | A comment containing a description of an element in the architecture. |
| DerivedFrom | DerivedFrom | Dependency | – | Relation that shows that a functional or non-functional requirement is based on a process, role and task carrier, information element or oth … |
| DescribedBy | DescribedBy | Dependency | – | A relationship that expresses that an architectural description describes an architecture. |
| DesiredEffect | DesiredEffect | Dependency | – | A tuple relating the Desirer (a Capability or OrganizationalResource) to an ActualState. |
| Desirer | Desirer | – | 🔒 ja | Abstract type used to group architecture elements that might desire a particular effect. |
| DocumentReference | DocumentReference | Class | – | The element describes a regulation, instruction or a general document. |
| ElementCatalogue | – | Package | – |  |
| EnduringTask | EnduringTask | Class | – | A type of template behavior recognized by an enterprise as being essential to achieving its goals - i.e. |
| Energy | Energy | Class | – | A representation of any kind of energy. |
| EnterpriseGoal | EnterpriseGoal | Class | – | A statement about a state or condition of the enterprise to be brought about or sustained through appropriate Means. |
| EnterprisePhase | EnterprisePhase | Class | – | A current or future state of the wholeLifeEnterprise or another EnterprisePhase. |
| EnterpriseVision | EnterpriseVision | Class | – | A Vision describes the future state of the enterprise, without regard to how it is to be achieved. |
| Environment | Environment | Class | – | A definition of the environmental factors in which something exists or functions. |
| EnvironmentalCondition | EnvironmentalCondition | Dependency | – | Relationship that indicates under which environment an exhibits-relationship takes place. |
| EnvironmentalContext | EnvironmentalContext | Dependency | – | Relationship that indicates under which condition an measurement counts. |
| EnvironmentProperty | EnvironmentProperty | Class | – | A property of an Environment that is typed by a Condition. |
| Evaluates | Evaluates | Realisation | – | This relation states that an evaluation criterion (FulfilmentCriterion) can be assigned to a specific acceptance criterion (FitCriterion). |
| Exchange | Exchange | – | 🔒 ja | Abstract tuple, grouping OperationalExchanges and ResourceExchanges that exchange Resources. |
| ExchangeItem | ExchangeItem | – | 🔒 ja | An abstract grouping for elements that defines the types of elements that can be exchanged between Assets and conveyed by an Exchange. |
| Exhibits | Exhibits | Abstraction | – | A tuple that exists between a CapableElement and a Capability that it meets under specific environmental conditions. |
| Expresses | Expresses | Dependency | – | A relationship that expresses that an architectural description includes the following architectures. |
| FieldedCapability | FieldedCapability | Object | – | An individual, fully-realized capability. |
| FillsPost | FillsPost | Dependency | – | A tuple that asserts that an ActualPerson fills an ActualPost. |
| Finding | Finding | Class | – | An ascertainment made in the model, which relates to the methodology used, the subject under consideration, the tool or something else. |
| FitCriterion | FitCriterion | Class | – | This element represents an acceptance criterion for a functional or non-functional requirement. |
| Forecast | Forecast | Dependency | – | A tuple that specifies a transition from one Asset, Standard, Competence to another future one. |
| ForecastPeriod | ForecastPeriod | Dependency | – | Planning phase for which the forecast is valid. |
| FormStoredIn | FormStoredIn | Dependency | – | Relation states that a digital form is stored in software. |
| FulfilmentCriterion | FulfilmentCriterion | Class | – | This element represents a criterion for evaluating the degree of implementation of a functional or non-functional requirement. |
| Function | Function | Activity | – | An Activity which is specified in the context to the ResourcePerformer (human or machine) that IsCapableToPerform it. |
| FunctionAction | FunctionAction | Action | – | A call of a Function indicating that the Function is performed by a ResourceRole in a specific context. |
| FunctionalRequirement | FunctionalRequirement | Requirement | – | The element represents a functional requirement (what should the system / software be able to do?). |
| FunctionControlFlow | FunctionControlFlow | ControlFlow | – | An ActivityEdge that shows the flow of control between FunctionActions. |
| FunctionEdge | FunctionEdge | – | 🔒 ja | A tuple that shows the flow of Resources (objects/data) between FunctionActions. |
| FunctionObjectFlow | FunctionObjectFlow | ObjectFlow | – | An ActivityEdge that shows the flow of Resources (objects/data) between FunctionActions. |
| FunctionSubject | FunctionSubject | Dependency | – | A relationship that expresses that a function uses certain resources. |
| GeoPoliticalExtentType | GeoPoliticalExtentType | DataType | – | A geospatial extent whose boundaries are defined by declaration or agreement by political parties. |
| GoalForActualEnterprisePhase | GoalForActualEnterprisePhase | Dependency | – | A relationship that expresses which actual enterprisephase implements an enterprisegoal. |
| HighLevelOperationalConcept | HighLevelOperationalConcept | Class | – | Describes the Resources and Locations required to meet an operational scenario from an integrated systems point of view. |
| HostedOn | HostedOn | Dependency | – | Relation states that hardware (virtualized) or software is hosted on a virtualized platform or physical hardware. |
| Implements | Implements | Abstraction | – | A tuple that defines how an element in the upper layer of abstraction is implemented by a semantically equivalent element (i.e. |
| ImplementsProtocol | ImplementsProtocol | Dependency | – | A relationship that expresses which protocol implements an architectural element. |
| Information | Information | Note | – | A comment that describes the state of an item of interest in any medium or form -- and is communicated or received. |
| InformationElement | InformationElement | Class | – | An item of information that flows between OperationalPerformers and is produced and consumed by the OperationalActivities that the Operation … |
| InformationRole | InformationRole | Part | – | A usage of InformationElement that exists in the context of an OperationalAsset. |
| InteractionMessage | InteractionMessage | Message | 🔒 ja | An abstract type that groups several types of messages used in the InteractionScenario. |
| InteractionRole | InteractionRole | Lifeline | 🔒 ja | An abstract type that represents an individual participant in the InteractionScenario. |
| IsAccountableFor | IsAccountableFor | Dependency | – | A relation that expresses that an OrganizationalResource is responsible for a resource, service or project in the context of an approval. |
| IsCapableToPerform | IsCapableToPerform | Abstraction | – | A relationship that says that a capable element performs an activity or action. |
| IsDuplicateOf | IsDuplicateOf | Dependency | – | Relation that represents that two requirements convey the same content. |
| IsEquivalentToStandardElement | IsEquivalentToStandardElement | Dependency | – | Relationship that indicates that a model element corresponds to a catalog element. |
| IsResponsibleFor | IsResponsibleFor | Dependency | – | A relation that expresses that an OrganizationalResource is responsible for a resource, service or project. |
| JustifiedBy | JustifiedBy | Dependency | – | Relation states that an Constraint is derived from a reference (Reference, DocumentReference, SMEReference). |
| KnownResource | KnownResource | Class | – | Asserts that a known ResourcePerformer constrains the implementation of the OperationalPerformer that plays the role in the LogicalArchitect … |
| Location | Location | Class, DataType | – | A specification of the generic area in which a LocationHolder is required to be located. |
| LocationHolder | LocationHolder | – | 🔒 ja | Abstract type, used to group elements that are allowed to be associated with a Location. |
| LocationType | LocationType | Dependency | – | A relationship that expresses which location is assigned to a location holder. |
| MapsToCapability | MapsToCapability | Abstraction | – | A tuple denoting that an Activity contributes to providing a Capability. |
| MeasurableElement | MeasurableElement | – | 🔒 ja | Abstract type, grouping elements that can be measured by applying MeasurementSets to them. |
| Measurement | Measurement | Part | – | A property of an element representing something in the physical world, expressed in amounts of a unit of measure. |
| MeasurementType | MeasurementType | Class | – | A type of a property representing something in the physical world, expressed in amounts of a unit of measure. |
| Metadata | Metadata | Note | – | A comment that can be applied to any element in the architecture. |
| MilestoneDependency | MilestoneDependency | Dependency | – | A tuple between two ActualProjectMilestones that denotes one ActualProjectMilestone follows from another. |
| NaturalResource | NaturalResource | Class | – | Type of physical resource that occurs in nature. |
| NeedsModificationOf | NeedsModificationOf | Dependency | – | Relation stats that a project makes adjustments to a resource. |
| NeedsResource | NeedsResource | Dependency | – | Relation stats that a project needs a resource. |
| NeedsService | NeedsService | Dependency | – | A relation that expresses that a project needs a service |
| NonfunctionalRequirement | NonfunctionalRequirement | Requirement | – | The element represents a non-functional requirement (how should the system / software be able to do something?). |
| OperationalActivity | OperationalActivity | Activity | – | An Activity that captures a logical process, specified independently of how the process is carried out. |
| OperationalActivityAction | OperationalActivityAction | Action | – | A call of an OperationalActivity in the context of another OperationalActivity. |
| OperationalActivityEdge | OperationalActivityEdge | – | 🔒 ja | A tuple that shows the flow of Resources (objects/information) between OperationalActivityActions. |
| OperationalAgent | OperationalAgent | Class | 🔒 ja | An abstract type grouping Operational Architecture and Operational Performer. |
| OperationalArchitecture | OperationalArchitecture | Class | – | A type used to denote a model of the Architecture, described from the Operational perspective. |
| OperationalArchitectureOfEnterprisePhase | OperationalArchitectureOfEnterprisePhase | Dependency | – | Relationship that says that in a actual enterprisephase an operational architecture is valid. |
| OperationalAsset | OperationalAsset | Class | 🔒 ja | An abstract element used to group the elements of OperationalAgent and InformationElement allowing them to own InformationRoles. |
| OperationalConnector | OperationalConnector | Connector | – | A Connector that goes between OperationalRoles representing a need to exchange Resources. It can carry a number of OperationalExchanges. |
| OperationalConstraint | OperationalConstraint | Class | – | A Rule governing a logical architectural element i.e. OperationalPerformer, OperationalActivity, InformationElement etc. |
| OperationalControlFlow | OperationalControlFlow | ControlFlow | – | An ActivityEdge that shows the flow of control between OperationalActivityActions. |
| OperationalExchange | OperationalExchange | InformationFlow | – | Asserts that a flow can exist between OperationalPerformers (i.e. flows of information, people, materiel, or energy). |
| OperationalExchangeItem | OperationalExchangeItem | – | 🔒 ja | An abstract grouping for elements that defines the types of elements that can be exchanged between OperationalPerformers and conveyed by an … |
| OperationalInterface | OperationalInterface | Class | – | A declaration that specifies a contract between the OperationalPerformer it is related to, and any other OperationalPerformers it can intera … |
| OperationalMessage | OperationalMessage | Message | – | Message for use in an Operational Event-Trace which carries any of the subtypes of OperationalExchange. |
| OperationalMessageFlow | OperationalMessageFlow | ControlFlow | – | A ProcessMessageFlow that shows the flow of message between OperationalActivityActions of different ActivityPartitions like Pools. |
| OperationalMethod | OperationalMethod | Operation | – | behavioral feature of a OperationalPerformer whose behavior is specified in an OperationalActivity. |
| OperationalObjectFlow | OperationalObjectFlow | ObjectFlow | – | An ActivityEdge that shows the flow of Resources (objects/information) between OperationalActivityActions. |
| OperationalParameter | OperationalParameter | Parameter | – | A type that represents inputs and outputs of an OperationalActivity. It is typed by an OperationalExchangeItem. |
| OperationalPerformer | OperationalPerformer | Class | – | A logical entity that IsCapableToPerform OperationalActivities which produce, consume and process Resources. |
| OperationalPort | OperationalPort | Port | – | An interaction point for an OperationalAgent through which it can interact with the outside environment and which is defined by an Operation … |
| OperationalRole | OperationalRole | Part | – | Usage of a OperationalPerformer or OperationalArchitecture in the context of another OperationalPerformer or OperationalArchitecture. |
| OperationalSignal | OperationalSignal | Signal | – | An item of information that flows between OperationalPerformers and is produced and consumed by the OperationalActivities that the Operation … |
| OperationalSignalProperty | OperationalSignalProperty | Part | – | A property of an OperationalSignal typed by OperationalExchangeItem. It enables OperationalExchangeItem e.g. |
| OperationalStateDescription | OperationalStateDescription | Class | – | A state machine describing the behavior of a OperationalPerformer, depicting how the OperationalPerformer responds to various events and the … |
| Organization | Organization | Class | – | A group of OrganizationalResources (Persons, Posts, Organizations and Responsibilities) associated for a particular purpose. |
| OrganizationalResource | OrganizationalResource | Class | 🔒 ja | An abstract type for Organization, Person Post and Responsibility. |
| OriginatesFrom | OriginatesFrom | Dependency | – | Relation that derives an element in the architectural model from a reference (Reference, DocumentReference, SMEReference). |
| OwnedMilestone | OwnedMilestone | Dependency | – | Relationship that expresses that actual project has a actual milestone. |
| OwnsActualMeasurementSet | OwnsActualMeasurementSet | Dependency | – | A relationship that expresses which actual measurement set an element owns. |
| OwnsMeasurement | OwnsMeasurement | Dependency | – | A relationship that expresses which measurement or measurement type an element owns. |
| OwnsProcess | OwnsProcess | Abstraction | – | A dependency relationship denoting that an ActualOrganizationResource owns an OperationalActivity. |
| PaperForm | PaperForm | Class | – | Form is a digitized or digitizable document, for example a scanned document. |
| PartOfCatalogue | PartOfCatalogue | Aggregation | – | This relation states that a category (RequirementCategory) belongs to a requirements catalog (RequirementCatalogue). |
| PartOfCategory | PartOfCategory | Aggregation | – | This relation states that his functional or non-functional requirement belongs to a category (RequirementCategory) of the requirements catal … |
| PerformsInContext | PerformsInContext | Abstraction | – | A relationship that says that a role performs an activity or action. |
| Person | Person | Class | – | A type of a human being used to define the characteristics that need to be described for ActualPersons (e.g. |
| PhysicalArchitectureOfEnterprisePhase | PhysicalArchitectureOfEnterprisePhase | Dependency | – | A relationship that expresses that an actual enterprise phase has resource architectures. |
| PhysicalLocation | PhysicalLocation | Dependency | – | A relationship that expresses that a location holder operates in an actual location. |
| PhysicalResource | PhysicalResource | Class | 🔒 ja | An abstract type defining physical resources (i.e. OrganizationalResource, ResourceArtifact and NaturalResource). |
| Post | Post | Class | – | A type of job title or position that a person can fill (e.g. Lawyer, Solution Architect, Machine Operator or Chief Executive Officer). |
| PostRole | PostRole | Part | – | A usage of a post in the context of another OrganizationalResource. Creates a whole-part relationship. |
| ProblemDomain | ProblemDomain | Part | – | A property associated with a logical architecture, used to specify the scope of the problem. |
| ProcessEdge | ProcessEdge | – | 🔒 ja | An abstract type that represents a behavior or process (i.e. a Function or OperationalActivity) that can be performed by a Performer. |
| ProcessGeneralization | ProcessGeneralization | Generalization | – | A ProcessGeneralization is a taxonomic relationship between a more general Process and a more specific Process. |
| ProcessMessageFlow | ProcessMessageFlow | – | 🔒 ja | A tuple that shows the flow of message between different ActivityPartitions like Pools. |
| ProcessOperation | ProcessOperation | – | 🔒 ja | An abstract type that represents a behavior or process (i.e. a Function or OperationalActivity) that can be performed by a Performer. |
| ProcessParameter | ProcessParameter | – | 🔒 ja | An abstract type that represents a behavior or process (i.e. a Function or OperationalActivity) that can be performed by a Performer. |
| ProcessUsage | ProcessUsage | – | 🔒 ja | An abstract type that represents a behavior or process (i.e. |
| Project | Project | Class | – | A type that describes types of time-limited endeavours that are required to meet one or more Capability needs. |
| ProjectMilestone | ProjectMilestone | Class | – | A type of event in a Project by which progress is measured. |
| ProjectMilestoneRole | ProjectMilestoneRole | Part | – | The role played by a ProjectMilestone in the context of a Project. |
| ProjectMilestoneToProjectTheme | ProjectMilestoneToProjectTheme | Dependency | – | A relationship that expresses which project theme is handled by which project milestone. |
| ProjectProvidesFunction | ProjectProvidesFunction | Dependency | – | Relation stats that a project realizes a function. |
| ProjectRole | ProjectRole | Part | – | Usage of a Project in the context of another Project. Creates a whole-part relationship. |
| ProjectSequence | ProjectSequence | Dependency | – | A tuple between two ActualProjects that denotes one ActualProject cannot start before the previous ActualProject is finished. |
| ProjectStatus | ProjectStatus | Slot | – | The status (i.e. level of progress) of a ProjectTheme for an ActualProject at the time of the ActualProjectMilestone. |
| ProjectSupportActivity | ProjectSupportActivity | Dependency | – | Relation stats that a project supports an activity. |
| ProjectTheme | ProjectTheme | Part | – | A property of a ProjectMilestone that captures an aspect by which the progress of ActualProjects may be measured. |
| PropertySet | PropertySet | – | 🔒 ja | An abstract type grouping architectural elements that can own Measurements. |
| PropertySetGeneralization | PropertySetGeneralisation | Generalization | – | A PropertySetGeneralization is a taxonomic relationship between a more general PropertySet and a more specific PropertySet. |
| Protocol | Protocol | Class | – | A Standard for communication over a network. Protocols may be composite, represented as a ProtocolStack made up of ProtocolLayers. |
| ProtocolImplementation | ProtocolImplementation | – | 🔒 ja | An abstract type grouping architectural elements that can implement Protocols. |
| ProtocolLayer | ProtocolLayer | Part | – | Usage of a Protocol in the context of another Protocol. Creates a whole-part relationship. |
| Protocolstack | Protocolstack | Class | – | A sub type of Protocol that contains the ProtocolLayers, defining a complete stack. |
| ProvidedServiceLevel | ProviededServiceLevel | Object | – | A sub type of ActualService that details a specific service level delivered by the provider. |
| Provides | Provides | Dependency | – | Asserts that a operational agent provides a service. |
| ProvidesCompetence | ProvidesCompetence | Dependency | – | A tuple that asserts that an ActualOrganizationalResource provides a specific set of Competencies. |
| ProvidesServiceFunction | ProvidesServiceFunction | Dependency | – | Relationship that expresses that a service function is provided by an interface. |
| RatifiedStandards | RatifiedStandards | Dependency | – | A relationship that expresses that an actual organization releases a standard. |
| RealiseRequirement | RealiseRequirement | Realisation | – | Relation states that a functional or non-functional requirement is realized through this element. |
| RealizedDesiredEffect | RealizedDesiredEffect | Dependency | – | Relationship that expresses which connector DesiredEffect the connector AchievedEffect realizes. |
| RealizesRecommendation | RealizesRecommendation | Realisation | – | Relation states that a Recommendation is realized through this element. |
| RealizingAchievedEffect | RealizingAchievedEffect | Dependency | – | Relationship that expresses which connector AchievedEffect realizes the connector DesiredEffect. |
| Recommendation | Recommendation | Class | – | Need for action from a finding. |
| Reference | Reference | Class | – | Element describes all types of references. |
| RefersTo | RefersTo | Dependency | – | Relationship that assigns a finding to a recommendation. |
| Refines | Refines | Dependency | – | Relation that represents a refinement of a requirement by another requirement. |
| Replaces | Replaces | Dependency | – | Relation that represents a replacement of a requirement with another requirement. |
| ReplaceStandardElement | ReplaceStandardElement | Dependency | – | Relation that represents a replacement of a standard element with another standard element |
| RequiredEnvironment | RequiredEnvironment | Dependency | – | A relationship that expresses that a location holder operates under specific environmental conditions. |
| RequiredResource | RequiredResource | Dependency | – | Relationship that indicates which resources a project milestone requires |
| RequiredServiceLevel | RequiredServiceLevel | Object | – | A sub type of ActualService that details a specific service level required of the provider. |
| RequirementCatalogue | RequirementCatalogue | Class | – | Element represents a catalog of requirements, which consists of different categories (RequirementCategory) of functional and non-functional … |
| RequirementCategory | RequirementCategory | Class | – | Element represents a category of a catalog of requirements. |
| Requires | Requires | Dependency | – | Relation that represents that a requirement assumes another requirement. |
| RequiresCompetence | RequiresCompetence | Abstraction | – | A tuple that asserts that an ActualOrganizationalResource is required to have a specific set of Competencies. |
| Resource | Resource | – | 🔒 ja | Abstract element grouping for all elements that can be conveyed by an Exchange. |
| ResourceArchitecture | ResourceArchitecture | Class | – | A type used to denote a model of the Architecture, described from the ResourcePerformer perspective. |
| ResourceArtifact | ResourceArtifact | Class | – | A type of man-made object that contains no human beings (i.e. satellite, radio, petrol, gasoline, etc.). |
| ResourceAsset | ResourceAsset | Class | 🔒 ja | An abstract element used to group the elements of ResourcePerformer and DataElement allowing them to own DataRoles |
| ResourceConnector | ResourceConnector | Connector | – | A channel for exchange between two ResourceRoles. |
| ResourceConstraint | ResourceConstraint | Class | – | A rule governing the structural or functional aspects of an implementation. |
| ResourceDependency | ResourceDependency | Dependency | – | Relationship that is a dependency of a resource on a resource. |
| ResourceExchange | ResourceExchange | InformationFlow | – | Asserts that a flow can exist between ResourcePerformers (i.e. flows of data, people, material, or energy). |
| ResourceExchangeItem | ResourceExchangeItem | – | 🔒 ja | An abstract type grouping elements that defines the types of elements that can be exchanged between ResourcePerformers and conveyed by a Res … |
| ResourceInterface | ResourceInterface | Class | – | A declaration that specifies a contract between the ResourcePerformers it is related to and any other ResourcePerformers it can interact wit … |
| ResourceMessage | ResourceMessage | Message | – | Message for use in an Resource Event-Trace which carries any of the subtypes of ResourceExchange. |
| ResourceMethod | ResourceMethod | Operation | – | A behavioral feature of a ResourcePerformer whose behavior is specified in a Function. |
| ResourceMitigation | ResourceMitigation | Class | – | A set of measures intended to implement an OperationalMitigation. |
| ResourceParameter | ResourceParameter | Parameter | – | A type that represents inputs and outputs of an Function. It is typed by a ResourceInteractionItem. |
| ResourcePerformer | ResourcePerformer | Class | 🔒 ja | An abstract grouping of elements that can perform Functions. |
| ResourcePort | ResourcePort | Port | – | An interaction point for a ResourcePerformer through which it can interact with the outside environment and which is defined by a ResourceIn … |
| ResourceRole | ResourceRole | Part | – | Usage of a ResourcePerformer in the context of another ResourcePerformer. Creates a whole-part relationship. |
| ResourceSignal | ResourceSignal | Signal | – | A property of an element representing something in the physical world, expressed in amounts of a unit of measure. |
| ResourceSignalProperty | ResourceSignalProperty | Part | – | A property of an ResourceSignal typed by ResourceExchangeItem. It enables ResourceExchangeItem e.g. |
| ResourceStateDescription | ResourceStateDescription | StateMachine | – | A state machine describing the behavior of a ResourcePerformer, depicting how the ResourcePerformer responds to various events and the actio … |
| ResourceToServiceDependency | ResourceToServiceDependency | Dependency | – | Relation states that a resource is dependent on a service. |
| Responsibility | Responsibility | Class | – | The type of duty required of a Person or Organization. |
| Responsible | Responsible | Dependency | – | Relation states that a project is responsible for a service or a material resource. |
| ResultsFrom | ResultsFrom | Dependency | – | Relationship expresses that an element of architecture is the reason for a finding. |
| Rule | Rule | Constraint | 🔒 ja | An abstract type for all types of constraint (i.e. an OperationalConstraint could detail the rules of accountancy best practice). |
| SameAs | SameAs | Dependency | – | A tuple that asserts that two elements refer to the same real-world thing. |
| Satisfy | Satisfy | Dependency | – | This relation states that an constraint affects an element. |
| SecurityConstraint | SecurityConstraint | Constraint | – | A type of rule that captures a formal statement to define security laws, regulations, guidances, and policy. |
| SecurityEnclave | SecurityEnclave | Class | – | Collection of information systems connected by one or more internal networks under the control of a single authority and security policy. |
| SecurityProcess | SecurityProcess | Activity | – | The security-related procedure that satisfies the security control requirement. |
| ServiceConnector | ServiceConnector | Connector | – | A channel for exchange between two ServiceSpecifications. Where one acts as the consumer of the other. |
| ServiceDependency | ServiceDependency | Dependency | – | Relationship that is a dependency of a service on a service, operational node or resource. |
| ServiceExchange | – | InformationFlow | – | Asserts that a flow can exist between Services (i.e., flows of information, people, material, or energy). |
| ServiceFunction | ServiceFunction | Activity | – | An Activity that describes the abstract behavior of ServiceSpecifications, regardless of the actual implementation. |
| ServiceFunctionAction | ServiceFunctionAction | Action | – | A call of a ServiceFunction in the context of another ServiceFunction. |
| ServiceGeneralization | ServiceGeneralization | Generalization | – | A ServiceGeneralization is a taxonomic relationship between a more general ServiceSpecification and a more specific ServiceSpecification. |
| ServiceInterface | ServiceInterface | Class | – | A contract that defines the ServiceMethods and ServiceMessageHandlers that the ServiceSpecification realizes. |
| ServiceMessage | ServiceMessage | Message | – | Message for use in a Service Event-Trace. |
| ServiceMethod | ServiceMethod | Operation | – | A behavioral feature of a ServiceSpecification whose behavior is specified in a ServiceFunction. |
| ServiceParameter | ServiceParameter | Parameter | – | A type that represents inputs and outputs of a ServiceFunction, represents inputs and outputs of a ServiceSpecification. |
| ServicePolicy | ServicePolicy | Class | – | A constraint governing the use of one or more ServiceSpecifications. |
| ServicePort | ServicePort | Port | – | An interaction point for a ServiceSpecification through which it can interact with the outside environment and which is defined by a Service … |
| ServiceProvision | ServiceProvision | Abstraction | – | An assertion that a Resource delivers a Service to a specified ServiceLevel. |
| ServiceSpecification | ServiceSpecification | Class | – | The specification of a set of functionality provided one element for the use of others. |
| ServiceSpecificationRole | ServiceSpecificationRole | Part | – | An assertion that a ServiceSecification calls upon another ServiceSpecification in order to deliver its stated functionality. |
| ServiceStateDescription | ServiceStateDescription | StateMachine | – | A state machine descripting the behavior of a ServiceSpecification, depicting how the ServiceSpecification responds to various events and th … |
| SMEReference | SMEReference | Class | – | Element stands for a result of a workshop or expert knowledge. |
| Software | Software | Class | – | A sub-type of ResourceArtifact that specifies an executable computer program. |
| Stakeholder | Stakeholder | – | 🔒 ja | individual, team, organization, or classes thereof, having an interest in an EnterprisePhase [ISO/IEC/IEEE 42010:2011]. |
| StakeholderConcern | StakeholderConcern | Dependency | – | A relationship that expresses which concern a stakeholder has. |
| Standard | Standard | Class | – | A ratified and peer-reviewed specification that is used to guide or constrain the architecture. |
| StandardOperationalActivity | StandardOperationalActivity | Activity | – | A sub-type of OperationalActivity that is a standard operating procedure. |
| StateDescription | StateDescription | StateMachine | – | An abstract type that represents a state machine (i.e. |
| StatementTask | StatementTask | Dependency | – | A relationship that expresses that an actual enterprise phase fulfills a actual enduring task. |
| StemsFrom | StemsFrom | Dependency | – | Relationship that states that one requirement stems from another. |
| StoredIn | StoredIn | Dependency | – | Relation states that a digital form or data is stored in software. |
| StrategicConstraint | StrategicConstraint | Class | – | A Rule governing a capability. |
| SubjectOfForecast | SubjectOfForecast | Class | 🔒 ja | An abstract type grouping elements that can be the subject of a Forecast. |
| SubjectOfOperationalConstraint | SubjectOfOperationalConstraint | – | 🔒 ja | An abstract type grouping elements that can be the subject of an OperationalConstraint. |
| SubjectOfResourceConstraint | SubjectOfResourceConstraint | – | 🔒 ja | An abstract type grouping elements that can be the subject of a ResourceConstraint. |
| SubjectOfSecurityConstraint | SubjectOfSecurityConstraint | – | 🔒 ja | An abstract grouping of elements that can be the subject of a SecurityConstraint. |
| SubOrganization | SubOrganization | Part | – | A type of a human being used to define the characteristics that need to be described for ActualPersons (e.g. |
| SuccessorOf | – | Dependency | – | A relationship between two elements that indicates that one element is the successor of the other. |
| System | System | Class | – | An integrated set of elements, subsystems, or assemblies that accomplish a defined objective. |
| Technology | Technology | Class | – | A sub type of ResourceArtifact that indicates a technology domain, i.e. nuclear, mechanical, electronic, mobile telephony etc. |
| TemporalPart | TemporalPart | Part | – | A current or future state of the wholeLifeEnterprise or another EnterprisePhase. |
| ToBeRealizedBy | ToBeRealizedBy | Dependency | – | Relation states that a functional or non-functional requirement should be realized through this element. |
| UAFElement | UAFElement | – | 🔒 ja | Abstract super type for all of the UAF elements. It provides a way for all of the UAF elements to have a common set of properties. |
| VersionedElement | VersionedElement | – | 🔒 ja | An abstract type grouping ResourcePerformer and ServiceSpecification that allows VersionOfConfiguration to be related to ActualProjectMilest … |
| VersionOfConfiguration | VersionOfConfiguration | Part | – | A property of a WholeLifeConfiguration, used in version control of a VersionedElement. |
| VersionReleased | VersionReleased | Dependency | – | A relationship that expresses that an actual project milestone releases an versioned element. |
| VersionSuccession | VersionSucession | Dependency | – | A tuple between two VersionOfConfigurations that denotes that one VersionOfConfiguration follows from another. |
| VersionWithdrawn | VersionWithdrawn | Dependency | – | A relationship that expresses that an actual project milestone withdraws an versioned element. |
| View | View | Class | – | An architecture view expresses the architecture of the system-of-interest in accordance with an architecture viewpoint (or simply, viewpoint … |
| Viewpoint | Viewpoint | Class | – | An architecture viewpoint frames (to formulate or construct in a particular style or language) one or more concerns. |
| ViewpointsInArchitecturalDescription | ViewpointsInArchitecturalDescription | Dependency | – | A relationship that expresses that an architectural description includes the following viewpoints. |
| ViewpointToStakeholder | ViewpointToStakeholder | Dependency | – | A relationship that expresses which stakeholder needs viewpoint. |
| ViewsInArchitecturalDescription | ViewsInArchitecturalDescription | Dependency | – | A relationship that expresses that an architectural description includes the following views. |
| VisionForActualEnterprisePhase | VisionForActualEnterprisePhase | Dependency | – | A relationship that expresses which actual enterprisephase implements an enterprisevision. |
| WholeLifeConfiguration | WholeLifeConfiguration | Class | – | A set of VersionedElements. |
| WholeLifeEnterprise | WholeLifeEnterprise | Class | – | A WholeLifeEnterprise is a purposeful endeavor of any size involving people, organizations and supporting systems. |

## 2. Abstrakte Stereotype (🔒) — nicht instanziierbar

Diese Typen dürfen weder als Element- noch als Kanten-Stereotyp verwendet werden. Für eine Regel mit abstraktem Endpunkt gelten alle aufgeführten konkreten Subtypen.

| Abstrakter Typ | Konkrete Subtypen |
|---|---|
| 🔒 Achiever | ActualEnterprisePhase, ActualOrganization, ActualPerson, ActualPost, ActualProject, ActualResource, FieldedCapability, Function, OperationalActivity, SecurityProcess, ServiceFunction, ServiceSpecification, StandardOperationalActivity |
| 🔒 ActualOrganizationalResource | ActualOrganization, ActualPerson, ActualPost, ActualProject |
| 🔒 ActualResponsibleResource | ActualOrganization, ActualPerson, ActualPost |
| 🔒 ActualState | ActualCondition, ActualEnduringTask, ActualEnterprisePhase, ActualEnvironment, ActualLocation, ActualMeasurement, ActualMeasurementSet, ActualOrganization, ActualPerson, ActualPost, ActualProject, ActualProjectMilestone, ActualProjectMilestoneRole, ActualPropertySet, ActualResource, ActualService, FieldedCapability, ProjectStatus, ProvidedServiceLevel, RequiredServiceLevel |
| 🔒 Architecture | CapabilityConfiguration, OperationalArchitecture, ResourceArchitecture, ResourceMitigation, SecurityEnclave, System |
| 🔒 Asset | CapabilityConfiguration, DataElement, Energy, InformationElement, KnownResource, NaturalResource, OperationalArchitecture, OperationalPerformer, Organization, Person, Post, Project, ResourceArchitecture, ResourceArtifact, ResourceMitigation, Responsibility, SecurityEnclave, Software, System, Technology |
| 🔒 AssetRole | DataRole, InformationRole, OperationalRole, PostRole, ProblemDomain, ProjectRole, ResourceRole, SubOrganization |
| 🔒 BusinessProcess | Function, OperationalActivity, SecurityProcess, ServiceFunction, StandardOperationalActivity |
| 🔒 BWRequirement | FunctionalRequirement, NonfunctionalRequirement |
| 🔒 CapableElement | ActualEnduringTask, ActualEnterprisePhase, ActualOrganization, ActualPerson, ActualPost, ActualProject, ActualResource, ActualService, CapabilityConfiguration, Energy, FieldedCapability, KnownResource, NaturalResource, OperationalArchitecture, OperationalPerformer, Organization, Person, Post, Project, ProvidedServiceLevel, RequiredServiceLevel, ResourceArchitecture, ResourceArtifact, ResourceMitigation, Responsibility, SecurityEnclave, ServiceSpecification, Software, System, Technology |
| 🔒 ConceptItem | CapabilityConfiguration, DataElement, Energy, InformationElement, KnownResource, Location, NaturalResource, OperationalArchitecture, OperationalPerformer, Organization, Person, Post, Project, ResourceArchitecture, ResourceArtifact, ResourceMitigation, Responsibility, SecurityEnclave, Software, System, Technology |
| 🔒 Desirer | Capability, CapabilityConfiguration, CapabilityRole, Energy, KnownResource, NaturalResource, OperationalArchitecture, OperationalPerformer, Organization, Person, Post, Project, ResourceArchitecture, ResourceArtifact, ResourceMitigation, Responsibility, SecurityEnclave, Software, System, Technology |
| 🔒 Exchange | Command, Control, OperationalExchange, ResourceExchange, ServiceExchange |
| 🔒 ExchangeItem | CapabilityConfiguration, DataElement, DataRole, Energy, GeoPoliticalExtentType, InformationElement, InformationRole, KnownResource, NaturalResource, OperationalSignal, Organization, Person, Post, Project, ResourceArchitecture, ResourceArtifact, ResourceMitigation, ResourceSignal, Responsibility, SecurityEnclave, Software, System, Technology |
| 🔒 FunctionEdge | FunctionControlFlow, FunctionObjectFlow |
| 🔒 InteractionMessage | OperationalMessage, ResourceMessage, ServiceMessage |
| 🔒 InteractionRole | OperationalRole, PostRole, ProblemDomain, ProjectRole, ResourceRole, ServiceSpecificationRole, SubOrganization |
| 🔒 LocationHolder | CapabilityConfiguration, DataElement, Energy, InformationElement, KnownResource, NaturalResource, OperationalArchitecture, OperationalPerformer, OperationalRole, Organization, Person, Post, PostRole, ProblemDomain, Project, ProjectRole, ResourceArchitecture, ResourceArtifact, ResourceMitigation, ResourceRole, Responsibility, SecurityEnclave, Software, SubOrganization, System, Technology |
| 🔒 MeasurableElement | AchievedEffect, ActivityPerformableUnderCondition, Alias, ArbitraryConnector, ArchitecturalDescription, ArchitecturalReference, ArchitecturalSequence, ArchitectureMetadata, Capability, CapabilityConfiguration, CapabilityDependency, CapabilityForTask, CapabilityGeneralization, CapabilityRole, CapabilityRoleDependency, Command, Competence, ConceptRole, Concern, Condition, Consumes, Control, DataElement, DataRole, Definition, DesiredEffect, EnduringTask, Energy, EnterpriseGoal, EnterprisePhase, EnterpriseVision, Environment, EnvironmentProperty, Exhibits, FillsPost, Forecast, Function, FunctionAction, FunctionControlFlow, FunctionObjectFlow, GeoPoliticalExtentType, HighLevelOperationalConcept, Implements, Information, InformationElement, InformationRole, IsCapableToPerform, KnownResource, Location, MapsToCapability, Measurement, Metadata, MilestoneDependency, NaturalResource, OperationalActivity, OperationalActivityAction, OperationalArchitecture, OperationalConnector, OperationalConstraint, OperationalControlFlow, OperationalExchange, OperationalInterface, OperationalMessage, OperationalMethod, OperationalObjectFlow, OperationalParameter, OperationalPerformer, OperationalPort, OperationalRole, OperationalSignal, OperationalSignalProperty, OperationalStateDescription, Organization, OwnsProcess, PerformsInContext, Person, Post, PostRole, ProblemDomain, ProcessGeneralization, Project, ProjectMilestone, ProjectMilestoneRole, ProjectRole, ProjectSequence, ProjectTheme, PropertySetGeneralization, Protocol, ProtocolLayer, Protocolstack, ProvidesCompetence, RequiresCompetence, ResourceArchitecture, ResourceArtifact, ResourceConnector, ResourceConstraint, ResourceExchange, ResourceInterface, ResourceMessage, ResourceMethod, ResourceMitigation, ResourceParameter, ResourcePort, ResourceRole, ResourceSignal, ResourceSignalProperty, ResourceStateDescription, Responsibility, SameAs, SecurityConstraint, SecurityEnclave, SecurityProcess, ServiceConnector, ServiceExchange, ServiceFunction, ServiceFunctionAction, ServiceGeneralization, ServiceInterface, ServiceMessage, ServiceMethod, ServiceParameter, ServicePolicy, ServicePort, ServiceProvision, ServiceSpecification, ServiceSpecificationRole, ServiceStateDescription, Software, Standard, StandardOperationalActivity, StrategicConstraint, SubOrganization, System, Technology, TemporalPart, VersionOfConfiguration, VersionSuccession, View, Viewpoint, WholeLifeConfiguration, WholeLifeEnterprise |
| 🔒 OperationalActivityEdge | OperationalControlFlow, OperationalObjectFlow |
| 🔒 OperationalAgent | KnownResource, OperationalArchitecture, OperationalPerformer |
| 🔒 OperationalAsset | InformationElement, KnownResource, OperationalArchitecture, OperationalPerformer |
| 🔒 OperationalExchangeItem | CapabilityConfiguration, Energy, GeoPoliticalExtentType, InformationElement, InformationRole, KnownResource, NaturalResource, OperationalSignal, Organization, Person, Post, Project, ResourceArchitecture, ResourceArtifact, ResourceMitigation, Responsibility, SecurityEnclave, Software, System, Technology |
| 🔒 OrganizationalResource | Organization, Person, Post, Project, Responsibility |
| 🔒 PhysicalResource | Energy, NaturalResource, Organization, Person, Post, Project, ResourceArtifact, Responsibility, Software, Technology |
| 🔒 ProcessEdge | FunctionControlFlow, FunctionObjectFlow, OperationalControlFlow, OperationalObjectFlow |
| 🔒 ProcessMessageFlow | OperationalMessageFlow |
| 🔒 ProcessOperation | OperationalMethod, ResourceMethod, ServiceMethod |
| 🔒 ProcessParameter | OperationalParameter, ResourceParameter, ServiceParameter |
| 🔒 ProcessUsage | FunctionAction, OperationalActivityAction, ServiceFunctionAction |
| 🔒 PropertySet | Capability, CapabilityConfiguration, CapabilityRole, Competence, Concern, Condition, DataElement, DataRole, EnduringTask, Energy, EnterpriseGoal, EnterprisePhase, EnterpriseVision, Environment, GeoPoliticalExtentType, HighLevelOperationalConcept, InformationElement, InformationRole, KnownResource, Location, NaturalResource, OperationalArchitecture, OperationalInterface, OperationalPerformer, OperationalSignal, Organization, Person, Post, Project, ProjectMilestone, Protocol, Protocolstack, ResourceArchitecture, ResourceArtifact, ResourceInterface, ResourceMitigation, ResourceSignal, Responsibility, SecurityEnclave, ServiceInterface, ServiceSpecification, Software, Standard, System, Technology, TemporalPart, View, Viewpoint, WholeLifeConfiguration, WholeLifeEnterprise |
| 🔒 ProtocolImplementation | ResourceConnector, ResourcePort |
| 🔒 Resource | CapabilityConfiguration, DataElement, DataRole, Energy, GeoPoliticalExtentType, InformationElement, InformationRole, KnownResource, NaturalResource, OperationalSignal, Organization, Person, Post, Project, ResourceArchitecture, ResourceArtifact, ResourceMitigation, ResourceSignal, Responsibility, SecurityEnclave, Software, System, Technology |
| 🔒 ResourceAsset | CapabilityConfiguration, DataElement, Energy, KnownResource, NaturalResource, Organization, Person, Post, Project, ResourceArchitecture, ResourceArtifact, ResourceMitigation, Responsibility, SecurityEnclave, Software, System, Technology |
| 🔒 ResourceExchangeItem | CapabilityConfiguration, DataElement, DataRole, Energy, GeoPoliticalExtentType, KnownResource, NaturalResource, Organization, Person, Post, Project, ResourceArchitecture, ResourceArtifact, ResourceMitigation, ResourceSignal, Responsibility, SecurityEnclave, Software, System, Technology |
| 🔒 ResourcePerformer | CapabilityConfiguration, Energy, KnownResource, NaturalResource, Organization, Person, Post, Project, ResourceArchitecture, ResourceArtifact, ResourceMitigation, Responsibility, SecurityEnclave, Software, System, Technology |
| 🔒 Rule | OperationalConstraint, ResourceConstraint, SecurityConstraint, ServicePolicy, StrategicConstraint |
| 🔒 Stakeholder | ActualOrganization, ActualPerson, ActualPost, ActualProject, Organization, Person, Post, Project, Responsibility |
| 🔒 SubjectOfForecast | CapabilityConfiguration, Competence, DataElement, Energy, InformationElement, KnownResource, NaturalResource, OperationalArchitecture, OperationalPerformer, Organization, Person, Post, Project, Protocol, Protocolstack, ResourceArchitecture, ResourceArtifact, ResourceMitigation, Responsibility, SecurityEnclave, Software, Standard, System, Technology |
| 🔒 SubjectOfOperationalConstraint | DataModel, DataRole, InformationElement, InformationRole, KnownResource, OperationalActivity, OperationalArchitecture, OperationalExchange, OperationalPerformer, OperationalRole, OperationalSignal, PostRole, ProblemDomain, ProjectRole, ResourceRole, SecurityProcess, StandardOperationalActivity, SubOrganization |
| 🔒 SubjectOfResourceConstraint | ActualOrganization, ActualPerson, ActualPost, ActualProject, ActualResource, CapabilityConfiguration, DataElement, DataModel, Energy, FieldedCapability, Function, KnownResource, NaturalResource, Organization, Person, Post, PostRole, Project, ProjectRole, ResourceArchitecture, ResourceArtifact, ResourceMitigation, ResourcePort, ResourceRole, Responsibility, SecurityEnclave, SecurityProcess, Software, SubOrganization, System, Technology |
| 🔒 SubjectOfSecurityConstraint | CapabilityConfiguration, Command, Control, DataElement, DataRole, Energy, InformationElement, InformationRole, KnownResource, NaturalResource, OperationalArchitecture, OperationalExchange, OperationalPerformer, OperationalRole, Organization, Person, Post, PostRole, ProblemDomain, Project, ProjectRole, ResourceArchitecture, ResourceArtifact, ResourceExchange, ResourceMitigation, ResourceRole, Responsibility, SecurityEnclave, SecurityProcess, ServiceExchange, Software, SubOrganization, System, Technology |
| 🔒 UAFElement | AchievedEffect, ActivityPerformableUnderCondition, ActualCondition, ActualEnduringTask, ActualEnterprisePhase, ActualEnvironment, ActualLocation, ActualMeasurement, ActualMeasurementSet, ActualOrganization, ActualOrganizationRole, ActualPerson, ActualPost, ActualProject, ActualProjectMilestone, ActualProjectMilestoneRole, ActualPropertySet, ActualResource, ActualResourceRelationship, ActualResourceRole, ActualService, Alias, ArbitraryConnector, ArchitecturalDescription, ArchitecturalReference, ArchitecturalSequence, ArchitectureMetadata, Capability, CapabilityConfiguration, CapabilityDependency, CapabilityForTask, CapabilityGeneralization, CapabilityRole, CapabilityRoleDependency, Command, Competence, ConceptRole, Concern, Condition, Consumes, Control, DataElement, DataModel, DataRole, Definition, DesiredEffect, EnduringTask, Energy, EnterpriseGoal, EnterprisePhase, EnterpriseVision, Environment, EnvironmentProperty, Exhibits, FieldedCapability, FillsPost, Forecast, Function, FunctionAction, FunctionControlFlow, FunctionObjectFlow, GeoPoliticalExtentType, HighLevelOperationalConcept, Implements, Information, InformationElement, InformationRole, IsCapableToPerform, KnownResource, Location, MapsToCapability, Measurement, Metadata, MilestoneDependency, NaturalResource, OperationalActivity, OperationalActivityAction, OperationalArchitecture, OperationalConnector, OperationalConstraint, OperationalControlFlow, OperationalExchange, OperationalInterface, OperationalMessage, OperationalMethod, OperationalObjectFlow, OperationalParameter, OperationalPerformer, OperationalPort, OperationalRole, OperationalSignal, OperationalSignalProperty, OperationalStateDescription, Organization, OwnsProcess, PerformsInContext, Person, Post, PostRole, ProblemDomain, ProcessGeneralization, Project, ProjectMilestone, ProjectMilestoneRole, ProjectRole, ProjectSequence, ProjectStatus, ProjectTheme, PropertySetGeneralization, Protocol, ProtocolLayer, Protocolstack, ProvidedServiceLevel, ProvidesCompetence, RequiredServiceLevel, RequiresCompetence, ResourceArchitecture, ResourceArtifact, ResourceConnector, ResourceConstraint, ResourceExchange, ResourceInterface, ResourceMessage, ResourceMethod, ResourceMitigation, ResourceParameter, ResourcePort, ResourceRole, ResourceSignal, ResourceSignalProperty, ResourceStateDescription, Responsibility, SameAs, SecurityConstraint, SecurityEnclave, SecurityProcess, ServiceConnector, ServiceExchange, ServiceFunction, ServiceFunctionAction, ServiceGeneralization, ServiceInterface, ServiceMessage, ServiceMethod, ServiceParameter, ServicePolicy, ServicePort, ServiceProvision, ServiceSpecification, ServiceSpecificationRole, ServiceStateDescription, Software, Standard, StandardOperationalActivity, StrategicConstraint, SubOrganization, System, Technology, TemporalPart, VersionOfConfiguration, VersionSuccession, View, Viewpoint, WholeLifeConfiguration, WholeLifeEnterprise |
| 🔒 VersionedElement | CapabilityConfiguration, Energy, KnownResource, NaturalResource, Organization, Person, Post, Project, ResourceArchitecture, ResourceArtifact, ResourceMitigation, Responsibility, SecurityEnclave, ServiceSpecification, Software, System, Technology |

## 3. Topologie-Regeln

203 Stereotype mit Beziehungsregeln, davon 133 vollständig (Quelle und Ziel). Nur vollständige Regeln sind maschinell prüfbar.

| Stereotype | Erlaubte Quellen (client/source/end[0]) | Erlaubte Ziele (supplier/target/end[1]) | Weitere Rollen |
|---|---|---|---|
| AchievedEffect | Achiever | ActualState | – |
| ActivityPerformableUnderCondition | BusinessProcess | ActualCondition | – |
| ActivitySupportsService | OperationalActivity | ServiceSpecification | – |
| ActsUpon | OperationalActivity, OperationalActivityAction | OperationalExchangeItem, PaperForm | – |
| ActualCondition | – | – | classifier → Condition |
| ActualConditionToActualResource | ActualResource | ActualCondition | – |
| ActualEnduringTask | – | – | classifier → EnduringTask |
| ActualEnterprisePhase | – | – | classifier → EnterprisePhase |
| ActualEnvironment | – | – | classifier → Environment |
| ActualLocation | – | – | classifier → Location |
| ActualMeasurement | – | – | definingFeature → Measurement, owningInstance → ActualPropertySet |
| ActualMeasurementSetAppliesFor | ActualMeasurementSet | MeasurableElement | – |
| ActualOrganization | – | – | classifier → Organization |
| ActualOrganizationRole | – | – | definingFeature → PostRole, definingFeature → SubOrganization, owningInstance → ActualOrganization |
| ActualPerson | – | – | classifier → Person |
| ActualPost | – | – | classifier → Post |
| ActualProject | – | – | classifier → Project, definingFeature → ProjectRole |
| ActualProjectConsults | ActualProject | Organization | – |
| ActualProjectDependency | ActualProject | ActualProject | – |
| ActualProjectInforms | ActualProject | Organization | – |
| ActualProjectMilestone | – | – | classifier → ProjectMilestone |
| ActualProjectMilestoneRole | – | – | definingFeature → ProjectMilestoneRole, owningInstance → ActualProject, value.instance → ActualProjectMilestone |
| ActualPropertySet | – | – | classifier → PropertySet |
| ActualResource | – | – | classifier → ResourcePerformer |
| ActualResourceNeededByActualProjectMilestone | ActualResource | ActualProjectMilestone | – |
| ActualResourceRelationship | ActualResource | ActualResource | realizes → ResourceExchange |
| ActualResourceRole | – | – | definingFeature → ResourceRole, owningInstance → ActualResource |
| ActualResourceToActualProjectMilestone | ActualResource | ActualProjectMilestone | – |
| ActualService | – | – | classifier → ServiceSpecification |
| ActualServiceSpecificationRole | – | – | definingFeature → ServiceSpecificationRole, owningInstance → ActualService |
| AffectedActivity | OperationalExchangeItem | OperationalActivity | – |
| AffectedFunctions | ResourceExchangeItem | Function | – |
| AffectedResource | OperationalActivity | OperationalExchangeItem | – |
| AlignsWithGoal | OperationalActivity, OperationalAgent, ResourcePerformer, ServiceSpecification | EnterpriseGoal | – |
| ArbitraryConnector | ConceptRole | ConceptRole | – |
| ArchitecturalReference | ArchitecturalDescription | ArchitecturalDescription | – |
| ArchitecturalSequence | ArchitecturalDescription | ArchitecturalDescription | – |
| ArchitectureForProject | ActualProject, ActualProjectMilestone | ArchitecturalDescription | – |
| ArchitectureMetadata | – | – | annotatedElement → ArchitecturalDescription |
| BoundaryCondition | ResourceConnector | Environment | – |
| CapabilityDependency | Capability | Capability | – |
| CapabilityForTask | Capability | ActualEnduringTask, EnduringTask | – |
| CapabilityGeneralization | Capability | Capability | – |
| CapabilityRole | – | – | class → Capability, type → Capability |
| CapabilityRoleDependency | CapabilityRole | CapabilityRole | – |
| Checks | FitCriterion | BWRequirement | – |
| Classified | ArchitecturalDescription, DataElement, DocumentReference, InformationElement, ServiceSpecification | Classification | – |
| Command | OrganizationalResource, ResourceRole | OrganizationalResource, ResourceRole | conveyed → DataElement |
| CompetenceForRole | ResourceRole | Competence | – |
| CompliesViewpoint | View | Viewpoint | – |
| ConceptRole | – | – | class → HighLevelOperationalConcept, type → ConceptItem |
| ConcernForActualEnterprisePhase | ActualEnterprisePhase | Concern | – |
| ConcernForView | View | Concern | – |
| ConcernForViewpoint | Viewpoint | Concern | – |
| ConflictsWith | BWRequirement | BWRequirement | – |
| ConformsTo | UAFElement | Standard | – |
| ConsumedBy | ServiceSpecification, ServiceSpecificationRole | OperationalPerformer, OperationalRole | – |
| Consumes | OperationalActivity, OperationalActivityAction | ActualService, ServiceSpecification | – |
| Control | PhysicalResource, ResourceRole | PhysicalResource, ResourceRole | conveyed → DataElement |
| DataElement | – | – | owner → DataModel |
| DataElementStoredIn | DataElement | ResourcePerformer, ResourceRole | – |
| DataRole | – | – | class → ResourceAsset, type → DataElement |
| DerivedFrom | BWRequirement | UAFElement | – |
| DescribedBy | Architecture | ArchitecturalDescription | – |
| DesiredEffect | Desirer | ActualState | – |
| EnvironmentalCondition | Exhibits | Environment | – |
| EnvironmentalContext | Measurement | ActualCondition | – |
| EnvironmentProperty | – | – | class → Environment, type → Condition |
| Evaluates | FulfilmentCriterion | FitCriterion | – |
| Exhibits | CapableElement | Capability | – |
| Expresses | Architecture | ArchitecturalDescription | – |
| FieldedCapability | – | – | classifier → CapabilityConfiguration |
| FillsPost | ActualPerson | ActualPost | – |
| Forecast | SubjectOfForecast | SubjectOfForecast | – |
| ForecastPeriod | Forecast | ActualEnterprisePhase | – |
| FormStoredIn | PaperForm | Software | – |
| FunctionAction | – | – | activity → Function, behavior → Function |
| FunctionControlFlow | ActivityInitial, DecisionNode, ForkNode, FunctionAction, JoinNode, MergeNode | ActivityFinal, DecisionNode, FlowFinal, ForkNode, FunctionAction, JoinNode, MergeNode | – |
| FunctionEdge | – | – | owner → Function |
| FunctionObjectFlow | ActivityInitial, DecisionNode, ForkNode, FunctionAction, JoinNode, MergeNode | ActivityFinal, DecisionNode, FlowFinal, ForkNode, FunctionAction, JoinNode, MergeNode | – |
| FunctionSubject | Function | ResourceExchangeItem | – |
| GoalForActualEnterprisePhase | ActualEnterprisePhase | EnterpriseGoal | – |
| HostedOn | ResourceArchitecture, ResourceArtifact, ResourceRole | ResourceArchitecture, ResourceArtifact, ResourceRole | – |
| Implements | DataElement, Function, InformationElement, OperationalActivity, OperationalActivityAction, OperationalConstraint, ResourceConnector, ResourceConstraint, ResourceExchange, ResourceInterface, ResourcePerformer, ResourceRole, ServicePolicy, StrategicConstraint | ActualEnduringTask, InformationElement, OperationalActivity, OperationalActivityAction, OperationalAgent, OperationalConnector, OperationalConstraint, OperationalExchange, OperationalInterface, OperationalRole, ResourceConnector, ResourceConstraint, ServiceFunction, ServiceInterface, ServicePolicy, StrategicConstraint | – |
| ImplementsProtocol | ProtocolImplementation | Protocol | – |
| Information | – | – | annotatedElement → UAFElement |
| InformationElement | – | – | owner → DataModel |
| InformationRole | – | – | class → OperationalAsset, type → InformationElement |
| IsAccountableFor | Organization | ActualProject, ResourcePerformer, ServiceSpecification | – |
| IsCapableToPerform | OperationalAgent, ResourcePerformer, ServiceSpecification | Function, FunctionAction, Lane, OperationalActivity, OperationalActivityAction, Pool, ServiceFunction, ServiceFunctionAction | – |
| IsDuplicateOf | BWRequirement | BWRequirement | – |
| IsEquivalentToStandardElement | UAFElement | UAFElement | – |
| IsResponsibleFor | Organization | ActualProject, ResourcePerformer, ServiceSpecification | – |
| JustifiedBy | OperationalConstraint, ResourceConstraint, ServicePolicy, StrategicConstraint | Reference | – |
| LocationType | LocationHolder | Location | – |
| MapsToCapability | BusinessProcess | Capability | – |
| Measurement | – | – | class → PropertySet, type → MeasurementType |
| Metadata | – | – | annotatedElement → UAFElement |
| MilestoneDependency | ActualProjectMilestone | ActualProjectMilestone | – |
| NeedsModificationOf | ActualProject | PhysicalResource, ResourceArchitecture, ResourceRole | – |
| NeedsResource | ActualProject | PhysicalResource, ResourceArchitecture, ResourceRole | – |
| NeedsService | ActualProject | ServiceSpecification, ServiceSpecificationRole | – |
| OperationalActivity | – | – | ownedParameter → OperationalParameter |
| OperationalActivityAction | – | – | activity → OperationalActivity, behavior → OperationalActivity |
| OperationalActivityEdge | – | – | owner → OperationalActivity |
| OperationalAgent | – | – | ownedOperation → OperationalMethod, ownedPort → OperationalPort |
| OperationalArchitectureOfEnterprisePhase | ActualEnterprisePhase | OperationalArchitecture | – |
| OperationalConnector | OperationalPort, OperationalRole | OperationalPort, OperationalRole | – |
| OperationalControlFlow | Gateway, IntermediateEvent, OperationalActivityAction, StartEvent | EndEvent, Gateway, IntermediateEvent, OperationalActivityAction | – |
| OperationalExchange | OperationalActivity, OperationalAgent, OperationalRole, ServiceSpecification | OperationalActivity, OperationalAgent, OperationalRole, ServiceSpecification | conveyed → OperationalExchangeItem, realizingActivityEdge → OperationalActivityEdge, realizingConnector → OperationalConnector, realizingMessage → OperationalMessage |
| OperationalMessage | – | – | receiveEvent.event.operation → OperationalMethod |
| OperationalMessageFlow | IntermediateEvent, Lane, OperationalActivityAction, Pool | IntermediateEvent, Lane, OperationalActivityAction, Pool | – |
| OperationalMethod | – | – | method → OperationalActivity, ownedOperation → OperationalInterface, ownedParameter → OperationalParameter |
| OperationalObjectFlow | Gateway, IntermediateEvent, OperationalActivityAction, StartEvent | EndEvent, Gateway, IntermediateEvent, OperationalActivityAction | – |
| OperationalParameter | – | – | type → OperationalExchangeItem |
| OperationalPort | – | – | class → OperationalAgent, type → OperationalInterface |
| OperationalRole | – | – | class → OperationalAgent, class → OperationalArchitecture, class → OperationalPerformer, type → KnownResource, type → OperationalAgent, type → OperationalArchitecture, type → OperationalPerformer |
| OperationalSignalProperty | – | – | class → OperationalSignal, type → OperationalExchangeItem |
| OperationalStateDescription | – | – | owner → OperationalAgent |
| OriginatesFrom | UAFElement | Reference | – |
| OwnedMilestone | ActualProject | ActualProjectMilestone | – |
| OwnsActualMeasurementSet | MeasurableElement | ActualMeasurementSet | – |
| OwnsMeasurement | MeasurableElement | Measurement, MeasurementType | – |
| OwnsProcess | ActualOrganizationalResource | OperationalActivity | – |
| PartOfCatalogue | RequirementCategory | RequirementCatalogue | – |
| PartOfCategory | BWRequirement, RequirementCategory | RequirementCategory | – |
| PerformsInContext | OperationalRole, ResourceRole, ServiceSpecificationRole | Function, FunctionAction, Lane, OperationalActivity, OperationalActivityAction, Pool, ServiceFunction, ServiceFunctionAction | – |
| PhysicalArchitectureOfEnterprisePhase | ActualEnterprisePhase | ResourceArchitecture | – |
| PhysicalLocation | LocationHolder | ActualLocation | – |
| PostRole | – | – | class → Organization, class → Post, type → Post |
| ProblemDomain | – | – | class → OperationalArchitecture, type → OperationalPerformer |
| ProcessGeneralization | BusinessProcess | BusinessProcess | – |
| ProjectMilestoneRole | – | – | class → Project, type → ProjectMilestone |
| ProjectMilestoneToProjectTheme | ProjectMilestone | ProjectTheme | – |
| ProjectProvidesFunction | ActualProject | Function | – |
| ProjectRole | – | – | class → Project, type → Project |
| ProjectSequence | ActualProject | ActualProject | – |
| ProjectStatus | – | – | definingFeature → ProjectTheme |
| ProjectSupportActivity | ActualProject | OperationalActivity | – |
| PropertySetGeneralization | CapabilityConfiguration, PropertySet, System | CapabilityConfiguration, PropertySet, System | – |
| ProtocolLayer | – | – | class → Protocolstack, type → Protocol |
| Provides | OperationalPerformer, OperationalRole | ServiceSpecification, ServiceSpecificationRole | – |
| ProvidesCompetence | ActualOrganizationalResource | Competence | – |
| ProvidesServiceFunction | ServiceInterface | ServiceFunction | – |
| RatifiedStandards | ActualOrganization | Standard | – |
| RealiseRequirement | DataElement, Function, Measurement, MeasurementType, Protocol, Protocolstack, ResourcePerformer, ResourcePort, ResourceRole, ServiceFunction, ServiceInterface, ServiceSpecification, ServiceSpecificationRole, Standard | BWRequirement | – |
| RealizedDesiredEffect | AchievedEffect | DesiredEffect | – |
| RealizesRecommendation | UAFElement | Recommendation | – |
| RealizingAchievedEffect | DesiredEffect | AchievedEffect | – |
| RefersTo | Recommendation | Finding | – |
| Refines | BWRequirement | BWRequirement | – |
| Replaces | BWRequirement | BWRequirement | – |
| ReplaceStandardElement | Reference, UAFElement | Reference, UAFElement | – |
| RequiredEnvironment | LocationHolder | ActualEnvironment | – |
| RequiredResource | ProjectMilestone | ResourcePerformer | – |
| Requires | BWRequirement | BWRequirement | – |
| RequiresCompetence | OrganizationalResource | Competence | – |
| ResourceConnector | ResourcePort, ResourceRole | ResourcePort, ResourceRole | – |
| ResourceDependency | ResourcePerformer, ResourcePort, ResourceRole | ResourcePerformer, ResourcePort, ResourceRole | – |
| ResourceExchange | ResourcePerformer, ResourceRole, ServiceSpecificationRole | ResourcePerformer, ResourceRole, ServiceSpecificationRole | conveyed → ResourceExchangeItem, realizingActivityEdge → FunctionEdge, realizingConnector → ResourceConnector, realizingMessage → ResourceMessage |
| ResourceMessage | – | – | Connector → ResourceConnector, receiveEvent.event.operation → ResourceMethod |
| ResourceMethod | – | – | method → Function, ownedOperation → ResourceInterface, ownedOperation → ResourcePerformer, ownedParameter → ResourceParameter |
| ResourceParameter | – | – | ownedParameter → Function, type → ResourceExchangeItem |
| ResourcePerformer | – | – | ownedPort → ResourcePort |
| ResourcePort | – | – | class → ResourcePerformer, type → ResourceInterface |
| ResourceRole | – | – | class → ResourcePerformer, type → ResourcePerformer |
| ResourceSignalProperty | – | – | class → ResourceSignal, type → ResourceExchangeItem |
| ResourceStateDescription | – | – | owner → ResourcePerformer |
| ResourceToServiceDependency | ResourcePerformer, ResourceRole | ServiceSpecification, ServiceSpecificationRole | – |
| Responsible | ActualProject | PhysicalResource, ResourceArchitecture, ResourceRole, ServiceSpecification | – |
| ResultsFrom | Finding | Classification, EndEvent, FitCriterion, FulfilmentCriterion, FunctionalRequirement, Gateway, IntermediateEvent, Lane, Measurement, MeasurementType, NonfunctionalRequirement, Pool, Reference, RequirementCatalogue, RequirementCategory, StartEvent, UAFElement | – |
| SameAs | Software, UAFElement | Software, UAFElement | – |
| Satisfy | Capability, OperationalActivityAction, ServiceSpecification, SubjectOfOperationalConstraint, SubjectOfResourceConstraint | OperationalConstraint, ResourceConstraint, ServicePolicy, StrategicConstraint | – |
| SecurityConstraint | – | – | constrainedElement → SubjectOfSecurityConstraint |
| ServiceConnector | ServicePort, ServiceSpecificationRole | ServicePort, ServiceSpecificationRole | – |
| ServiceDependency | ServiceSpecification | OperationalAgent, ResourcePerformer, ServiceSpecification | – |
| ServiceExchange | ServiceSpecification | ServiceSpecification | realizingConnector → ServiceConnector, realizingMessage → ServiceMessage |
| ServiceFunction | – | – | ownedParameter → ServiceParameter |
| ServiceFunctionAction | – | – | activity → ServiceFunction, behavior → ServiceFunction |
| ServiceGeneralization | ServiceSpecification | ServiceSpecification | – |
| ServiceInterface | – | – | ownedOperation → ServiceMethod |
| ServiceMethod | – | – | method → ServiceFunction, ownedParameter → ServiceParameter, receiveEvent.event.operation → ServiceMessage |
| ServiceParameter | – | – | type → OperationalExchangeItem |
| ServicePort | – | – | class → ServiceSpecification, type → ServiceInterface |
| ServiceProvision | ActualResource, ResourcePerformer, ResourceRole | ActualService, ServiceSpecification, ServiceSpecificationRole | – |
| ServiceSpecification | – | – | ownedOperation → ServiceMethod, ownedPort → ServicePort |
| ServiceSpecificationRole | – | – | class → ServiceSpecification, type → ServiceSpecification |
| ServiceStateDescription | – | – | owner → ServiceSpecification |
| StakeholderConcern | Stakeholder | Concern | – |
| StatementTask | ActualEnterprisePhase | ActualEnduringTask | – |
| StemsFrom | BWRequirement | BWRequirement | – |
| SubOrganization | – | – | class → Organization, type → Organization |
| SuccessorOf | ResourcePerformer, ServiceSpecification, Standard | ResourcePerformer, ServiceSpecification, Standard | – |
| TemporalPart | – | – | class → EnterprisePhase, type → EnterprisePhase |
| ToBeRealizedBy | BWRequirement | DataElement, Function, Measurement, MeasurementType, Protocol, Protocolstack, ResourcePerformer, ResourcePort, ResourceRole, ServiceFunction, ServiceInterface, ServiceSpecification, ServiceSpecificationRole, Standard | – |
| VersionOfConfiguration | – | – | class → WholeLifeConfiguration, type → VersionedElement |
| VersionReleased | ActualProjectMilestone | VersionedElement | – |
| VersionSuccession | VersionOfConfiguration | VersionOfConfiguration | – |
| VersionWithdrawn | ActualProjectMilestone | VersionedElement | – |
| ViewpointsInArchitecturalDescription | ArchitecturalDescription | Viewpoint | – |
| ViewpointToStakeholder | Viewpoint | Stakeholder | – |
| ViewsInArchitecturalDescription | ArchitecturalDescription | View | – |
| VisionForActualEnterprisePhase | ActualEnterprisePhase | EnterpriseVision | – |

## 4. Viewpoints

52 NAFv4-Viewpoints (DiagramProfile).

### A1 - Meta-Data Definitions
Architectures, particularly large ones, usually require meta-data tags to aid with searching and discovery.

### A2 - Architecture Products
The A2 Viewpoint specifies the structure of an architecture, and the products that describe the architecture. Each product may correspond to an architecture view. This viewpoint also traces the architectures onto the Ent

### A3 - Architecture Correspondence
ISO/IEC/IEEE42010 introduces the idea of architecture correspondence and correspondence rules. Quoting from ISO/IEC/IEEE 42010; “A correspondence defines a relation between AD (Architecture Description) elements. Corresp

### A4 - Methodology Used
The A4 Viewpoint specifies the methodology used for the architecting activities. This methodology is described in NAFv4 Chapter 2. The content of the A4 viewpoint can also be modeled in the A1 viewpoint.

### A5 - Architecture Status
Since NAFv3.0, it has been possible to assign version numbers to views and specify their approval dates. In NAFv4.0, this is integrated with the meta-model’s generic project and milestone approach so that architecture re

### A6 - Architecture Version
Where the A5 Viewpoint shows the current version number and approval status for the architecture, the A6 Viewpoint shows the complete history of the architecture.

### A7 - Architecture Compliance
The A7 Viewpoint gives the overall specification of architecture meta-data.

### A8 - Standards
The A8 Viewpoint encompasses both technical and non-technical standards. The standards specified in the A8 view can be applied across the architecture to a variety of structural and behavioural elements. Standards are es

### Ar - Architecture Roadmap
The Ar Viewpoint shows the history of the architecture project as well as its future direction.

### C1 - Capability Taxonomy
The C1 Viewpoint specifies all the capabilities that are referenced throughout one or more architectures – i.e. one C1 may provide the definitive list of capabilities for a number of logical and resource architectures. T

### C2 - Enterprise Vision
The purpose of the C2 Viewpoint is to provide a strategic context for the capabilities described in the architecture and to specify the scope for the architecture. The C2 Viewpoint is high-level and describes the vision,

### C3 - Capability Dependencies
The C3 Viewpoint is intended to provide a means of analysing the dependencies between capabilities and between capability clusters. The composition of capabilities (into clusters) is logical and the purpose of the cluste

### C4 - Standard Processes
The C4 Viewpoint specifies Standard Operational Activities that can be re-used across multiple logical architectures (e.g. in L4, Logical Activities).

### C5 - Effects
The purpose of the C5 Viewpoint is to describe the operational effect of the capabilities, activities and services according to the expected goals. The C5 Viewpoint is high-level description that should be easily underst

### C7 - Performance Parameters
In the C7 Viewpoint the capability requirements (and existing capabilities) can be expressed in terms of Measures of Effectiveness (MoEs). These are high-level metrics used to judge the level of capability.

### C8 - Planning Assumptions
The C8 Viewpoint is concerned with identification and description of assumptions that have been made for the implementation of capabilities. Assumptions can be expressed by means of requirements.

### Cr - Capability Roadmap
The Cr Viewpont supports the Capability Audit process by providing a method to identify gaps or duplications in capability provision. Cr indicates capability increments, which are derived from delivery milestones within 

### L1 - Node Types
The L1 Viewpoint defines all of the Nodes that will appear in a Logical Architecture. Nodes are elements of capability assembled and orchestrated in the Logical Architecture (see L2 - Logical Scenario and L4 - Logical Ac

### L2 - Logical Scenario
The L2 Viewpoint specifies Nodes (elements of capability) in context of each other. The context is usually expressed in terms of the information that flows between the nodes (e.g. the information flow requirements betwee

### L3 - Node Interactions
L3 is used to provide further detail of the interoperability requirements associated with the operational capability of interest. The focus is on logical flows that cross the capability boundary. Although the primary pur

### L4 - Logical Activities
The L4 Viewpoint describes the operational activities that are being conducted within the mission or scenario. These activities are defined at a logical, solution-neutral level so as to enable different solutions in the 

### L5 - Logical States
The L5 Viewpoint specifies the typical states a node may have and the possible transitions between those states (i.e. changes of state). Triggers for state changes may also be defined. Actions may be associated with a gi

### L6 - Logical Sequence
Operational Event-Trace Descriptions, sometimes called sequence diagrams, event scenarios or timing diagrams, allow the tracing of interactions between nodes in a scenario or critical sequence of events. The node interac

### L7 - Information Model
The L7 Viewpoint is used to document the business information. It describes the information that can be exchanged along the logical flows in the architecture, specified in L3 Node Interactions.

### L8 - Logical Constraints
The L8 Viewpoint is used to constrain the logical architecture without forcing a particular solution. L8 is used for rules which are not expressed as behavioural models, interactions or measures of effectiveness, i.e. th

### Lr - Lines of Development
The Lr Viewpoint is primarily intended to support the acquisition process across multiple projects or programmes, highlighting dependencies the logical dependencies between capabilities, projects and the integration of a

### L2-L3 - Logical Concept
The L2-L3 Viewpoint is concerned with providing an executive level, scenario-based communication of the architecture purpose, scope and content.

### P1 - Resource Types
The P1 Viewpoint collects together all the Resource Types in the architecture together with a depiction of their performance characteristics. P1 also provides a summary of the technologies and competencies that impact on

### P2 - Resource Structure
The P2 Viewpoint links together the operational and physical architecture viewpoints by depicting how types of Resource are structured and interact to realize the logical architecture specified in L2, Logical Scenario. T

### P3 - Resource Connectivity
The networks and pathways documented in a P3 Viewpoint represent the physical implementation of the logical flows identified in a L2, Logical Scenario, or L3, Node Interactions View.

### P4 - Resource Functions
The Functionality Description provides detailed information regarding the allocation of functions to resources, and flows between Resource Functions. The P4 Viewpoint is the Physical Resource counterpart to the L4 Logica

### P5 - Resource States
The P5 Viewpoint identifies the states a Resource can be, the allowable changes between those states, and the stimuli (e.g. triggers and events) that cause the state changes.

### P6 - Resource Sequence
The P6 Viewpoint is valuable for moving to the next level of detail from the initial solution design, to help define a sequence of functions and Resource Interactions, and to ensure that each participating Resource or Po

### P7 - Data Model
The P7 Viewpoint is one of the architectural products closest to actual system design in the NAF. It is used to describe how the information represented in the L7 Logical Data Model Viewpoint is implemented.

### P8 - Resource Constraints
The P8 Viewpoint describes constraints on the Resources, Resource Functions, data and communications that make up a Physical Architecture.

### Pr - Configuration Management
The Pr Viewpoint provides an overview of how Resource Assets change over time (note that NAF v3.1 only allowed for Capability Configurations whereas now this is opened up to all Resource Types). It shows the structure of

### L4-P4 - Activity To Function Mapping
The L4-P4 Viewpoint depicts the mapping of Resource Functions (and optionally, the resources that provide them) to operational activities and/or service functions. For operational activities it thus identifies the transf

### R2 - Requirement Catalogue
The R2 represents a catalog of requirements in the architectural model. For this purpose, categories can be created in which the functional and non-functional requirements can be grouped.

### R3 - Requirement Dependencies
The R3 is used to show dependencies between different requirements.

### R7 - Requirement Derivation
The R7 assigns functional and non-functional requirements to the demanding architectural elements. In addition, information about the planned realization can be shown.

### R8 - Requirement Fulfilment
The R8 is used to determine and map acceptance and evaluation criteria for the individual functional and non-functional requirements.

### Rr - Requirement Realization
In the Rr, requirements are assigned to the realizing architectural elements.

### S1 - Service Taxonomy
The purpose of the S1 Viewpoint is to provide a governance structure for a Service-Oriented Architecture. Along with S3, Service Interfaces, it specifies a standard library of service specifications for an enterprise, to

### S2 - Service Structure
The S2 Viewpoint is concerned with identification and description of how services are structured to create a higher-aggregated service. To provide highlevel views, dependencies to other services, nodes and resources as w

### S3 - Service Interfaces
The S3 Viewpoint is concerned with the identification and definition of service interfaces.

### S4 - Service Functions
The S4 Viewpoint is the key behavioural specification for services. Equivalent in nature to L4, Logical Activities and P4, Resources Functions, it specifies a set of functions that a service implementation is expected to

### S5 - Service States
The S5 Viewpoint is a specification of the allowable states of a service, and the possible transitions between them. This specification constrains how implementations of the service will behave. It is, though, generally 

### S6 - Service Interactions
Service Interaction Descriptions, sometimes called sequence diagrams, event scenarios or timing diagrams, allow the tracing of interactions between services in a composition or critical sequence of events.

### S7 - Service Interface Parameters
Specifies the interfaces that a service provides and uses, defines which services are compatible with which other services.

### S8 - Service Policy
The S8 Viewpoint specifies constraints against services to which implementations must conform.

### Sr - Service Roadmap
The Sr Viewpoint supports the Service Audit process by providing a method to identify gaps or duplications in service provision. Sr indicates service lifetime evolutions, which are derived from delivery milestones within

### C1-S1 - Capability to Service Mapping
A C1-S1 Viewpoint presents a simple mapping of services to capabilities, showing which services contribute to which capability.

## 5. Tagged-Value-Definitionen

27 Property-Typen.

| Property | Datensatz | Beschreibung | Einschränkungen (aus MDG) |
|---|---|---|---|
| approvalDate | Property Types | approvalDate | Type=Date; |
| concern | Property Types | Type=RefGUID; | Type=RefGUID; Values=Class; Stereotypes=Concern; |
| Constraints | Property Types |  | Type=Date; |
| Date | Property Types | Date | Type=Date; |
| dateCompleted | Property Types | dateCompleted | Type=Date; |
| endDate | Property Types | endDate | Type=Date; |
| forecastedUsage | Property Types |  | Type=RefGUID; Values=Class; |
| forecastPeriod | Property Types |  | Type=RefGUID; Values=Object; Stereotypes=ActualEnterprisePhase; |
| forecastSubject | Property Types |  | Type=RefGUID; Values=Class; |
| goal | Property Types | goal | Type=RefGUID; Values=Class; Stereotypes=EnterpriseGoal; |
| implements | Property Types |  | Type=RefGUID; Values=Class; Stereotypes=Protocol; |
| mandatedDate | Property Types | mandatedDate | Type=Date; |
| NAFv4DeuExtension | Property Types |  | Type=Boolean; Default=True; |
| NAFv4Extension | Property Types |  | Type=Boolean; Default=True; |
| nameRequired | Property Types |  | Type=Boolean; Default=false; |
| ownedInformationElement | Property Types |  | Type=RefGUIDList; Values=Class; Stereotypes=InformationElement, DataElement; |
| physicalLocation | Property Types |  | Type=RefGUID; Values=ActualLocation; Stereotypes=ActualLocation; |
| ratifiedBy | Property Types |  | Type=RefGUID; Values=Object; Stereotypes=ActualOrganization; |
| requiredEnvironment | Property Types |  | Type=RefGUID; Values=Object; Stereotypes=ActualEnvironment; |
| retiredDate | Property Types | retiredDate | Type=Date; |
| stakeholder | Property Types |  | Type=RefGUID; Values=Class; Stereotypes=ActualOrganization; |
| startDate | Property Types | startDate | Type=Date; |
| versionReleasedAtMilestone | Property Types |  | Type=RefGUID; Values=Object; Stereotypes=ActualProjectMilestone; |
| versionWithdrawnAtMilestone | Property Types |  | Type=RefGUID; Values= Object; Stereotypes=ActualProjectMilestone; |
| view | Property Types |  | Type=RefGUID; Values=Class; Stereotypes=View_; |
| viewpoint | Property Types |  | Type=RefGUID; Values=Class; Stereotypes=viewpoint; |
| vision | Property Types | vision | Type=RefGUID; Values=Class; Stereotypes=EnterpriseVision; |

## 6. Stereotyp-Tags

225 Tags an 66 Stereotypen.

| Stereotype | Tag | Typ | Erlaubte Werte | Default |
|---|---|---|---|---|
| ActualEnterprisePhase | endDate | endDate | – | – |
| ActualEnterprisePhase | startDate | startDate | – | – |
| ActualEnvironment | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| ActualLocation | address | char | – | – |
| ActualLocation | customKind | char | – | – |
| ActualLocation | locationNamedByAddress | boolean | true,false | – |
| ActualLocation | locationKind | enumeration | Surface,Point,GeoStationaryPoint,SolidVolume,Line,PlanarSurface,PolygonArea,RectangularArea,ElipticalArea,CircularArea,Other | – |
| ActualLocation | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| ActualMeasurement | intention | enumeration | Actual,Required,Estimate | – |
| ActualOrganization | shortName | String | – | – |
| ActualOrganization | serviceType | String | – | – |
| ActualProject | endDate | endDate | – | – |
| ActualProject | startDate | startDate | – | – |
| ActualProject | projectKind | enumeration | Programme,Portfolio,PersonnelDevelopment | – |
| ActualProject | project-ID |  | – | – |
| ActualProject | projectShortTitle |  | – | – |
| ActualProjectMilestone | endDate | endDate | – | – |
| ActualProjectMilestone | startDate | startDate | – | – |
| ActualProjectMilestone | kind | enumeration | InService,Deployed,NoLongerUsed,OutOfService,Other | – |
| ActualProjectMilestone | projectStatus | StatusIndicators | – | – |
| ActualState | endDate | endDate | – | – |
| ActualState | startDate | startDate | – | – |
| ArchitecturalDescription | status | String | – | – |
| ArchitecturalDescription | version | String | – | – |
| ArchitecturalDescription | methodologyUsed | String | – | – |
| ArchitecturalDescription | approvalAuthority | String | – | – |
| ArchitecturalDescription | architect | String | – | – |
| ArchitecturalDescription | assumptionAndConstraint | String | – | – |
| ArchitecturalDescription | creatingOrganization | String | – | – |
| ArchitecturalDescription | dateCompleted | dateCompleted | – | – |
| ArchitecturalDescription | purpose | String | – | – |
| ArchitecturalDescription | recommendations | String | – | – |
| ArchitecturalDescription | summaryOfFindings | String | – | – |
| ArchitecturalDescription | toolsUsed | String | – | – |
| ArchitecturalDescription | toBe | boolean | true,false | – |
| ArchitecturalDescription | approvalDate | approvalDate | – | – |
| ArchitecturalDescription | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| Architecture | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| Asset | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| BusinessProcess | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| BWRequirement | Uuid | String | – | – |
| BWRequirement | Afo_ID | String | – | – |
| BWRequirement | AG_ID | String | – | – |
| BWRequirement | Akteur | String | – | – |
| BWRequirement | Anforderungsart | String | – | – |
| BWRequirement | Ansprechpartner | String | – | – |
| BWRequirement | Detailstufe | int | – | – |
| BWRequirement | Freitext | String | – | – |
| BWRequirement | Gewicht (absolut) | float | – | – |
| BWRequirement | Kategorie | String | – | – |
| BWRequirement | Kritikalität | String | – | – |
| BWRequirement | Markierung | boolean | true,false | – |
| BWRequirement | Objectid | Sting | – | – |
| BWRequirement | Object und Ergänzungen | String | – | – |
| BWRequirement | Operative Bewertung | String | – | – |
| BWRequirement | Phasen | String | – | – |
| BWRequirement | Position | int | – | – |
| BWRequirement | Projektrolle | String | – | – |
| BWRequirement | Prozesswort | String | – | – |
| BWRequirement | QS_Status | String | – | – |
| BWRequirement | Rang | int | – | – |
| BWRequirement | Singular | boolean | true,false | – |
| BWRequirement | Status | String | – | – |
| BWRequirement | Subjekt | String | – | – |
| BWRequirement | Text | String | – | – |
| BWRequirement | Titelsperre | boolean | true,false | – |
| BWRequirement | Bezug | String | – | – |
| BWRequirement | Verbindlichkeit | String | – | – |
| BWRequirement | Hinweis | String | – | – |
| BWRequirement | Zu | boolean | true,false | – |
| BWRequirement | Priorität Vergabe | String | – | – |
| BWRequirement | Regelungen | String | – | – |
| BWRequirement | Vererbung | String | – | – |
| BWRequirement | Nachweisart | String | – | – |
| BWRequirement | Bemerkung | String | – | – |
| BWRequirement | Anforderung manuell | boolean | true,false | – |
| BWRequirement | Aktivität | String | – | – |
| BWRequirement | Qualität | String | – | – |
| BWRequirement | Randbedingung | String | – | – |
| Capability | Status | enumeration | Schwarz,Rot,Orange,Gelb,Grün,not set | – |
| Capability | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| CapabilityConfiguration | Avoiding redundancy in IT-SysBw | enumeration | gegeben,nicht gegeben (bewusst),nicht gegeben (Harmonisierung geplant),keine Relevanz,not set | – |
| CapabilityConfiguration | Avoids provider monopoly | enumeration | Ja,Nein,keine Relevanz,not set | – |
| CapabilityConfiguration | Client separation | enumeration | Rechte- und Rollenmanagement,dedizierte virtuelle Server,dedizierte Plattenpartitionen,dedizierte virtuelle LANs,unterschiedliche Verschlüsselung in den Datenbereichen,physische Trennung,keine,keine Relevanz,not set | – |
| CapabilityConfiguration | Environmentally friendly and sustainable | enumeration | Ja,Nein,keine Relevanz,not set | – |
| CapabilityConfiguration | Fulfilled C5 requirements catalogue of the BSI | enumeration | Ja,Nein,keine Relevanz,not set | – |
| CapabilityConfiguration | Geodata and geoservices | enumeration | Standard-konform,nicht Standard-konform,keine Relevanz,not set | – |
| CapabilityConfiguration | IT-Planning board involved | enumeration | Ja (Einbindung erfolgt),Nein (Einbindung nicht erfolgt),nicht erforderlich,keine Relevanz,not set | – |
| CapabilityConfiguration | NdB usage | enumeration | Ja (entsprechend vorgesehener Art und Weise),Ja (mit Abweichungen),Nein,keine Relevanz,not set | – |
| CapabilityConfiguration | RDF usage | enumeration | Ja,Nein,keine Relevanz,not set | – |
| CapabilityConfiguration | Reference architectures | enumeration | berücksichtigt,nicht berücksichtigt,teilweise berücksichtigt,keine verfügbar,keine Relevanz,not set | – |
| CapabilityConfiguration | Reusability of existing solutions | enumeration | Ja,teilweise Wiederverwendung,keine Wiederverwendung,keine Lösungen vorhanden,keine Relevanz,not set | – |
| CapabilityConfiguration | Security-by-Default | enumeration | Ja,Nein,keine Relevanz,not set | – |
| CapabilityConfiguration | String.Latin character set | enumeration | Ja,Nein,keine Relevanz,not set | – |
| CapabilityConfiguration | Usability and accessibility | enumeration | Ja,Nein,nur benutzerfreundlich,nur barrierefrei,keine Relevanz,not set | – |
| CapabilityConfiguration | UTF-8 character set | enumeration | Ja,Nein,keine Relevanz,not set | – |
| CapabilityConfiguration | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| CapabilityRole | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| Classification | Definition | String | – | – |
| Classification | Responsibility | STANAG 1059 NATO-Country Codes | – | – |
| Competence | ATB | String | – | – |
| Competence | ATN | String | – | – |
| Competence | AVR | String | – | – |
| DataElement | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| DataModel | kind | enumeration | Conceptual,Logical,Physical | – |
| DataModel | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| EnterpriseGoal | benefits | String | – | – |
| EnterpriseGoal | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| EnterprisePhase | toBe | enumeration | true,false,unknown,not set | – |
| EnterprisePhase | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| EnterpriseVision | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| Environment | kind | enumeration | TerrainType,WeatherConditions,LightConditions,CBRNEnvironment,SituationType | – |
| Environment | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| EnvironmentProperty | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| ExchangeItem | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| FieldedCapability | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| Finding | Type | enumeration | Method,Tool,Others,Subject | – |
| FitCriterion | text | String | – | – |
| FulfilmentCriterion | text | String | – | – |
| Function | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| GeoPoliticalExtentType | kind | enumeration | GeoFeatureType,RegionOfCountryType,CountryType,RegionOfWorldType,FacilityType,SiteType,InstallationType | – |
| GeoPoliticalExtentType | customKind | String | – | – |
| Information | informationKind | enumeration | Information,Domaininformation,PositionReferenceFrame,PredigreeInformation,Data | – |
| InformationElement | Event | String | – | – |
| InformationElement | Eventtriggered | enumeration | true,false,unknown,not set | – |
| InformationElement | AmountOfInformation | String | – | – |
| InformationElement | ConfirmationRequired | enumeration | true,false,unknown,not set | – |
| InformationElement | DeviceControl | enumeration | true,false,unknown,not set | – |
| InformationElement | Frequency | String | – | – |
| InformationElement | InformationMedium | enumeration | voice,data,both,unknown | – |
| InformationElement | IntegrityTestRequired | enumeration | true,false,unknown,not set | – |
| InformationElement | MachineReadable | enumeration | true,false,unknown,not set | – |
| InformationElement | MaxOpInterruptTime | String | – | – |
| InformationElement | MaxTransDelayTime | String | – | – |
| InformationElement | Periodic | enumeration | unknown,automated,none-automated,both | – |
| InformationElement | ReceiverAuthRequired | enumeration | true,false,unknown,not set | – |
| InformationElement | Simultaneously | enumeration | true,false,unknown,not set | – |
| InformationElement | TransmitterAuthRequired | enumeration | true,false,unknown,not set | – |
| InformationElement | UserAuthRequired | enumeration | true,false,unknown,not set | – |
| InformationElement | UserConfirmationRequired | enumeration | true,false,unknown,not set | – |
| Location | customKind | String | – | – |
| Location | kind | enumeration | CircularAreaType,ElipticalAreaType,GeoStationaryPointType,LineType,OtherType,PlanarSurfaceType,PointType,PolygonAreaType,RectangularAreaType,SolidVolumeType,SurfaceType | – |
| Measurement | ITSD_ServiceClass | enumeration | not set,Serviceklasse 1,Serviceklasse 2,Serviceklasse 3 | not set |
| MeasurementType | ITSD_Group | enumeration | Bezugszeitraum,Individuelle Serviceeigenschaft,Kontinuität,Kapazität,Serviceabruftermintrue,Servicekalender,Serviceleistungsfähigkeit,Servicesicherheit,Serviceverfügbarkeit,Servicewiederherstellbarkeit,Servicezuverlässigkeit,Sicherheit,Verfügbarkeit | Individuelle Serviceeigenschaft |
| Metadata | dublinCoreElement | String | – | – |
| Metadata | metaDataScheme | String | – | – |
| Metadata | name | String | – | – |
| Metadata | category | String | – | – |
| OperationalActivity | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| OperationalAsset | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| OperationalConstraint | Id | String | – | – |
| OperationalConstraint | Uuid | String | – | – |
| OperationalConstraint | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| OperationalExchange | exchangeKind | enumeration | MaterielExchange,OrganizationalExchange,EnergyExchange,InformationExchange,ConfigurationExchange,GeoPoliticalExtentExchange | – |
| OperationalPerformer | Nationality | enumeration | UN,NATO-PfP,NATO,DEU,MN,EU,TCN,NLD,National,Unknown,not set | – |
| OperationalPerformer | SizeIndicator | enumeration | Theatre,Armygroup,Army,Corps,Command,Division,Brigade,Regiment,Battalion,Company,Echelon,Platoon,Section,Squad,Team,Unknown,not set | – |
| OperationalRole | Nationality | enumeration | UN,NATO-PfP,NATO,DEU,MN,EU,TCN,NLD,National,Unknown,not set | – |
| OperationalRole | SizeIndicator | enumeration | Theatre,Armygroup,Army,Corps,Command,Division,Brigade,Regiment,Battalion,Company,Echelon,Platoon,Section,Squad,Team,Unknown,not set | – |
| Project | Architectural guidelines of the Federal Government | enumeration | berücksichtigt,nicht berücksichtigt,teilweise berücksichtigt,keine Relevanz,not set | – |
| Project | Catalogue usage | enumeration | Ja,Nein,keine Relevanz,not set | – |
| Project | Criteria of architecture quality fulfilled | enumeration | Ja,Teilweise,Nein,keine Relevanz,not set | – |
| Project | Implemented SASPF specification | enumeration | Ja,Nein,keine Relevanz,not set | – |
| Project | Implementing Change Management | enumeration | CPM,RfC bei I1.4,Changeprozess SASPF,kein,keine Relevanz,not set | – |
| Project | Modeling according to PlgABw | enumeration | Ja,Nein,keine Relevanz,not set | – |
| Project | Modeling according to SysArch IT-SysBw | enumeration | Ja,Nein,keine Relevanz,not set | – |
| Project | OpArch (FFF) existing | enumeration | zu erstellen,Ja (gemäß Vorgaben),Ja (methodische Mängel),Ja (inhaltliche Mängel),Ja (methodische & inhaltliche Mängel),Nein,keine Relevanz,not set | – |
| Project | SDP existing | enumeration | zu erstellen,Ja (gemäß Vorgaben),Ja (methodische Mängel),Ja (inhaltliche Mängel),Ja (methodische & inhaltliche Mängel),Nein,keine Relevanz,not set | – |
| Project | Service docum. according to IT-Service Designer Bw | enumeration | Ja,Nein,keine Relevanz,not set | – |
| Project | SIR existing | enumeration | zu erstellen,Ja (gemäß Vorgaben),Ja (methodische Mängel),Ja (inhaltliche Mängel),Ja (methodische & inhaltliche Mängel),Nein,keine Relevanz,not set | – |
| Project | SSO existing | enumeration | zu erstellen,Ja (gemäß Vorgaben),Ja (methodische Mängel),Ja (inhaltliche Mängel),Ja (methodische & inhaltliche Mängel),Nein,keine Relevanz,not set | – |
| Project | Systemsteckbrief (GeNu) existing | enumeration | zu erstellen,Ja (gemäß Vorgaben),Ja (methodische Mängel),Ja (inhaltliche Mängel),Ja (methodische & inhaltliche Mängel),Nein,keine Relevanz,not set | – |
| Project | Systemsteckbrief (LV) existing | enumeration | zu erstellen,Ja (gemäß Vorgaben),Ja (methodische Mängel),Ja (inhaltliche Mängel),Ja (methodische & inhaltliche Mängel),Nein,keine Relevanz,not set | – |
| Project | Used templates and specifications for SIR | String | – | – |
| Project | Used templates and specifications for SSO | String | – | – |
| Project | Used templates for FFF | String | – | – |
| Project | Used templates for GeNu | String | – | – |
| Project | Used templates for LV | String | – | – |
| Project | Used templates for SDP | String | – | – |
| ProjectTheme | status | enumeration | NotApplicable,Complete,InProgress,NotStarted,InTest | – |
| Recommendation | Type | enumeration | Method,Tool,Others,Subject | – |
| Reference | Date | Date | – | – |
| ResourceArchitecture | materialPlanningNumber |  | – | – |
| ResourceArtifact | Scalability | enumeration | scale up (vertikal),scale out (horizontal),keine Skalierung,keine Relevanz,not set | – |
| ResourceArtifact | Scaling method | enumeration | Sharding,Clustering,Partitionierung,keine,keine Relevanz,not set | – |
| ResourceArtifact | Type of scalability | enumeration | keine Skalierung,Lastskalierbarkeit,räumliche Skalierung,zeitlich-räumliche Skalierung,strukturelle Skalierung,keine Relevanz,not set | – |
| ResourceArtifact | materialPlanningNumber |  | – | – |
| ResourceConnector | Bandwidth | String | – | – |
| ResourceExchange | exchangeKind | enumeration | ResourceCommunication,ResourceMovment,ResourceEnergyFlow,GeoPoliticalExtentExchange | – |
| ResourcePerformer | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| ResourcePort | Richardson Maturity Model | enumeration | Level 0,Level 1,Level 2,Level 3,keine Relevanz,not set | – |
| ResourceRole | roleKind | enumeration | Part,Component,Used Configuration,Used Physical Architecture,Human Resource,Platform,System,Sub Organisation,Post Role,Responsibiliy Role,Equipment,Sub System Part,Hosted Software,Artifact Compoment,Natural Resource Component,Other | – |
| ResourceRole | Virtualization level | enumeration | vollständige Virtualisierung,Paravirtualisierung,Betriebssystemvirtualisierung,nicht virtualisiert,keine Relevanz,not set | – |
| ResourceRole | Virtualization location | enumeration | Bare Metal,Hosted,keine Virtualisierung,keine Relevanz,not set | – |
| ResourceRole | SecurityDomain | String | – | – |
| ResourceRole | IT security accreditation | enumeration | akkreditiert VS-NfD,akkreditiert Geheim,konform VS-NfD,konform Geheim,nicht akkreditiert,keine Relevanz,not set | – |
| ResourceRole | Programming language | enumeration | ABAP,Java,PHP,C++,C#,Python,keine Relevanz,not set | – |
| ResourceRole | x86 processor architecture | enumeration | Ja,Nein,begründete Abweichung,keine Relevanz,not set | – |
| ResultsFrom | Type | enumeration | Method,Tool,Others,Subject | – |
| Rule | ruleKind | enumeration | StructuralAssertion,ActionAssertion,Derivation,Contract,Constraint,Guidance,SecurityPolicy,Caveat | – |
| ServiceFunction | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| ServiceFunction | ITSD_UtilityUsage | enumeration | not set,IT-Service,IT-Anwender,Betrieb,IT-Service/IT-Anwender,IT-Service/Betrieb,IT-Anwender/Betrieb,IT-Service/IT-Anwender/Betrieb | not set |
| ServiceSpecification | Approved service tailoring | enumeration | Ja,noch offen,nicht erforderlich,Nein,keine Relevanz,not set | – |
| ServiceSpecification | Critical service | enumeration | Ja,Nein,keine Relevanz,not set | – |
| ServiceSpecification | Kind of robustness | String | – | – |
| ServiceSpecification | Measure for robustness | String | – | – |
| ServiceSpecification | Minimization of dependencies | enumeration | Ja,Nein,keine Relevanz,not set | – |
| ServiceSpecification | Service with mission reference | enumeration | Ja,Nein,keine Relevanz,not set | – |
| ServiceSpecification | Status | enumeration | geplant,not set,realisiert | – |
| ServiceSpecification | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| ServiceSpecification | ITSD_ServiceTyp | enumeration | IT-Servicekomponente,IT-Service,IT-Servicemodul | – |
| Software | Role model in IAM | enumeration | Vollständig,Teilweise,Nein,keine Relevanz,not set | – |
| Software | Scalable (on infrastructure) | enumeration | Ja,Nein,keine Relevanz,not set | – |
| Software | Scaling method | enumeration | Sharding,Clustering,Partitionierung,keine,keine Relevanz,not set | – |
| Standard | mandatedDate | mandatedDate | – | – |
| Standard | retiredDate | retiredDate | – | – |
| Standard | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| StoredIn | originalSource | enumeration | true,false,unknown,not set | – |
| UAFElement | URI | String | – | – |
| View | MachineReadable | enumeration | true,false,unknown,not set | – |
| View | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| Viewpoint | purpose | String | – | – |
| Viewpoint | language | String | – | – |
| Viewpoint | method | String | – | – |
| Viewpoint | AbstractionLevel | enumeration | not set,0,1,2,3,4,5,6,R | – |
| WholeLifeConfiguration | kind | enumeration | Service,OrganizationalResource,ResourcePerformer | – |
## 7. Aliases

| Schreibvariante | Kanonischer Name |
|---|---|
| PropertySetGeneralisation | PropertySetGeneralization |
| ServiceSpecificationGeneralization | ServiceGeneralization |

## 8. Kennzahlen

- Stereotype: 318 (davon 44 abstrakt)
- Topologie-Regeln: 203 (davon 133 vollständig)
- Viewpoints: 52
- Property-Typen: 27
- Stereotyp-Tags: 225

Quelle: offizielle ADMBw-MDG-Technologie (BAAINBw), Datei `NAFv4-ADMBw-MDG-2026.05.xml`.