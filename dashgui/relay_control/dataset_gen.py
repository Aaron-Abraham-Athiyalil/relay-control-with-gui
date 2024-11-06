import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic data with more realistic ranges and noise
current_values = np.random.uniform(0, 10, 500) + np.random.normal(0, 0.1, 500)  # Adding noise to currents
voltage_values = np.random.uniform(220, 230, 500) + np.random.normal(0, 0.5, 500)  # Adding noise to voltages

# Double the data points for balanced classes
currents = np.concatenate((current_values, current_values))
voltages = np.concatenate((voltage_values, voltage_values))

# Create additional features (e.g., power)
power_values = currents * voltages  # Simulating power as V * I

data = {
    'IR': currents,
    'IY': currents,
    'IB': currents,
    'VR': voltages,
    'VY': voltages,
    'VB': voltages,
    'Power': power_values
}

# More complex relay logic with different conditions
data['L1'] = ((currents > 5) & (voltages > 226) & (power_values > 1200)).astype(int)
data['L2'] = ((currents <= 5) & (voltages <= 224) & (power_values <= 1100)).astype(int)
data['L3'] = ((currents > 5) | (voltages > 225) | (power_values > 1150)).astype(int)
data['L4'] = ((currents <= 5) & (voltages > 225) & (power_values < 1000)).astype(int)
data['L5'] = ((currents > 5) & (voltages <= 225) & (power_values > 1250)).astype(int)
data['L6'] = ((currents <= 5) | (voltages <= 225) | (power_values < 1050)).astype(int)
data['L7'] = ((currents > 6) & (voltages > 227) & (power_values > 1300)).astype(int)
data['L8'] = ((currents <= 4) & (voltages <= 223) & (power_values < 950)).astype(int)

# Convert to DataFrame
df = pd.DataFrame(data)

# Shuffle the data for better randomness
df = df.sample(frac=1).reset_index(drop=True)

# Save to CSV
df.to_csv('high_quality_synthetic_data_v2.csv', index=False)

print("Improved high-quality dataset created and saved as 'high_quality_synthetic_data_v2.csv'")
