import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from collections import defaultdict

def jarzynski_free_energy(work_values, temperature_K):
    """Calculates the free energy difference using the Jarzynski Equality."""
    K_B = 8.314462618 / 1000.0  # Boltzmann constant in kJ/(mol*K)
    beta = 1.0 / (K_B * temperature_K)
    
    if not work_values:
        return np.nan
    exp_avg = np.mean(np.exp(-beta * np.asarray(work_values)))
    if exp_avg <= 0 or np.isinf(exp_avg):
        return np.nan
    delta_F = -1.0 / beta * np.log(exp_avg)
    return delta_F

# --- Main execution block ---

if __name__ == "__main__":
    
    CV_FOLDER = "CV"
    NUM_RUNS = 150
    # Adjusted start ID to 1 and end ID to 150 (inclusive)
    RUN_START_ID = 1
    RUN_END_ID = 150
    
    NUM_BLOCKS = 5
    RUNS_PER_BLOCK = NUM_RUNS // NUM_BLOCKS
    TEMPERATURE = 300.0  # Kelvin (adjust as needed)
    
    if NUM_RUNS % NUM_BLOCKS != 0:
        print("Error: The number of runs must be divisible by the number of blocks.")
        sys.exit(1)

    # Store the FE estimates for each exact CV value from each of the 5 blocks
    fe_estimates_per_cv = defaultdict(list)
    
    print(f"Dividing {NUM_RUNS} runs (IDs {RUN_START_ID} to {RUN_END_ID}) into {NUM_BLOCKS} blocks.")
    
    # Loop over each block
    for block_id in range(NUM_BLOCKS):
        print(f"Processing Block {block_id + 1}...")
        
        # Determine which run IDs belong to this block
        # Start index is offset by RUN_START_ID - 1
        current_block_start_run_id = (block_id * RUNS_PER_BLOCK) + RUN_START_ID
        current_block_end_run_id = current_block_start_run_id + RUNS_PER_BLOCK
        
        work_in_block_by_cv = defaultdict(list)
        
        for run_id in range(current_block_start_run_id, current_block_end_run_id):
            file_path = os.path.join(CV_FOLDER, f"{run_id}.cv")
            
            if not os.path.exists(file_path):
                print(f"Warning: File not found: {file_path}. Skipping run {run_id}.")
                continue
                
            try:
                cv_values, work_values = np.loadtxt(file_path, usecols=(4, -1), unpack=True)
                
                for cv, work in zip(cv_values, work_values):
                    work_in_block_by_cv[cv].append(work)

            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        
        for cv_val, works in work_in_block_by_cv.items():
            if len(works) >= 10: 
                local_fe = jarzynski_free_energy(works, TEMPERATURE)
                if not np.isnan(local_fe):
                    fe_estimates_per_cv[cv_val].append(local_fe)

    # --- Final Profile Calculation ---
    profile_cv = []
    profile_fe = []
    profile_fe_err = []

    print("Calculating final profile and errors from 5 blocks...")
    for cv_val in sorted(fe_estimates_per_cv.keys()):
        fe_estimates = fe_estimates_per_cv[cv_val]
        
        if len(fe_estimates) == NUM_BLOCKS: 
            mean_fe = np.mean(fe_estimates)
            std_dev = np.std(fe_estimates, ddof=1)
            std_err_mean = std_dev / np.sqrt(len(fe_estimates))
            
            profile_cv.append(cv_val)
            profile_fe.append(mean_fe)
            profile_fe_err.append(std_err_mean)

    # Normalize the profile
    min_fe = min(profile_fe)
    profile_fe_normalized = np.asarray(profile_fe) - min_fe
    
    # Plot and save results
    try:
        plt.style.use('ggplot')
    except OSError:
        plt.style.use('classic')
    plt.figure(figsize=(10, 6))
    
    plt.errorbar(profile_cv, profile_fe_normalized, yerr=profile_fe_err, 
                 fmt='-o', capsize=5, label='Jarzynski Profile (Exact CV, 5-Block Avg)')
    
    plt.xlabel('Collective Variable', fontsize=14)
    plt.ylabel('Free Energy (kJ/mol)', fontsize=14)
    plt.title('Free Energy Profile via Jarzynski Equality (Exact CV, 5-Block Avg Error)', fontsize=16)
    plt.legend()
    
    plt.savefig('PMF_150_block_avg.png', dpi=300)

    np.savetxt('predicted_PMF.txt', 
               np.column_stack([profile_cv, profile_fe_normalized, profile_fe_err]),
               header='CV_Value  Free_Energy_(kJ/mol)  Error_(kJ/mol)',
               fmt='%.4f')
    print("\nFree energy profile data saved to 'predicted_PMF.txt'")
    print("Free energy profile plot saved to 'PMF_150_block_avg.png'")

