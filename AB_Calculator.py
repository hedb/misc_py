import math
from scipy.stats import norm


def myLog(m):
    #print(m)
    return


def calc(input):
    A = {}
    B = {}
    A["mean"] = input["A"]["SX"] / input["A"]["N"]
    B["mean"] = input["B"]["SX"] / input["B"]["N"]
    mean_diff = B["mean"]-A["mean"]
    B["lift"] = mean_diff/A["mean"]

    A["var"] = input["A"]["SX2"] / input["A"]["N"] - A["mean"]*A["mean"]
    B["var"] = input["B"]["SX2"] / input["B"]["N"] - B["mean"]*B["mean"]

    myLog('A["var"] : ' + str(A["var"]))
    myLog('B["var"] : ' + str(B["var"]))

    pooled_var = (A["var"]*input["A"]["N"] + B["var"]*input["B"]["N"]) / ( input["A"]["N"] + input["B"]["N"])
    myLog(pooled_var)

    A["SE2"] = pooled_var / input["A"]["N"]
    B["SE2"] = pooled_var / input["B"]["N"]
    combined_se2 = (A["SE2"] + B["SE2"]) if ( (A["SE2"] + B["SE2"])>0 ) else 0.000000001
    myLog(combined_se2)
    combined_se = math.sqrt(combined_se2) if (combined_se2 > 0) else 0.000000001
    myLog("combined_se=" + str(combined_se))

    zCritical =  norm.ppf(1-input["alpha"]/input["tails"])
    myLog(zCritical)

    err = combined_se / A["mean"] * zCritical
    ci = err * zCritical

    raw_z = (mean_diff/combined_se) * input["direction"]
    myLog("raw_z=" + str(raw_z))

    actual_z= abs(raw_z) if (input["tails"] == 2 ) else raw_z
    myLog("actual_z=" + str(actual_z))

    p_val = input["tails"] * (1-norm.cdf(actual_z))

    test_completion =min( (input["MDE"]/ci)**2 ,1 )

    return \
        {
            "A_mean":   A["mean"],
            "B_mean":   B["mean"],
            "lift":     B["lift"],
            "err":      err,
            "ci":       ci,
            "p_val":    p_val,
            "test_completion" : test_completion



        }



if __name__ == "__main__":
    test1 = {
            'A':{'N':19947,'SX':11966,'SX2':11966},
            'B':{'N':3567,'SX':2031,'SX2':2031},
            'tails':1,
            'alpha':.05,
            'direction':1,
            'MDE':.03
        }


    test2 = {
            'A':{'N':12600,'SX':845,'SX2':845},
            'B':{'N':5290,'SX':379,'SX2':379},
            'tails':1,
            'alpha':.05,
            'direction':1,
            'MDE':.03
        }


    test3 = {
            'A':{'N':12600,'SX':12600,'SX2':12600},
            'B':{'N':5290,'SX':10580,'SX2':21160},
            'tails':1,
            'alpha':.05,
            'direction':1,
            'MDE':.03
        }


    test4 = {
            'A':{'N':416479,'SX':16212,'SX2':16212},
            'B':{'N':419157,'SX':16585,'SX2':16585},
            'tails':1,
            'alpha':.05,
            'direction':1,
            'MDE':.03
        }


    print(calc(test4))