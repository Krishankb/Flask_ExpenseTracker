def getMin(arr, N):
    minInd = 0
    for i in range(1, N):
        if (arr[i] < arr[minInd]):
            minInd = i
    return minInd

def getMax(arr, N):
    maxInd = 0
    for i in range(1, N):
        if (arr[i] > arr[maxInd]):
            maxInd = i
    return maxInd

def minCashFlowRec(amount, N, debt):

    mxCredit = getMax(amount, N)
    mxDebit = getMin(amount, N)

    if (amount[mxCredit] == 0 and amount[mxDebit] == 0):
        return 0

    mn = min(-amount[mxDebit], amount[mxCredit])
    amount[mxCredit] -= mn
    amount[mxDebit] += mn

    debt[mxDebit][mxCredit] = mn

    minCashFlowRec(amount, N, debt)

def minCashFlow(graph, N, debt):

    amount = [0 for i in range(N)]

    for p in range(N):
        for i in range(N):
            amount[p] += (graph[i][p] - graph[p][i])

    minCashFlowRec(amount, N, debt)
