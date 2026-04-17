# Clinical Informatics - Genomics Informatics

## Overview
| Component | Description | URL |
|-----------|-------------|-----|
| **Definition** | **Application of informatics to genomic and genetic data** | https://www.genome.gov/genetics-glossary/Genomic-Informatics |
| **Applications** | **Precision medicine**, **Pharmacogenomics**, **Disease risk assessment**, **Diagnosis** | https://www.genome.gov/health/Genomics-and-Medicine |

## Genomic Data Types
| Data Type | Description | URL |
|-----------|-------------|-----|
| **DNA Sequence** | **Whole genome**, **Whole exome**, **Targeted panels** | https://www.genome.gov/about-genomics/fact-sheets/Sequencing-Human-Genome |
| **Variants** | **SNPs**, **Indels**, **CNVs**, **Structural variants** | https://www.genome.gov/genetics-glossary/Variant |
| **Gene Expression** | **RNA-Seq**, **Microarray** | https://www.genome.gov/genetics-glossary/Gene-Expression |
| **Epigenomics** | **DNA methylation**, **Histone modification** | https://www.genome.gov/genetics-glossary/Epigenomics |
| **Pharmacogenomics** | **Genetic variants affecting drug response** | https://www.genome.gov/genetics-glossary/Pharmacogenomics |

## Clinical Genomic Data Standards
| Standard | Purpose | URL |
|----------|---------|-----|
| **HGVS** | **Variant nomenclature** | https://varnomen.hgvs.org |
| **VCF** | **Variant Call Format** (variant data) | https://samtools.github.io/hts-specs/VCFv4.3.pdf |
| **BAM/CRAM** | **Aligned sequence data** | https://samtools.github.io/hts-specs/ |
| **HL7 FHIR Genomics** | **Exchange of genomic data in EHR** | https://www.hl7.org/fhir/genomics.html |
| **LOINC** | **Genetic test codes** | https://loinc.org |
| **ClinVar** | **Variant-disease relationships** | https://www.ncbi.nlm.nih.gov/clinvar/ |

## EHR Integration of Genomic Data
| Challenge | Solution | URL |
|-----------|----------|-----|
| **Data Volume** | **Store pointers to external repositories**, **Store key variants only** | https://www.healthit.gov/topic/precision-medicine |
| **Interpretation** | **Clinical decision support** for genomic results | https://www.healthit.gov/topic/precision-medicine |
| **Reanalysis** | **Periodic re-evaluation** as knowledge evolves | https://www.healthit.gov/topic/precision-medicine |
| **Patient Privacy** | **GINA** (Genetic Information Nondiscrimination Act) protections | https://www.eeoc.gov/genetic-information-discrimination |

## Pharmacogenomics
| Gene | Drug | Clinical Implication | URL |
|------|------|---------------------|-----|
| **CYP2C19** | **Clopidogrel** | **Poor metabolizers ? Alternative antiplatelet** | https://cpicpgx.org/guidelines/guideline-for-clopidogrel-and-cyp2c19/ |
| **CYP2D6** | **Codeine**, **Tamoxifen** | **Poor metabolizers ? ? Efficacy; Ultrarapid ? ? Toxicity** | https://cpicpgx.org/guidelines/ |
| **CYP2C9/VKORC1** | **Warfarin** | **Guide initial dosing** | https://cpicpgx.org/guidelines/guideline-for-warfarin-and-cyp2c9-and-vkorc1/ |
| **HLA-B*57:01** | **Abacavir** | **Hypersensitivity risk ? Avoid** | https://cpicpgx.org/guidelines/guideline-for-abacavir-and-hla-b/ |
| **HLA-B*15:02** | **Carbamazepine** | **SJS/TEN risk ? Avoid** (Asian ancestry) | https://cpicpgx.org/guidelines/guideline-for-carbamazepine-and-hla-b/ |
| **TPMT/NUDT15** | **Azathioprine**, **6-MP** | **Deficient ? Severe myelosuppression ? Reduce dose** | https://cpicpgx.org/guidelines/guideline-for-thiopurines-and-tpmt-and-nudt15/ |
| **SLCO1B1** | **Simvastatin** | **? Myopathy risk ? Lower dose or alternative** | https://cpicpgx.org/guidelines/guideline-for-simvastatin-and-slco1b1/ |

---
*Part of Clawpack Mediclaw - Clinical Informatics Reference*
