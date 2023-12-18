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
    dict_time = {'2023-10-16': {'2022252207': 0.3823641466731407, '2561744167': 0.5034083599499424,
                                '5821279480': 0.4953777614292539, '7109370363': 0.5255707489788671,
                                '1595443924': 0.5898068997542045, '7239083016': 0.5406590245421166,
                                '1783497251': 0.5672839283046082},
                 '2023-10-01': {'2022252207': 0.4102953505835861, '2561744167': 0.5024522611317931,
                                '5821279480': 0.5062888399159378, '7109370363': 0.5649592130894724,
                                '1595443924': 0.7912161200236325, '7239083016': 0.5629888428427622,
                                '1783497251': 0.4835046523184062},
                 '2023-09-16': {'2022252207': 0.42444821614628725, '2561744167': 0.5103435714318713,
                                '5821279480': 0.4634670269164296, '7109370363': 0.547083693949714,
                                '1595443924': 0.5233116734163612, '7239083016': 0.554973945787247,
                                '1783497251': 0.5280920233765012},
                 '2023-09-01': {'2022252207': 0.4382646818976215, '2561744167': 0.5169422044200699,
                                '5821279480': 0.45211381143906987, '7109370363': 0.5030909559398201,
                                '1595443924': 0.4705378067093219, '7239083016': 0.5427423461016949,
                                '1783497251': 0.5078372178490088},
                 '2023-08-16': {'2022252207': 0.4626161850964197, '2561744167': 0.5180928949664072,
                                '5821279480': 0.45338933845758533, '7109370363': 0.5578940319561161,
                                '1595443924': 0.4934347423154331, '7239083016': 0.5267019050217563,
                                '1783497251': 0.3454264719422891},
                 '2023-08-01': {'2022252207': 0.5764478801516103, '2561744167': 0.5732550066979819,
                                '5821279480': 0.496957607586024, '7109370363': 0.647600273016502,
                                '1595443924': 0.5323484031242997, '7239083016': 0.6311351431899177,
                                '1783497251': 0.5526374379560677},
                 '2023-07-16': {'2022252207': 0.5485110544151702, '2561744167': 0.5163457752943525,
                                '5821279480': 0.46319939466806037, '7109370363': 0.49654746676797257,
                                '1595443924': 0.5457493559818916, '7239083016': 0.6223843427983656,
                                '1783497251': 0.6147820979356766},
                 '2023-07-01': {'2022252207': 0.512804401729434, '2561744167': 0.5259255206026103,
                                '5821279480': 0.3762061177030214, '7109370363': 0.6411864965211863,
                                '1595443924': 0.5442762991865567, '7239083016': 0.413892715794684,
                                '1783497251': 0.4742997168440506},
                 '2023-06-16': {'2022252207': 0.5405181784631388, '2561744167': 0.46113971755635713,
                                '5821279480': 0.43142514602998544, '7109370363': 0.5905806243810072,
                                '1595443924': 0.5548942275387792, '7239083016': 0.3257876478075124,
                                '1783497251': 0.5516743692052033},
                 '2023-06-01': {'2022252207': 0.4714405922933652, '2561744167': 0.5169431971063964,
                                '5821279480': 0.4626824125167875, '7109370363': 0.5504526543163322,
                                '1595443924': 0.24450116977095604, '7239083016': 0.5002429542975386,
                                '1783497251': 0.3977822089162838},
                 '2023-05-16': {'2022252207': 0.5198935277180691, '2561744167': 0.620885185186938,
                                '5821279480': 0.4263990454913641, '7109370363': 0.6283852660636433,
                                '1595443924': 0.516610806760712, '7239083016': 0.4832438800578558,
                                '1783497251': 0.6094308464017261},
                 '2023-05-01': {'2022252207': 0.5843915155133422, '2561744167': 0.47926167330876784,
                                '5821279480': 0.4483913361837139, '7109370363': 0.5618296004321072,
                                '1595443924': 0.5103963218380452, '7239083016': 0.29658709883258977,
                                '1783497251': 0.4940249933790546}}

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

if __name__ == "__main__":
    user_id_list = []
    with open('list_bozhu.txt', 'r', encoding='utf-8') as reader:
        for row in reader:
            user_id_list.append(row.split()[1])
    sort_user_id = sorted(map(int, user_id_list))
    sorted_dict_time = get_sorted_dict_time(sort_user_id)

    Degroot_draw(sorted_dict_time)
    # print(get_weight_FJ(sorted_dict_time))
    # FJ_draw(sorted_dict_time)
    # w_ij, s_ij = get_weight_FJ(sorted_dict_time)
