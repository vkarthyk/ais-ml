from NNFactory import NNFactory
from ml.NNLearning.CNND1ClassifierLearning import CNND1ClassifierLearning

FEATURE_PATH = 'data/useful/IndicatorCompactTable.csv'
TARGET_PATH = 'data/useful/IndicatorTargets.csv'
TARGET_COL = 'indicator_type'

MODEL_SAVE_PATH = 'model_save/CNN1d_all_10000st_1e-3lr_target20_v%s_%s.mdl'


def get_model_path(version='1', cpu_or_gpu='cpu'):
    return MODEL_SAVE_PATH % (version, cpu_or_gpu)


# MODEL_SAVE_PATH = 'CNN1d_all_1000st_1e-2lr.mdl'
nnfactory = NNFactory(max_row_per_time=10000)
nnfactory.set_learning_class(CNND1ClassifierLearning, target_num=20)
# nnleanring.train(lr=1e-1, steps=100
#                  , featurepath=FEATURE_PATH, targetpath=TARGET_PATH, targetcol=TARGET_COL
#                  , featurecolblacklist=['stix_name']
#                  # , rowlist=range(80)
#                  )
# nnleanring.save(MODEL_SAVE_PATH%1)
# nnleanring.train(lr=1e-2, steps=100
#                  , featurepath=FEATURE_PATH, targetpath=TARGET_PATH, targetcol=TARGET_COL
#                  , featurecolblacklist=['stix_name']
#                  # , rowlist=range(80)
#                  )
# nnleanring.save(MODEL_SAVE_PATH%2)
# nnleanring.train(lr=1e-3, steps=1000
#                  , featurepath=FEATURE_PATH, targetpath=TARGET_PATH, targetcol=TARGET_COL
#                  , featurecolblacklist=['stix_name']
#                  # , rowlist=range(80)
#                  )
# nnleanring.save(MODEL_SAVE_PATH%3)
# nnleanring.load(MODEL_SAVE_PATH%3, D_in=270, target_num=20)
# nnleanring.train(lr=1e-4, steps=1000
#                  , featurepath=FEATURE_PATH, targetpath=TARGET_PATH, targetcol=TARGET_COL
#                  , featurecolblacklist=['stix_name']
#                  # , rowlist=range(80)
#                  )
# nnleanring.save(MODEL_SAVE_PATH%4)

nnfactory.load(get_model_path('3', 'cpu'), D_in=270, target_num=20)
# nnfactory.load(get_model_path('4', 'gpu'), D_in=270, target_num=20)
# nnleanring.load(MODEL_SAVE_PATH, D_in=270, target_num=20)
# nnleanring.test(FEATURE_PATH, TARGET_PATH, TARGET_COL, featurecolblacklist=['stix_name'], rowlist=range(40000,50000))
# nnleanring.test(FEATURE_PATH, TARGET_PATH, TARGET_COL, featurecolblacklist=['stix_name'], rowlist=range(80))
nnfactory.test(FEATURE_PATH, TARGET_PATH, TARGET_COL, featurecolblacklist=['stix_name'], rowlist=range(120000,130000))
