
import numpy as np

def mitotic_oscilator(t, x, params = {}):

    v_i = params.get("v_i", 0.025)
    v_d = params.get("v_d", 0.25)
    K_d = params.get("K_d", 0.02)
    k_d = params.get("k_d", 0.01)
    K_c = params.get("K_c", 0.5)
    V_M1 = params.get("V_M1", 3)
    K_1 = params.get("K_1", 0.005)
    V_2 = params.get("V_2", 1.5)
    K_2 = params.get("K_2", 0.005)
    V_M3 = params.get("V_M3", 1)
    K_3 = params.get("K_3", 0.005)
    V_4 = params.get("V_4", 0.5)
    K_4 = params.get("K_4", 0.005)

    C = x[0]
    M = x[1]
    X = x[2]

    C_prim = v_i - v_d * X * C / (K_d + C) - k_d * C

    V_1 = C / (K_c + C) * V_M1
    M_prim = V_1 * (1 - M) / (K_1 + 1 - M) - V_2 * M / (K_2 + M)

    V_3 = M * V_M3
    X_prim = V_3 * (1 - X) / (K_3 + 1 - X) - V_4 * X / (K_4 + X)

    return np.array([C_prim, M_prim, X_prim])

