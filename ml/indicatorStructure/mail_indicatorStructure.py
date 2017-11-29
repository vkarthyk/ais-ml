import pandas as pd
import matplotlib.pylab as plt
from ml.NNLearning.CNND1ClassifierLearning import CNND1ClassifierLearning
from common.Logger import logger
from ml.NNLearning import utils


# Read data
df_structure = pd.read_csv('~/sdb1/ais/data/useful/IndicatorCompactTable.csv', nrows=10000).fillna('None')
df_type_desc = pd.read_csv('~/sdb1/ais/data/IndicatorTargets.csv', nrows=10000).fillna('None')

# Normalize data
df_structure = df_structure.ix[:,1:]
df_type = df_type_desc[['indicator_type']]
df_type, ix_to_label = utils.get_series_ids(df_type)

totle_row_num, c = df_structure.shape[0], df_structure.shape[1]
# rt,ct = df_type.shape[0], df_type.shape[1]

# Define test holdout
test_row_num = int(totle_row_num * 0.2)

# Split holdouts
df_train_structure = df_structure.ix[:totle_row_num - test_row_num - 1]
df_train_type = df_type.ix[:totle_row_num - test_row_num - 1]

df_test_structure = df_structure.ix[totle_row_num - test_row_num:]
df_test_type = df_type.ix[totle_row_num - test_row_num:]

nn = CNND1ClassifierLearning()

# Set up
nn._set_features(df_train_structure)
nn._set_targets(df_train_type)
# nn.set_cell_num(10)
nn._set_learning_rate(1e-2)
#nn.set_mod('classifier')

nn._build()

# Learn(step)
#nn.learn(500000)

nn._load_model('CNN1d8000ro_500st_1e-3lr.mdl')
nn._learn(50)
nn._save_model('CNN1d8000ro_500st_1e-3lr.mdl')

# Test result
logger.rst('loss:', nn._pred(df_test_structure, df_test_type, data='loss'))


logger.rst('confusion matrix:')
cm = nn._pred(df_test_structure, df_test_type, data='confusion_matrix', format='tensor')
utils.pprint_ix_to_label(ix_to_label)
utils.pprint_confusion_matrix(cm, indents=5)


