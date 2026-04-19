#!/usr/bin/env python3
"""
Tourism Buddy — Tourist Scam Database
Common scams by destination with descriptions and avoidance strategies.
"""

from typing import List, Optional

GLOBAL_SCAMS = [
    {
        "name": "Fake Taxi / Rigged Meter",
        "description": "Unlicensed taxis at airports/stations with no meter or a 'broken' meter. They charge 3-10x the normal rate.",
        "avoidance": "Only use official taxi stands, ride-hailing apps (Uber/Grab/Bolt), or pre-booked transfers. If using a taxi, insist on the meter. Know approximate cost beforehand.",
        "severity": "medium",
        "locations": ["worldwide"],
        "tags": ["transport", "airport"],
    },
    {
        "name": "Currency Confusion",
        "description": "Giving change in wrong currency, old/invalid bills, or bills of wrong denomination that look similar.",
        "avoidance": "Familiarize yourself with local currency before arrival. Count change carefully. Use a currency converter app. Pay by card when possible.",
        "severity": "medium",
        "locations": ["worldwide"],
        "tags": ["money", "shopping"],
    },
    {
        "name": "Free Bracelet / Rosemary Sprig",
        "description": "Someone puts a bracelet on your wrist or gives you a 'gift', then aggressively demands payment. Often works in teams — one distracts, others pickpocket.",
        "avoidance": "Firmly refuse. Keep hands in pockets near known scam areas. Say NO and walk away immediately. Don't let anyone touch you.",
        "severity": "low",
        "locations": ["Paris", "Rome", "Barcelona", "Madrid", "Milan"],
        "tags": ["street", "tourist-area"],
    },
    {
        "name": "Fake Police",
        "description": "People posing as plainclothes police ask to 'check your wallet' for counterfeit bills, then steal cash during the inspection.",
        "avoidance": "Real police rarely check wallets on the street. Ask for badge ID, suggest going to the nearest police station. Never hand over your wallet.",
        "severity": "high",
        "locations": ["Bogota", "Barcelona", "Prague"],
        "tags": ["street", "identity"],
    },
    {
        "name": "Broken Camera / Photo Request",
        "description": "Tourist asks you to take their photo, then 'drops' their camera. Claims you broke it and demands compensation. Or they grab YOUR phone and run.",
        "avoidance": "Be cautious with strangers' electronics. Decline politely. Hold phone with strap around wrist.",
        "severity": "medium",
        "locations": ["worldwide"],
        "tags": ["street", "tourist-area"],
    },
    {
        "name": "Closed Attraction Redirect",
        "description": "Touts near popular attractions claim 'it's closed today' (it's not) and offer to take you somewhere else — a shop or overpriced 'alternative' where they get commission.",
        "avoidance": "ALWAYS verify yourself. Walk to the entrance and check. Google current hours. Never trust strangers saying an attraction is closed.",
        "severity": "medium",
        "locations": ["Bangkok", "Delhi", "Istanbul", "Cairo", "Agra"],
        "tags": ["tourist-area", "shopping"],
    },
    {
        "name": "Gem / Carpet / Tailoring 'Investment' Scam",
        "description": "Friendly local befriends you, takes you to a 'special' gem/carpet shop, tells you items are worth 10x back home. They're actually worthless fakes.",
        "avoidance": "Never buy high-value items from people you just met. If it sounds too good to be true, it is. Research fair prices. Take 24 hours to decide.",
        "severity": "high",
        "locations": ["Bangkok", "Istanbul", "Jaipur", "Marrakech"],
        "tags": ["shopping", "trust"],
    },
    {
        "name": "WiFi Honeypot",
        "description": "Fake 'free WiFi' hotspots near tourist areas that intercept your data — passwords, banking info, personal data.",
        "avoidance": "Use a VPN. Don't connect to random open WiFi. Use your phone's hotspot or eSIM data. Never access banking on public WiFi.",
        "severity": "high",
        "locations": ["worldwide"],
        "tags": ["tech", "digital"],
    },
    {
        "name": "Motorbike Rental Damage Scam",
        "description": "Rent a scooter/motorbike; when you return it, owner claims you damaged it (pre-existing damage) and demands huge payment. They may keep your passport as 'deposit'.",
        "avoidance": "NEVER leave your passport as deposit. Photo/video the vehicle from all angles before renting. Use reputable rental companies. Check reviews.",
        "severity": "high",
        "locations": ["Bali", "Phuket", "Chiang Mai", "Hanoi", "Ho Chi Minh City"],
        "tags": ["transport", "rental"],
    },
    {
        "name": "Restaurant Bill Padding",
        "description": "Items you didn't order appear on the bill, or prices are higher than menu listed. 'Cover charge' or 'service fee' added sneakily.",
        "avoidance": "Check menu prices before ordering. Ask about cover charges upfront. Review bill carefully. Photograph the menu. Avoid restaurants with touts outside.",
        "severity": "medium",
        "locations": ["Venice", "Athens", "Istanbul", "tourist areas worldwide"],
        "tags": ["food", "money"],
    },
    {
        "name": "ATM Skimming / DCC Scam",
        "description": "ATM reads your card data via hidden device. Or ATM offers 'helpful' currency conversion (DCC) at terrible rates — always adds 5-10% cost.",
        "avoidance": "Use ATMs inside banks, not standalone ones. Cover PIN entry. ALWAYS choose 'charge in local currency' (decline conversion). Check for loose card readers.",
        "severity": "high",
        "locations": ["worldwide"],
        "tags": ["money", "tech"],
    },
    {
        "name": "Tuk-Tuk / Rickshaw Tour Detour",
        "description": "Driver offers incredibly cheap city tour, but spends most of it at commission shops (tailors, jewelers) where they earn kickbacks.",
        "avoidance": "Agree on specific destinations before starting. If they stop at shops, decline to enter. Use ride-hailing apps for fair-price transport.",
        "severity": "low",
        "locations": ["Bangkok", "Delhi", "Cairo", "Siem Reap"],
        "tags": ["transport", "shopping"],
    },
    {
        "name": "Pickpocket Distraction Teams",
        "description": "Groups work together — one person distracts (petition, baby trick, bumping into you) while another steals your wallet/phone.",
        "avoidance": "Use a money belt under clothing. Keep phone in front pocket with hand on it. Be extra alert in crowded areas, metro, and tourist sites.",
        "severity": "high",
        "locations": ["Barcelona", "Rome", "Paris", "Naples", "Prague", "Lisbon"],
        "tags": ["street", "tourist-area"],
    },
    {
        "name": "Overpriced Boat / Island Tour",
        "description": "Booked a 'luxury' boat tour that turns out to be a crowded, overpriced, low-quality trip with hidden fees for snorkeling gear, lunch, etc.",
        "avoidance": "Book through your hotel or a reputable agency. Read recent reviews. Ask exactly what's included. Compare at least 3 providers.",
        "severity": "medium",
        "locations": ["Bali", "Phuket", "Halong Bay", "Cancun"],
        "tags": ["tour", "water"],
    },
]


def get_scams_for_destination(destination: str, severity: Optional[str] = None) -> List[dict]:
    """Get relevant scams for a destination.

    Args:
        destination: City or country name (case-insensitive).
        severity: Optional filter — 'high', 'medium', or 'low'.

    Returns:
        List of scam dictionaries relevant to the destination.
    """
    if not isinstance(destination, str) or not destination.strip():
        raise ValueError("destination must be a non-empty string.")

    destination_lower = destination.lower().strip()
    relevant = []

    for scam in GLOBAL_SCAMS:
        matched = False
        for loc in scam["locations"]:
            loc_lower = loc.lower()
            # Match: worldwide, or exact city/country match (word boundaries)
            if "worldwide" in loc_lower:
                matched = True
                break
            # Check if destination contains the location name or vice versa
            # Use word-level matching to reduce false positives
            if _location_match(destination_lower, loc_lower):
                matched = True
                break

        if matched:
            if severity and scam["severity"] != severity.lower():
                continue
            relevant.append(scam)

    # Sort by severity (high first)
    severity_order = {"high": 0, "medium": 1, "low": 2}
    relevant.sort(key=lambda s: severity_order.get(s["severity"], 3))

    return relevant


def _location_match(destination: str, location: str) -> bool:
    """Smart location matching that reduces false positives.

    Matches if:
    - Location words appear in destination (e.g., "Bangkok" in "Bangkok, Thailand")
    - Destination words appear in location (e.g., "Bali" found in "Bali")

    Does NOT match partial substrings (e.g., "Paris" won't match "comparison").
    """
    dest_words = set(destination.replace(",", " ").split())
    loc_words = set(location.replace(",", " ").split())

    # Check if any location word is in destination, or vice versa
    for loc_word in loc_words:
        if len(loc_word) < 3:
            continue  # Skip tiny words like "in", "of"
        for dest_word in dest_words:
            if len(dest_word) < 3:
                continue
            if loc_word == dest_word:
                return True
    return False


def get_scams_by_tag(tag: str) -> List[dict]:
    """Get scams filtered by tag (e.g., 'money', 'transport', 'street')."""
    tag_lower = tag.lower().strip()
    return [s for s in GLOBAL_SCAMS if tag_lower in s.get("tags", [])]


def get_all_tags() -> List[str]:
    """Return all available scam tags."""
    tags = set()
    for scam in GLOBAL_SCAMS:
        tags.update(scam.get("tags", []))
    return sorted(tags)


def format_scam_report(destination: str, severity: Optional[str] = None) -> str:
    """Format scam warnings for a destination.

    Args:
        destination: City or country name.
        severity: Optional filter — 'high', 'medium', or 'low'.

    Returns:
        Formatted markdown scam report.
    """
    if not isinstance(destination, str) or not destination.strip():
        return "Error: Please provide a valid destination name."

    scams = get_scams_for_destination(destination, severity)

    severity_emoji = {"high": "[HIGH]", "medium": "[MED]", "low": "[LOW]"}
    filter_note = f" (filtered: {severity} only)" if severity else ""

    lines = [
        f"# TOURIST SCAM ALERT — {destination}{filter_note}",
        f"Found {len(scams)} relevant scam warnings.",
        "",
    ]

    if not scams:
        lines.append("No specific scam warnings found for this destination.")
        lines.append("Always stay vigilant and follow general safety rules.")
        lines.append("")
    else:
        for i, scam in enumerate(scams, 1):
            badge = severity_emoji.get(scam["severity"], "[?]")
            lines.extend([
                f"## {i}. {badge} {scam['name']}",
                f"**Risk Level:** {scam['severity'].upper()}",
                f"**How it works:** {scam['description']}",
                f"**How to avoid:** {scam['avoidance']}",
                f"**Common in:** {', '.join(scam['locations'])}",
                "",
            ])

    lines.extend([
        "---",
        "## GENERAL SAFETY RULES",
        "1. If something feels off, trust your gut and walk away",
        "2. Keep valuables in a money belt under clothing",
        "3. Don't flash expensive electronics / jewelry",
        "4. Be extra cautious with anyone who approaches YOU first",
        "5. Research common scams BEFORE arriving at each destination",
        "6. Share your itinerary with someone back home",
        "7. Keep emergency numbers saved offline on your phone",
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Tourism Buddy — Scam Database")
        print(f"Tracking {len(GLOBAL_SCAMS)} scams across worldwide destinations.\n")
        print("Usage:")
        print("  python scam_database.py <destination>                 report for a city/country")
        print("  python scam_database.py <destination> <severity>      filter (high/medium/low)")
        print("  python scam_database.py --tag <tag>                   filter by tag")
        print("  python scam_database.py --tags                        list all tags\n")
        print("Examples:")
        print("  python scam_database.py Bangkok")
        print("  python scam_database.py Paris high")
        print("  python scam_database.py --tag transport")
        sys.exit(0)

    if sys.argv[1] == "--tags":
        print("Available tags:", ", ".join(get_all_tags()))
        sys.exit(0)

    if sys.argv[1] == "--tag" and len(sys.argv) >= 3:
        scams = get_scams_by_tag(sys.argv[2])
        print(f"Scams tagged '{sys.argv[2]}': {len(scams)}\n")
        for s in scams:
            print(f"- [{s['severity'].upper()}] {s['name']}")
            print(f"    {s['description']}")
            print()
        sys.exit(0)

    dest = sys.argv[1]
    severity = sys.argv[2] if len(sys.argv) > 2 else None
    print(format_scam_report(dest, severity))
