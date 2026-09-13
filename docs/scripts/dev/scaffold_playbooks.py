#!/usr/bin/env python3
"""One-time scaffold: write the eight project-type playbooks with PLACEHOLDER assemblies.

Every dollar figure here is a national-average placeholder marked `[to load]`; the ROM stage flags
each priced line UNCERTAIN until the company's buyout history replaces the numbers (playbook status
seed → approved). Quantity rules are deliberately simple and stated on every line.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parents[2] / "core" / "tools" / "data" / "estimating" / "playbooks"
SRC = "seed-placeholder-2026 [to load: company buyout history]"


def A(code, trade, desc, unit, basis, factor, low, target, high, conf=0.5, labor_share=0.0, notes=""):
    return {"code": code, "trade": trade, "description": desc, "unit": unit, "qty": {"basis": basis, "factor": factor},
            "low": low, "target": target, "high": high, "source": SRC, "confidence": conf, "labor_share": labor_share, "notes": notes}


def R(risk, severity, trade="", excl="", rfi=""):
    return {"risk": risk, "severity": severity, "trade": trade, "mitigation_exclusion": excl, "rfi": rfi}


GC_TI = {"superintendent_fte": 1.0, "pm_fte": 0.25, "pe_fte": 0.0, "safety_fte": 0.25, "trailer": False, "toilets": 1, "dumpsters_per_month": 2, "fence": False}
GC_GU = {"superintendent_fte": 1.0, "pm_fte": 0.5, "pe_fte": 0.5, "safety_fte": 0.5, "trailer": True, "toilets": 2, "dumpsters_per_month": 3, "fence": True}

COMMON_TI_EXCL = ["permit and impact fees unless stated", "hazardous materials abatement", "after-hours or weekend work unless stated",
                  "hidden conditions behind existing finishes or below slab", "landlord-required work not shown", "low-voltage cabling, AV, security beyond raceway",
                  "furniture, fixtures and equipment purchase (owner-furnished)", "utility company fees and service upgrades"]

PLAYBOOKS = [
    {
        "project_type": "restaurant-ti", "aliases": ["restaurant", "restaurant remodel", "restaurant build-out", "qsr", "cafe", "bar", "kitchen"],
        "version": "1.0", "status": "seed", "building_type_band": "restaurant ti", "default_class": 5,
        "schedule_range_days": {"low": 60, "target": 100, "high": 160},
        "typical_trades": ["demo", "framing-drywall", "paint-finish", "flooring", "ceiling", "plumbing", "hvac", "electrical", "hood-kitchen", "fire-suppression", "fire-alarm", "fire-sprinkler", "millwork", "general-conditions"],
        "intake_fields": {"gross_sf": {"required": True}, "kitchen_sf": {"default_ratio_of_gross": 0.30, "note": "kitchen assumed 30% of gross when not given"},
                          "hood_lf": {"default": 12, "note": "one 12 LF Type I hood assumed"}, "fixture_count": {"default": 8, "note": "8 plumbing fixtures assumed (restrooms + kitchen sinks)"},
                          "restroom_count": {"default": 2, "note": "two restrooms assumed"}, "existing_sprinklered": {"default": 1, "note": "building assumed sprinklered (1 = yes)"}},
        "general_conditions": GC_TI,
        "assemblies": [
            A("02-selective-demo-ti", "demo", "Selective demolition of walls, ceilings and finishes with haul-off and protection", "SF", "gross_sf", 1.0, 3.50, 5.50, 9.00),
            A("09-partitions-ti", "framing-drywall", "Metal stud partitions with 5/8 GWB both sides, taped and finished (per SF of floor area)", "SF", "gross_sf", 0.9, 9.00, 13.00, 19.00, 0.45),
            A("09-paint-ti", "paint-finish", "Interior paint, doors and frames, patch-to-match (per SF of floor area)", "SF", "gross_sf", 1.0, 2.20, 3.20, 4.80),
            A("09-flooring-dining", "flooring", "Dining/front-of-house flooring with prep, base and transitions", "SF", "dining_sf", 1.0, 6.00, 9.50, 15.00),
            A("09-flooring-kitchen-quarry", "flooring", "Kitchen quarry tile or epoxy with cove base", "SF", "kitchen_sf", 1.0, 12.00, 17.00, 25.00),
            A("09-ceiling-act-ti", "ceiling", "ACT ceiling and grid, washable tile in kitchen", "SF", "gross_sf", 0.85, 4.50, 6.50, 9.50),
            A("22-plumbing-fixture-ti", "plumbing", "Plumbing fixture set with rough-in, relocation and reconnection", "EA", "fixture_count", 1.0, 2400.00, 3600.00, 5500.00),
            A("22-grease-waste-ti", "plumbing", "Grease waste routing, floor sinks and interceptor tie-in (existing interceptor)", "LS", "each", 1.0, 7000.00, 14000.00, 24000.00, 0.4),
            A("23-hood-type1-per-lf", "hood-kitchen", "Type I hood, grease duct, exhaust fan, roof curb and fire-suppression coordination (per LF of hood)", "LF", "hood_lf", 1.0, 1450.00, 1800.00, 2400.00),
            A("23-mua-unit", "hood-kitchen", "Make-up air unit with curb, duct and controls", "EA", "each", 1.0, 14000.00, 22000.00, 34000.00, 0.4),
            A("23-hvac-ti", "hvac", "Ductwork modifications, diffusers, controls and TAB using existing RTUs (per SF)", "SF", "gross_sf", 1.0, 7.00, 11.00, 18.00),
            A("26-electrical-restaurant", "electrical", "Panels, circuits, kitchen equipment connections, lighting and devices (per SF)", "SF", "gross_sf", 1.0, 16.00, 24.00, 36.00),
            A("21-fire-suppression-hood", "fire-suppression", "Wet-chemical hood suppression system with tie-ins", "EA", "each", 1.0, 5500.00, 8500.00, 12500.00),
            A("28-fire-alarm-ti", "fire-alarm", "Fire alarm device changes, hood interlock and monitoring coordination", "LS", "each", 1.0, 3500.00, 6500.00, 11000.00, 0.4),
            A("21-sprinkler-relocate-ti", "fire-sprinkler", "Sprinkler head relocations and additions (per SF, existing system)", "SF", "gross_sf", 1.0, 1.50, 2.50, 4.50, 0.4),
            A("12-millwork-restaurant", "millwork", "Counters, service stations and casework install (per LF assumed = perimeter × 0.15)", "LF", "perimeter_lf", 0.15, 350.00, 550.00, 900.00, 0.4),
        ],
        "common_rfis": ["Is the final kitchen equipment schedule with cut sheets available?", "Are hood and fire-suppression drawings available, and is make-up air existing or new?",
                        "Is the grease interceptor existing, approved and adequately sized?", "Are gas service and electrical service capacities confirmed?",
                        "Are the existing RTUs adequate for the kitchen heat load?", "Are health department comments available?", "Which items are owner-furnished, and who installs them?"],
        "common_exclusions": ["kitchen equipment purchase", "grease interceptor replacement", "RTU replacement and make-up air unless shown", "electrical service upgrade", "gas meter upgrade"] + COMMON_TI_EXCL,
        "risk_checklist": [R("Hood / make-up air", "high", "hood-kitchen", "make-up air unit unless shown on drawings", "Is make-up air existing or new?"),
                           R("Grease interceptor capacity and routing", "high", "plumbing", "grease interceptor replacement", "Is the grease interceptor existing, approved and adequately sized?"),
                           R("Gas and electrical service capacity", "high", "electrical", "electrical service and gas meter upgrades", "Are gas and electrical service capacities confirmed?"),
                           R("RTU capacity for kitchen heat load", "high", "hvac", "RTU replacement", "Are the existing RTUs adequate for the kitchen heat load?"),
                           R("Health department and Fire Marshal review", "medium", "general-conditions", "", "Are health department comments available?"),
                           R("Slab trenching for plumbing relocations", "medium", "plumbing", "", "Are existing under-slab line locations known?"),
                           R("Owner-furnished equipment timing", "medium", "hood-kitchen", "", "Which items are owner-furnished?")],
    },
    {
        "project_type": "salon-beauty", "aliases": ["salon", "beauty", "spa", "nail salon", "barber"], "version": "1.0", "status": "seed",
        "building_type_band": "salon ti", "default_class": 5, "schedule_range_days": {"low": 45, "target": 75, "high": 120},
        "typical_trades": ["demo", "framing-drywall", "plumbing", "electrical", "hvac", "flooring", "paint-finish", "ceiling", "millwork", "general-conditions"],
        "intake_fields": {"gross_sf": {"required": True}, "station_count": {"default": 8, "note": "8 styling stations assumed"}, "shampoo_bowls": {"default": 3, "note": "3 shampoo bowls assumed"},
                          "restroom_count": {"default": 1, "note": "one restroom assumed"}},
        "general_conditions": GC_TI,
        "assemblies": [
            A("02-selective-demo-ti", "demo", "Selective demolition and haul-off", "SF", "gross_sf", 1.0, 2.50, 4.00, 7.00),
            A("09-partitions-ti", "framing-drywall", "Metal stud partitions with GWB both sides (per SF of floor area)", "SF", "gross_sf", 0.7, 9.00, 13.00, 19.00, 0.45),
            A("22-shampoo-bowl-set", "plumbing", "Shampoo bowl with rough-in, drain and hot/cold supply", "EA", "shampoo_bowls", 1.0, 2800.00, 4200.00, 6500.00),
            A("22-water-heater-salon", "plumbing", "Commercial water heater sized for bowls with recirculation", "EA", "each", 1.0, 4500.00, 7500.00, 12000.00, 0.4),
            A("22-restroom-set", "plumbing", "ADA restroom fixture set with rough-in", "EA", "restroom_count", 1.0, 7500.00, 11000.00, 16000.00),
            A("26-station-electrical", "electrical", "Dedicated circuits, outlets and lighting per styling station", "EA", "station_count", 1.0, 900.00, 1400.00, 2200.00),
            A("26-electrical-base-ti", "electrical", "Panel work, lighting and general devices (per SF)", "SF", "gross_sf", 1.0, 8.00, 12.00, 18.00),
            A("23-hvac-ti", "hvac", "Ductwork modifications, exhaust and TAB using existing units (per SF)", "SF", "gross_sf", 1.0, 5.00, 8.00, 13.00),
            A("09-flooring-lvp", "flooring", "LVP or tile flooring with prep and base", "SF", "gross_sf", 1.0, 5.50, 8.00, 12.00),
            A("09-paint-ti", "paint-finish", "Interior paint and finish touch-up (per SF of floor area)", "SF", "gross_sf", 1.0, 2.00, 3.00, 4.50),
            A("09-ceiling-act-ti", "ceiling", "ACT ceiling and grid", "SF", "gross_sf", 0.9, 4.00, 6.00, 9.00),
            A("12-millwork-salon", "millwork", "Reception desk, station mirrors/backing and cabinetry install (owner-furnished stations)", "LS", "each", 1.0, 6000.00, 12000.00, 22000.00, 0.4),
        ],
        "common_rfis": ["How many shampoo bowls and styling stations?", "Are chairs and stations owner-furnished, and who installs them?", "Is water heater capacity adequate?",
                        "Are floor penetrations for drains allowed by the landlord?", "Is existing HVAC capacity adequate?", "Are electrical loads for dryers confirmed?"],
        "common_exclusions": ["styling stations, chairs and equipment purchase", "water heater upgrade beyond capacity shown", "landlord-required corridor or storefront work"] + COMMON_TI_EXCL,
        "risk_checklist": [R("Under-slab trenching for bowl drains", "high", "plumbing", "slab trenching beyond 40 LF", "Are floor penetrations and drain routes confirmed?"),
                           R("Water heater capacity", "high", "plumbing", "water heater upgrade beyond capacity shown", "Is water heater capacity adequate for the bowl count?"),
                           R("Electrical load for dryers and stations", "medium", "electrical", "", "Are electrical loads confirmed?"),
                           R("Venting limitations", "medium", "plumbing", "", "Are vent routes available?"),
                           R("Finish expectations vs budget", "low", "paint-finish", "", "")],
    },
    {
        "project_type": "medical-dental", "aliases": ["medical office", "dental", "clinic", "medical", "dental office", "medical office ti"], "version": "1.0", "status": "seed",
        "building_type_band": "medical office ti", "default_class": 5, "schedule_range_days": {"low": 75, "target": 120, "high": 180},
        "typical_trades": ["demo", "framing-drywall", "plumbing", "hvac", "electrical", "fire-alarm", "fire-sprinkler", "flooring", "ceiling", "millwork", "paint-finish", "general-conditions"],
        "intake_fields": {"gross_sf": {"required": True}, "exam_rooms": {"default_ratio_of_gross": 0.004, "note": "one exam/operatory room per 250 SF assumed"},
                          "restroom_count": {"default": 2, "note": "two restrooms assumed"}, "hand_sinks": {"default_ratio_of_gross": 0.004, "note": "one hand sink per exam room assumed"}},
        "general_conditions": GC_TI,
        "assemblies": [
            A("02-selective-demo-ti", "demo", "Selective demolition and haul-off", "SF", "gross_sf", 1.0, 2.50, 4.00, 7.00),
            A("09-partitions-medical", "framing-drywall", "Partitions with sound batts and backing for medical casework (per SF of floor area)", "SF", "gross_sf", 1.2, 10.00, 14.50, 21.00, 0.45),
            A("22-hand-sink-set", "plumbing", "Exam-room hand sink with rough-in and ADA trim", "EA", "hand_sinks", 1.0, 2800.00, 4000.00, 6000.00),
            A("22-restroom-set", "plumbing", "ADA restroom fixture set with rough-in", "EA", "restroom_count", 1.0, 7500.00, 11000.00, 16000.00),
            A("22-medical-utilities-allow", "plumbing", "Specialty utilities (vacuum, air, sterilization) rough-in coordination (allowance-type)", "LS", "each", 1.0, 6000.00, 12000.00, 25000.00, 0.3),
            A("23-hvac-medical", "hvac", "Zoned ductwork, exhaust, controls and TAB (per SF)", "SF", "gross_sf", 1.0, 9.00, 14.00, 22.00),
            A("26-electrical-medical", "electrical", "Panels, equipment circuits, lighting, exam-room devices (per SF)", "SF", "gross_sf", 1.0, 18.00, 26.00, 38.00),
            A("28-fire-alarm-ti", "fire-alarm", "Fire alarm device changes and monitoring coordination", "LS", "each", 1.0, 3500.00, 6500.00, 11000.00, 0.4),
            A("21-sprinkler-relocate-ti", "fire-sprinkler", "Sprinkler head relocations (per SF, existing system)", "SF", "gross_sf", 1.0, 1.50, 2.50, 4.50, 0.4),
            A("09-flooring-medical", "flooring", "Sheet vinyl / LVT with integral base in clinical areas, carpet tile elsewhere", "SF", "gross_sf", 1.0, 7.00, 10.00, 15.00),
            A("09-ceiling-act-ti", "ceiling", "ACT ceiling and grid, cleanroom-rated tile in clinical rooms", "SF", "gross_sf", 0.9, 4.50, 7.00, 10.50),
            A("12-millwork-exam-room", "millwork", "Exam/operatory casework, countertops and blocking (per room)", "EA", "exam_rooms", 1.0, 4500.00, 7500.00, 12000.00, 0.4),
            A("09-paint-ti", "paint-finish", "Interior paint with epoxy in wet areas (per SF)", "SF", "gross_sf", 1.0, 2.40, 3.40, 5.00),
        ],
        "common_rfis": ["Are medical/dental equipment cut sheets and utility requirements available?", "Are specialty utilities (vacuum, air, gas) required?",
                        "Are accessibility (TAS/ADA) requirements shown?", "Are plumbing fixture and hand-sink counts final?", "Are HVAC zones and exhaust requirements defined?",
                        "Are fire alarm or sprinkler changes needed?"],
        "common_exclusions": ["medical and dental equipment purchase and installation", "medical gas certification", "x-ray shielding unless shown", "TDLR registration and inspection fees"] + COMMON_TI_EXCL,
        "risk_checklist": [R("Accessibility / TAS review", "high", "general-conditions", "", "Are accessibility requirements shown and has TAS review been requested?"),
                           R("Equipment utility requirements unknown", "high", "plumbing", "specialty utilities beyond the allowance carried", "Are equipment cut sheets available?"),
                           R("Infection-control finish requirements", "medium", "flooring", "", "Are finish specifications for clinical areas defined?"),
                           R("Inspection requirements (health, radiology)", "medium", "general-conditions", "", ""),
                           R("Owner equipment delays", "medium", "millwork", "", "")],
    },
    {
        "project_type": "retail-ti", "aliases": ["retail", "retail tenant improvement", "retail build-out", "store", "shop"], "version": "1.0", "status": "seed",
        "building_type_band": "retail ti", "default_class": 5, "schedule_range_days": {"low": 45, "target": 75, "high": 120},
        "typical_trades": ["demo", "framing-drywall", "ceiling", "electrical", "hvac", "flooring", "paint-finish", "millwork", "fire-alarm", "fire-sprinkler", "general-conditions"],
        "intake_fields": {"gross_sf": {"required": True}, "fitting_rooms": {"default": 0, "note": "no fitting rooms assumed"}, "restroom_count": {"default": 1, "note": "one restroom assumed"}},
        "general_conditions": GC_TI,
        "assemblies": [
            A("02-selective-demo-ti", "demo", "Selective demolition and haul-off", "SF", "gross_sf", 1.0, 2.00, 3.50, 6.00),
            A("09-partitions-ti", "framing-drywall", "Partitions and furring (per SF of floor area)", "SF", "gross_sf", 0.5, 9.00, 13.00, 19.00, 0.45),
            A("09-ceiling-act-ti", "ceiling", "ACT ceiling or exposed-ceiling paint", "SF", "gross_sf", 1.0, 4.00, 6.00, 9.00),
            A("26-electrical-retail", "electrical", "Lighting, power, fixture connections (per SF)", "SF", "gross_sf", 1.0, 10.00, 15.00, 23.00),
            A("23-hvac-ti", "hvac", "Duct modifications and TAB using existing units (per SF)", "SF", "gross_sf", 1.0, 5.00, 8.00, 13.00),
            A("09-flooring-retail", "flooring", "Sales-floor flooring with prep and base", "SF", "gross_sf", 1.0, 5.00, 8.00, 13.00),
            A("09-paint-ti", "paint-finish", "Interior paint (per SF of floor area)", "SF", "gross_sf", 1.0, 1.80, 2.80, 4.20),
            A("12-fixture-install-retail", "millwork", "Owner-furnished fixture and casework installation coordination", "LS", "each", 1.0, 4000.00, 9000.00, 18000.00, 0.4),
            A("28-fire-alarm-ti", "fire-alarm", "Fire alarm device changes", "LS", "each", 1.0, 2500.00, 5000.00, 9000.00, 0.4),
            A("21-sprinkler-relocate-ti", "fire-sprinkler", "Sprinkler head relocations (per SF)", "SF", "gross_sf", 1.0, 1.20, 2.00, 3.50, 0.4),
        ],
        "common_rfis": ["Are fixture and lighting plans final?", "Are landlord criteria and the landlord work letter available?", "Are storefront changes included?",
                        "Are low-voltage and security systems by owner?", "Are after-hours rules imposed by the center?"],
        "common_exclusions": ["storefront and signage unless shown", "fixtures and merchandising equipment purchase", "low-voltage, security and POS systems", "landlord work-letter items"] + COMMON_TI_EXCL,
        "risk_checklist": [R("Landlord criteria and work letter", "high", "general-conditions", "landlord work-letter items", "Are landlord criteria available?"),
                           R("After-hours rules in the center", "medium", "general-conditions", "after-hours premium beyond stated hours", "Are after-hours rules imposed?"),
                           R("Fixture delivery timing", "medium", "millwork", "", ""),
                           R("Low-voltage scope gaps", "medium", "electrical", "low-voltage, security and POS systems", "Are low-voltage systems by owner?")],
    },
    {
        "project_type": "office-buildout", "aliases": ["office", "office build-out", "office ti", "corporate interiors", "tenant improvement office"], "version": "1.0", "status": "seed",
        "building_type_band": "tenant improvement office", "default_class": 5, "schedule_range_days": {"low": 45, "target": 80, "high": 130},
        "typical_trades": ["demo", "framing-drywall", "ceiling", "electrical", "hvac", "paint-finish", "flooring", "millwork", "doors-hardware", "fire-alarm", "fire-sprinkler", "general-conditions"],
        "intake_fields": {"gross_sf": {"required": True}, "private_offices": {"default_ratio_of_gross": 0.005, "note": "one private office per 200 SF assumed"},
                          "conference_rooms": {"default": 2, "note": "two conference rooms assumed"}, "break_rooms": {"default": 1, "note": "one break room assumed"}},
        "general_conditions": GC_TI,
        "assemblies": [
            A("02-selective-demo-ti", "demo", "Selective demolition and haul-off", "SF", "gross_sf", 1.0, 1.80, 3.00, 5.50),
            A("09-partitions-office", "framing-drywall", "Office partitions to deck with sound batts (per SF of floor area)", "SF", "gross_sf", 1.1, 9.00, 13.00, 19.00, 0.45),
            A("08-office-door-set", "doors-hardware", "Office door, frame, hardware and sidelight", "EA", "private_offices", 1.0, 1800.00, 2600.00, 3800.00),
            A("09-ceiling-act-ti", "ceiling", "ACT ceiling and grid", "SF", "gross_sf", 0.95, 4.00, 6.00, 9.00),
            A("26-electrical-office", "electrical", "Lighting with controls, power, data raceway (per SF)", "SF", "gross_sf", 1.0, 11.00, 16.00, 24.00),
            A("23-hvac-office", "hvac", "VAV/duct modifications, thermostats and TAB (per SF)", "SF", "gross_sf", 1.0, 6.00, 9.50, 15.00),
            A("09-paint-ti", "paint-finish", "Interior paint (per SF of floor area)", "SF", "gross_sf", 1.0, 1.80, 2.80, 4.20),
            A("09-flooring-office", "flooring", "Carpet tile with LVT in break areas, base", "SF", "gross_sf", 1.0, 5.00, 7.50, 11.00),
            A("12-millwork-break-room", "millwork", "Break room and copy-area casework with countertops", "EA", "break_rooms", 1.0, 6000.00, 10000.00, 16000.00, 0.4),
            A("28-fire-alarm-ti", "fire-alarm", "Fire alarm device changes", "LS", "each", 1.0, 2500.00, 5000.00, 9000.00, 0.4),
            A("21-sprinkler-relocate-ti", "fire-sprinkler", "Sprinkler head relocations (per SF)", "SF", "gross_sf", 1.0, 1.20, 2.00, 3.50, 0.4),
        ],
        "common_rfis": ["Is the furniture plan final?", "Are data and low-voltage systems by owner?", "Are conference-room AV needs included?", "Are existing RTUs/VAVs adequate?",
                        "Are fire alarm or sprinkler changes needed?", "Is the building's after-hours HVAC and freight policy known?"],
        "common_exclusions": ["furniture, AV and data cabling", "landlord base-building work", "restroom modifications unless shown"] + COMMON_TI_EXCL,
        "risk_checklist": [R("Data / low-voltage scope gaps", "high", "electrical", "furniture, AV and data cabling", "Are data and low-voltage systems by owner?"),
                           R("Sound and privacy expectations", "medium", "framing-drywall", "", "Are acoustic requirements defined for offices and conference rooms?"),
                           R("HVAC balancing with new partitions", "medium", "hvac", "", "Are existing units adequate?"),
                           R("Landlord requirements and building rules", "medium", "general-conditions", "landlord base-building work", "")],
    },
    {
        "project_type": "white-box", "aliases": ["white box", "whitebox", "vanilla shell", "shell finish-out", "landlord white box"], "version": "1.0", "status": "seed",
        "building_type_band": "white box", "default_class": 5, "schedule_range_days": {"low": 40, "target": 70, "high": 110},
        "typical_trades": ["demo", "framing-drywall", "plumbing", "hvac", "electrical", "fire-sprinkler", "fire-alarm", "ceiling", "paint-finish", "general-conditions"],
        "intake_fields": {"gross_sf": {"required": True}, "restroom_count": {"default": 1, "note": "one restroom assumed"}, "hvac_included": {"default": 1, "note": "HVAC distribution assumed included (1 = yes)"}},
        "general_conditions": GC_TI,
        "assemblies": [
            A("02-selective-demo-ti", "demo", "Demolition of previous tenant finishes if any", "SF", "gross_sf", 1.0, 1.00, 2.00, 4.00, 0.4),
            A("09-partitions-white-box", "framing-drywall", "Demising and restroom partitions, drywall to landlord standard (per SF)", "SF", "gross_sf", 0.4, 9.00, 13.00, 19.00, 0.45),
            A("22-restroom-set", "plumbing", "ADA restroom fixture set with rough-in", "EA", "restroom_count", 1.0, 7500.00, 11000.00, 16000.00),
            A("23-hvac-distribution", "hvac", "HVAC distribution from existing unit with diffusers and thermostat (per SF)", "SF", "gross_sf", 1.0, 5.00, 8.00, 12.00),
            A("26-electrical-white-box", "electrical", "Panel, code lighting, receptacles (per SF)", "SF", "gross_sf", 1.0, 7.00, 11.00, 16.00),
            A("21-sprinkler-relocate-ti", "fire-sprinkler", "Sprinkler heads to code (per SF)", "SF", "gross_sf", 1.0, 1.50, 2.50, 4.50, 0.4),
            A("28-fire-alarm-ti", "fire-alarm", "Code-required fire alarm devices", "LS", "each", 1.0, 2500.00, 5000.00, 9000.00, 0.4),
            A("09-ceiling-act-ti", "ceiling", "ACT ceiling and grid or exposed-ceiling paint", "SF", "gross_sf", 1.0, 3.50, 5.50, 8.50),
            A("09-paint-ti", "paint-finish", "Prime and paint to landlord standard (per SF)", "SF", "gross_sf", 1.0, 1.50, 2.30, 3.50),
        ],
        "common_rfis": ["What is the landlord-required white-box condition (work letter)?", "Are restrooms included?", "Is the HVAC unit existing and adequate?",
                        "Is flooring included or excluded?", "Are sprinkler and fire alarm changes required by code for the shell?"],
        "common_exclusions": ["flooring unless stated", "tenant-specific improvements", "HVAC unit replacement", "storefront work"] + COMMON_TI_EXCL,
        "risk_checklist": [R("Unclear landlord criteria", "high", "general-conditions", "items beyond the landlord work letter", "What is the landlord-required white-box condition?"),
                           R("Scope boundary landlord vs tenant", "high", "general-conditions", "tenant-specific improvements", "Which items are tenant scope?"),
                           R("Utility capacity", "medium", "electrical", "", "Are service sizes confirmed?"),
                           R("Life-safety requirements for the shell", "medium", "fire-sprinkler", "", "Are code-required changes identified?")],
    },
    {
        "project_type": "ground-up-retail", "aliases": ["ground up retail", "ground-up", "retail ground-up", "new retail building", "pad building", "strip center"], "version": "1.0", "status": "seed",
        "building_type_band": "retail strip", "default_class": 5, "schedule_range_days": {"low": 180, "target": 270, "high": 400},
        "typical_trades": ["site-civil", "concrete-slab", "structural", "masonry", "roofing-envelope", "storefront-openings", "plumbing", "hvac", "electrical", "fire-sprinkler", "fire-alarm", "framing-drywall", "ceiling", "paint-finish", "general-conditions"],
        "intake_fields": {"gross_sf": {"required": True}, "lot_sf": {"default_ratio_of_gross": 4.0, "note": "site area assumed 4 × building area"},
                          "storefront_lf": {"default_ratio_of_gross": 0.02, "note": "storefront length assumed 2% of gross SF in LF"}, "restroom_count": {"default": 2, "note": "two restrooms assumed"}},
        "general_conditions": GC_GU,
        "assemblies": [
            A("31-site-earthwork-pad", "site-civil", "Building pad cut/fill, grading and erosion control (per SF of lot)", "SF", "lot_sf", 1.0, 1.50, 2.50, 4.50, 0.4),
            A("32-paving-parking", "site-civil", "Asphalt parking, curbs, striping and walks (per SF of lot outside building)", "SF", "lot_sf", 0.6, 5.50, 8.00, 12.00, 0.4),
            A("33-site-utilities-ls", "site-civil", "Site utilities to 5 ft outside building (water, sanitary, storm) — allowance-type", "LS", "each", 1.0, 60000.00, 110000.00, 190000.00, 0.3),
            A("03-foundation-sog-retail", "concrete-slab", "Spread and continuous footings, 5in slab on grade with vapor barrier (per SF)", "SF", "gross_sf", 1.0, 11.00, 16.00, 24.00, 0.5, 0.35),
            A("05-steel-joist-deck-retail", "structural", "Steel columns, beams, joists and deck (per SF)", "SF", "gross_sf", 1.0, 16.00, 24.00, 36.00),
            A("04-cmu-brick-exterior", "masonry", "8in CMU exterior walls with brick veneer at front (per LF of perimeter, 20 ft high)", "LF", "perimeter_lf", 1.0, 520.00, 760.00, 1100.00),
            A("07-tpo-roof-retail", "roofing-envelope", "TPO roof over polyiso with coping and drains (per SF)", "SF", "gross_sf", 1.0, 11.00, 15.00, 22.00),
            A("08-storefront-per-lf", "storefront-openings", "Aluminum storefront with entrances (per LF, 10 ft high)", "LF", "storefront_lf", 1.0, 750.00, 1100.00, 1600.00),
            A("22-plumbing-retail-shell", "plumbing", "Domestic water, sanitary, restroom sets and roof drains (per SF)", "SF", "gross_sf", 1.0, 7.00, 11.00, 16.00),
            A("23-hvac-rtu-shell", "hvac", "Packaged RTUs with distribution (per SF)", "SF", "gross_sf", 1.0, 14.00, 20.00, 30.00),
            A("26-electrical-retail-shell", "electrical", "Service, gear, lighting and power (per SF)", "SF", "gross_sf", 1.0, 16.00, 24.00, 36.00),
            A("21-sprinkler-new-per-sf", "fire-sprinkler", "Wet-pipe sprinkler system design-build (per SF)", "SF", "gross_sf", 1.0, 3.50, 5.00, 7.50),
            A("28-fire-alarm-new", "fire-alarm", "Addressable fire alarm system", "LS", "each", 1.0, 12000.00, 20000.00, 35000.00, 0.4),
            A("09-interior-finish-shell", "framing-drywall", "Interior furring, drywall at exterior walls and restrooms (per SF)", "SF", "gross_sf", 1.0, 4.00, 6.50, 10.00),
            A("09-ceiling-act-ti", "ceiling", "ACT ceiling and grid in finished areas (per SF)", "SF", "gross_sf", 0.5, 4.00, 6.00, 9.00),
            A("09-paint-ti", "paint-finish", "Interior and exterior paint (per SF)", "SF", "gross_sf", 1.0, 2.00, 3.00, 4.50),
        ],
        "common_rfis": ["Are civil plans and the geotechnical report available?", "Are utilities (water, sanitary, storm, power, gas) confirmed at the property line?",
                        "Are fire lane and hydrant requirements confirmed?", "Is the structural system (steel, PEMB, tilt) decided?", "Are landscape and irrigation included?",
                        "Are utility company fees included or excluded?", "Are offsite improvements required?"],
        "common_exclusions": ["offsite improvements and utility company fees", "landscape and irrigation unless shown", "unsuitable soils and rock", "tenant finish-out beyond shell", "impact fees"],
        "risk_checklist": [R("Utility availability and capacity", "high", "site-civil", "offsite improvements and utility company fees", "Are utilities confirmed at the property line?"),
                           R("Unsuitable soils / geotech", "high", "concrete-slab", "unsuitable soils and rock", "Is the geotechnical report available?"),
                           R("Fire lane and hydrant requirements", "high", "site-civil", "", "Are fire lane and hydrant requirements confirmed?"),
                           R("Long-lead steel / PEMB", "medium", "structural", "", "Is the structural system decided?"),
                           R("Drainage and detention", "medium", "site-civil", "", "Is detention required?"),
                           R("Permit and platting delays", "medium", "general-conditions", "", "")],
    },
    {
        "project_type": "industrial-warehouse", "aliases": ["warehouse", "industrial", "distribution", "flex", "tilt-wall", "pemb", "shell building"], "version": "1.0", "status": "seed",
        "building_type_band": "tilt-wall industrial", "default_class": 5, "schedule_range_days": {"low": 210, "target": 300, "high": 450},
        "typical_trades": ["site-civil", "concrete-slab", "structural", "roofing-envelope", "doors-hardware", "fire-sprinkler", "electrical", "hvac", "plumbing", "framing-drywall", "paint-finish", "general-conditions"],
        "intake_fields": {"gross_sf": {"required": True}, "office_sf": {"default_ratio_of_gross": 0.10, "note": "office finish-out assumed 10% of gross"},
                          "dock_doors": {"default_ratio_of_gross": 0.0002, "note": "one dock position per 5,000 SF assumed"}, "clear_height_ft": {"default": 28, "note": "28 ft clear assumed"},
                          "lot_sf": {"default_ratio_of_gross": 3.0, "note": "site area assumed 3 × building area"}, "esfr": {"default": 1, "note": "ESFR sprinklers assumed (1 = yes)"}},
        "general_conditions": GC_GU,
        "assemblies": [
            A("31-site-earthwork-pad", "site-civil", "Pad cut/fill, grading and erosion control (per SF of lot)", "SF", "lot_sf", 1.0, 1.50, 2.50, 4.50, 0.4),
            A("32-paving-truck-court", "site-civil", "Concrete truck court, asphalt auto parking, curbs (per SF of lot outside building)", "SF", "lot_sf", 0.55, 6.00, 9.00, 14.00, 0.4),
            A("33-site-utilities-ls", "site-civil", "Site utilities to 5 ft outside building — allowance-type", "LS", "each", 1.0, 80000.00, 150000.00, 260000.00, 0.3),
            A("03-slab-6in-warehouse", "concrete-slab", "6in slab on grade with joints and sealer (per SF)", "SF", "gross_sf", 1.0, 6.50, 9.00, 13.00, 0.5, 0.35),
            A("03-tilt-wall-per-sf", "concrete-slab", "Tilt-wall panels cast, erected and painted (per SF of building, 28 ft clear)", "SF", "gross_sf", 1.0, 20.00, 28.00, 40.00, 0.5, 0.25),
            A("05-steel-joist-deck-warehouse", "structural", "Steel columns, girders, joists and deck (per SF)", "SF", "gross_sf", 1.0, 13.00, 19.00, 28.00),
            A("07-tpo-roof-warehouse", "roofing-envelope", "TPO roof over polyiso with drains and skylights (per SF)", "SF", "gross_sf", 1.0, 9.00, 13.00, 19.00),
            A("08-dock-position", "doors-hardware", "Dock door, leveler, seal and bumpers per position", "EA", "dock_doors", 1.0, 14000.00, 20000.00, 30000.00),
            A("21-esfr-per-sf", "fire-sprinkler", "ESFR sprinkler system design-build with pump if required (per SF)", "SF", "gross_sf", 1.0, 3.50, 5.00, 8.00),
            A("26-electrical-warehouse", "electrical", "Service, gear, high-bay lighting, dock power (per SF)", "SF", "gross_sf", 1.0, 7.00, 10.50, 16.00),
            A("23-hvac-warehouse-ventilation", "hvac", "Warehouse ventilation and unit heaters, office RTUs (per SF)", "SF", "gross_sf", 1.0, 3.50, 5.50, 9.00),
            A("22-plumbing-warehouse", "plumbing", "Restrooms, hose bibbs, roof drains (per SF)", "SF", "gross_sf", 1.0, 2.50, 4.00, 6.50),
            A("09-office-finish-out", "framing-drywall", "Office finish-out (partitions, ceilings, flooring, doors) per SF of office", "SF", "office_sf", 1.0, 65.00, 95.00, 140.00),
            A("09-paint-ti", "paint-finish", "Interior paint at office and exposed CMU/tilt reveals (per SF)", "SF", "gross_sf", 1.0, 0.80, 1.30, 2.20),
        ],
        "common_rfis": ["Is the building PEMB, tilt-wall or steel frame?", "Are dock positions and door sizes final?", "Is ESFR required for the storage classification?",
                        "Are storage and racking plans available?", "Are power requirements known?", "Are office areas included?", "Is site/civil complete and is the geotech available?"],
        "common_exclusions": ["racking and material-handling equipment", "process power beyond the service shown", "offsite improvements and utility company fees", "unsuitable soils and rock", "impact fees"],
        "risk_checklist": [R("Fire protection classification (ESFR, pump)", "high", "fire-sprinkler", "fire pump unless required by the flow test", "Is ESFR required for the storage classification?"),
                           R("Slab specification vs racking loads", "high", "concrete-slab", "slab upgrades beyond 6in", "Are storage and racking plans available?"),
                           R("Electrical service size", "high", "electrical", "process power beyond the service shown", "Are power requirements known?"),
                           R("Long-lead steel and tilt panel sub capacity", "medium", "structural", "", "Is the structural system decided?"),
                           R("Drainage and detention", "medium", "site-civil", "", ""),
                           R("Utility availability", "medium", "site-civil", "offsite improvements and utility company fees", "Are utilities confirmed?")],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for pb in PLAYBOOKS:
        p = OUT / f"{pb['project_type']}.yaml"
        header = ("# Project-type playbook — SEED (status: seed). Every low/target/high is a national-average PLACEHOLDER\n"
                  "# marked [to load]; replace with the company's buyout history and set status: approved (approved_by, date).\n")
        p.write_text(header + yaml.safe_dump(pb, sort_keys=False, allow_unicode=True, width=140), encoding="utf-8")
        print("wrote", p.name, f"({len(pb['assemblies'])} assemblies, {len(pb['risk_checklist'])} risks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
