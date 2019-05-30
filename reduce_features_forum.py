import math

def delta_angle_norm(a, b) :
    delta = (a - b)
    delta += (delta < -math.pi) * 2 * math.pi
    delta -= (delta > math.pi) * 2 * math.pi
    return delta

def angle_invert(angle, invert_mask) :
    return (
        -999 * (angle == -999) +
        (angle != -999) * (
            angle * (invert_mask == False) +
            (-angle) * (invert_mask == True)
        )
    )

def reduce_angles(X) :
    """ This function works in-place!"""
    
    delta_angle = 'PRI_tau_phi'
    for angle in ['PRI_lep_phi', 'PRI_met_phi'] :
        X['%s-%s' % (angle, delta_angle)] = delta_angle_norm(X[angle], X[delta_angle])
        del X[angle]
        
    for angle in ['PRI_jet_leading_phi', 'PRI_jet_subleading_phi'] :
        X['%s-%s'% (angle, delta_angle)] = (
            delta_angle_norm(X[angle], X[delta_angle]) * (X[angle] != -999) +
            (-999) * (X[angle] == -999)
        )
        del X[angle]

    del X[delta_angle]
    
    invert_mask = X['PRI_tau_eta'] < 0
    for angle in ['PRI_tau_eta', 'PRI_lep_eta', 'PRI_jet_leading_eta', 'PRI_jet_subleading_eta'] :
        X[angle] = angle_invert(X[angle], invert_mask)
