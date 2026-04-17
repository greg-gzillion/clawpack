# Clinical Informatics - Data Standards and Interoperability

## Overview
| Component | Description | URL |
|-----------|-------------|-----|
| **Interoperability** | **Ability of systems to exchange and use information** | https://www.healthit.gov/topic/interoperability |
| **Levels** | **Foundational** (exchange), **Structural** (format), **Semantic** (meaning), **Organizational** (policy) | https://www.healthit.gov/topic/interoperability |

## Key Data Standards
| Standard | Purpose | URL |
|----------|---------|-----|
| **HL7 v2** | **Messaging** (ADT, ORM, ORU) | https://www.hl7.org/implement/standards/product_brief.cfm?product_id=185 |
| **HL7 v3 / CDA** | **Clinical Document Architecture** (structured documents) | https://www.hl7.org/implement/standards/product_brief.cfm?product_id=7 |
| **FHIR** | **Fast Healthcare Interoperability Resources** (RESTful API, modern web standards) | https://www.hl7.org/fhir/ |
| **DICOM** | **Medical imaging** and related data | https://www.dicomstandard.org |
| **LOINC** | **Laboratory and clinical observations** | https://loinc.org |
| **SNOMED CT** | **Clinical terminology** (diagnoses, procedures, findings) | https://www.snomed.org |
| **RxNorm** | **Medications** | https://www.nlm.nih.gov/research/umls/rxnorm/index.html |
| **ICD-10-CM/PCS** | **Diagnoses and procedures** (billing) | https://www.cms.gov/medicare/coding-billing/icd-10-codes |

## FHIR (Fast Healthcare Interoperability Resources)
| Component | Description | URL |
|-----------|-------------|-----|
| **Resources** | **Discrete data units** (Patient, Observation, MedicationRequest, Condition) | https://www.hl7.org/fhir/resourcelist.html |
| **RESTful API** | **HTTP methods** (GET, POST, PUT, DELETE) | https://www.hl7.org/fhir/http.html |
| **SMART on FHIR** | **App platform** for EHR integration | https://smarthealthit.org |
| **US Core** | **FHIR profiles** required for US interoperability | https://www.hl7.org/fhir/us/core/ |

## Terminologies and Ontologies
| Terminology | Domain | URL |
|-------------|--------|-----|
| **SNOMED CT** | **Clinical findings**, **Procedures**, **Body structures**, **Organisms**, **Substances** | https://www.nlm.nih.gov/healthit/snomedct/index.html |
| **LOINC** | **Laboratory tests**, **Clinical observations**, **Document types** | https://loinc.org |
| **RxNorm** | **Medications** (brand, generic, ingredients) | https://www.nlm.nih.gov/research/umls/rxnorm/ |
| **ICD-10-CM** | **Diagnoses** (morbidity reporting) | https://www.cdc.gov/nchs/icd/icd-10-cm.htm |
| **ICD-10-PCS** | **Inpatient procedures** | https://www.cms.gov/medicare/coding-billing/icd-10-codes/icd-10-pcs |
| **CPT** | **Outpatient procedures and services** | https://www.ama-assn.org/practice-management/cpt |
| **NDC** | **National Drug Code** (packaged medications) | https://www.fda.gov/drugs/development-approval-process-drugs/national-drug-code-database-background-information |

## USCDI (United States Core Data for Interoperability)
| Data Class | Examples | URL |
|------------|----------|-----|
| **Patient Demographics** | **Name**, **DOB**, **Sex**, **Race**, **Ethnicity**, **Address** | https://www.healthit.gov/isa/united-states-core-data-interoperability-uscdi |
| **Allergies/Intolerances** | **Substance**, **Reaction**, **Severity** | https://www.healthit.gov/isa/united-states-core-data-interoperability-uscdi |
| **Medications** | **Active medications**, **Medication history** | https://www.healthit.gov/isa/united-states-core-data-interoperability-uscdi |
| **Problems** | **Problem list** (diagnoses) | https://www.healthit.gov/isa/united-states-core-data-interoperability-uscdi |
| **Procedures** | **Surgical and other procedures** | https://www.healthit.gov/isa/united-states-core-data-interoperability-uscdi |
| **Laboratory** | **Lab results**, **Reference ranges** | https://www.healthit.gov/isa/united-states-core-data-interoperability-uscdi |
| **Vital Signs** | **BP**, **HR**, **RR**, **Temp**, **O2 Sat**, **BMI** | https://www.healthit.gov/isa/united-states-core-data-interoperability-uscdi |
| **Clinical Notes** | **Discharge summary**, **Progress note**, **Consult note** | https://www.healthit.gov/isa/united-states-core-data-interoperability-uscdi |

---
*Part of Clawpack Mediclaw - Clinical Informatics Reference*
