from IndicatorStructureNN import IndicatorStructureNN
from ml.NNLearning.CNND1ClassifierLearning import CNND1ClassifierLearning

FEATURE_PATH = 'data/useful/IndicatorCompactTable.csv'
TARGET_PATH = 'data/useful/IndicatorTargets.csv'
TARGET_COL = 'indicator_type'

MODEL_SAVE_PATH = 'model_save/%dCNN1d_all_10000st_1e-3lr.target20.mdl'

# MODEL_SAVE_PATH = 'CNN1d_all_1000st_1e-2lr.mdl'
nnleanring = IndicatorStructureNN(max_row_per_time=10000)
nnleanring.set_learning_class(CNND1ClassifierLearning, target_num=20)
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
nnleanring.load(MODEL_SAVE_PATH%3, D_in=270, target_num=20)
nnleanring.train(lr=1e-4, steps=1000
                 , featurepath=FEATURE_PATH, targetpath=TARGET_PATH, targetcol=TARGET_COL
                 , featurecolblacklist=['stix_name']
                 # , rowlist=range(80)
                 )
nnleanring.save(MODEL_SAVE_PATH%4)

# nnleanring.load(MODEL_SAVE_PATH, D_in=270, target_num=20)
# nnleanring.test(FEATURE_PATH, TARGET_PATH, TARGET_COL, featurecolblacklist=['stix_name'], rowlist=range(40000,50000))
# nnleanring.test(FEATURE_PATH, TARGET_PATH, TARGET_COL, featurecolblacklist=['stix_name'], rowlist=range(80))
nnleanring.test(FEATURE_PATH, TARGET_PATH, TARGET_COL, featurecolblacklist=['stix_name'], rowlist=range(8000, 10000))
