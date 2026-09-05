"""
TrustShield ML Pipeline: Benchmark Fraud Dataset Generator
Constructs a realistic, temporally ordered transaction fraud dataset (15,000+ records)
with genuine fraud patterns, class imbalance (~3%), and non-memorizing features.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_fraud_dataset(n_samples: int = 16000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    random.seed(seed)
    
    # 1. Base timestamp: past 90 days, chronologically ordered
    start_time = datetime(2026, 1, 1, 0, 0, 0)
    seconds_span = 90 * 24 * 3600
    random_seconds = np.sort(np.random.randint(0, seconds_span, size=n_samples))
    timestamps = [start_time + timedelta(seconds=int(s)) for s in random_seconds]
    
    hours = [t.hour for t in timestamps]
    days_of_week = [t.weekday() for t in timestamps]
    
    # 2. Payment methods and merchant categories
    payment_methods = ['UPI', 'CARD', 'NETBANKING', 'WALLET']
    method_probs = [0.55, 0.30, 0.10, 0.05]
    chosen_methods = np.random.choice(payment_methods, size=n_samples, p=method_probs)
    
    merchant_categories = [
        'E_COMMERCE', 'ELECTRONICS', 'GAMING_DIGITAL', 
        'TRAVEL_HOSPITALITY', 'UTILITIES', 'FASHION', 'GROCERY'
    ]
    cat_probs = [0.30, 0.15, 0.10, 0.15, 0.10, 0.12, 0.08]
    chosen_categories = np.random.choice(merchant_categories, size=n_samples, p=cat_probs)
    
    # 3. Realistic amount distribution (log-normal, in INR)
    # Median ~ ₹1,200, mean ~ ₹3,500, occasional high values
    log_amounts = np.random.normal(7.1, 1.2, size=n_samples)
    amounts = np.round(np.exp(log_amounts), 2)
    amounts = np.clip(amounts, 50.0, 350000.0)
    
    # 4. Behavioral and contextual features
    # Account age in days (exponential distribution)
    account_age_days = np.random.exponential(scale=240, size=n_samples).astype(int) + 1
    
    # Transaction velocity (1-hour and 24-hour)
    base_velocity_1h = np.random.poisson(lam=1.2, size=n_samples)
    base_velocity_24h = base_velocity_1h + np.random.poisson(lam=3.5, size=n_samples)
    
    # Failed attempts in past 15 minutes
    failed_attempts = np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.88, 0.07, 0.03, 0.015, 0.005])
    
    # Distance from typical location (km)
    location_distance_km = np.random.exponential(scale=15.0, size=n_samples)
    
    # Device novelty (0 = known device, 1 = new device)
    is_new_device = np.random.choice([0, 1], size=n_samples, p=[0.75, 0.25])
    
    # Merchant security & domain features
    domain_age_days = np.random.exponential(scale=450, size=n_samples).astype(int) + 3
    has_ssl = np.random.choice([1, 0], size=n_samples, p=[0.96, 0.04])
    has_business_info = np.random.choice([1, 0], size=n_samples, p=[0.92, 0.08])
    is_free_email_domain = np.random.choice([1, 0], size=n_samples, p=[0.12, 0.88])
    
    hours_arr = np.array(hours)
    
    # 5. Realistic Fraud Generation Mechanism (ground truth latent logit)
    # Fraud rate ~ 2.8% to 3.2%
    z = (
        -4.2  # Base low fraud prior
        + 0.65 * (np.log1p(amounts) > 9.5)  # Very high amount (> ~₹13,000)
        + 1.1 * (base_velocity_1h >= 5)      # Rapid burst velocity
        + 0.8 * (base_velocity_24h >= 12)    # 24h burst
        + 1.25 * (failed_attempts >= 2)      # Multiple failed PIN/OTP tries
        + 0.75 * (is_new_device == 1)        # New unverified device
        + 0.6 * (account_age_days < 14)      # Freshly registered account
        + 0.9 * (domain_age_days < 30)       # Infant merchant domain (<30 days)
        + 1.3 * (has_ssl == 0)               # Missing or invalid SSL
        + 0.85 * (has_business_info == 0)    # Missing merchant identity
        + 0.5 * (location_distance_km > 120) # Anomaly geolocation
        + 0.6 * ((hours_arr >= 1) & (hours_arr <= 4))# Late-night fraud window (1 AM - 4 AM)
        + 0.4 * (chosen_categories == 'GAMING_DIGITAL')
        + 0.3 * (chosen_methods == 'CARD')   # Card not present higher fraud rate than UPI
    )
    
    # Add slight random noise to prevent deterministic memorization
    z += np.random.normal(0, 0.4, size=n_samples)
    
    # Sigmoid to probability
    fraud_prob = 1.0 / (1.0 + np.exp(-z))
    is_fraud = (np.random.uniform(0, 1, size=n_samples) < fraud_prob).astype(int)
    
    # Inject correlated bursts for actual fraud rows
    for i in range(n_samples):
        if is_fraud[i] == 1:
            if random.random() < 0.6:
                base_velocity_1h[i] = max(base_velocity_1h[i], random.randint(4, 9))
                base_velocity_24h[i] = max(base_velocity_24h[i], base_velocity_1h[i] + random.randint(5, 15))
            if random.random() < 0.5:
                failed_attempts[i] = max(failed_attempts[i], random.randint(2, 4))
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'amount': amounts,
        'payment_method': chosen_methods,
        'merchant_category': chosen_categories,
        'hour_of_day': hours,
        'day_of_week': days_of_week,
        'account_age_days': account_age_days,
        'velocity_1h': base_velocity_1h,
        'velocity_24h': base_velocity_24h,
        'failed_attempts_15m': failed_attempts,
        'location_distance_km': np.round(location_distance_km, 1),
        'is_new_device': is_new_device,
        'domain_age_days': domain_age_days,
        'has_ssl': has_ssl,
        'has_business_info': has_business_info,
        'is_free_email_domain': is_free_email_domain,
        'is_fraud': is_fraud
    })
    
    return df

if __name__ == '__main__':
    df = generate_fraud_dataset(16000)
    print(f"Generated {len(df)} transactions.")
    print(f"Fraud count: {df['is_fraud'].sum()} ({df['is_fraud'].mean()*100:.2f}%)")
    df.to_csv('backend/ml/transactions_dataset.csv', index=False)
    print("Saved to backend/ml/transactions_dataset.csv")
