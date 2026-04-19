#!/usr/bin/env python3
"""
Tourism Buddy — Budget Tracker
Tracks trip expenses, categorizes spending, and provides budget alerts.
"""

import json
import os
import uuid
import re
from datetime import datetime, date
from pathlib import Path
from typing import Optional, List, Dict

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

VALID_CATEGORIES = [
    "flights", "accommodation", "food", "activities",
    "transport", "shopping", "emergency", "other",
]


def _validate_date(date_str: str, field_name: str = "date") -> str:
    """Validate and return a date string in YYYY-MM-DD format."""
    if not isinstance(date_str, str):
        raise TypeError(f"{field_name} must be a string, got {type(date_str).__name__}")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError(
            f"Invalid {field_name}: '{date_str}'. Use YYYY-MM-DD format (e.g., '2026-05-01')."
        )


def _validate_amount(amount: float, field_name: str = "amount") -> float:
    """Validate that amount is a positive number."""
    if not isinstance(amount, (int, float)):
        raise TypeError(f"{field_name} must be a number, got {type(amount).__name__}")
    if amount < 0:
        raise ValueError(f"{field_name} cannot be negative: {amount}")
    return float(amount)


def get_trip_file(trip_name: str) -> Path:
    if not isinstance(trip_name, str) or not trip_name.strip():
        raise ValueError("trip_name must be a non-empty string.")
    safe_name = re.sub(r'[^\w\-]', '_', trip_name.lower().strip())
    return DATA_DIR / f"trip_{safe_name}.json"


def create_trip(
    trip_name: str,
    destination: str,
    start_date: str,
    end_date: str,
    total_budget: float,
    currency: str = "USD",
    budget_breakdown: Optional[dict] = None,
) -> dict:
    """Create a new trip with budget allocation.

    Args:
        trip_name: Unique name for this trip.
        destination: Where you're going.
        start_date: Trip start date (YYYY-MM-DD).
        end_date: Trip end date (YYYY-MM-DD).
        total_budget: Total budget amount (must be > 0).
        currency: Currency code (default: USD).
        budget_breakdown: Custom category percentages (must sum to ~1.0).

    Returns:
        dict: The created trip data.

    Raises:
        ValueError: If dates are invalid or budget is not positive.
    """
    start_date = _validate_date(start_date, "start_date")
    end_date = _validate_date(end_date, "end_date")
    total_budget = _validate_amount(total_budget, "total_budget")

    if total_budget <= 0:
        raise ValueError("total_budget must be greater than 0.")

    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
    if end_dt < start_dt:
        raise ValueError(f"end_date ({end_date}) cannot be before start_date ({start_date}).")

    default_breakdown = {
        "flights": 0.30,
        "accommodation": 0.25,
        "food": 0.20,
        "activities": 0.10,
        "transport": 0.08,
        "shopping": 0.05,
        "emergency": 0.02,
    }
    breakdown = budget_breakdown or default_breakdown

    # Validate breakdown sums to roughly 1.0
    total_pct = sum(breakdown.values())
    if not (0.95 <= total_pct <= 1.05):
        raise ValueError(
            f"budget_breakdown percentages sum to {total_pct:.2f}, should be ~1.0"
        )

    trip = {
        "name": trip_name,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "total_budget": total_budget,
        "currency": currency,
        "budget_breakdown": {
            cat: round(total_budget * pct, 2) for cat, pct in breakdown.items()
        },
        "expenses": [],
        "created_at": datetime.now().isoformat(),
    }

    filepath = get_trip_file(trip_name)
    filepath.write_text(json.dumps(trip, indent=2, ensure_ascii=False), encoding="utf-8")
    return trip


def load_trip(trip_name: str) -> dict:
    """Load trip data from file."""
    filepath = get_trip_file(trip_name)
    if not filepath.exists():
        raise FileNotFoundError(f"Trip '{trip_name}' not found. Create it first with create_trip().")
    return json.loads(filepath.read_text(encoding="utf-8"))


def list_trips() -> List[dict]:
    """List all saved trips with basic info."""
    trips = []
    for f in DATA_DIR.glob("trip_*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            total_spent = sum(e["amount"] for e in data.get("expenses", []))
            trips.append({
                "name": data["name"],
                "destination": data["destination"],
                "budget": data["total_budget"],
                "spent": round(total_spent, 2),
                "currency": data["currency"],
                "dates": f"{data['start_date']} → {data['end_date']}",
            })
        except (json.JSONDecodeError, KeyError):
            continue
    return trips


def add_expense(
    trip_name: str,
    amount: float,
    category: str,
    description: str,
    expense_date: Optional[str] = None,
    local_amount: Optional[float] = None,
    local_currency: Optional[str] = None,
) -> dict:
    """Add an expense to a trip.

    Args:
        trip_name: Name of the trip.
        amount: Expense amount in trip currency (must be > 0).
        category: Expense category (flights, accommodation, food, activities,
                  transport, shopping, emergency, other).
        description: What this expense was for.
        expense_date: Date of expense (YYYY-MM-DD, defaults to today).
        local_amount: Optional amount in local currency.
        local_currency: Optional local currency code.

    Returns:
        dict with 'expense' and 'alerts' keys.
    """
    amount = _validate_amount(amount, "amount")
    if amount <= 0:
        raise ValueError("Expense amount must be greater than 0.")

    category = category.lower().strip()
    if category not in VALID_CATEGORIES:
        raise ValueError(
            f"Unknown category '{category}'. Valid: {', '.join(VALID_CATEGORIES)}"
        )

    if expense_date:
        expense_date = _validate_date(expense_date, "expense_date")
    else:
        expense_date = date.today().isoformat()

    filepath = get_trip_file(trip_name)
    if not filepath.exists():
        raise FileNotFoundError(f"Trip '{trip_name}' not found. Create it first.")

    trip = json.loads(filepath.read_text(encoding="utf-8"))

    # Use UUID for robust expense ID (not fragile len+1)
    expense = {
        "id": str(uuid.uuid4())[:8],
        "amount": amount,
        "category": category,
        "description": description,
        "date": expense_date,
        "timestamp": datetime.now().isoformat(),
    }
    if local_amount is not None and local_currency:
        expense["local_amount"] = _validate_amount(local_amount, "local_amount")
        expense["local_currency"] = local_currency

    trip["expenses"].append(expense)
    filepath.write_text(json.dumps(trip, indent=2, ensure_ascii=False), encoding="utf-8")

    # Check budget alerts
    alerts = check_budget_alerts(trip)
    return {"expense": expense, "alerts": alerts}


def delete_expense(trip_name: str, expense_id: str) -> bool:
    """Delete an expense by its ID."""
    filepath = get_trip_file(trip_name)
    if not filepath.exists():
        raise FileNotFoundError(f"Trip '{trip_name}' not found.")

    trip = json.loads(filepath.read_text(encoding="utf-8"))
    original_len = len(trip["expenses"])
    trip["expenses"] = [e for e in trip["expenses"] if str(e["id"]) != str(expense_id)]

    if len(trip["expenses"]) == original_len:
        raise ValueError(f"Expense ID '{expense_id}' not found in trip '{trip_name}'.")

    filepath.write_text(json.dumps(trip, indent=2, ensure_ascii=False), encoding="utf-8")
    return True


def get_summary(trip_name: str) -> dict:
    """Get spending summary for a trip."""
    trip = load_trip(trip_name)

    by_category: Dict[str, float] = {}
    by_date: Dict[str, float] = {}
    total_spent = 0.0

    for exp in trip["expenses"]:
        cat = exp["category"]
        by_category[cat] = by_category.get(cat, 0) + exp["amount"]
        d = exp["date"]
        by_date[d] = by_date.get(d, 0) + exp["amount"]
        total_spent += exp["amount"]

    remaining = trip["total_budget"] - total_spent

    # Safe percent calculation (avoid division by zero)
    if trip["total_budget"] > 0:
        percent_spent = round((total_spent / trip["total_budget"]) * 100, 1)
    else:
        percent_spent = 0.0

    # Calculate days remaining
    daily_budget_remaining = None
    days_left = None
    try:
        end = datetime.strptime(trip["end_date"], "%Y-%m-%d").date()
        today = date.today()
        days_left = max((end - today).days, 0)
        if days_left > 0 and remaining > 0:
            daily_budget_remaining = round(remaining / days_left, 2)
    except ValueError:
        pass

    return {
        "trip_name": trip["name"],
        "destination": trip["destination"],
        "currency": trip["currency"],
        "total_budget": trip["total_budget"],
        "total_spent": round(total_spent, 2),
        "remaining": round(remaining, 2),
        "percent_spent": percent_spent,
        "by_category": {k: round(v, 2) for k, v in by_category.items()},
        "by_date": dict(sorted(by_date.items())),
        "days_remaining": days_left,
        "suggested_daily_budget": daily_budget_remaining,
        "budget_allocation": trip["budget_breakdown"],
        "expense_count": len(trip["expenses"]),
    }


def check_budget_alerts(trip: dict) -> list:
    """Check for budget warnings."""
    alerts = []
    by_category: Dict[str, float] = {}
    total_spent = 0.0

    for exp in trip["expenses"]:
        cat = exp["category"]
        by_category[cat] = by_category.get(cat, 0) + exp["amount"]
        total_spent += exp["amount"]

    # Safe division — avoid ZeroDivisionError
    if trip["total_budget"] > 0:
        pct = (total_spent / trip["total_budget"]) * 100
        if pct >= 100:
            over = total_spent - trip["total_budget"]
            alerts.append(
                f"🔴 CRITICAL: Over budget by {trip['currency']} {over:,.2f}! "
                f"({pct:.0f}% of total budget)"
            )
        elif pct >= 90:
            alerts.append(f"🔴 CRITICAL: You've spent {pct:.0f}% of your total budget!")
        elif pct >= 75:
            alerts.append(f"🟡 WARNING: You've spent {pct:.0f}% of your total budget.")

    # Category alerts
    for cat, allocated in trip.get("budget_breakdown", {}).items():
        spent = by_category.get(cat, 0)
        if allocated > 0:
            cat_pct = (spent / allocated) * 100
            if cat_pct >= 100:
                over = spent - allocated
                alerts.append(
                    f"🔴 {cat.upper()}: Over budget by {trip['currency']} {over:.2f}!"
                )
            elif cat_pct >= 80:
                alerts.append(f"🟡 {cat.upper()}: {cat_pct:.0f}% of allocated budget used.")

    return alerts


def format_summary_table(summary: dict) -> str:
    """Format summary as a nice readable table."""
    cur = summary['currency']
    lines = [
        f"{'=' * 55}",
        f"  TRIP BUDGET REPORT — {summary['destination']}",
        f"{'=' * 55}",
        f"  Total Budget:  {cur} {summary['total_budget']:>10,.2f}",
        f"  Total Spent:   {cur} {summary['total_spent']:>10,.2f}",
        f"  Remaining:     {cur} {summary['remaining']:>10,.2f}",
        f"  Used: {summary['percent_spent']}%  |  Expenses: {summary.get('expense_count', '?')}",
        "",
    ]

    if summary.get("suggested_daily_budget"):
        lines.append(
            f"  Suggested daily budget ({summary['days_remaining']} days left): "
            f"{cur} {summary['suggested_daily_budget']:,.2f}"
        )
        lines.append("")

    lines.append(f"  {'Category':<15} {'Spent':>10} {'Budget':>10} {'%':>6}  Status")
    lines.append(f"  {'-' * 50}")

    for cat, allocated in summary["budget_allocation"].items():
        spent = summary["by_category"].get(cat, 0)
        pct = (spent / allocated * 100) if allocated > 0 else 0
        if pct >= 100:
            flag = " OVER"
        elif pct >= 80:
            flag = " WARN"
        else:
            flag = " OK"
        lines.append(
            f"  {cat:<15} {spent:>10,.2f} {allocated:>10,.2f} {pct:>5.0f}% {flag}"
        )

    if summary.get("by_date"):
        lines.append("")
        lines.append(f"  DAILY SPENDING:")
        lines.append(f"  {'-' * 30}")
        for d, amt in summary["by_date"].items():
            lines.append(f"  {d}  {cur} {amt:>10,.2f}")

    lines.append(f"\n{'=' * 55}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Demo — writes to a temp directory so your real data/ stays clean.
    import tempfile
    DATA_DIR = Path(tempfile.mkdtemp(prefix="tourism_buddy_demo_"))
    print(f"[demo] Using temp data dir: {DATA_DIR}\n")

    trip = create_trip(
        trip_name="Tokyo Demo",
        destination="Tokyo, Japan",
        start_date="2026-05-01",
        end_date="2026-05-08",
        total_budget=3000,
        currency="USD",
    )
    print(f"Created trip: {trip['name']}")

    add_expense("Tokyo Demo", 850, "flights", "Round trip LAX-NRT")
    add_expense("Tokyo Demo", 120, "accommodation", "Hotel night 1 - Shinjuku")
    add_expense("Tokyo Demo", 25, "food", "Ramen at Fuunji")
    add_expense("Tokyo Demo", 15, "transport", "Suica card charge")

    summary = get_summary("Tokyo Demo")
    print(format_summary_table(summary))

    print("\nAll demo trips:")
    for t in list_trips():
        print(f"  {t['name']} — {t['destination']} — {t['currency']} {t['spent']}/{t['budget']}")
