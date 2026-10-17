"""Generate synthetic healthcare member experience data for KPI dashboard."""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

REGIONS = ["Northeast", "Southeast", "Midwest", "Southwest", "West"]
CHANNELS = ["phone", "portal", "mobile_app", "email", "chat"]
CALL_REASONS = ["billing", "claims", "benefits", "enrollment", "pharmacy", "provider_search", "grievance"]

NUM_MEMBERS = 2000
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)


def generate_members():
    members = []
    for i in range(1, NUM_MEMBERS + 1):
        region = random.choice(REGIONS)
        age = random.randint(18, 85)
        plan_type = random.choices(
            ["HMO", "PPO", "EPO", "HDHP"],
            weights=[0.35, 0.30, 0.15, 0.20],
        )[0]
        tenure_months = random.randint(1, 120)
        members.append({
            "member_id": f"MBR-{i:05d}",
            "region": region,
            "age": age,
            "plan_type": plan_type,
            "tenure_months": tenure_months,
        })
    return pd.DataFrame(members)


def generate_interactions(members_df):
    rows = []
    current = START_DATE
    interaction_id = 0

    while current <= END_DATE:
        month = current.month
        # seasonal interaction volume (higher in Q1 and Q4)
        base_daily = 40 if month in [1, 2, 3, 10, 11, 12] else 30
        daily_count = np.random.poisson(base_daily)

        for _ in range(daily_count):
            interaction_id += 1
            member = members_df.sample(1).iloc[0]
            channel = random.choices(
                CHANNELS,
                weights=[0.35, 0.25, 0.20, 0.12, 0.08],
            )[0]
            reason = random.choice(CALL_REASONS)

            # satisfaction score (1-10), skewed by reason and channel
            base_sat = 7.0
            if reason == "grievance":
                base_sat -= 2.0
            elif reason == "billing":
                base_sat -= 1.0
            elif reason == "provider_search":
                base_sat += 0.5
            if channel in ["mobile_app", "portal"]:
                base_sat += 0.5
            sat_score = np.clip(np.random.normal(base_sat, 1.5), 1, 10)

            # handle time in minutes (phone only meaningful)
            handle_time = None
            if channel == "phone":
                ht_base = 8.0 if reason in ["grievance", "claims"] else 5.5
                handle_time = max(1.0, np.random.normal(ht_base, 2.5))

            resolved = random.random() < (0.72 if reason in ["grievance", "claims"] else 0.85)

            # NPS response (not everyone responds)
            nps_score = None
            if random.random() < 0.30:
                nps_base = 7 if sat_score > 6 else 4
                nps_score = int(np.clip(np.random.normal(nps_base, 2), 0, 10))

            # digital engagement flags
            used_portal = channel == "portal" or (random.random() < 0.40)
            used_mobile = channel == "mobile_app" or (random.random() < 0.25)
            submitted_claim_online = reason == "claims" and random.random() < 0.35

            # processing times (days)
            claim_processing_days = None
            if reason == "claims":
                claim_processing_days = max(1, int(np.random.normal(14, 5)))

            prior_auth_days = None
            if reason == "pharmacy":
                prior_auth_days = max(1, int(np.random.normal(5, 2)))

            rows.append({
                "interaction_id": f"INT-{interaction_id:06d}",
                "date": current.strftime("%Y-%m-%d"),
                "month": current.strftime("%Y-%m"),
                "member_id": member["member_id"],
                "region": member["region"],
                "plan_type": member["plan_type"],
                "age": member["age"],
                "tenure_months": member["tenure_months"],
                "channel": channel,
                "contact_reason": reason,
                "satisfaction_score": round(sat_score, 1),
                "nps_score": nps_score,
                "handle_time_minutes": round(handle_time, 1) if handle_time else None,
                "resolved_first_contact": resolved,
                "used_portal": used_portal,
                "used_mobile_app": used_mobile,
                "submitted_claim_online": submitted_claim_online,
                "claim_processing_days": claim_processing_days,
                "prior_auth_days": prior_auth_days,
            })

        current += timedelta(days=1)

    return pd.DataFrame(rows)


def generate_disenrollments(members_df):
    disenrolled = members_df.sample(frac=0.08, random_state=42).copy()
    disenrolled["disenroll_date"] = [
        (START_DATE + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d")
        for _ in range(len(disenrolled))
    ]
    disenrolled["disenroll_reason"] = [
        random.choice(["cost", "service_quality", "moved", "employer_change", "other"])
        for _ in range(len(disenrolled))
    ]
    disenrolled["voluntary"] = disenrolled["disenroll_reason"].isin(["cost", "service_quality"])
    return disenrolled[["member_id", "region", "disenroll_date", "disenroll_reason", "voluntary"]]


if __name__ == "__main__":
    print("Generating member data...")
    members = generate_members()

    print("Generating interactions...")
    interactions = generate_interactions(members)

    print("Generating disenrollments...")
    disenrollments = generate_disenrollments(members)

    output = interactions.copy()
    output.to_csv("data/member_experience_data.csv", index=False)
    disenrollments.to_csv("data/disenrollment_data.csv", index=False)
    members.to_csv("data/members.csv", index=False)

    print(f"\nGenerated {len(interactions):,} interactions for {NUM_MEMBERS:,} members")
    print(f"Disenrollments: {len(disenrollments)}")
    print(f"Date range: {interactions['date'].min()} to {interactions['date'].max()}")
    print(f"Regions: {interactions['region'].nunique()}")
    print("Files saved to data/")
