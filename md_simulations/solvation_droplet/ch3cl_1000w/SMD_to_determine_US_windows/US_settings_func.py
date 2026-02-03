import numpy as np

def read_pes(pesname,min_bias_center,max_bias_center,up_resolution):
    CVrange = max_bias_center - min_bias_center
    PES_CVmin = min_bias_center - CVrange / 3.
    PES_CVmax = max_bias_center + CVrange / 3.

    pes_file = open(pesname,"r")
    pesdata = pes_file.readlines()
    pes_file.close()
    CV = []
    PES = []
    for i in range(len(pesdata)):
        ll = pesdata[i].split()
        if ll[0][0] == "#": continue
        CV.append(float(ll[0]))
        PES.append(float(ll[1]))
    if up_resolution:
        nCV = len(CV)
        newCV = []
        newPES = []
        for i in range(nCV-1):
            nCV = (CV[i] + CV[i+1]) /2.
            nPES = (PES[i] + PES[i+1]) /2.
            newCV.append(CV[i])
            newCV.append(nCV)
            newPES.append(PES[i])
            newPES.append(nPES)
        CV = newCV
        PES = newPES

    ## just to append to head and tail of CV, set equal to the value at bounds.
    filePES_CVmin = CV[0]
    filePES_CVmax = CV[-1]
    dCV = (CV[-1] - CV[0]) / (len(CV) - 1)
    Fleft = PES[0]
    Fright = PES[-1]

    if filePES_CVmin > PES_CVmin:
        addCV = []
        addPES = []
        aCV = filePES_CVmin
        while aCV > PES_CVmin:
            aCV -= dCV
            addCV.append(aCV)
            addPES.append(Fleft)
        addCV.reverse()
        addPES.reverse()
        CV = addCV + CV
        PES = addPES + PES

    if filePES_CVmax < PES_CVmax:
        addCV = []
        addPES = []
        aCV = filePES_CVmax
        while aCV < PES_CVmax:
            aCV += dCV
            addCV.append(aCV)
            addPES.append(Fright)
        CV = CV + addCV
        PES = PES + addPES
    CV = np.asarray(CV)
    PES = np.asarray(PES)
    return CV, PES, dCV

def get_first_derivative(x,y):
    return x, np.gradient(y,x)

def get_second_derivative(x,y):
    x, dy = get_first_derivative(x,y)
    return x, np.gradient(dy,x)

def biasPE(CV,kappa,bias_center):
    return 0.5*kappa*(CV - bias_center)**2

def check_nmin(x,y,lower_bound,upper_bound):
    ndata = len(x)
    decrease = True
    for i in range(ndata-1): ## not care about the 2nd derivative for now
        if x[i] >= lower_bound and x[i+1] <= upper_bound:
            slope1 = y[i+1] - y[i]
            #slope2 = y[i+2] - y[i+1]
            #second_d = slope2 - slope1
            if slope1 < 0 and not decrease: return False
            if slope1 > 0: decrease = False
            #if slope1 < 0.05 and slope1 > -0.05:
                #if slope2 < 0.01: return False
    return True

def get_Pb(bias_center,kappa,CV,dCV,PES,RT):
    PES_biased = PES + biasPE(CV,kappa,bias_center)
    Pb = np.exp(-PES_biased/RT)
    Pb /= np.sum(Pb)
    w_mean_CV = np.sum(CV*Pb)
    w_mean_sqCV = np.sum(CV**2*Pb)
    w_std_CV = np.sqrt(w_mean_sqCV - w_mean_CV**2)
    Pb /= dCV
    return w_mean_CV, w_std_CV, Pb, PES_biased

def get_minkappa(bias_center,kappaL,CV,dCV,PES,RT,min_bias_center,max_bias_center,tol_center_mean_diff):
    for kappa in kappaL:
        w_mean_CV, w_std_CV, Pb, PES_biased = get_Pb(bias_center,kappa,CV,dCV,PES,RT)
        diff = abs(w_mean_CV - bias_center)
        if not check_nmin(CV,PES_biased,min_bias_center,max_bias_center):
            continue
        if diff <= tol_center_mean_diff:
            return kappa, w_mean_CV, w_std_CV, Pb
    print ("Error: Could not find appropriate kappa for the window.")
    print ("Edit the kappaL if needed.")
    exit()

def get_minkappa_2nd_d(bias_center,kappaL,CV,dCV,PES,RT,min_bias_center,max_bias_center,tol_center_mean_diff,starting_kappa):
    for kappa in kappaL:
        if kappa < starting_kappa: continue
        w_mean_CV, w_std_CV, Pb, PES_biased = get_Pb(bias_center,kappa,CV,dCV,PES,RT)
        diff = abs(w_mean_CV - bias_center)
        if not check_nmin(CV,PES_biased,min_bias_center,max_bias_center):
            continue
        if diff <= tol_center_mean_diff:
            return kappa, w_mean_CV, w_std_CV, Pb
    print ("Error: Could not find appropriate kappa for the window.")
    print ("Edit the kappaL if needed.")
    exit()

def get_kappa_2nd_d(CV,PES):
    xi, kappa_CV = get_second_derivative(CV,PES)
    return abs(kappa_CV)


