import logitmodel
import lh


def main():
    theta = [1.20e-3, 1.10e-3]
    eta = [2.50e-3, 1.10e-3]
    CL = ['s1', 's2']  # customr list
    CV = [20, 80]  # customer value of time
    CAT = {'s1': [0.9, 2.75], 's2': [0.6, 1.75]}  # customer access time
    CExP = {'s1': [0, 0], 's2': [0, 0]}  # customer extra price
    # transportation time list [HSR transportation time, Air transportation
    # time]
    TL = [5, 2]
    CostL = [20, 100]

    Lamda=0.1
    TotalDemand=1000
    expDemand = [Lamda*TotalDemand, (1-Lamda)*TotalDemand]
    HSR = list(range(300, 1000, 5))  # HSR price list
    AIR = list(range(400, 1500, 5))  # Air price list
    HSRPayoff, AIRPayoff = logitmodel.payoffMatrix(HSR, AIR, TL, CostL, expDemand, CL,
                                                   CV, CExP, CAT, theta, eta, isHSRPlayer1=True)
    result = lh.lemkeHowson(HSRPayoff, AIRPayoff)
    HSREquPrice=[HSR[i] for i in range(len(result[0])) if result[0][i]==1][0]
    HSR_index=[i for i in range(len(result[0])) if result[0][i]==1][0]
    AIREquPrice=[AIR[i] for i in range(len(result[1])) if result[1][i]==1][0]
    AIR_index=[i for i in range(len(result[1])) if result[1][i]==1][0]
    """
    determine demand
    """
    eq_tprice,eq_ttime=logitmodel.totalTimePrice([HSREquPrice,AIREquPrice],TL,CL,CExP,CAT)
    eq_utility=logitmodel.UtilityFunction(eq_tprice, eq_ttime,CL,CV)
    eq_demand=logitmodel.DemandFunction(CL,expDemand, eq_utility, theta, eta)
    eq_marketshare=logitmodel.MarketShare(CL,eq_utility, theta)
    HSR_market=dict(zip(CL,[eq_demand[s]*eq_marketshare[s][0] for s in CL]))
    AIR_market=dict(zip(CL,[eq_demand[s]*eq_marketshare[s][1] for s in CL]))
    print(HSREquPrice,AIREquPrice)
    print(HSRPayoff.getItem(HSR_index,AIR_index),AIRPayoff.getItem(HSR_index,AIR_index))
    print("HSR Market Share",HSR_market)
    print("AIR Market Share",AIR_market)

if __name__ == "__main__":
    main()
