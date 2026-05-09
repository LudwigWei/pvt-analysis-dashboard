from __future__ import annotations


def classify_fluid(api: float, gor: float) -> dict:
    if gor > 100000:
        return {
            "name": "Dry Gas",
            "desc": "Non-condensable gas reservoir. No liquid production at surface conditions.",
        }
    if gor > 50000:
        return {
            "name": "Wet Gas",
            "desc": "Gas with minor surface condensate. API typically above 60°.",
        }
    if gor > 3300:
        return {
            "name": "Gas Condensate / Retrograde Gas",
            "desc": "Rich gas system. Liquid retrograde condensation occurs as pressure drops below dew point.",
        }
    if gor > 2000:
        return {
            "name": "Near-Critical / Volatile Oil",
            "desc": "High-shrinkage oil near the critical point. Properties are very sensitive to pressure changes.",
        }
    if api >= 40:
        return {
            "name": "Black Oil — Light Crude",
            "desc": "Light crude oil. Low viscosity, high API gravity, good mobility.",
        }
    if api >= 25:
        return {
            "name": "Black Oil — Medium Crude",
            "desc": "Medium gravity crude oil. Solution gas drive commonly dominant.",
        }

    return {
        "name": "Heavy Oil",
        "desc": "Low API gravity, high viscosity crude. May require enhanced recovery methods.",
    }
