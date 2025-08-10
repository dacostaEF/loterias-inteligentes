#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import math
import numpy as np
from datetime import datetime, date

def _to_native(x):
    """Converte tipos NumPy/Pandas para tipos nativos Python"""
    # Tipos NumPy → nativos
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x) if not (np.isnan(x) or np.isinf(x)) else 0.0
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, (np.generic,)):  # fallback para outros np.* genéricos
        try:
            return x.item()
        except Exception:
            return str(x)

    # Tipos Pandas problemáticos
    if x is pd.NA:
        return None
    if isinstance(x, (pd.Timestamp, pd.Timedelta)):
        return str(x)

    # Datetimes/dates
    if isinstance(x, (datetime, date)):
        return x.isoformat()

    # Floats nativos com NaN/Inf
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return 0.0

    return x

def limpar_valores_problematicos(obj):
    """Sanitiza valores para serialização JSON"""
    # dict
    if isinstance(obj, dict):
        return {str(k): limpar_valores_problematicos(v) for k, v in obj.items()}

    # listas/tuplas/conjuntos
    if isinstance(obj, (list, tuple, set)):
        return [limpar_valores_problematicos(v) for v in obj]

    # arrays NumPy → lista nativa
    if isinstance(obj, np.ndarray):
        return [limpar_valores_problematicos(v) for v in obj.tolist()]

    # Series/DataFrame como último recurso (se aparecerem)
    if isinstance(obj, pd.Series):
        return limpar_valores_problematicos(obj.tolist())
    if isinstance(obj, pd.DataFrame):
        return limpar_valores_problematicos(obj.to_dict(orient="records"))

    # atômicos
    obj2 = _to_native(obj)
    return obj2
