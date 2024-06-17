import numpy
from quadprog import solve_qp
import scipy
from matplotlib import pyplot as plt
import numpy as np
import cvxpy as cp
from scipy.optimize import minimize
from cvxopt import matrix, solvers
from pyomo.environ import *
import analyzer
from analyzer import tech_support


def get_sorted_dict_time(sort_user_id):
    dict_time={'2023-11-01': {'2022252207': 0.4999179351563939, '2561744167': 0.627276267265399, '5821279480': 0.5610765797154476, '7109370363': 0.784448038446263, '1595443924': 0.7137213000000552, '7239083016': 0.7088643414269123, '1783497251': 0.6366826931859616}}
    # dict_time={'2023-10-16': {'2022252207': 0.6000092922040725, '2561744167': 0.5928956534866884, '5821279480': 0.4848288602373373, '7109370363': 0.6792619270564006, '1595443924': 0.7752890493678434, '7239083016': 0.6804775543834852, '1783497251': 0.7093564720893181}}
    # dict_time = {'2023-10-01': {'2022252207': 0.552651113948973, '2561744167': 0.6008581478693906,
    #                             '5821279480': 0.5738377038384218, '7109370363': 0.710904152986947,
    #                             '1595443924': 0.8083277594245356, '7239083016': 0.6795840097687782,
    #                             '1783497251': 0.6825808760786612},
    #              '2023-09-16': {'2022252207': 0.6100529832408768, '2561744167': 0.6071422663335075,
    #                             '5821279480': 0.5719417412401707, '7109370363': 0.6696638025996607,
    #                             '1595443924': 0.6589907092930617, '7239083016': 0.6944493598683641,
    #                             '1783497251': 0.6594582686218584},
    #              '2023-09-01': {'2022252207': 0.5685347894433006, '2561744167': 0.6045270016322508,
    #                             '5821279480': 0.5452230344330624, '7109370363': 0.6366051686697941,
    #                             '1595443924': 0.5771693677845203, '7239083016': 0.6533988873101869,
    #                             '1783497251': 0.6788740313613554},
    #              '2023-08-16': {'2022252207': 0.601565806467557, '2561744167': 0.5982206207923645,
    #                             '5821279480': 0.5239878860811674, '7109370363': 0.655859087952008,
    #                             '1595443924': 0.5824143675994357, '7239083016': 0.5745106966401501,
    #                             '1783497251': 0.5296536682327806},
    #              '2023-08-01': {'2022252207': 0.6483830346930366, '2561744167': 0.7081364666288095,
    #                             '5821279480': 0.5941668300891308, '7109370363': 0.7371603026961917,
    #                             '1595443924': 0.7270600312880214, '7239083016': 0.7661281174050248,
    #                             '1783497251': 0.6652893293010491},
    #              '2023-07-16': {'2022252207': 0.6439330169479647, '2561744167': 0.649233095255323,
    #                             '5821279480': 0.5460082866724272, '7109370363': 0.5716514442897859,
    #                             '1595443924': 0.6628460325390879, '7239083016': 0.6327343093454403,
    #                             '1783497251': 0.8096088266372681},
    #              '2023-07-01': {'2022252207': 0.5933324073326132, '2561744167': 0.6216137176309025,
    #                             '5821279480': 0.5066116190791847, '7109370363': 0.7424314670214157,
    #                             '1595443924': 0.6563964440818612, '7239083016': 0.4901703939901842,
    #                             '1783497251': 0.5935132442777122},
    #              '2023-06-16': {'2022252207': 0.6171841228626438, '2561744167': 0.529494590116441,
    #                             '5821279480': 0.5130255264229324, '7109370363': 0.6666157192888184,
    #                             '1595443924': 0.7194078330470648, '7239083016': 0.5379764346657545,
    #                             '1783497251': 0.6263558104699439},
    #              '2023-06-01': {'2022252207': 0.6010490883474688, '2561744167': 0.6239970200911067,
    #                             '5821279480': 0.4972732697121849, '7109370363': 0.669838766210283,
    #                             '1595443924': 0.6926895081996918, '7239083016': 0.5570943786620931,
    #                             '1783497251': 0.685990571812324},
    #              '2023-05-16': {'2022252207': 0.6407769116356902, '2561744167': 0.6878171268293168,
    #                             '5821279480': 0.4739922469537595, '7109370363': 0.740787055864177,
    #                             '1595443924': 0.5422367394933054, '7239083016': 0.5510330650007719,
    #                             '1783497251': 0.6904641104103801}}

    sorted_dict_time = {}
    sorted_time = sorted(dict_time.keys())
    for time in sorted_time:
        sorted_dict_time[time] = [dict_time[time][str(j)] for j in sort_user_id]
    return sorted_dict_time


def get_matrix(x):
    T = len(x)
    k = len(x[list(x.keys())[0]])
    x_matrix = [[0 for i in range(k)] for j in range(T)]
    idx = 0
    for i in x:
        idy = 0
        for j in x[i]:
            x_matrix[idx][idy] = j
            idy += 1
        idx += 1
    return x_matrix


def get_weight_DeGroot(x):
    T = len(x)
    k = len(x[list(x.keys())[0]])
    n = k
    w = cp.Variable((n, k))
    x_matrix = [[0 for i in range(k)] for j in range(T)]
    idx = 0
    for i in x:
        idy = 0
        for j in x[i]:
            x_matrix[idx][idy] = j
            idy += 1
        idx += 1
    x_matrix = np.array(x_matrix)
    x_matrix = x_matrix.T
    obj = 0
    for t in range(T - 1):
        obj += cp.norm2(x_matrix[:, t + 1] - w @ x_matrix[:, t])
    constraints = [w[i, j] >= 0 for i in range(n) for j in range(n)]

    constraints += [cp.sum(w[i, :]) == 1 for i in range(n)]

    problem = cp.Problem(cp.Minimize(obj), constraints)
    # tech_support(problem)
    problem.solve()
    print(obj.value)
    return w.value


def draw(x_true, x_predict):
    for i in range(len(x_true)):
        plt.plot(x_true[i])
    plt.show()
    for i in range(len(x_true)):
        plt.plot(x_predict[i])
    plt.show()
    for i in range(len(x_true)):
        plt.subplot(len(x_true), 1, i + 1)
        plt.plot(x_true[i])
        plt.plot(x_predict[i])
    plt.show()


def Degroot_draw(sorted_dict_time):
    x_matrix = get_matrix(sorted_dict_time)
    w_ij = get_weight_DeGroot(sorted_dict_time)
    result_weight = np.where(w_ij < 0, 0, w_ij)
    predict_x = np.empty([12, 7])
    predict_x[0] = x_matrix[0]
    x_true = numpy.array(x_matrix).T
    for i in range(1, len(sorted_dict_time)):
        predict_x[i] = result_weight @ predict_x[i - 1]
    x_predict = predict_x.T
    draw(x_true, x_predict)


def FJ_draw(sorted_dict_time):
    x_matrix = get_matrix(sorted_dict_time)
    W, S = get_weight_FJ(sorted_dict_time)
    print(np.around(W, decimals=6), S)
    I = np.eye(7)
    predict_x = np.empty([12, 7])
    predict_x[0] = x_matrix[0]
    x_true = numpy.array(x_matrix).T
    for i in range(1, len(sorted_dict_time)):
        predict_x[i] = S @ (W @ predict_x[i - 1]) + (I - S) @ predict_x[0]
    x_predict = predict_x.T
    draw(x_true, x_predict)


def get_weight_FJ(x):
    T = len(x)
    k = len(x[list(x.keys())[0]])
    n = k
    S = cp.Variable((k, k))
    Y = cp.Variable((k, k))
    I = np.eye(7)
    x_matrix = [[0 for i in range(k)] for j in range(T)]
    idx = 0
    for i in x:
        idy = 0
        for j in x[i]:
            x_matrix[idx][idy] = j
            idy += 1
        idx += 1
    x_matrix = np.array(x_matrix)
    x_matrix = x_matrix.T
    obj = 0

    for t in range(T - 1):
        obj = cp.norm2(x_matrix[:, t + 1] - Y @ x_matrix[:, t] - (I - S) @ x_matrix[:, 0])
    # constraints = [w[i, j] >= 0 for i in range(n) for j in range(n)]
    constraints = [cp.sum(Y[i, :]) == S[i, i] for i in range(n)]
    constraints += [Y >= 0, Y <= 1]
    constraints += [0 <= S, S <= 1]
    constraints += [S[i, j] == 0 for i in range(n) for j in range(n) if i != j]
    objective = cp.Minimize(obj)
    # v = Visual(objective)
    # v.draw_graph()

    problem = cp.Problem(objective, constraints)
    # tech_support(problem)

    problem.solve(solver=cp.CPLEX)
    # print(Y.value)
    # print(S.value)
    S_inv = np.linalg.inv(S.value)
    W = np.dot(S_inv, Y.value)

    return W, S.value


def get_weight_FJ_within(x):
    T = len(x)
    k = len(x[list(x.keys())[0]])
    n = k
    S = cp.Variable((k, k))
    Y = cp.Variable((k, k))
    I = np.eye(7)
    x_matrix = [[0 for i in range(k)] for j in range(T)]
    idx = 0
    for i in x:
        idy = 0
        for j in x[i]:
            x_matrix[idx][idy] = j
            idy += 1
        idx += 1
    x_matrix = np.array(x_matrix)
    x_matrix = x_matrix.T
    obj = 0

    for t in range(T - 1):
        obj = cp.norm2(
            S @ cp.diag(W) @ x_matrix[:, t + 1] - (W - cp.diag(W)) @ x_matrix[:, t] - (I - S) @ x_matrix[:, 0])
    # constraints = [w[i, j] >= 0 for i in range(n) for j in range(n)]
    constraints = [cp.sum(Y[i, :]) == S[i, i] for i in range(n)]
    constraints += [Y >= 0, Y <= 1]
    constraints += [0 <= S, S <= 1]
    constraints += [S[i, j] == 0 for i in range(n) for j in range(n) if i != j]
    objective = cp.Minimize(obj)
    # v = Visual(objective)
    # v.draw_graph()

    problem = cp.Problem(objective, constraints)
    # tech_support(problem)

    problem.solve(solver=cp.CPLEX)
    # print(Y.value)
    # print(S.value)
    S_inv = np.linalg.inv(S.value)
    W = np.dot(S_inv, Y.value)

    return W, S.value


if __name__ == "__main__":
    user_id_list = []
    with open('list_bozhu.txt', 'r', encoding='utf-8') as reader:
        for row in reader:
            user_id_list.append(row.split()[1])
    sort_user_id = sorted(map(int, user_id_list))
    sorted_dict_time = get_sorted_dict_time(sort_user_id)

    print(sorted_dict_time.values())
    # Degroot_draw(sorted_dict_time)
    # print(get_weight_FJ(sorted_dict_time))
    FJ_draw(sorted_dict_time)
    # w_ij, s_ij = get_weight_FJ(sorted_dict_time)
