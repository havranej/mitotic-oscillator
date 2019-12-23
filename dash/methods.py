
import numpy as np

def rk4(state, f, h):
    t, x = state[:1], state[1:]
    
    k1 = h*f(t, x)
    k2 = h*f(t + 0.5*h, x + 0.5*k1)
    k3 = h*f(t + 0.5*h, x + 0.5*k2)
    k4 = h*f(t + h, x + k3)

    t_new = t + h
    x_new = x + (k1 + 2*k2 + 2*k3 + k4)/6

    new_state = np.concatenate((t_new, x_new))
    
    return new_state

def euler(state, f, h):
    t, x = state[:1], state[1:]
    
    t_new = t + h
    x_new = x + h * f(t, x)
    
    new_state = np.concatenate((t_new, x_new))
    
    return new_state
