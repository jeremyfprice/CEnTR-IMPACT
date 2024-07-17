// Create all nodes with null properties
CREATE (project:Project {title: null, projectID: null, engagementHours: null, individualsServed: null, infrastructureTools: null, status: null, startDate: null, endDate: null}),
       (challenge:Challenge {description: null}),
       (location:Location {latitude: null, longitude: null, name: null}),
       (institution:Institution {name: null, address: null, type: null}),
       (fundingSource:FundingSource {Future: null, type: null, name: null, amount: null}),
       (sector:Sector {type: null}),
       (researchMethodology:ResearchMethodology {Future_description: null}),
       (teachingInnovation:TeachingInnovation {Future_description: null}),
       (serviceOpportunity:ServiceOpportunity {Future_description: null}),
       (artifact:Artifact {title: null, type: null, URL: null, date: null}),
       (diversity:Diversity {value: null, descriptors: null, weights: null}),
       (resources:Resources {value: null, descriptors: null, weights: null}),
       (challengeOrigin:ChallengeOrigin {value: null, descriptors: null, weights: null}),
       (infrastructure:Infrastructure {value: null, descriptors: null, weights: null}),
       (decisionMaking:DecisionMaking {value: null, descriptors: null, weights: null}),
       (beneficence:Beneficence {value: null, descriptors: null, weights: null}),
       (reflection:Reflection {value: null, descriptors: null, weights: null}),
       (goalsMetScore:GoalsMetScore {value: null, descriptors: null, weights: null}),
       (outputsScore:OutputsScore {value: null, descriptors: null, weights: null}),
       (sustainabilityScore:SustainabilityScore {value: null, descriptors: null, weights: null}),
       (capacitiesScore:CapacitiesScore {value: null, descriptors: null, weights: null}),
       (durationScore:DurationScore {value: null, descriptors: null, weights: null}),
       (rippleScore:RippleScore {infoCentrality: null, transformationScore: null, score: null}),
       (frequencyScore:FrequencyScore {value: null, descriptors: null, weights: null}),
       (collaborationScore:CollaborationScore {value: null, descriptors: null, weights: null}),
       (voiceScore:VoiceScore {value: null, descriptors: null, weights: null}),
       (rippleDegree:RippleDegree {degreeNumber: null, degreeMembership: null, degreeInterConnectivity: null, degreeIntraConnectivity: null}),
       (impactScore:ImpactScore {score: null}),
       (alignmentSurvey:AlignmentSurvey {goalsValue: null, ethicsValue: null, outcomesValue: null, rolesValue: null}),
       (alignmentScore:AlignmentScore {goalsValue: null, ethicsValue: null, rolesValue: null, score: null}),
       (indicatorScore:IndicatorScore {score: null}),
       (contextScore:ContextScore {value: null}),
       (processScore:ProcessScore {value: null}),
       (outcomesScore:OutcomesScore {value: null}),
       (interventionScore:InterventionScore {value: null});

// Establish relationships
// Project bidirectional relationships with ResearchMethodology, TeachingInnovation, ServiceOpportunity
MERGE (project)-[:INTEGRATED_WITH]->(researchMethodology)
MERGE (researchMethodology)-[:INTEGRATED_WITH]->(project)
MERGE (project)-[:INTEGRATED_WITH]->(teachingInnovation)
MERGE (teachingInnovation)-[:INTEGRATED_WITH]->(project)
MERGE (project)-[:INTEGRATED_WITH]->(serviceOpportunity)
MERGE (serviceOpportunity)-[:INTEGRATED_WITH]->(project)

// Project single-direction relationships
MERGE (project)-[:ALIGNED_WITH]->(sector)
MERGE (project)-[:ADDRESSES]->(challenge)
MERGE (project)-[:TAKES_PLACE_IN]->(location)
MERGE (project)-[:GENERATES]->(artifact)

// Institutions, FundingSource, Person single-direction relationships to Project
MERGE (institution)-[:PARTNERS_IN]->(project)
MERGE (fundingSource)-[:SUPPORTS]->(project)
MERGE (person:Person)-[:CONTRIBUTES_TO]->(project)

// Project bidirectional relationships with different types
MERGE (project)-[:EXHIBITS]->(indicatorScore)
MERGE (indicatorScore)-[:INFORMS_STRATEGY]->(project)
MERGE (project)-[:EXHIBITS]->(alignmentScore)
MERGE (alignmentScore)-[:INFORMS_STRATEGY]->(project)
MERGE (project)-[:EXHIBITS]->(impactScore)
MERGE (impactScore)-[:INFORMS_STRATEGY]->(project)
MERGE (project)-[:EXHIBITS]->(rippleScore)
MERGE (rippleScore)-[:INFORMS_STRATEGY]->(project)

// Bidirectional relationships between other nodes
MERGE (sector)-[:INFORMS]->(researchMethodology)
MERGE (researchMethodology)-[:INTEGRATED_WITH]->(teachingInnovation)
MERGE (teachingInnovation)-[:INTEGRATED_WITH]->(serviceOpportunity)
MERGE (serviceOpportunity)-[:INFORMS]->(sector)
MERGE (teachingInnovation)-[:INFORMS]->(sector)
MERGE (challenge)-[:INFORMS]->(fundingSource)

// Single sided relationships with specific relationship names
MERGE (teachingInnovation)-[:RESULTS_IN]->(artifact)
MERGE (researchMethodology)-[:RESULTS_IN]->(artifact)
MERGE (serviceOpportunity)-[:RESULTS_IN]->(artifact)
MERGE (person)-[:CREATES]->(artifact)
MERGE (sector)-[:INFORMS]->(challenge)
MERGE (institution)-[:LOCATED_AT]->(location)
MERGE (fundingSource)-[:AWARDED_TO]->(institution)
MERGE (fundingSource)-[:AWARDED_TO]->(person)
MERGE (person)-[:CREATES]->(artifact)
MERGE (person)-[:EMBEDDED_IN]->(sector)
MERGE (person)-[:AFFILIATED_WITH]->(institution)
MERGE (rippleDegree)-[:FACTORS_INTO]->(rippleScore)

// Factors Into relationships
MERGE (voiceScore)-[:FACTORS_INTO]->(interventionScore)-[:FACTORS_INTO]->(impactScore)
MERGE (collaborationScore)-[:FACTORS_INTO]->(interventionScore)
MERGE (frequencyScore)-[:FACTORS_INTO]->(interventionScore)
MERGE (durationScore)-[:FACTORS_INTO]->(interventionScore)
MERGE (capacitiesScore)-[:FACTORS_INTO]->(outcomesScore)-[:FACTORS_INTO]->(impactScore)
MERGE (sustainabilityScore)-[:FACTORS_INTO]->(outcomesScore)
MERGE (outputsScore)-[:FACTORS_INTO]->(outcomesScore)
MERGE (goalsMetScore)-[:FACTORS_INTO]->(outcomesScore)
MERGE (reflection)-[:FACTORS_INTO]->(processScore)-[:FACTORS_INTO]->(impactScore)
MERGE (beneficence)-[:FACTORS_INTO]->(processScore)
MERGE (decisionMaking)-[:FACTORS_INTO]->(processScore)
MERGE (infrastructure)-[:FACTORS_INTO]->(processScore)
MERGE (challengeOrigin)-[:FACTORS_INTO]->(contextScore)-[:FACTORS_INTO]->(impactScore)
MERGE (resources)-[:FACTORS_INTO]->(contextScore)
MERGE (diversity)-[:FACTORS_INTO]->(contextScore)
MERGE (alignmentSurvey)-[:FACTORS_INTO]->(alignmentScore);
