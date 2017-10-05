from FeatureBuilder import FeatureBuilder

fb = FeatureBuilder(csv_file_name='~/sdb1/ais/ais_data.csv')
fb.run()
print fb.get_new_feature_df()