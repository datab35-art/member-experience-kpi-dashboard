"""KPI computation engine for member experience metrics."""

import pandas as pd
import numpy as np


def compute_csat(df, group_col=None):
    """Average satisfaction score (1-10 scale)."""
    if group_col:
        return df.groupby(group_col)["satisfaction_score"].mean()
    return df["satisfaction_score"].mean()


def compute_nps(df, group_col=None):
    """Net Promoter Score: % promoters (9-10) minus % detractors (0-6)."""
    nps_data = df.dropna(subset=["nps_score"])

    def _nps(series):
        promoters = (series >= 9).mean()
        detractors = (series <= 6).mean()
        return round((promoters - detractors) * 100, 1)

    if group_col:
        return nps_data.groupby(group_col)["nps_score"].apply(_nps)
    return _nps(nps_data["nps_score"])


def compute_fcr(df, group_col=None):
    """First Contact Resolution rate."""
    if group_col:
        return df.groupby(group_col)["resolved_first_contact"].mean()
    return df["resolved_first_contact"].mean()


def compute_avg_handle_time(df, group_col=None):
    """Average handle time for phone interactions."""
    phone = df[df["channel"] == "phone"].dropna(subset=["handle_time_minutes"])
    if group_col:
        return phone.groupby(group_col)["handle_time_minutes"].mean()
    return phone["handle_time_minutes"].mean()


def compute_abandonment_rate(df, group_col=None):
    """Simulated abandonment rate based on handle time (calls > 15 min proxy)."""
    phone = df[df["channel"] == "phone"].dropna(subset=["handle_time_minutes"])
    phone = phone.copy()
    phone["abandoned"] = phone["handle_time_minutes"] > 15

    if group_col:
        return phone.groupby(group_col)["abandoned"].mean()
    return phone["abandoned"].mean()


def compute_portal_adoption(df, group_col=None):
    """Percentage of interactions where member used portal."""
    if group_col:
        return df.groupby(group_col)["used_portal"].mean()
    return df["used_portal"].mean()


def compute_mobile_adoption(df, group_col=None):
    """Percentage of interactions where member used mobile app."""
    if group_col:
        return df.groupby(group_col)["used_mobile_app"].mean()
    return df["used_mobile_app"].mean()


def compute_online_claim_rate(df, group_col=None):
    """Percentage of claims submitted online."""
    claims = df[df["contact_reason"] == "claims"]
    if group_col:
        return claims.groupby(group_col)["submitted_claim_online"].mean()
    return claims["submitted_claim_online"].mean()


def compute_avg_claim_processing(df, group_col=None):
    """Average claim processing time in days."""
    claims = df.dropna(subset=["claim_processing_days"])
    if group_col:
        return claims.groupby(group_col)["claim_processing_days"].mean()
    return claims["claim_processing_days"].mean()


def compute_avg_prior_auth(df, group_col=None):
    """Average prior authorization turnaround in days."""
    pa = df.dropna(subset=["prior_auth_days"])
    if group_col:
        return pa.groupby(group_col)["prior_auth_days"].mean()
    return pa["prior_auth_days"].mean()


def compute_disenrollment_rate(disenrollments, total_members):
    """Overall disenrollment rate."""
    return len(disenrollments) / total_members


def compute_voluntary_churn_rate(disenrollments, total_members):
    """Voluntary churn (cost + service quality reasons)."""
    voluntary = disenrollments[disenrollments["voluntary"]]
    return len(voluntary) / total_members


def monthly_kpi_summary(df):
    """Compute all KPIs by month for trend analysis."""
    months = sorted(df["month"].unique())
    records = []

    for m in months:
        mdf = df[df["month"] == m]
        records.append({
            "month": m,
            "total_interactions": len(mdf),
            "csat": round(compute_csat(mdf), 2),
            "nps": compute_nps(mdf),
            "fcr": round(compute_fcr(mdf), 3),
            "avg_handle_time": round(compute_avg_handle_time(mdf), 1),
            "abandonment_rate": round(compute_abandonment_rate(mdf), 3),
            "portal_adoption": round(compute_portal_adoption(mdf), 3),
            "mobile_adoption": round(compute_mobile_adoption(mdf), 3),
            "online_claim_rate": round(compute_online_claim_rate(mdf), 3),
            "avg_claim_days": round(compute_avg_claim_processing(mdf), 1),
            "avg_prior_auth_days": round(compute_avg_prior_auth(mdf), 1),
        })

    return pd.DataFrame(records)


def regional_kpi_summary(df):
    """Compute all KPIs by region for benchmarking."""
    regions = sorted(df["region"].unique())
    records = []

    for r in regions:
        rdf = df[df["region"] == r]
        records.append({
            "region": r,
            "total_interactions": len(rdf),
            "csat": round(compute_csat(rdf), 2),
            "nps": compute_nps(rdf),
            "fcr": round(compute_fcr(rdf), 3),
            "avg_handle_time": round(compute_avg_handle_time(rdf), 1),
            "abandonment_rate": round(compute_abandonment_rate(rdf), 3),
            "portal_adoption": round(compute_portal_adoption(rdf), 3),
            "mobile_adoption": round(compute_mobile_adoption(rdf), 3),
        })

    return pd.DataFrame(records)
