"""Synthetic clinical-intel fixtures (not real trial or company data)."""

from __future__ import annotations

COMPANIES = [
    {
        "id": "co-aurora",
        "name": "Aurora Nucleotide",
        "hq": "Boston, MA",
        "focus": ["oncology", "kinase"],
    },
    {
        "id": "co-harbor",
        "name": "Harbor Peptide",
        "hq": "San Diego, CA",
        "focus": ["immunology", "peptides"],
    },
    {
        "id": "co-linden",
        "name": "Linden RNA Works",
        "hq": "Cambridge, UK",
        "focus": ["rare disease", "RNA"],
    },
]

TARGETS = [
    {
        "id": "tgt-braf",
        "symbol": "BRAF",
        "name": "B-Raf proto-oncogene",
        "modality_fit": ["small molecule", "degrader"],
    },
    {
        "id": "tgt-il17a",
        "symbol": "IL17A",
        "name": "Interleukin 17A",
        "modality_fit": ["antibody", "peptide"],
    },
    {
        "id": "tgt-smn1",
        "symbol": "SMN1",
        "name": "Survival of motor neuron 1",
        "modality_fit": ["ASO", "gene therapy"],
    },
]

TRIALS = [
    {
        "id": "NCT90001001",
        "title": "Phase 2 study of AN-214 in BRAF-altered solid tumors",
        "phase": "Phase 2",
        "status": "Recruiting",
        "condition": "Solid tumors",
        "company_id": "co-aurora",
        "target_ids": ["tgt-braf"],
        "start_date": "2025-11-01",
        "summary": "Open-label dose expansion of a BRAF-pathway inhibitor in adults.",
    },
    {
        "id": "NCT90001002",
        "title": "Phase 1 safety of HP-88 for moderate plaque psoriasis",
        "phase": "Phase 1",
        "status": "Active, not recruiting",
        "condition": "Psoriasis",
        "company_id": "co-harbor",
        "target_ids": ["tgt-il17a"],
        "start_date": "2024-06-15",
        "summary": "First-in-human IL17A-directed peptide candidate.",
    },
    {
        "id": "NCT90001003",
        "title": "Phase 3 LR-splice ASO in pediatric SMA type 2",
        "phase": "Phase 3",
        "status": "Recruiting",
        "condition": "Spinal muscular atrophy",
        "company_id": "co-linden",
        "target_ids": ["tgt-smn1"],
        "start_date": "2026-01-10",
        "summary": "Pivotal ASO study with motor function primary endpoint.",
    },
    {
        "id": "NCT90001004",
        "title": "Phase 1b AN-214 + checkpoint inhibitor combination",
        "phase": "Phase 1",
        "status": "Not yet recruiting",
        "condition": "Melanoma",
        "company_id": "co-aurora",
        "target_ids": ["tgt-braf"],
        "start_date": "2026-09-01",
        "summary": "Combination expansion after monotherapy RP2D.",
    },
]
