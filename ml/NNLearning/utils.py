import torch
from common.Logger import Logger
import numpy as np

logger = Logger('utils')

def get_tensor(df, ttype='float'):
    if ttype == 'int':
        return torch.from_numpy(df.as_matrix().astype('int')).int()
    elif ttype == 'long':
        return torch.from_numpy(df.as_matrix().astype('int')).long()
    else:
        return torch.from_numpy(df.as_matrix().astype('int')).float()

def init_matrix(m, n, v=''):
    rst = []
    for i in range(m):
        rst.append([v]*n)
    return rst


def confusion_matrix(pred_tsr, real_tsr, n):
    print 'conf mat n', n
    cm = init_matrix(n, n, 0)
    for i in range(len(pred_tsr)):
        cm[real_tsr[i]][pred_tsr[i]] += 1
    return cm


def max_ix(tsr):
    return torch.max(tsr, 1)[1], len(tsr[0])


def get_series_ids(x, existed_ix_to_label=[]):
    '''Function returns a pandas series consisting of ids,
       corresponding to objects in input pandas series x
       Example:
       get_series_ids(pd.Series(['a','a','b','b','c']))
       returns Series([0,0,1,1,2], dtype=int)'''

    values = np.unique(x)
    # print existed_ix_to_label
    # print values
    values = existed_ix_to_label + list(set(values) - set(existed_ix_to_label))
    # print values
    values2nums = dict(zip(values,range(len(values))))
    return x.replace(values2nums), values


def pprint_confusion_matrix(cm, lgr=logger, indents=8, len_ix_to_label=0):
    if len_ix_to_label is 0:
        len_ix_to_label = len(cm)
    lgr.rst('')
    first_column_align = 10
    top_left_str = 'Real\\Pred'
    title = top_left_str +' '*(first_column_align-len(top_left_str))+'|'
    alignstr = '{:>'+str(indents) + '}'
    first_column_align_str = '{:>'+str(first_column_align)+'}'
    # for i in range(len(cm)):
    for i in range(len_ix_to_label):
        title = title+alignstr.format(i)+' '
    lgr.rst(title)
    lgr.rst('_' * (first_column_align + (indents + 1) * len_ix_to_label))
    # for i, r in enumerate(cm):
    for i in range(len_ix_to_label):
        r = cm[i]
        s = first_column_align_str.format(i) + '|'
        for j in range(len_ix_to_label):
            c = r[j]
            s += alignstr.format(c) + ' '
        lgr.rst(s)

def pprint_ix_to_label(lst, lgr=logger):
    for i, label in enumerate(lst):
        lgr.rst(i, label)

# def type_to_types_probability_vector_tensor(target, total_types):
#     lst = []
#     for i in target:
#         t = [0]*total_types
#         t[target] = 1
#         lst.append()
#

def list_element_addition(l1, l2):
    if len(l1) is 0:
        return l2
    if len(l2) is 0:
        return l1
    return [sum(x) for x in zip(l1, l2)]

def list_element_addition_2d(m1, m2):
    if len(m1) is 0:
        return m2
    if len(m2) is 0:
        return m1
    result = []
    for l1, l2 in zip(m1, m2):
        result.append(list_element_addition(l1, l2))
    return result

def print_time_consumed(t):
    t = int(t)
    logger.info('time consumed:', t/60/60, 'h', (t/60)%60, 'm', (t)%60, 's')
