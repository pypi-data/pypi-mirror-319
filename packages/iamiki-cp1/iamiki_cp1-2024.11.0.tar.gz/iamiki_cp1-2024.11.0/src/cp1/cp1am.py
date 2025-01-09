# cp1am.py - Ed 0.1.0 du 14/11/2024 - @cp1iogrib modified

__version__ = "2024.11.0"

import pandas as pd
import numpy as np
import warnings
from datetime import datetime
import matplotlib.pyplot as plt
#import cp1datasets
#from .io.cp1iogrib import cp_gribdata

# mask, mask: user mask to apply on df_metoc ; m0: calculation mask
# @IAM: take into account python timeit function results

def cpam_metoc2df(df_metoc=None, filename=None, npdataset=None, mask=None, C=None):
    """Fonction for collecting metoc data into a dataframe suitable for CP1 callculations"""
    dfcolumns = ["zp", "pzp", "z1", "tc1", "hr1", "z2", "v2", "tc0", "H13ini", "salt"]
    CPC = C.copy() if C is not None else init_cp1_const()  # Needed
    ## dfin = dataframe with metoc data as an input for CP1 calculations
    if df_metoc is not None:
        dfin = df_metoc
    elif filename is not None:
        # Assuming cp1datasets.get_inputtestfile is a function to read the file
        dfin = cp1datasets.get_inputtestfile(filename)[0]
    elif npdataset is not None:
        # Assuming npdataset is a numpy array that can be converted to a DataFrame
        dfin = pd.DataFrame(npdataset)  # npdataset from cp1iogrib
    else:
        # testfile = filename if filename is not None else './data/cp1_21inputtestset.txt'
        raise ValueError(
            "cpam_metoc2df requires MetOc data: "
            + "either a DataFrame, an input file, or date in association with a dataset."
        )

    dfin = dfin.astype('float32')
    mask = mask if mask is not None else pd.Series([True] * len(dfin), index=dfin.index)
    # default values
    dfin = cp_default_column_values(
        dfin,
        fill_values={"salt": 37.0, "opensea": True},
        empty_code_values={"salt": 0.0, "opensea": 0.0},
    )  # @IAM:

    # check for necessary data
    missing_columns = [col for col in dfcolumns if col not in dfin.columns.tolist()]
    if missing_columns:
        raise ValueError(f"Missing necessary '{col}' MetOc Data.")

    dfmetocout = pd.DataFrame(
        {"mout": cp_metocwithinvalidityrange(dfin)}, index=dfin.index
    )
    # dfmetocout['mout'] = cp_metocwithinvalidityrange(dfin) # ajoute une colonne de plausibilité des entrées
    # Afficher un éventuel warning avec la liste des numéros de ligne
    # metoc_outofrange = dfin.index[dfin['mout']].tolist()
    metoc_outofrange = dfmetocout.index[dfmetocout["mout"]].tolist()
    if len(metoc_outofrange) > 0:
        warnings.warn(
            f"Certaines entrées météo sont peu plausibles cf. lignes : {metoc_outofrange}"
        )
    else:
        warnings.warn("Toutes les entrées météo sont dans la plage de plausibilité")

    # @IAM: Questionable ; modifying dfin is for ascendant compatibility reasons only (with other soft)
    dfin['opensea'] = dfin['opensea'].astype(bool)
    dfin.loc[dfin["v2"] < 0.5, "v2"] = 0.5  # @IAM: questionable
    dfin.loc[mask, "hr1"] = np.minimum(
        dfin.loc[mask, "hr1"], cp_humsurf(dfin.loc[mask, "salt"])
    )  # @IAM: !

    return dfin, dfmetocout


def cpam_rf(dfin, mask=None, C=None):
    """Fonction de calcul CPAM sur un fichier/dataset/dataframe"""
    # cpam_rf -> cp_clso -> cp_zc -> cp_ducts
    CPC = C.copy() if C is not None else init_cp1_const()  # Needed
    m0 = mask if mask is not None else pd.Series([True] * len(dfin), index=dfin.index)

    rtol = CPC["reltol"]
    # dfcalc is the size of df_metoc => You may choose your calculation mask in accordance
    #print("Resolution clso...")
    dfcalc, dfi, dfconv = cp_clso(
        dfin, C=CPC, mask=m0, tol=CPC["tol"]
    )  # dfcalc.loc[mask] calculé
    m0 = dfcalc["mask"]  # m0 & validityrange

    # thvs, h13, v195, zinf, hvag
    dfcalc.loc[m0, ["h13", "zinf", "zrefm1"]] = cp_h13zinfhvag(
        dfin, dfcalc, C=CPC, mask=m0
    )

    # zc = duct height, if any
    #print("Resolution zc positifs...")
    dfcalc.loc[m0, ["zc"]], dfipos = cp_zc(
        dfin, dfcalc, C=CPC, mask=m0, reltol=rtol, thresh=0.157
    )
    mpos = dfcalc["zc"] > 0
    if CPC["condneg"]:  # pseudo calculations for zc in case of Infraref
        #print("Resolution zc négatifs...")
        mneg = m0 & ~(dfcalc["zc"] > 0)  # conserve les 0 et les nan
        dfcalc.loc[mneg, ["zc"]], dfineg = cp_zc(
            dfin, dfcalc, C=CPC, mask=mneg, reltol=rtol, thresh=0.0
        )
        dfcalc.loc[mneg, ["zc"]] = -dfcalc.loc[mneg, ["zc"]]

    # calculs des points caractéristiques des conduits
    #print("Identication, caractérisation conduits...")
    dfident = cp_ident(dfin=dfin, df=dfcalc, C=CPC)
    
    # filtering dfident inaccordance with CPCn
    nbident = len(dfident)
    dfident = dfident[(dfident["Z3"] >= CPC["zcmin"]) & (dfident["Z3"] <= CPC["zcmax"])]
    if (len(dfident)<nbident):
        print(f"{nbident-len(dfident)} rows from the duct identification dataframe were filtered because they were out of the range [zcmin <= Zc <= zcmax]")
    
    dfcaract = cp_caract(dfident)  
    # to be compiled with original metoc geo and date within an operational loop 

    # dfcalc # mout, zc, mol, tz, tindM, tdMdz, nbpoints = f (dfin, CPC, mask, lambda=0)
    return dfcalc, dfi, dfconv, dfident, dfcaract


def cp_ident(dfin, df, C=None, mask=None):
    """
    Duct Identification - zc > 0
    """
    C = C if C is not None else init_cp1_const()
    mask = mask if mask is not None else df["mask"]
    mpos = mask & (df["zc"] > 0)  # only for real Evaporation Ducts i.e. zc > 0

    dfid = pd.DataFrame(index=dfin[mpos].index).assign(
        Z3=0.0, Z2=0.0, Z1=0.0, M3=0.0, M2=0.0, M1=0.0
    )

    # z, pz, tcz, hrz, uz, Nz, Mz, ez, esz, thz, tkz, qz, hrz, dNdZ, dMdz
    z13, _, _, _, _, _, M13, _, _, _, _, _, _, _, _ = cp_hleval(
        zstr="h13", dfin=dfin, df=df, C=C, mask=mpos
    )
    zzc, _, _, _, _, _, Mzc, _, _, _, _, _, _, _, _ = cp_hleval(
        zstr="zc", dfin=dfin, df=df, C=C, mask=mpos
    )
    zz0, _, _, _, _, _, Mz0, _, _, _, _, _, _, _, _ = cp_hleval(
        zstr="zrefm1", dfin=dfin, df=df, C=C, mask=mpos
    )

    dfid.loc[:, "Z3"] = zzc
    dfid.loc[:, "Z2"] = z13
    dfid.loc[:, "Z1"] = zz0
    dfid.loc[:, "M3"] = Mzc
    dfid.loc[:, "M2"] = M13
    dfid.loc[:, "M1"] = Mz0  # np.squeeze(Mz0)

    return dfid


def cp_caract(dfident):
    """
    Duct Caracterization based upon a Duct Identification Mi(Zi), i=1..3
    """
    dfcr = pd.DataFrame(index=dfident.index).assign(
        Zc=0.0, Mc=0.0, Ec=0.0, Eg=0.0, dM=0.0, Mb=0.0
    )
    dfcr["Zc"] = dfident["Z3"]
    dfcr["Mc"] = dfident["M3"]
    dfcr["Ec"] = -dfident["Z1"] + dfcr["Zc"]
    dfcr["Eg"] = -dfident["Z2"] + dfcr["Zc"]
    dfcr["dM"] = dfident["M2"] - dfcr["Mc"]
    dfcr["Mb"] = dfident["M1"]

    return dfcr


def cp_dfcalc(dfin, C=None, m0=None):
    """Initialisation de df de calcul correspondant à un dfin météo"""
    # /!\ dfcalc est limité à mask (vecteur de booleen = True par défaut)
    C = C if C is not None else init_cp1_const()
    m0 = m0 if m0 is not None else pd.Series([True] * len(dfin), index=dfin.index)

    # dfcalc A la dimension de dfin ; mais on peut passer un masque de calcul
    dfcalc = pd.DataFrame(
        index=dfin.index
    )  # initialise dfcalc en respectant les indices @IAM: que m0 ; non ! par choix

    # NWVR = Not Within the "marine validity range of CP1 calculations"
    dfcalc["mask"] = m0 & ~cp_metocwithinvalidityrange(dfin)
    mask = dfcalc["mask"]

    # Adding needed calculations columns with np.nan values to dfcalc
    new_metoc = ["hr0", "thv0", "thv1", "th0", "th1", "q0"]
    new_columns = ["zc", "v1", "ribz1", "lmo", "z0", "z0t", "z0q",
        "psim10", "us0", "us", "ustar",
        "p1", "dpdz", "psih1", "psim1", "psim2", "v2calc",
        "ths", "qs", "thvs", "h13", "zinf", "zrefm1",
        new_metoc,
    ]
    dfcalc[new_columns] = np.nan
    dfcalc["psim10"] = 0.0
    dfcalc["z0"] = 1e-4
    dfcalc.loc[mask, new_metoc] = cp_thermodyn(dfin.loc[mask], C=C)[new_metoc]

    ## initialization (needed for clso calculation)
    dfcalc.loc[mask, "v1"] = (
        dfin.loc[mask, "v2"]
        * np.log(dfin.loc[mask, "z1"] / 100000)
        / np.log(dfin.loc[mask, "z2"] / 100000)
    )
    dfcalc.loc[mask, "ribz1"] = cp_bulkrichardson(dfin, dfcalc, C=C, mask=mask)
    dfcalc.loc[mask, "us0"] = rugvent_init(
        dfin, dfcalc, psim10=0, z0=1e-4, C=C, mask=mask
    )
    dfcalc.loc[mask, "z0"], dfcalc.loc[mask, "ustar"] = rugvent(
        dfin, dfcalc, C=C, mask=mask
    )
    dfcalc.loc[mask, "z0t"] = rugtemp(dfcalc, C=C, mask=mask)

    return dfcalc  # , mout


def cp_clso(dfin, C=None, mask=None, tol=1e-4, lignacap=[0]):
    """Résolution de la C.L en Atmosphére Marine, selon la théorie (similitude) de Monin-Obukhov
    via la détermination des paramètre d'échelle de la Couche Limite
    via le calcul de la Longueur de Monin Obukhov (lmo)
    à partir des paramètre 'Bulk' observés : sst(z=0) thr(z1) uv(z2)"""
    C = C if C is not None else init_cp1_const()
    m0 = (
        mask.astype(bool)
        if mask is not None
        else pd.Series([True] * len(dfin), index=dfin.index)
    )
    # mask est le masque global de calcul, qui permet de rejeter les terres, NaN et valeurs input hors plage
    # m0 est un masque de découpage des calculs lorsque les données de modèles dépasseraient la RAM
    # m1, m2, ... sont des sous-masques d'itérations sur les calculs vectoriels à reltol données
    dfcalc = cp_dfcalc(
        dfin, C=C, m0=m0
    )  # initialise complètement le df de calcul CP1AM
    m0 = dfcalc["mask"]  # masque de calcul, exclut les calculs sur mout
    lignacap = (
        lignacap if lignacap is not None else []
    )  # [] renverra juste un dfconv "vide"
    listacap = ["v1", "ribz1", "lmo", "z0", "z0t", "ustar", "us0", "us", "psim10"]

    # dfcalc étant complètement initialisé
    #   ribz1, z0, psim10, us0, ustar,
    # cp_clso est constitué de 2 boucles imbriquées permettant de résoudre
    # a) la convergence sur v2(z2)
    # b) la convergence sur u*
    # c) l'appel interne à cp_lmo résoud également de façon itérative LMO (zeta)
    #    ai retiré :    lmo=np.nan, zetaz1=np.nan, us=0.,
    dfi = pd.DataFrame(index=dfcalc[m0].index).assign(
        z0ini=1e-4, v2calc=0.0, psih=0.0, nbiv2=0, diffv2=1.0,
        ribz1sign=0, swapsign=0, nbius=0, diffustar=1.0, rap=1.0,
    )
    # nb : cp_dfcalc a tout initialisé, y compris v1
    ma = m0.copy().astype(bool)
    qiterv2 = 0
    # Initialiser dfconv avec les valeurs dfcalc(ligaconv) pour qiterustar=0
    dfconv = dfcalc.loc[lignacap, listacap].copy().assign(qiterv2=qiterv2)

    maxiterv2=20 # checked with overall cov test and sensibility analyses
    while dfi["diffv2"].max(skipna=True) > tol:  # reltol:
        qiterv2 += 1
        m1 = dfi["diffv2"] > tol  # reltol - Masque de convergence sur v2
        ma.loc[m0] = m1.astype(bool)
        dfi.loc[m1, "nbiv2"] += 1  # Add 1 to nbiter where iter is True
        if qiterv2>(maxiterv2-1):
            break
        dfcalc.loc[ma, "v1"] = (
            dfcalc.loc[ma, "v1"] / dfi.loc[m1, "rap"]
        )  # ie proportionnellement V2calc/V2
        dfcalc.loc[ma, "ribz1"] = cp_bulkrichardson(
            dfin, dfcalc, C=C, mask=ma
        )  # .rename(columns={'rib': 'ribz1'})
        swap = (np.sign(dfcalc.loc[ma, "ribz1"]) != dfi.loc[m1, "ribz1sign"])
        dfi.loc[m1, "swapsign"] += swap  # stability change
        dfi.loc[m1, "ribz1sign"] = np.sign(dfcalc.loc[ma, "ribz1"])
        dfcalc.loc[ma & swap, "psim10"] = 0.0  # @IAM: ?why, add a swap test
        dfi.loc[m1 & swap, "z0ini"] = 1e-4  # @IAM: ?why, add a swap test
        dfcalc.loc[ma, "us0"] = dfcalc.loc[ma, "v1"] / (
            C["cov0"] + (1 / C["k"]) * np.log(dfin.loc[ma, "z1"] / dfi.loc[m1, "z0ini"])
        )  # @IAM: z0ini !?
        qiterustar = 0
        mb = ma.copy()
        dfi.loc[mb, "diffustar"] = 1.0
        while dfi["diffustar"].max(skipna=True) > tol:  # reltol:
            qiterustar += 1
            m2 = dfi["diffustar"] > tol  # reltol - Masque de convergence sur ustar
            mb.loc[m0] = m2
            dfi.loc[m2, "nbius"] += 1  # Add 1 to nbiter where iter is True

            dfcalc.loc[mb, "z0"], dfcalc.loc[mb, "ustar"] = rugvent(
                dfin, dfcalc, C=C, mask=mb
            )  # ma->mb
            dfcalc.loc[mb, "z0t"] = rugtemp(dfcalc, C=C, mask=mb)
            # cp_lmo => [#'ribz1', 'riz1', 'lmo', 'zetaz1', 'psih', 'psim10', 'nbiter', 'err', 'rap']
            dfcalc.loc[mb, ["zetaz1", "lmo", "psim10"]] = cp_lmo(
                dfin, dfcalc, C=C, mask=mb, reltol=1e-4
            )[["zetaz1", "lmo", "psim"]].rename(columns={"psim": "psim10"})
            dfcalc.loc[mb, "us0"] = dfcalc.loc[mb, "v1"] / (
                C["cov0"]
                + (1 / C["k"])
                * (
                    np.log(dfin.loc[mb, "z1"] / dfcalc.loc[mb, "z0"])
                    - dfcalc.loc[mb, "psim10"]
                )
            )
            dfi.loc[m2, "diffustar"] = (
                (dfcalc.loc[mb, "ustar"] - dfcalc.loc[mb, "us0"])
                / dfcalc.loc[mb, "us0"]
            ).abs()

        dfcalc.loc[ma, "us"] = dfcalc.loc[ma, "us0"]  # @IAM: remplace us0 par ustar ?
        _, _, _, dfcalc.loc[ma, "psim2"] = cp_phipsi(
            dfin.loc[ma, "z2"], dfcalc.loc[ma, "lmo"], C=C
        )
        dfi.loc[m1, "v2calc"] = dfcalc.loc[ma, "us"] * (
            C["cov0"]
            + (1 / C["k"])
            * np.log(
                dfin.loc[ma, "z2"] / dfcalc.loc[ma, "z0"] - dfcalc.loc[ma, "psim2"]
            )
        )
        dfi.loc[m1, "rap"] = dfi.loc[m1, "v2calc"] / dfin.loc[ma, "v2"]
        dfi.loc[m1, "diffv2"] = (dfi.loc[m1, "v2calc"] - dfin.loc[ma, "v2"]).abs()
        # tol ? ou retol i.e. dfi['diffv2']=(dfi['v2calc']-dfi['v2'])/dfi['v2']

        # compiler dfconv avec copie des valeurs de dfcalc pour qiterustar en cours
        dfconv = pd.concat(
            [dfconv, dfcalc.loc[lignacap, listacap].copy().assign(qiterv2=qiterv2)]
        )

    # On dispose désormais d'un V1(z1) cohérent (LMO) des entrées : t(z1), hr(z1) et V2(z2)
    _, _, dfcalc.loc[m0, ["psih1"]], dfcalc.loc[m0, ["psim1"]] = cp_phipsi(
        dfin.loc[m0, ["z1"]].values, dfcalc.loc[m0, ["lmo"]].values
    )
    dfcalc.loc[m0, ["psim10"]] = dfcalc.loc[m0, ["psim1"]].rename(
        columns={"psim1": "psim10"}
    )  # @IAM
    dfcalc.loc[m0, ["z0q"]] = rughum(dfcalc, C=C, mask=m0)

    dfcalc.loc[m0, ["ths", "qs"]] = thqstar(dfin.loc[mask], dfcalc, C=C, mask=m0)
    dfcalc.loc[m0, ["thvs"]] = (
        dfcalc.loc[m0, "ths"]
        + C["alf"]
        * dfcalc.loc[m0, "qs"]
        * (dfcalc.loc[m0, "th1"] + dfcalc.loc[m0, "th0"])
        / 2
    )

    return (
        dfcalc,
        dfi,
        dfconv,
    )  # dfi only for convergence analyses if needed: dfi[['nbiv2', 'diffv2', 'nbius', 'diffustar']]


def cp_zc(dfin, df, C=None, mask=None, reltol=1e-4, thresh=0.157):
    """
    :return: DataFrame containing the duct height (zc), based on gradN loop
    :return: ermax, erreur maximum liée à l'itération (ermax < 0,1%)
    """
    C = C if C is not None else init_cp1_const()
    m0 = mask if mask is not None else df["mask"]
    if isinstance(m0, list):
        m0 = np.array(m0, dtype=bool)
    ma = m0.copy()
    # un mask mi est également utilisé pour limiter les recalculs au fur et à mesure des itérations
    # initialize zc as zcold, and rap as 0.1
    dfi = pd.DataFrame(index=dfin[m0].index).assign(
        zcold=1.0, zc=1.0, nbiter=0, err=1.0
    )  # initialise dfcalc en respectant les indices @IAM
    mas = df["lmo"] > 0
    ms = mas[m0]  # = dfcalc.loc[m0, 'lmo'] >0 # stable atm mask
    m1 = dfi["err"].abs() > reltol  # initialise
    p1dpdz = cp_thermodyn(dfin.loc[m0], C=C)[["p1", "dpdz"]]
    maxiter = 40 # checked with overall cov test and sensibility analyses
    while any(m1):
        ma.loc[m0] = m1  # .astype(bool)
        dfi.loc[m1, "nbiter"] += 1
        # dfi.loc[m1, 'zcold'] = dfi.loc[m1, 'zc']
        _, _, _, thz, qz, _ = cp_phipsival(dfi.loc[m1, "zc"], dfin, df, C=C, mask=ma)
        pz = p1dpdz.loc[m1, "p1"] + p1dpdz.loc[m1, "dpdz"] * (
            dfi.loc[m1, "zc"] - dfin.loc[ma, "z1"]
        )
        tkz = thz / ((1000 / pz) ** C["gam"])
        # ptqz = cp_thermodyn(dfin, C=CPC)[['p1', 'tk1', 'q1', 'dpdz']]
        c1, c2, c3 = cp_gradN(pz, tkz, qz, p1dpdz.loc[m1, "dpdz"], C=C)
        s = -(c2 * df.loc[ma, "qs"] + c3 * df.loc[ma, "ths"]) / (
            C["k"] * df.loc[ma, "lmo"] * (thresh + c1)
        )
        # no real positive zc solution for zetac = s * phih(zetac) # if ~exist, early end
        exist = (s * df.loc[ma, "lmo"] > 0)  
        dfi.loc[m1, "zc"] = (exist + 0.0) * dfi.loc[m1, "zc"]  
        dfi.loc[m1, "zcold"] = (exist + 0.0) * dfi.loc[m1, "zc"]
        m1.loc[m1] = exist
        # stable atm => x1 = cp_pol2quadratic(s = s, cophist=6)
        dfi.loc[m1 & ms, "zc"] = (
            cp_pol2quadratic(s[m1 & ms], C["cophist"]) * df.loc[ma & mas, "lmo"]
        )
        # unstables atm => x1, x2, x3, det = cp_pol3cubic(s2 = s * s, cophiun=20)
        dfi.loc[m1 & ~ms, "zc"] = (
            cp_pol3cubic(s[m1 & ~ms] ** 2, C["cophiun"]) * df.loc[ma & ~mas, "lmo"]
        )  # .cp_pol3cubic(...)[0]
        dfi.loc[m1, "err"] = (dfi.loc[m1, "zcold"] - dfi.loc[m1, "zc"]) / dfi.loc[
            m1, "zcold"
        ]
        m1.loc[m1] = dfi.loc[m1, "err"].abs() > reltol  # loop on True m1
        
        if any(dfi.loc[m1, "nbiter"]>maxiter): #DEBUG
            break

    return dfi["zc"], dfi


def init_cp1_const():
    """Initialise et retourne les constantes physiques pour le module cp1."""
    # usage: g2 = cp1_const['g'] ** 2
    cp1_const = {
        "g": 9.807,  # Accélération due à la gravité en [m/s^2]
        "R": 287.05,  # Constante des gaz parfaits pour l'air sec [J/kg/K]
        "mu": 0.622,  # Rapport des masses molaires de l'eau et de l'air sec [.]
        "gam": 0.28548,  # Passage des températures aux températures potentielles [.]
        "alf": 0.608,  # (1-mu)/mu : Pour le calcul des températures virtuelles [.]
        "Arf": 77.6,  # Pour l'indice de réfraction aux radiofréquences [K/hPa]
        "Brf": 3.73256e5,  # [K2/hPa]
        "z10": 10,  # Altitude de 10 mètres [m]
        "k": 0.41,  # Cste de Von Karman ; valeur version OC ; usuellement k=0.40 [.]
        "cov0": 0,  # Reliant la vitesse du vent à l'altitude 0 avec la vitesse de frottement; v0 = cov0*ustar
        "alfcpm": 0.011,  # Constante de Charnock, Cf Garrat, 1977, 1994. valeur assez consensuelle pour la pleine mer
        "alfccot": 0.017,  # valeur conseillée en zone côtière
        "ppv": 0.1,  # Coefficients de la régression linéaire permettant de passer de la vitesse du vent à 19,5 m à la hauteur H1/3 des vagues :
        "ordov": 0,  # H1/3 = ppv*V195 + ordov (en zone côtière seulement)
        "ppos": 0.027,  # H1/3 = ppos * V195^2 (en pleine mer seulement)
        "coup": 1.0,  # Coefficient empirique permettant de déterminer, à partir de H1/3, l'altitude zinf où s'opère la transition entre profils bulk et profils linéaires : zinf = coup*H1/3
        "hvag": 0.65,  # hauteur des vagues = hvag * H1/3
        "cophiun": 20,  # coefficient des fonctions de stabilités phi (EDSON et al.) dans les cas Instables ; 20 pour Edson et al ; 16 pour Dyer et Hicks
        "cophist": 6,  # coefficient des fonctions de stabilités phi (KONDO) dans les cas Stables ; 6 pour Kondo [1995]
        "tol": 1e-4,  # absolute tolerance for iterative calculations
        "reltol": 1e-4,  # tolerance relative (par défaut) à convergence utilisée dans les itérations
        "condneg": True,  # does CP1 make calculations for zc in case of infrarefraction (zc<0)
        "zrefM1": 0.05,  # ref height above MSL as a ref for M1 duct height ; .05 m
        "zcmin": 1.,
        "zcmax": 50.,
    }
    # Create a new dictionary CPC that is the union of CPConstantes and CPConfiguration
    # CPC = {**CPConstantes, **CPConfiguration}
    return cp1_const


def init_JdTest():
    """Initialise et retourne un tableau numérique de Metoc tests."""
    return np.zeros((9, 11))


def cp_default_column_values(
    df,
    fill_values={"salt": 37.0, "opensea": False},
    empty_code_values={"salt": 0.0, "opensea": 0},
):
    """
    Get columns that need to be updated with NaN values filled or added if they do not exist.
    Also replace empty code values with specified default values.

    :param df: The DataFrame to check.
    :type df: pd.DataFrame
    :param fill_values: A dictionary where keys are column names and values are the default values to fill NaNs with.
    :type fill_values: dict
    :param empty_code_values: A dictionary where keys are column names and values are the default values to replace empty code values with.
    :type empty_code_values: dict
    :return: A DataFrame with the columns updated.
    :rtype: pd.DataFrame

    Example usage:
    dfin.update(cp_default_column_values(dfin, {'salt': 37, 'opensea': False}, {'salt': 0, 'opensea': 0}))
    """
    # Cette version de la fonction vérifie si chaque colonne existe et, si ce n'est pas le cas, l'ajoute avec une valeur par défaut. Si la colonne existe mais contient des valeurs manquantes, elle remplit ces valeurs avec la valeur par défaut spécifiée en utilisant .loc. De plus, elle remplace les valeurs vides (définies dans empty_code_values) par les valeurs par défaut spécifiées, en castant explicitement les valeurs pour éviter les warnings de type.

    for column, value in fill_values.items():
        if column in df:
            # Check if the column contains only NaN or empty code values
            if df[column].isna().all() or (
                empty_code_values.get(column) is not None
                and (df[column] == empty_code_values[column]).all()
            ):
                df[column] = value
                df[column] = df[column].astype(type(value))
                warnings.warn(
                    f"Column '{column}' contains only NaN or empty code values. It has been replaced with {value}."
                )
            else:
                if df[column].isna().any():
                    # Cast value to the column's dtype to avoid warnings
                    cast_value = (
                        value
                        if pd.api.types.is_dtype_equal(df[column].dtype, type(value))
                        else df[column].dtype.type(value)
                    )
                    df.loc[df[column].isna(), column] = cast_value
                    warnings.warn(
                        f"Missing values in column '{column}' are replaced with {value}."
                    )
                if empty_code_values.get(column) is not None:
                    # Cast value to the column's dtype to avoid warnings
                    cast_value = (
                        value
                        if pd.api.types.is_dtype_equal(df[column].dtype, type(value))
                        else df[column].dtype.type(value)
                    )
                    df.loc[df[column] == empty_code_values[column], column] = cast_value
                    warnings.warn(
                        f"Empty code values in column '{column}' are replaced with {value}."
                    )
        else:
            df = df.assign(**{column: value})
            warnings.warn(
                f"Column '{column}' does not exist. It has been added with default value {value}."
            )

    return df


def cp_metocwithinvalidityrange(df):
    # check wether metoc inputs are within the marine validity range of CP1 calculations
    # Créer un vecteur de booléens qui vérifie les conditions spécifiées
    # Exemple d'utilisation: mout = cp_metocwithinvalidityrange(df)
    required_columns = ["tc1", "tc0", "hr1", "v2", "pzp"]
    # Vérifier l'existence des colonnes requises
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(
                f"La colonne requise '{col}' est manquante dans le DataFrame."
            )
    # @IAM: penche en faveur de critères paramétrables, ou au pire au sein de CPC, mais pas 'en dur'
    conditions = ( (df["tc1"] >= -10) & (df["tc1"] <= 50)
        & (df["tc0"] >= 0) & (df["tc0"] <= 40)
        & (df["hr1"] >= 10) & (df["hr1"] <= 100)
        & (df["v2"] >= 0)  & (df["v2"] <= 50)
        & (df["pzp"] >= 950) & (df["pzp"] <= 1050) )
    return ~conditions


def cp_humsurf(abssalinity):
    """Estimated relative humidity at the sea surface hr0 [%] as a function of absolute salinity [g/kg]."""
    hr0 = 100 * (1 - (5.37e-4 * abssalinity))

    return hr0


def cp_thermodyn(df, C=None):
    """Calcul des variables météo dérivées."""
    # Transformation des températures (en °C) et humidités relatives,
    # connues aux altitudes 0 et z1, en températures potentielles virtuelles,
    # humidités spécifiques (+ gradient de pression atmosphérique)
    # Exemple: dfcalc = cp_thermodyn(dfinput)
    C = C if C is not None else init_cp1_const()

    dfout = pd.DataFrame(index=df.index)  # initialise le dfout, conserve les index
    # humidité relative à la surface de l'eau en fonction de la salinité
    dfout["hr0"] = cp_humsurf(df["salt"])  # 100 * (1 - (5.37e-4 * df['salt']))
    # °Celcius -> Kelvin
    dfout["tk0"] = df["tc0"] + 273.15
    dfout["tk1"] = df["tc1"] + 273.15
    # pressions de vapeur saturante et pressions partielles de vapeur
    dfout["esp1"] = np.exp(19.32 - 4223 / (df["tc1"] + 273.15 - 32))
    dfout["e1"] = df["hr1"] * dfout["esp1"] / 100
    dfout["esp0"] = np.exp(19.32 - 4223 / (df["tc0"] + 273.15 - 32))
    dfout["e0"] = dfout["hr0"] * dfout["esp0"] / 100
    # valeurs intermédiaires, recalculées après recalcul de p1
    dfout["p1"] = df["pzp"] - 0.12 * (df["z1"] - df["zp"])
    dfout["q1"] = C["mu"] * dfout["e1"] / (dfout["p1"] + (C["mu"] - 1) * dfout["e1"])
    dfout["dpdz"] = (
        -C["g"] * dfout["p1"] / (C["R"] * dfout["tk1"] * (1 + C["alf"] * dfout["q1"]))
    )
    # valeurs affinées, avec la valeur p1 actualisée
    # p1 (pression à l'altitude z1) déduire de pzp à l'altitide zp
    dfout["p1"] = df["pzp"] + dfout["dpdz"] * (df["z1"] - df["zp"])
    # humidité spécifique à l'altitude z1
    dfout["q1"] = C["mu"] * dfout["e1"] / (dfout["p1"] + (C["mu"] - 1) * dfout["e1"])
    # gradient de pression atmosphérique à l'altitude z1
    dfout["dpdz"] = (
        -C["g"] * dfout["p1"] / (C["R"] * dfout["tk1"] * (1 + C["alf"] * dfout["q1"]))
    )
    # Estimation de la pression atmosphérique à l'altitude 0
    dfout["p0"] = dfout["p1"] - dfout["dpdz"] * df["z1"]
    # humidité spécifique à l'altitude 0
    dfout["q0"] = C["mu"] * dfout["e0"] / (dfout["p0"] + (C["mu"] - 1) * dfout["e0"])
    # températures potentielles
    dfout["th0"] = dfout["tk0"] * (1000 / dfout["p0"]) ** C["gam"]
    dfout["th1"] = dfout["tk1"] * (1000 / dfout["p1"]) ** C["gam"]
    # températures potentielles virtuelles
    dfout["thv0"] = dfout["th0"] * (1 + C["alf"] * dfout["q0"])
    dfout["thv1"] = dfout["th1"] * (1 + C["alf"] * dfout["q1"])

    return dfout


def cp_gradN(p, T, q, dpdz, C=None):  # , il=0
    """
    Expression du gradient dN/dz en fonction des gradients de q et theta
    N=f(p,H,tc) => N=f(p,q,th) => dN/dz=c1+c2*dq/dz+c3*dth/dz
    où c1,c2,c3 sont des fonctions de p, q, T
    Remarque : dp/dz est pris en compte dans c1
    Entrées : p (pression atmosphérique de l'air en hPa)
            : q (humidité spécifique en kg/kg)
            : T (température en K)
    Sorties : c1, c2, c3
    """
    C = C if C is not None else init_cp1_const()

    kp = (1000 / p) ** C["gam"]
    # pour le gradient de température : dTdz=cot1*dpdz+cot3*dthdz
    cot1 = C["gam"] * T / p
    cot3 = 1 / kp
    # cas des radiofréquences
    cc1 = (1 / T) * (C["Arf"] + (C["Brf"] * q / (T * C["mu"] * (1 + C["alf"] * q))))
    cc2 = (p * C["Brf"] / (C["mu"] * T * T)) * (1 / ((1 + C["alf"] * q) ** 2))
    cc3 = -(p / (T * T)) * (
        C["Arf"] + (2 * C["Brf"] * q / (T * C["mu"] * (1 + C["alf"] * q)))
    )
    # Expressions finales pour c1, c2 et c3
    c1 = (cc1 + cc3 * cot1) * dpdz
    c2 = cc2
    c3 = cc3 * cot3

    return c1, c2, c3


def cp_indiceN(p, T, q, C=None):  # , il=0
    """
    Calcul du coindice de réfraction de l'air (indiceN)
    :param p: pression atmosphérique de l'air en hPa
    :param q: humidité spécifique en kg/kg
    :param T: température en K
    :param C: dictionnaire contenant les constantes physiques alf, mu, Arf, Brf
    :param il: indicateur de type de fréquence (0 pour radiofréquences, autre pour fréquences optiques)
    :return: indice de réfraction de l'air
    """
    C = C if C is not None else init_cp1_const()

    # Radio Frequency @IAM: indN = p*cc1 ?? (cf. cp_gradN)
    indN = (p / T) * (C["Arf"] + (C["Brf"] * q / (T * C["mu"] * (1 + C["alf"] * q))))
    # Optic : indN = p * (Aop * (1 - q) + Bop * q / mu) / (T * (1 + alf * q))

    return indN


def cp_phipsi(z, lmo, C=None):
    """
    Calculate stability functions.
    Refer to KONDO (1975) for stable cases and EDSON et al. (1991) for unstable cases.

    Parameters:
    z (array-like or scalar): Array or scalar of positive height values. (z >= 0)
                              If array, must be compatible with lmo for element-wise division.
                              Must be given in the same units as lmo.
    lmo (array-like or scalar): Array or scalar of Monin-Obukhov Length values.
                                If array, must be compatible with z for element-wise division.
                                If scalar, it will be broadcasted to match the size of z.
                                Must be given in the same units as z.
    C (dict, optional): Dictionary containing physical constants. If None, default constants will be used.

    Returns:
    tuple: Four arrays (phih, phim, psih, psim) representing the stability functions.

    Raises:
    ValueError: If z and lmo are not compatible for element-wise division.

    Notes:
    - If z and lmo are both arrays, they must have the same size.
    - If either z or lmo is a scalar, it will be broadcasted to match the size of the other array.
    - The function handles NaN values in z by propagating NaNs to the corresponding positions in the output arrays.

    Example:
    >>> z = np.array([5, 10, np.nan, 20])
    >>> lmo = 10
    >>> phih, phim, psih, psim = cp_phipsi(z, lmo)
    """
    #
    C = C if C is not None else init_cp1_const()
    try:
        zeta = z / lmo
    except Exception as e:
        raise ValueError(
            "z and lmo must be compatible for elementwise division: " + str(e)
        )

    if np.isscalar(lmo):
        lmo = np.full_like(zeta, lmo)

    unstab = zeta < 0

    phih, phim, psih, psim = (np.empty_like(zeta) for _ in range(4))
    phih[~unstab], phim[~unstab], psih[~unstab], psim[~unstab] = kon_stab(
        zeta[~unstab], C=C
    )
    phih[unstab], phim[unstab], psih[unstab], psim[unstab] = ed_inst(zeta[unstab], C=C)

    return phih, phim, psih, psim


def kon_stab(zeta, C=None):
    """
    Calcul des fonctions de stabilité dans les cas stables
    Cf. KONDO (1975)

    :param zeta: valeur de zeta = z/lmo
    :param C=None: dictionnary with C['cophist'] (=6 for Kondo 1975)
    :return: phih, phim, psih, psim
    """
    C = C if C is not None else init_cp1_const()

    phih = 1 + (C["cophist"] * zeta / (1 + zeta))
    phim = 1 + (C["cophist"] * zeta / (1 + zeta))
    psih = -C["cophist"] * np.log(1 + zeta)
    psim = -C["cophist"] * np.log(1 + zeta)

    return phih, phim, psih, psim


def ed_inst(zeta, C=None):
    """
    Calcul des fonctions de stabilité dans les cas instables
    Cf. EDSON et al. (1991)

    :param zeta: valeur de zeta
    :param C=None: dictionnary with C['cophiun'] (=20 Edson 1991)
    :return: phih, phim, psih, psim
    """
    C = C if C is not None else init_cp1_const()

    phih = (1 - C["cophiun"] * zeta) ** (-1 / 2)
    phim = (1 - C["cophiun"] * zeta) ** (-1 / 4)
    xh = (1 - C["cophiun"] * zeta) ** (1 / 2)
    psih = 2 * np.log((1 + xh) / 2)
    xm = (1 - C["cophiun"] * zeta) ** (1 / 4)
    psim = (
        2 * np.log((1 + xm) / 2)
        + np.log((1 + xm * xm) / 2)
        - 2 * np.arctan(xm)
        + np.pi / 2
    )

    return phih, phim, psih, psim


def cp_bulkrichardson(dfin, df, C=None, mask=None):
    """
    Calculate the Bulk Richardson Number BRN (=Rib).

    :param df: DataFrame containing the columns 'z1', 'thv1', 'thv0', and 'v1'.
    :param C: Dictionary containing physical constants. If None, uses init_cp1_const().
    :param mask: Boolean mask to select rows for calculation. If None, uses df['mask'].
    :return: Series containing the Bulk Richardson Number (Rib).

    :reference: https://en.wikipedia.org/wiki/Bulk_Richardson_number
    :reference: https://fr.wikipedia.org/wiki/Nombre_global_de_Richardson
    """
    C = C if C is not None else init_cp1_const()
    mask = mask if mask is not None else df["mask"]

    # @IAM: /!\ température potentielle virtuelle thv = {\displaystyle \theta _{v}}
    # utilisée pour tenir compte de l'influence de la pression et de l'humidité
    # grr l'approx. entre z1 et z0=0 n'est pas celle là : https://en.wikipedia.org/wiki/Richardson_number
    # formula: rib = g * z1 * (thv1 - thv0) / ((thv1 + thv0) / 2 * v1 ** 2)
    rib = (
        C["g"]
        * dfin.loc[mask, "z1"]
        * (df.loc[mask, "thv1"] - df.loc[mask, "thv0"])
        / ((df.loc[mask, "thv1"] + df.loc[mask, "thv0"]) / 2 * df.loc[mask, "v1"] ** 2)
    )

    return rib  # pd.DataFrame({'rib': rib})


def rughum(df, C=None, mask=None):
    """
    Calculate the roughness length for humidity (z0q in meters).
    Refer to MESTAYER (1996) and GARRAT (1994).

    :param df: DataFrame containing the column 'z0'.
    :param C: Dictionary containing physical constants. If None, uses init_cp1_const().
    :param mask: Boolean mask to select rows for calculation. If None, uses df['mask'].
    :return: DataFrame containing the roughness length for humidity (z0q).
    """
    C = C if C is not None else init_cp1_const()
    mask = mask if mask is not None else df["mask"]

    # formula: z0q = z10 * exp(-k^2 / (cen * log(z10 / z0)))
    cen = 1.1e-3
    z0q = C["z10"] * np.exp(
        -C["k"] ** 2 / (cen * np.log(C["z10"] / df.loc[mask, "z0"]))
    )

    return z0q  # pd.DataFrame({'z0q': z0q})


def rugtemp(df, C=None, mask=None):
    """
    Calculate the roughness length for temperature (z0t in meters).
    Refer to MESTAYER (1996) and GARRAT (1994).

    :param df: DataFrame containing the column 'z0'.
    :param C: Dictionary containing physical constants. If None, uses init_cp1_const().
    :param mask: Boolean mask to select rows for calculation. If None, uses df['mask'].
    :return: DataFrame containing the roughness length for temperature (z0t).
    """
    C = C if C is not None else init_cp1_const()
    mask = mask if mask is not None else df["mask"]

    # formula: z0t = z10 * exp(-k^2 / (chn * log(z10 / z0)))
    chn = 1.1e-3
    z0t = C["z10"] * np.exp(
        -C["k"] ** 2 / (chn * np.log(C["z10"] / df.loc[mask, "z0"]))
    )

    return z0t  # pd.DataFrame({'z0t': z0t})


def rugvent_init(dfin, df, psim10=0, z0=1e-4, C=None, mask=None):
    """
    Initiate roughness length (us0) for wind (z0 in meters).
    with initial psim1_init = 0 and z0_init = 1e-4

    :param df: DataFrame containing the columns 'z1', 'z0' and 'v1'.
    :param C: Dictionary containing physical constants. If None, uses init_cp1_const().
    :param mask: Boolean mask to select rows for calculation. If None, uses df['mask'].
    :return: DataFrame containing the friction velocity (ustar).
    """
    C = C if C is not None else init_cp1_const()
    mask = mask if mask is not None else df["mask"]

    # formula: ustar = v1 / (cov0 + (1 / k) * (log(z1 / z0) - psim10))
    ustar = df.loc[mask, "v1"] / (
        C["cov0"] + (1 / C["k"]) * (np.log(dfin.loc[mask, "z1"] / z0) - psim10)
    )

    return ustar  # pd.DataFrame({'ustar': ustar})


def rugvent(dfin, df, C=None, mask=None):
    """
    Calculate the roughness length for wind (z0 in meters).
    Refer to FORAND (1995) and MESTAYER (1996).

    :param df: DataFrame containing the columns 'us0', 'psim10', 'tc1', 'tc0', 'opensea', 'z1', and 'v1'.
    :param C: Dictionary containing physical constants. If None, uses init_cp1_const().
    :param mask: Boolean mask to select rows for calculation. If None, uses df['mask'].
    :return: DataFrame containing the friction velocity (ustar) and (z0)
    """
    C = C if C is not None else init_cp1_const()
    mask = mask if mask is not None else df["mask"]

    # Calculate the kinematic viscosity of air as a function of temperature
    # Linear regression based on Garratt's values
    # formula: nu = ((0.009267 * ((tc1 + tc0) / 2)) + 1.3458) * 1e-5
    nu = (
        (0.009267 * ((dfin.loc[mask, "tc1"] + dfin.loc[mask, "tc0"]) / 2)) + 1.3458
    ) * 1e-5

    # Determine the Charnock constant
    alfc = np.where(dfin.loc[mask, "opensea"], C["alfcpm"], C["alfccot"])

    # formula: z0 = (0.11 * nu / us0) + (alfc * us0^2) / g
    z0 = (0.11 * nu / df.loc[mask, "us0"]) + (alfc * df.loc[mask, "us0"] ** 2) / C["g"]

    # formula: ustar = v1 / (cov0 + (1 / k) * (log(z1 / z0) - psim10))
    ustar = df.loc[mask, "v1"] / (
        C["cov0"]
        + (1 / C["k"]) * (np.log(dfin.loc[mask, "z1"] / z0) - df.loc[mask, "psim10"])
    )

    return z0, ustar  # pd.DataFrame({'ustar': ustar, 'z0': z0})


def thqstar(dfin, df, C=None, mask=None):
    """
    Calculate the scaling parameters ths and qs
    from meteorological measurements, calculated roughness lengths, and the value
    of the psih function at altitude z1.

    :param df: DataFrame containing the columns 'psih1', 'z0q', 'z0t', 'th1', 'th0', 'q1', 'q0', and 'z1'.
    - psih1: valeur de la fonction psih à l'altitude z1
    - z0q: longueur de rugosité en humidité en m
    - z0t: longueur de rugosité en température en m
    - th1: température potentielle à la hauteur z1
    - th0: température potentielle à la surface
    - q1: humidité spécifique à la hauteur z1
    - q0: humidité spécifique à la surface
    - z1: hauteur en mètres
    :param C: Dictionary containing physical constants. If None, uses init_cp1_const().
    :param mask: Boolean mask to select rows for calculation. If None, uses df['mask'].
    :return: DataFrame containing the scaling parameters ths and qs.
    """
    C = C if C is not None else init_cp1_const()
    mask = mask if mask is not None else df["mask"]

    dft = pd.DataFrame(index=df.index)
    dft.loc[mask, ["th1", "th0", "q1", "q0"]] = cp_thermodyn(dfin.loc[mask], C=C)[
        ["th1", "th0", "q1", "q0"]
    ]
    # formula: ths = (th1 - th0) * k / (log(z1 / z0t) - psih1)
    vint_ths = (
        np.log(dfin.loc[mask, "z1"] / df.loc[mask, "z0t"]) - df.loc[mask, "psih1"]
    )
    ths = (dft.loc[mask, "th1"] - dft.loc[mask, "th0"]) * C["k"] / vint_ths

    # formula: qs = (q1 - q0) * k / (log(z1 / z0q) - psih1)
    vint_qs = np.log(dfin.loc[mask, "z1"] / df.loc[mask, "z0q"]) - df.loc[mask, "psih1"]
    qs = (dft.loc[mask, "q1"] - dft.loc[mask, "q0"]) * C["k"] / vint_qs

    return pd.DataFrame(
        {"ths": ths, "qs": qs}
    )  # with consistent index relative to dfin and mask


def cp_lmo(dfin, df, C=None, mask=None, reltol=1e-4):
    """
    :return: DataFrame containing the Monin-Obukhov length(lmo), based on zeta(z1) loop

    :param z0: longueur de rugosité en m
    :param z0t: longueur de rugosité en température en m
    :param z1: hauteur en mètres
    :param ribz1: nombre de Richardson 'BULK' (BRN = Bulk Richardson number)
    :return: ermax, erreur maximum liée à l'itération (ermax < 0,1%)
    """
    C = C if C is not None else init_cp1_const()
    m0 = mask if mask is not None else df["mask"]
    if isinstance(m0, list):
        m0 = np.array(m0, dtype=bool)
    ma = m0.copy()
    # un mask mi est également utilisé pour limiter les recalculs au fur et à mesure des itérations
    # initialize riz1 as ribz1, and rap as 0.1
    dfi = (
        df.loc[m0, ["ribz1"]]
        .copy()
        .rename(columns={"ribz1": "riz1"})
        .assign(lmo=0.0, zetaz1=0.0, psih=0.0, psim=0.0, nbiter=0, err=1.0, rap=0.1)
    )

    isstable = (
        df.loc[m0, "ribz1"] >= 0
    )  # Masque de stabilité, masque de calculs selon Stable ou non
    m1 = dfi["err"].abs() > reltol
    while any(m1):  # ie while dfi['err'].abs().max(skipna=True) > reltol:
        ma.loc[m0] = m1
        ms, mu = m1 & isstable, m1 & ~isstable
        dfi.loc[m1, "nbiter"] += 1  # Add 1 to nbiter where iter is False
        dfi.loc[m1, "riz1"] = dfi.loc[m1, "riz1"] / dfi.loc[m1, "rap"]
        # Calc zetaz1 as either riz1 or the maximum of the roots of the polynomials - STABLE CASE (II-21)
        dfi.loc[mu, "zetaz1"] = dfi.loc[mu, "riz1"]  # UNSTABLE CASE (II-20)
        # OK : dfi.loc[ms, 'zetaz1'] = dfi.loc[ms, 'riz1'].apply(lambda riz1: max(np.roots([1, (1 - (1+C['cophist']) * riz1), -riz1])))
        # Ou OK : Equivalent polynomial instruction np.polynomial.Polynomial([-riz1, (1 - 7 * riz1), 1]).roots()
        # In fine, cp_pol2quadratic, juste pour éviter la boucle sur pandas.map ou numpy.vectorize
        dfi.loc[ms, "zetaz1"] = cp_pol2quadratic(dfi.loc[ms, "riz1"], C["cophist"])
        _, _, dfi.loc[m1, "psih"], dfi.loc[m1, "psim"] = cp_phipsi(
            dfin.loc[ma, "z1"], dfin.loc[ma, "z1"] / dfi.loc[m1, "zetaz1"], C=C
        )
        ribc = (
            dfi.loc[m1, "zetaz1"]
            * (
                np.log(dfin.loc[ma, "z1"] / df.loc[ma, "z0t"])
                - dfi.loc[mu | ms, "psih"]
            )
            / (
                (
                    np.log(dfin.loc[ma, "z1"] / df.loc[ma, "z0"])
                    - dfi.loc[mu | ms, "psim"]
                )
                ** 2
            )
        )
        dfi.loc[m1, "rap"] = ribc / df.loc[ma, "ribz1"]
        dfi.loc[m1, "err"] = (ribc - df.loc[ma, "ribz1"]) / df.loc[ma, "ribz1"]
        m1.loc[m1] = (
            dfi.loc[m1, "err"].abs() > reltol
        )  # Nb : np.nan > reltol = False => ok even if nan

    dfi["lmo"] = dfin.loc[m0, "z1"] / dfi["zetaz1"]
    return dfi


def cp_h13zinfhvag(dfin, df, C=None, mask=None):
    """
    Calcul des valeurs absentes de H1/3 à partir du vent U(19.5 m)
        et des paramètres de opensea
    Calcul par définition de
    - zinf = C['coup'] * H1/3 = 1.0 * H1/3
    - hvag = C['hvag'] * H1/3 = 0.65 * H1/3
    à partir des dataframe cp_calc issus des calculs de clso
    """
    C = C if C is not None else init_cp1_const()
    mask = mask if mask is not None else df["mask"]

    dfh = pd.DataFrame(index=dfin[mask].index).assign(h13=0.0, zinf=0.0, hvag=0.0)

    mhpos = mask & (dfin["H13ini"] > 0)  # on ne calcule que les h13 non connus

    dfh.loc[mhpos, "h13"] = dfin.loc[mhpos, "H13ini"]

    _, _, _, _, _, v195 = cp_phipsival(19.5, dfin, df, C=C, mask=~mhpos)

    dfh.loc[~mhpos & dfin["opensea"], "h13"] = C["ppos"] * (v195**2)
    dfh.loc[~mhpos & ~dfin["opensea"], "h13"] = C["ppv"] * v195 + C["ordov"]
    dfh["zinf"] = C["coup"] * dfh["h13"]
    dfh["hvag"] = C["hvag"] * dfh["h13"]
    dfh["zrefm1"] = C["zrefM1"] + 0.0 * dfh["hvag"]  # as a minimum ref z for all duct

    return dfh  # ['h13', 'zinf', 'hvag', 'zrefm1']


def cp_profilz(zinf=None, zc=None, nbpts=100, zmax=200, step=0.05):
    """
    Generate a vertical profile vector with a combination of linear and logarithmic spacing.

    Parameters
    ----------
    zinf, zc : float
        The lower bound and critical values to be included in the profile.
    zc : float
        The critical value to be included in the profile.
    zmax : float, optional
        The maximum value of the profile (default is 200).
    step : float, optional
        The step size for the initial linear spacing (default is 0.05).

    Returns
    -------
    cpz : ndarray
        A 1D array of 100 points, with a combination of linear and logarithmic spacing,
        including the values zinf and zc.
    """
    # Generate 100 linearly spaced points from 0 to 1 with a step of 0.01
    linear_part = np.linspace(1, nbpts, nbpts)
    # Generate 99 logarithmically spaced points from 1 to zmax
    log_part = np.logspace(0, np.log10(nbpts), nbpts)
    # Combine the linear and logarithmic parts
    cpz = step * linear_part + (log_part - 1) * (zmax - step * linear_part) / (nbpts - 1)

    # Replace the values closest to zinf and zc with zinf and zc
    if zinf is not None:
        cpz[np.argmin(np.abs(cpz - zinf))] = zinf
    if zc is not None:
        cpz[np.argmin(np.abs(cpz - zc))] = zc
    # cpz = np.insert(cpz, 0, 0.01)
    return cpz


def cp_phipsival(z, dfin, df, C=None, mask=None):
    """
    z >= max(z0, z0t, z0q)
    Calcul des valeurs absolues des paramètres x(z) = th(z), q(z) et u(z)
    et des gradients associés qx(z) = qth(z), gq(s) et gu(z)
    à partir des variables x(0), x(s) et des lois cp_phipsi
    """
    C = C if C is not None else init_cp1_const()
    mask = (
        mask if mask is not None else df["mask"]
    )  # devrait toujours avoir un nb raisonnable
    z = (
        z if z is not None else df.loc[mask, "zc"].values
    )  # et non xp_profilz = 100 points par défaut
    lmo = df.loc[mask, "lmo"].copy().values
    if np.isscalar(z):
        z = np.full_like(lmo, z)

    try:  # déjà fait dans phipsi => facultatif, mais j'aime bien remonter l'erreur à la source
        zeta = z / lmo
    except Exception as e:
        raise ValueError(
            "z and lmo must be compatible for elementwise division: " + str(e)
        )

    # Do not use inside calculation loops:
    # maxz0 = df.loc[mask, ['z0', 'z0t', 'z0q']].max(axis=1)
    # z = np.maximum(z, maxz0)

    phih, phim, psih, psim = cp_phipsi(zeta * lmo, z / zeta, C=C)  # for dims <=> z, lmo
    # gradients
    gthz = (df.loc[mask, "ths"] / (C["k"] * z)) * phih
    gqz = (df.loc[mask, "qs"] / (C["k"] * z)) * phih
    guz = (df.loc[mask, "us"] / (C["k"] * z)) * phim
    # valeurs np.maximum(z , df.loc[mask, 'z0t'] )
    thz = df.loc[mask, "th0"] + (df.loc[mask, "ths"] / C["k"]) * (
        np.log(z / df.loc[mask, "z0t"]) - psih
    )  # z >= z0t > 0
    qz = df.loc[mask, "q0"] + (df.loc[mask, "qs"] / C["k"]) * (
        np.log(z / df.loc[mask, "z0q"]) - psih
    )  # z >= z0q > 0
    uz = df.loc[mask, "us"] * (
        C["cov0"] + (1 / C["k"]) * (np.log(z / df.loc[mask, "z0"]) - psim)
    )  # v(z0)=0 ; z >= z0 > 0

    return gthz, gqz, guz, thz, qz, uz


def cp_hleval(zstr, dfin, df, C=None, mask=None):
    """
    h level PTUM(z) - horizontal  profiles - thermodynamic calculations
    dfin = cp1 metoc inputs
    df = cp1 clso calculation results
    """
    # check zstr is in df.colums ('h13' | 'zc' | 'z1ref' | ... or any column in meters above sea level within df pandas dataframe)
    if zstr not in df.columns:
        raise ValueError(f"The column '{zstr}' does not exist in the dataframe 'df'.")
    C = C if C is not None else init_cp1_const()
    m0 = mask if mask is not None else df["mask"]
    z = df.loc[m0, zstr]

    dft = cp_thermodyn(
        dfin.loc[m0], C=C
    )  # dfthermody, because we need p1, dpdz, hr0, th0, ... not necessarily saved within df
    dfp = pd.DataFrame(index=df.loc[mask].index).assign(
        maxz0=0.0, thzinf=0.0, qzinf=0.0, uzinf=0.0, gthzinf=0.0, gqzinf=0.0, guzinf=0.0
    )
    # monolevel h [m] calculations associated with clso-lmo results
    phih, phim, psih, psim = cp_phipsi(z, df.loc[m0, "lmo"], C=C)
    # valeurs np.maximum(z , df.loc[mask, 'z0t'] )
    thz = dft["th0"] + (df.loc[m0, "ths"] / C["k"]) * (
        np.log(z / df.loc[m0, "z0t"]) - psih
    )
    thzc = thz - 273.15
    qz = dft["q0"] + (df.loc[m0, "qs"] / C["k"]) * (
        np.log(z / df.loc[m0, "z0q"]) - psih
    )
    uz = df.loc[m0, "us"] * (
        C["cov0"] + (1 / C["k"]) * (np.log(z / df.loc[m0, "z0"]) - psim)
    )
    # atm pressure, water partial pressure, tk, saturated vapor pressure and rh
    pz = dft["p1"] + dft["dpdz"] * (z - dfin.loc[m0, "z1"])
    ez = qz * pz / (qz * (1 - C["mu"]) + C["mu"])
    tkz = thz / np.power((1000 / pz), C["gam"])
    tcz = tkz - 273.15
    esz = np.exp(19.32 - 4223 / (tcz + 273.15 - 32))  # @IAM: ^^
    hrz = np.minimum(100, np.minimum(dft["hr0"], 100 * ez / esz))  # @IAM: /!\/!\
    # coindices N and modified coindices M - cf. ITU
    Nz = cp_indiceN(pz, tkz, qz, C=C)
    Mz = Nz + 0.157 * z
    # dndz, dMdz
    c1, c2, c3 = cp_gradN(pz, tkz, qz, dft["dpdz"], C=C)
    dNdz = c1 + (phih / (C["k"] * z)) * (c2 * df.loc[m0, "qs"] + c3 * df.loc[m0, "ths"])
    dMdz = dNdz + 0.157
    # columns = ['z', 'pz','tz', 'qz', 'uz', 'tkz', 'tcz', 'Hz', 'Nz', 'indMz']

    return z, pz, tcz, hrz, uz, Nz, Mz, ez, esz, thz, tkz, qz, hrz, dNdz, dMdz


def cp_profileval(z, dfin, df, C=None, mask=None):
    """
    profile PTUM(z) - vertical profiles - thermodynamic calculations
    """
    C = C if C is not None else init_cp1_const()
    m0 = (
        mask if mask is not None else df["mask"]
    )  # devrait toujours avoir un nb raisonnable @IAM: Only one
    z0 = (
        z.copy() if z is not None else cp_profilz()
    )  # et non cp_profilz = 100 points par défaut

    lmo = df.loc[m0, "lmo"].copy().values
    vlmo = np.array(lmo)
    vz = np.array(z)
    vindex = dfin[m0].index
    dftherm = cp_thermodyn(dfin.loc[m0], C=C)  # need p1, dpdz, hr0

    dfp = pd.DataFrame(index=df.loc[mask].index).assign(
        maxz0=0.0, thzinf=0.0, qzinf=0.0, uzinf=0.0, gthzinf=0.0, gqzinf=0.0, guzinf=0.0
    )
    # Test sur l'altitude du calcul
    dfp["maxz0"] = df.loc[mask, ["z0", "z0t", "z0q"]].max(
        axis=1
    )  # sous cette hauteur, cst...
    # Calcul de thetav, q, u et de leurs gradients à l'altitude zinf = coup*h13
    # zetainf = df.loc[mask, 'zinf'] / df.loc[mask, 'lmo']
    (
        dfp["gthzinf"],
        dfp["gqzinf"],
        dfp["guzinf"],
        dfp["thzinf"],
        dfp["qzinf"],
        dfp["uzinf"],
    ) = cp_phipsival(df.loc[mask, "zinf"], dfin, df, C=C, mask=mask)

    for i in range(len(df.loc[m0])):
        dfi = df.loc[m0].iloc[i]  # clso calculation results
        dfm = dfin.loc[m0].iloc[i]  # metoc inputs
        dft = dftherm.iloc[i]  # thermodynamic calculation results
        dfl = dfp.iloc[i]  # profiles properties
        z = z0.copy()
        z = np.maximum(
            z, dfl["maxz0"]
        )  # No real values under z0 except for constant PTU

        phih, phim, psih, psim = cp_phipsi(z, dfi.loc["lmo"], C=C)
        # gradients
        gthz = (dfi["ths"] / (C["k"] * z)) * phih
        gqz = (dfi["qs"] / (C["k"] * z)) * phih
        guz = (dfi["us"] / (C["k"] * z)) * phim
        # valeurs np.maximum(z , df.loc[mask, 'z0t'] )
        thz = dfi["th0"] + (dfi["ths"] / C["k"]) * (
            np.log(z / dfi["z0t"]) - psih
        )  # z >= z0t > 0
        qz = dfi["q0"] + (dfi["qs"] / C["k"]) * (
            np.log(z / dfi["z0q"]) - psih
        )  # z >= z0q > 0
        uz = dfi["us"] * (
            C["cov0"] + (1 / C["k"]) * (np.log(z / dfi["z0"]) - psim)
        )  # v(z0)=0 ; z >= z0 > 0

        # Additional calculations for option "linear part of profile" # @IAM: not used by now
        # thz = dfl['thzinf'] + dfl['gthzinf'] * (z - dfi['zinf'])
        # tz = thz - 273.15
        # qz = dfl['qzinf'] + dfl['gqzinf'] * (z - dfi['zinf'])
        # uz = dfl['uzinf'] + dfl['guzinf'] * (z - dfi['zinf'])
        #
        # qzinf = (z < dfi['zinf'])
        thz = dfi["th0"] + (dfi["ths"] / C["k"]) * (np.log(z / dfi["z0t"]) - psih)
        tz = thz - 273.15
        qz = dfi["q0"] + (dfi["qs"] / C["k"]) * (np.log(z / dfi["z0q"]) - psih)
        uz = dfi["us"] * (C["cov0"] + (1 / C["k"]) * (np.log(z / dfi["z0"]) - psim))

        # atm pressure, water partial pressure, tk, saturated vapor pressure and rh
        pz = dft["p1"] + dft["dpdz"] * (z - dfm["z1"])
        ez = qz * pz / (qz * (1 - C["mu"]) + C["mu"])
        tkz = thz / np.power((1000 / pz), C["gam"])
        tcz = tkz - 273.15
        esz = np.exp(19.32 - 4223 / (tcz + 273.15 - 32))
        hrz = np.minimum(100, np.minimum(dft["hr0"], 100 * ez / esz))  # @IAM: /!\/!\
        # coindices N and modified coindices M - cf. ITU
        Nz = cp_indiceN(pz, tkz, qz, C=C)
        Mz = Nz + 0.157 * z
        # dndz, dMdz
        # c1, c2, c3 = cp_gradN(pz, tkz, qz, p1dpdz.loc[m1, 'dpdz'], C=C)
        # dNdz = c1 + (phih / (C['k'] * z)) * (c2 * dfi['qs'] + c3 * dfi['ths'])
        # dMdz = dNdz + 0.157
        # columns = ['z', 'tz', 'qz', 'uz', 'pz', 'tkz', 'tcz', 'Hz', 'Nz', 'indMz']
    return z, pz, ez, esz, thz, tkz, qz, hrz, Nz, Mz


### Just few useful plots
def cp_profileplot(qindprof, dfin, df, C):
    """
    Plots meteorological profiles for a given profile index.

    Parameters:
    qprof (int): Profile index to plot.
    dfin (DataFrame): Input dataframe containing initial data.
    df (DataFrame): Dataframe containing calculated data.
    C (object): Configuration or constants used in profile calculations.

    Returns:
    None: Displays the plots of meteorological profiles.
    """
    # Example usage: cp_profileplot(qprof=0, dfin=dfin, df=dfcalc, C=CPC)
    mi0, _, _ = cp_bool2pos2ind(df, mask_ind=[qindprof])
    if not mi0.any():
        warnings.warn(f"{qindprof} is not an index of the dataframe")
    else:
        z, pz, ez, esz, thz, tkz, qz, hrz, Nz, Mz = cp_profileval(
            z=cp_profilz(nbpts=50, zmax=100), dfin=dfin, df=df, C=C, mask=mi0
        )

        fig, axs = plt.subplots(1, 3, figsize=(15, 8))

        # First plot: z(pz) and z(hrz) with secondary x-axis
        ax1 = axs[0]
        ax2 = ax1.twiny()
        ax1.plot(pz, z, "b-", label="pz")
        ax2.plot(hrz, z, "r--", label="hrz")

        ax1.set_xlabel("atm. pressure pz [hPa]")
        ax1.set_ylabel("z [m] above sea level")
        ax1.set_title(f"#{qindprof} met profiles: z(pz) and z(hrz)")
        ax2.set_xlabel("hrz")

        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")

        # Second plot: z(thz) and z(tkz)
        axs[1].plot(thz, z, label="thz")
        axs[1].plot(tkz, z, label="tkz")
        axs[1].set_xlabel("thz / tkz")
        axs[1].set_ylabel("z [m] above sea level")
        axs[1].set_title(f"#{qindprof} met profiles: z(thz) and z(tkz)")
        axs[1].legend()

        # Third plot: z(Nz) and z(Mz)
        axs[2].plot(Nz, z, label="Nz")
        axs[2].plot(Mz, z, label="Mz")
        axs[2].set_xlabel("coindices Nz / Mz")
        axs[2].set_ylabel("z [m] above sea level")
        axs[2].set_title(f"#{qindprof} met profiles: z(Nz) and z(Mz)")
        axs[2].legend()

        plt.tight_layout()
        plt.show()

        # Reference
        today_date = datetime.today().strftime("%Y-%m-%d")
        print(f"@IAMiki, CP1, {today_date}")

        return


def cp_bool2pos2ind(df, mask_bool=None, mask_pos=None, mask_ind=None):
    """
    Convert a mask provided in one of three forms (boolean, positions, or indices) to all three standard forms.

    Parameters:
    df (pd.DataFrame): Input dataframe with a long integer index.
    mask_bool (np.ndarray or pd.Series, optional): Boolean mask.
    mask_pos (np.ndarray or list, optional): Mask as positions.
    mask_ind (np.ndarray or list, optional): Mask as indices.

    Returns:
    tuple: (mi, pi, ii) where mi is the boolean mask, pi is the positions mask, and ii is the indices mask.

    Example:
    >>>data = {'v1': [10, 20, 30, 40, 50]}
    >>>index = [0, 1, 8, 22, 135]
    >>>df = pd.DataFrame(data, index=index)
    >>>mask_bool = df['v1'] > 20
    >>>mi, pi, ii = df_bool2pos2ind(df, mask_bool=mask_bool)
    """

    if mask_bool is not None:
        try:
            # Convert boolean mask to positions and indices
            mi = mask_bool
            pi = np.where(mask_bool)[0]
            ii = df.index[mask_bool]
        except Exception as e:
            if len(mask_bool) != len(df):
                raise ValueError(
                    f"The boolean mask must have the same dimension as the dataframe (expected {len(df)} elements)."
                )
            raise ValueError(f"Error with boolean mask: {e}")
    elif mask_pos is not None:
        try:
            # Convert positions mask to boolean and indices
            mi = np.zeros(len(df), dtype=bool)
            mi[mask_pos] = True
            pi = mask_pos
            ii = df.index[mask_pos]
        except Exception as e:
            if not all(0 <= pos < len(df) for pos in mask_pos):
                raise ValueError(
                    f"All position indices must be between 0 and {len(df) - 1}."
                )
            raise ValueError(f"Error with positions mask: {e}")
    elif mask_ind is not None:
        try:
            if len(mask_ind) != len(set(mask_ind)):
                raise ValueError("The index mask should contain unique values.")
            # Convert indices mask to boolean and positions
            mi = df.index.isin(mask_ind)
            pi = np.where(mi)[0]
            ii = mask_ind
        except Exception as e:
            if not all(ind in df.index for ind in mask_ind):
                raise ValueError(
                    "All indices in the index mask must correspond to the dataframe's index."
                )
            raise ValueError(f"Error with index mask: {e}")
    else:
        raise ValueError("One of mask_bool, mask_pos, or mask_ind must be provided.")

    return mi, pi, ii


def cp_dim(a, b):
    if np.isscalar(a):
        if isinstance(b, np.ndarray):
            return np.full_like(b, a)
        elif isinstance(b, pd.Series):
            return pd.Series(np.full_like(b.values, a))
        elif isinstance(b, list):
            return [a] * len(b)
        else:
            return a
    elif isinstance(a, np.ndarray) and a.size == 1:
        if isinstance(b, np.ndarray):
            return np.full_like(b, a.item())
        elif isinstance(b, pd.Series):
            return pd.Series(np.full_like(b.values, a.item()))
        elif isinstance(b, list):
            return [a.item()] * len(b)
        else:
            return a.item()
    elif isinstance(a, pd.Series) and a.size == 1:
        if isinstance(b, np.ndarray):
            return np.full_like(b, a.item())
        elif isinstance(b, pd.Series):
            return pd.Series(np.full_like(b.values, a.item()))
        elif isinstance(b, list):
            return [a.item()] * len(b)
        else:
            return a.item()
    else:
        return a


### For timeit results encourage NOT to use panda map/applymap with np.roots
def cp_pol2quadratic(s, cophist=6):
    """
    Solves a quadratic equation of the form x^2 + (1-7s)x - s = 0 for an array of values s.
    param: s
    param: cophist = C['cophist'] = 6 [according to Kondo 1975]
    Returns an array of the maximum values of the real solutions.
    """
    # discr toujours positif donc pas besoin : s = np.full(s.shape, np.nan)
    d = 4 * s + (1 - (1 + cophist) * s) ** 2
    s1 = (-1 + (1 + cophist) * s + np.sqrt(d)) / 2
    # s2 = (-1+(1+cophist)*s - np.sqrt(d))/2
    return s1  # , s2


def cp_pol3cubic(s2, cophiun=20):
    """
    solve bubic polynomial equation (a=cophiun) x^3 + (b=-1) x^2 + (c=0) x + (d=s^2)) = 0
    return the only x solution for CP1

    Paramètres:
    a (np.ndarray): Scalaire cophiun.
    d (np.ndarray): Vecteur des coefficients sqrt(s).

    Retourne:
    x (np.ndarray): Vecteur des solutions x.
    discr (np.ndarray): Vecteur des discriminants.

    Examples:
    cp_cubic(0, 20) # 0.05
    x1, x2, x3, det = cp_pol3cubic(np.array([0, 1e-4, 10]), 20)
    x1, x2, x3, det = cp_pol3cubic(pd.Series(np.array([0, 1e-4, 10])), 20)
    coefficients = [20, -1, 0, 1e-4]
    roots = np.roots(coefficients)
    """
    a, b, c = -1. / cophiun, 0, s2 / cophiun
    p = np.atleast_1d(np.full_like(s2, b - a**2 / 3))
    q = np.atleast_1d(2 * a**3 / 27 - a * b / 3 + c)

    # Initialiser les vecteurs de sortie
    r1, r2, r3 = (np.full_like(s2, np.nan) for _ in range(3))

    # passage en x^3+p*x+q = 0
    det = q**2 / 4 + p**3 / 27

    # Masque pour les discriminants
    pos = det > 0

    if any(pos):
        # Pour det > 0 # 3 real distinct solutions
        u = np.cbrt(-q[pos] / 2 + np.sqrt(det[pos]))
        v = np.cbrt(-q[pos] / 2 - np.sqrt(det[pos]))
        r1[pos] = u + v
        r2[pos] = (-q[pos] / 2 + det[pos] ** 0.5) ** (1 / 3) + (
            -q[pos] / 2 - det[pos] ** 0.5
        ) ** (1 / 3)
        r3[pos] = np.conj(r2[pos])

    if any(~pos):
        # Pour det <= 0 # 1 real distinct solution
        r = np.sqrt(-p[~pos] ** 3 / 27)
        t = np.arccos(-q[~pos] / 2 / r)
        r = np.cbrt(r)
        r1[~pos] = 2 * r * np.cos(t / 3)
        r2[~pos] = 2 * r * np.cos((t + 2 * np.pi) / 3)
        r3[~pos] = 2 * r * np.cos((t + 4 * np.pi) / 3)

    # xi final = ri - a/3
    x1, x2, x3 = r1 - a / 3, r2 - a / 3, r3 - a / 3
    minx = np.nanmin(
        np.array([x1, x2, x3]), axis=0
    )  # unstables cases <=> lmo <0 => zc < 0

    return minx  # , x1, x2, x3 , det


############################# UTILS
# for future integration of ISO 80000
def format_ndigits_pow_of_3(x, n):
    """Formate selon une notation scientifique (X.10^n noté Xen)
    selon des puissances entières de 3"""
    if x == 0:
        return "0"
    exponent = int(np.floor(np.log10(abs(x)) / 3) * 3)
    mantissa = x / (10**exponent)
    if exponent == 0:
        return f"{mantissa:.{n}g}"
    return f"{mantissa:.{n}g}e{exponent}"


def df_sci_formatted(df2print, n):
    """Formate l'affichage d'un dataframe selon :
    - une notation scientifique en 10^3.n
    - avec un nombre de chiffres significatif
    Nb : utile pour formatter y compris au sein d'un Nb/jupyter/..."""
    df2print_formatted = df2print.copy()
    float_cols = df2print_formatted.select_dtypes(include=["float"]).columns
    df2print_formatted[float_cols] = df2print_formatted[float_cols].map(
        lambda x: format_ndigits_pow_of_3(x, n)
    )
    return df2print_formatted


def cp_win(df, N=int):
    """
    Partitions (windows) for a DataFrame into N parts (N > 0).

    Parameters:
    df (pd.DataFrame): The input DataFrame to partition.
    N (int): The number of partitions. Must be greater than 0.

    Returns:
    pd.DataFrame: A DataFrame with boolean columns indicating the partition each row belongs to.
    """
    import numpy as np
    import pandas as pd

    N = max(1, N)
    # Create an empty DataFrame with the same index as df
    result = pd.DataFrame(index=df.index)
    M = len(df) // N + 1
    # Create boolean columns w1 to wN
    for i in range(N):
        col_name = f"w{i+1}"
        result[col_name] = (df.index // M) == i

    return result
