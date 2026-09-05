"""
TrustShield ML Pipeline: Calibrated Inference Pipeline Definition
Encapsulates scikit-learn preprocessing and calibrated probability inference.
"""

import numpy as np
import pandas as pd

class CalibratedInferencePipeline:
    def __init__(self, preproc, calib, features):
        self.preprocessor = preproc
        self.calibrator = calib
        self.features = features
        
    def predict_proba(self, X_df):
        clean_df = X_df.copy()
        for col in self.features:
            if col not in clean_df.columns:
                clean_df[col] = np.nan
        X_clean = clean_df[self.features]
        trans = self.preprocessor.transform(X_clean)
        return self.calibrator.predict_proba(trans)
        
    def predict_risk(self, transaction_dict):
        df_single = pd.DataFrame([transaction_dict])
        prob = float(self.predict_proba(df_single)[0, 1])
        return prob
