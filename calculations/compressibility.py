def oil_compressibility(bo: float, bo2: float, bo1: float, p2: float, p1: float) -> float:
    if bo == 0:
        raise ValueError("bo must be non-zero")
    if p2 == p1:
        raise ValueError("p2 and p1 must be different")
    co = -(1.0 / bo) * ((bo2 - bo1) / (p2 - p1))
    return co
