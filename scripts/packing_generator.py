#!/usr/bin/env python3
"""
Tourism Buddy — Smart Packing List Generator
Generates customized packing lists based on destination, weather, activities, and trip style.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class TripProfile:
    destination: str
    climate: str  # tropical, temperate, cold, desert, humid
    season: str  # summer, winter, spring, autumn, rainy
    duration_days: int
    activities: List[str] = field(default_factory=list)  # hiking, beach, business, temple, nightlife
    style: str = "standard"  # backpacker, standard, luxury, business
    has_kids: bool = False
    accessibility_needs: bool = False
    laundry_available: bool = False


VALID_CLIMATES = ["tropical", "cold", "desert", "temperate", "humid"]
VALID_ACTIVITIES = ["hiking", "beach", "business", "temple", "nightlife", "photography", "winter_sports"]
VALID_STYLES = ["backpacker", "standard", "luxury", "business"]


# Base essentials every trip needs
ESSENTIALS = {
    "documents": [
        "Passport (check 6-month validity!)",
        "Visa / e-visa printout",
        "Travel insurance documents",
        "Hotel booking confirmations",
        "Flight tickets / e-tickets",
        "Emergency contact card",
        "Copies of all documents (digital in cloud + paper separate from originals)",
    ],
    "money": [
        "Credit card (notify bank of travel!)",
        "Backup debit card (different bank)",
        "Small amount of local currency for arrival",
        "Money belt or hidden pouch",
    ],
    "tech": [
        "Phone + charger",
        "Power adapter (check outlet type!)",
        "Portable battery pack",
        "Headphones / earbuds",
    ],
    "health": [
        "Prescription medications (in original packaging)",
        "Basic first aid kit",
        "Hand sanitizer",
        "Face masks",
        "Insect repellent",
        "Sunscreen SPF 50+",
        "Any required vaccination cards",
    ],
    "comfort": [
        "Reusable water bottle",
        "Travel pillow (for long flights)",
        "Eye mask + earplugs",
        "Ziplock bags (multiple sizes)",
        "Small padlock",
    ],
}

# Climate-specific additions
CLIMATE_ITEMS = {
    "tropical": [
        "Lightweight breathable clothing",
        "Quick-dry underwear",
        "Waterproof phone case",
        "Umbrella / compact rain jacket",
        "Anti-chafe balm",
        "Reef-safe sunscreen",
        "Mosquito net (if rural areas)",
    ],
    "cold": [
        "Thermal base layers",
        "Insulated jacket / down jacket",
        "Warm hat + gloves + scarf",
        "Warm socks (wool/merino)",
        "Lip balm (cold weather cracks lips)",
        "Hand/toe warmers",
        "Waterproof boots",
    ],
    "desert": [
        "Sun hat with wide brim",
        "Lightweight long sleeves (sun protection)",
        "Scarf/shemagh (sand/sun protection)",
        "Electrolyte packets",
        "Eye drops (dry air)",
        "Closed-toe breathable shoes",
    ],
    "temperate": [
        "Layers (temperatures fluctuate)",
        "Light jacket",
        "Comfortable walking shoes",
        "Compact umbrella",
    ],
    "humid": [
        "Moisture-wicking clothing",
        "Anti-humidity hair products",
        "Extra underwear (you'll sweat)",
        "Talcum powder / anti-chafe",
        "Waterproof bag for electronics",
    ],
}

# Activity-specific additions
ACTIVITY_ITEMS = {
    "hiking": [
        "Hiking boots (broken in!)",
        "Hiking socks (wool blend)",
        "Daypack / backpack",
        "Trekking poles (if serious hikes)",
        "Trail snacks",
        "Water purification tablets",
        "Blister patches",
    ],
    "beach": [
        "Swimsuit(s)",
        "Beach towel (microfiber = packable)",
        "Flip flops / water shoes",
        "Snorkel gear (or rent locally)",
        "After-sun lotion",
        "Waterproof phone pouch",
        "Beach bag",
    ],
    "business": [
        "Business suits / formal attire",
        "Dress shoes",
        "Laptop + charger",
        "Business cards",
        "Wrinkle-release spray",
        "Portable steamer",
    ],
    "temple": [
        "Long pants / skirt (knee-covering)",
        "Shirts that cover shoulders",
        "Scarf / shawl (for covering)",
        "Slip-on shoes (easy temple removal)",
        "Socks (temple floors can be cold/dirty)",
    ],
    "nightlife": [
        "Going-out outfit",
        "Comfortable dance shoes",
        "Small crossbody bag (keep close)",
        "Minimal jewelry (less theft risk)",
    ],
    "photography": [
        "Camera + lenses",
        "Extra SD cards + batteries",
        "Tripod (compact travel version)",
        "Lens cleaning kit",
        "Camera rain cover",
        "Drone (check local laws!)",
    ],
    "winter_sports": [
        "Ski/snowboard gear (or rent list)",
        "Goggles",
        "Balaclava / neck gaiter",
        "UV lip balm",
        "Hand warmers",
        "Moisture-wicking base layers",
    ],
}

# Style modifications
STYLE_MODS = {
    "backpacker": {
        "add": [
            "Quick-dry travel towel",
            "Headlamp",
            "Carabiners",
            "Dry bags",
            "Hostel sheet liner / sleeping bag",
            "Combination lock for lockers",
            "Laundry soap sheets",
            "Collapsible utensils",
        ],
        "remove_hint": "Pack light! Aim for carry-on only. Wear your heaviest items on the plane.",
    },
    "luxury": {
        "add": [
            "Nice dinner outfit(s)",
            "Jewelry / accessories",
            "Travel-size luxury toiletries",
            "Silk sleep mask",
            "Cashmere travel blanket",
        ],
        "remove_hint": "Hotels will provide most toiletries. Focus on style items.",
    },
    "business": {
        "add": [
            "Portfolio / briefcase",
            "Business casual extras",
            "Laptop bag",
            "Presentation clicker",
        ],
        "remove_hint": "Keep leisure items minimal. Hotels usually offer laundry service.",
    },
}

# Family additions
FAMILY_ITEMS = [
    "Kid snacks (lots of them)",
    "Entertainment for travel (tablet, coloring books, small toys)",
    "Kid medications (fever reducer, anti-nausea)",
    "Stroller (if toddler) — check airline policy",
    "Car seat (if road trip)",
    "Baby carrier / sling",
    "Wet wipes (industrial quantities)",
    "Change of clothes in carry-on (for spills)",
    "Favorite stuffed animal / comfort item",
    "Night light (plug-in or battery)",
]

# Accessibility additions
ACCESSIBILITY_ITEMS = [
    "Mobility aids (wheelchair, cane, walker)",
    "Accessible transport booking confirmations",
    "Medical documentation / disability card",
    "Extra medication supply (in case of delays)",
    "Comfort cushion for long flights/drives",
    "Portable ramp (if needed)",
    "Emergency medical alert bracelet",
]


def generate_packing_list(profile: TripProfile) -> dict:
    """Generate a complete packing list based on trip profile.

    Args:
        profile: A TripProfile with trip details.

    Returns:
        dict with sections, tips, clothing_quantity, dont_pack, and warnings.
    """
    result = {
        "trip_info": {
            "destination": profile.destination,
            "climate": profile.climate,
            "duration": f"{profile.duration_days} days",
            "style": profile.style,
            "activities": profile.activities,
        },
        "sections": {},
        "tips": [],
        "dont_pack": [],
        "warnings": [],  # User-facing warnings for invalid inputs
    }

    # Validate climate with user-friendly warning
    if profile.climate not in VALID_CLIMATES:
        result["warnings"].append(
            f"Unknown climate '{profile.climate}' — using 'temperate' defaults. "
            f"Valid options: {', '.join(VALID_CLIMATES)}"
        )

    # Validate activities with user-friendly warning
    invalid_activities = [a for a in profile.activities if a not in VALID_ACTIVITIES]
    if invalid_activities:
        result["warnings"].append(
            f"Unknown activities ignored: {', '.join(invalid_activities)}. "
            f"Valid options: {', '.join(VALID_ACTIVITIES)}"
        )

    # Validate style
    if profile.style not in VALID_STYLES:
        result["warnings"].append(
            f"Unknown style '{profile.style}' — using 'standard'. "
            f"Valid options: {', '.join(VALID_STYLES)}"
        )

    # Validate duration
    if profile.duration_days <= 0:
        raise ValueError("duration_days must be at least 1.")

    # 1. Essentials (always included)
    for section, items in ESSENTIALS.items():
        result["sections"][f"essentials_{section}"] = items.copy()

    # 2. Climate-specific
    climate_items = CLIMATE_ITEMS.get(profile.climate, CLIMATE_ITEMS["temperate"])
    result["sections"]["climate_clothing"] = climate_items.copy()

    # 3. Activity-specific (only valid activities)
    for activity in profile.activities:
        if activity in ACTIVITY_ITEMS:
            result["sections"][f"activity_{activity}"] = ACTIVITY_ITEMS[activity].copy()

    # 4. Style modifications
    if profile.style in STYLE_MODS:
        mod = STYLE_MODS[profile.style]
        result["sections"][f"style_{profile.style}"] = mod["add"].copy()
        result["tips"].append(mod["remove_hint"])

    # 5. Family items
    if profile.has_kids:
        result["sections"]["family_kids"] = FAMILY_ITEMS.copy()

    # 6. Accessibility items
    if profile.accessibility_needs:
        result["sections"]["accessibility"] = ACCESSIBILITY_ITEMS.copy()

    # 7. Clothing quantity calculator
    LAUNDRY_CYCLE_DAYS = 4  # Assume you can do laundry every 4 days
    MAX_PACK_DAYS = 7       # No need to pack more than 7 days even for long trips

    if profile.laundry_available:
        clothing_days = min(profile.duration_days, LAUNDRY_CYCLE_DAYS)
        result["tips"].append(
            f"Laundry available! Pack for {clothing_days} days and wash every ~{LAUNDRY_CYCLE_DAYS} days."
        )
    else:
        clothing_days = min(profile.duration_days, MAX_PACK_DAYS)
        if profile.duration_days > MAX_PACK_DAYS:
            result["tips"].append(
                f"Long trip ({profile.duration_days} days) — pack {clothing_days} days of clothing. "
                f"Consider using hotel laundry services or finding a laundromat."
            )
        else:
            result["tips"].append(f"Pack {clothing_days} days of clothing.")

    result["clothing_quantity"] = {
        "underwear": clothing_days + 1,  # +1 buffer
        "socks": clothing_days + 1,
        "t_shirts_tops": clothing_days,
        "pants_shorts": max(clothing_days // 2, 2),
        "sleepwear": min(2, profile.duration_days),
    }

    # 8. Don't pack list
    result["dont_pack"] = [
        "Valuables you'd cry over losing",
        "Full-size toiletries (buy locally or use hotel's)",
        "Too many 'just in case' outfits",
        "Hardcover books (use e-reader)",
        "Expensive jewelry (theft risk)",
        "Prohibited items (check destination laws!)",
    ]

    # 9. Smart tips based on duration
    if profile.duration_days <= 3:
        result["tips"].append("Short trip — consider carry-on only for faster airport transit.")
    elif profile.duration_days >= 14:
        result["tips"].append("Extended trip — pack versatile mix-and-match pieces.")

    return result


def format_checklist(packing_list: dict) -> str:
    """Format packing list as a markdown checklist."""
    lines = [
        f"# PACKING LIST — {packing_list['trip_info']['destination']}",
        f"**{packing_list['trip_info']['duration']}** | "
        f"**{packing_list['trip_info']['climate'].title()}** | "
        f"**{packing_list['trip_info']['style'].title()} Style**",
    ]

    if packing_list['trip_info']['activities']:
        lines.append(f"Activities: {', '.join(packing_list['trip_info']['activities'])}")
    lines.append("")

    # Show warnings if any
    if packing_list.get("warnings"):
        lines.append("## Warnings")
        for w in packing_list["warnings"]:
            lines.append(f"- NOTE: {w}")
        lines.append("")

    section_names = {
        "essentials_documents": "Documents & ID",
        "essentials_money": "Money & Cards",
        "essentials_tech": "Tech & Gadgets",
        "essentials_health": "Health & Medicine",
        "essentials_comfort": "Comfort Items",
        "climate_clothing": "Climate-Appropriate Clothing",
        "family_kids": "Family & Kids",
        "accessibility": "Accessibility Items",
    }

    for section_key, items in packing_list["sections"].items():
        title = section_names.get(section_key, section_key.replace('_', ' ').title())
        lines.append(f"\n## {title}")
        for item in items:
            lines.append(f"- [ ] {item}")

    # Clothing quantities
    if "clothing_quantity" in packing_list:
        lines.append("\n## Clothing Quantities")
        for item, qty in packing_list["clothing_quantity"].items():
            lines.append(f"- [ ] {item.replace('_', ' ').title()}: **{qty}**")

    # Tips
    if packing_list["tips"]:
        lines.append("\n## Packing Tips")
        for tip in packing_list["tips"]:
            lines.append(f"- {tip}")

    # Don't pack
    if packing_list["dont_pack"]:
        lines.append("\n## DON'T Pack")
        for item in packing_list["dont_pack"]:
            lines.append(f"- {item}")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("Tourism Buddy — Packing List Generator")
        print("\nUsage:")
        print("  python packing_generator.py                           demo: Bali 10 days")
        print("  python packing_generator.py <dest> <climate> <days> [activities...]")
        print(f"\nClimates: {', '.join(VALID_CLIMATES)}")
        print(f"Activities: {', '.join(VALID_ACTIVITIES)}")
        print(f"Styles: {', '.join(VALID_STYLES)}")
        print("\nExamples:")
        print("  python packing_generator.py Iceland cold 7 hiking photography")
        print("  python packing_generator.py Bangkok tropical 5 temple nightlife")
        sys.exit(0)

    if len(sys.argv) >= 4:
        dest = sys.argv[1]
        climate = sys.argv[2]
        try:
            days = int(sys.argv[3])
        except ValueError:
            print(f"Invalid duration '{sys.argv[3]}' — must be an integer.")
            sys.exit(1)
        activities = sys.argv[4:] if len(sys.argv) > 4 else []
        profile = TripProfile(
            destination=dest,
            climate=climate,
            season="any",
            duration_days=days,
            activities=activities,
            style="standard",
        )
    else:
        # Default demo: tropical beach + temple trip
        profile = TripProfile(
            destination="Bali, Indonesia",
            climate="tropical",
            season="summer",
            duration_days=10,
            activities=["beach", "temple", "hiking", "photography"],
            style="standard",
            has_kids=False,
            laundry_available=True,
        )

    packing_list = generate_packing_list(profile)
    print(format_checklist(packing_list))
