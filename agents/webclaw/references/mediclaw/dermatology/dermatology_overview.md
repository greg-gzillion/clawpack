# Dermatology - Benign Neoplasms

## Epidermal Tumors
| Tumor | Clinical Features | URL |
|-------|-------------------|-----|
| Seborrheic Keratosis | Waxy, "stuck-on" papule/plaque; Horn cysts; Age >30; Leser-Trélat sign (eruptive SKs = internal malignancy) | https://www.ncbi.nlm.nih.gov/books/NBK545285/ |
| Dermatosis Papulosa Nigra | Small, darkly pigmented papules; Face, neck; Fitzpatrick IV-VI | https://www.ncbi.nlm.nih.gov/books/NBK545285/ |
| Stucco Keratosis | Small, white-gray papules; Lower extremities; Elderly | https://www.ncbi.nlm.nih.gov/books/NBK545285/ |
| Clear Cell Acanthoma | Erythematous, moist papule/nodule; Lower extremities; Punctate vessels on dermoscopy | https://www.ncbi.nlm.nih.gov/books/NBK542214/ |
| Epidermal Nevus | Congenital, verrucous, linear plaque; Following Blaschko lines | https://www.ncbi.nlm.nih.gov/books/NBK482467/ |
| Inflammatory Linear Verrucous Epidermal Nevus (ILVEN) | Pruritic, erythematous, linear plaque; Psoriasiform | https://www.ncbi.nlm.nih.gov/books/NBK482467/ |
| Nevus Sebaceus | Congenital, yellow-orange, hairless plaque; Scalp, face; Secondary neoplasms in adulthood (BCC, syringocystadenoma papilliferum) | https://www.ncbi.nlm.nih.gov/books/NBK482493/ |

## Melanocytic Nevi
| Nevus | Clinical Features | URL |
|-------|-------------------|-----|
| Congenital Melanocytic Nevus | Present at birth; Small (<1.5 cm), Medium (1.5-20 cm), Large/Giant (>20 cm); Increased melanoma risk (especially large/giant) | https://www.ncbi.nlm.nih.gov/books/NBK482211/ |
| Acquired Melanocytic Nevus | Junctional (flat), Compound (raised), Dermal (dome-shaped); Develop after birth | https://www.ncbi.nlm.nih.gov/books/NBK482211/ |
| Halo Nevus | Nevus surrounded by depigmented halo; Lymphocytic infiltration; May regress | https://www.ncbi.nlm.nih.gov/books/NBK482211/ |
| Blue Nevus | Blue-gray papule/nodule; Dermal melanocytes; Common (acquired) or Cellular (larger, may mimic melanoma) | https://www.ncbi.nlm.nih.gov/books/NBK482211/ |
| Spitz Nevus | Pink/red, dome-shaped papule/nodule; Children/young adults; Benign but may mimic melanoma | https://www.ncbi.nlm.nih.gov/books/NBK482211/ |
| Reed Nevus | Pigmented spindle cell nevus; Dark brown/black; Young women; Lower extremities | https://www.ncbi.nlm.nih.gov/books/NBK482211/ |
| Atypical (Dysplastic) Nevus | >5 mm; Irregular border; Variegated color; Macular component; Increased melanoma risk | https://www.ncbi.nlm.nih.gov/books/NBK482211/ |
| Meyerson Nevus | Nevus with surrounding eczematous halo | https://www.ncbi.nlm.nih.gov/books/NBK482211/ |
| Recurrent/Persistent Nevus | Pigmentation within scar after incomplete removal; Pseudomelanoma | https://www.ncbi.nlm.nih.gov/books/NBK482211/ |

## ABCDE Criteria for Melanoma
| Letter | Criterion | Description | URL |
|--------|-----------|-------------|-----|
| A | Asymmetry | One half unlike the other | https://www.aad.org |
| B | Border | Irregular, scalloped, poorly defined | https://www.aad.org |
| C | Color | Variegated (shades of brown, black, red, white, blue) | https://www.aad.org |
| D | Diameter | >6 mm (pencil eraser) | https://www.aad.org |
| E | Evolving | Changing in size, shape, color; New symptom (itching, bleeding) | https://www.aad.org |

## Ugly Duckling Sign
| Feature | Description | URL |
|---------|-------------|-----|
| Definition | Lesion that looks different from the patient's other nevi | https://www.aad.org |
| Significance | Important clinical clue for melanoma detection | https://www.aad.org |

## Derm
cd "C:\Users\greg\dev\clawpack\agents\webclaw\references\mediclaw"

# Create dermatology directory
New-Item -Path "dermatology" -ItemType Directory -Force | Out-Null
cd "dermatology"

Write-Host "?? BUILDING DERMATOLOGY REFERENCE MODULAR STRUCTURE WITH VERIFIED URLs" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Gray

# Create subdirectories
$folders = @(
    "eczematous_dermatitis",
    "papulosquamous_diseases",
    "acneiform_disorders",
    "infections",
    "autoimmune_blistering",
    "connective_tissue_disease",
    "vasculitis_purpura",
    "pigmentary_disorders",
    "benign_neoplasms",
    "malignant_neoplasms",
    "cutaneous_lymphoma",
    "hair_disorders",
    "nail_disorders",
    "genodermatoses",
    "pediatric_dermatology",
    "dermatologic_surgery",
    "cosmetic_dermatology",
    "dermatopathology",
    "dermatologic_emergencies",
    "key_guidelines",
    "resources"
)

foreach ($folder in $folders) {
    New-Item -Path $folder -ItemType Directory -Force | Out-Null
    Write-Host "? Created: $folder" -ForegroundColor Green
}

# 1. OVERVIEW
@'
# Dermatology - Overview

## What is Dermatology?
Dermatology is the medical specialty concerned with the diagnosis, treatment, and prevention of diseases of the skin, hair, nails, and mucous membranes. It encompasses medical, surgical, and cosmetic aspects of skin health.

## Skin Anatomy and Physiology
| Layer | Components | Function |
|-------|------------|----------|
| Epidermis | Stratum corneum, keratinocytes, melanocytes, Langerhans cells | Barrier protection, immune surveillance |
| Dermis | Collagen, elastin, fibroblasts, blood vessels, nerves | Structural support, thermoregulation |
| Subcutis | Adipose tissue | Insulation, energy storage |
| Appendages | Hair follicles, sebaceous glands, eccrine/apocrine glands | Thermoregulation, lubrication |

## Primary Skin Lesions
| Lesion | Description | Example |
|--------|-------------|---------|
| Macule | Flat, circumscribed, <1 cm | Freckle |
| Patch | Flat, circumscribed, >1 cm | Vitiligo |
| Papule | Elevated, solid, <1 cm | Acne |
| Plaque | Elevated, solid, >1 cm | Psoriasis |
| Nodule | Deep, solid, >1 cm | Basal cell carcinoma |
| Vesicle | Fluid-filled, <1 cm | Herpes simplex |
| Bulla | Fluid-filled, >1 cm | Bullous pemphigoid |
| Pustule | Pus-filled | Acne, folliculitis |
| Wheal | Transient, edematous | Urticaria |
| Scale | Flaking of stratum corneum | Psoriasis, seborrheic dermatitis |
| Crust | Dried serum, blood, pus | Impetigo |
| Erosion | Loss of epidermis | Herpes, pemphigus |
| Ulcer | Loss of epidermis and dermis | Venous stasis ulcer |
| Fissure | Linear crack | Angular cheilitis |
| Atrophy | Thinning of skin | Steroid atrophy, aging |
| Scar | Fibrous tissue replacing dermis | Post-surgical, acne |
| Telangiectasia | Dilated superficial blood vessels | Rosacea, sun damage |

## Secondary Skin Lesions
| Lesion | Description | Example |
|--------|-------------|---------|
| Scale | Accumulation of stratum corneum | Psoriasis |
| Crust | Dried exudate | Impetigo |
| Erosion | Partial loss of epidermis | Herpes |
| Ulcer | Full-thickness loss of epidermis | Venous ulcer |
| Excoriation | Linear erosion from scratching | Prurigo nodularis |
| Lichenification | Thickened skin with accentuated markings | Chronic eczema |
| Fissure | Linear crack | Hand dermatitis |
| Scar | Fibrous tissue | Post-surgical |
| Atrophy | Thinning | Topical steroid overuse |

## Key Professional Organizations
| Organization | URL |
|-------------|-----|
| American Academy of Dermatology (AAD) | https://www.aad.org |
| Society for Investigative Dermatology (SID) | https://www.sidnet.org |
| American Society for Dermatologic Surgery (ASDS) | https://www.asds.net |
| American Society for Mohs Surgery (ASMS) | https://www.mohssurgery.org |
| Society for Pediatric Dermatology (SPD) | https://pedsderm.net |
| Women's Dermatologic Society (WDS) | https://www.womensderm.org |
| Skin of Color Society (SOCS) | https://skinofcolorsociety.org |
| International Society of Dermatology (ISD) | https://www.intsocderm.org |
| European Academy of Dermatology and Venereology (EADV) | https://www.eadv.org |

---
*Part of Clawpack Mediclaw - Dermatology Reference*
