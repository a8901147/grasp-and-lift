import os
import re
import glob
import pandas as pd
import numpy as np

def parse_baseline_log(log_path):
    """
    Parses the log file from the feature_filterbank_v1 experiment to extract AUC scores.
    
    Returns:
        A dictionary mapping (subject_id, channel_name) to its AUC score.
    """
    baseline_scores = {}
    # Regex to capture subject, channel, and AUC score
    pattern = re.compile(r"--- AUC for Subj (\d+), Channel (\w+), Event HandStart: ([\d.]+) ---")
    
    try:
        with open(log_path, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    subject_id = int(match.group(1))
                    channel = match.group(2)
                    auc = float(match.group(3))
                    baseline_scores[(subject_id, channel)] = auc
    except FileNotFoundError:
        print(f"[ERROR] Baseline log file not found at: {log_path}")
    
    return baseline_scores

def parse_optimized_logs(optimized_dir):
    """
    Parses all run_exp.log files from the optimize_filterbank_freqs experiment.
    
    Returns:
        A dictionary mapping (subject_id, channel_name) to a dict containing 'auc' and 'freqs'.
    """
    optimized_results = {}
    # Find all relevant log files
    log_files = glob.glob(os.path.join(optimized_dir, 'subj*_*_handstart/run_exp.log'))
    
    # Regex to parse subject and channel from the directory name
    dir_pattern = re.compile(r"subj(\d+)_([^_]+)_handstart")
    # Regex to find the best AUC and frequencies in the log file
    auc_pattern = re.compile(r"Best Average AUC: ([\d.]+)")
    freq_pattern = re.compile(r"Best Frequencies: (.*\[.*\])")

    for log_file in log_files:
        dir_name = os.path.basename(os.path.dirname(log_file))
        dir_match = dir_pattern.search(dir_name)
        if not dir_match:
            continue
            
        subject_id = int(dir_match.group(1))
        channel = dir_match.group(2)
        
        best_auc = None
        best_freqs = "N/A"
        
        try:
            with open(log_file, 'r') as f:
                content = f.read()
                auc_match = auc_pattern.search(content)
                if auc_match:
                    best_auc = float(auc_match.group(1))
                
                freq_match = freq_pattern.search(content)
                if freq_match:
                    best_freqs = freq_match.group(1)

            if best_auc is not None:
                optimized_results[(subject_id, channel)] = {
                    'auc': best_auc,
                    'freqs': best_freqs
                }
        except FileNotFoundError:
            print(f"[WARNING] Log file not found, skipping: {log_file}")
            
    return optimized_results

def main():
    """
    Main function to run the comparison and generate the report.
    """
    # --- Define Paths ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '../../../../')) # Corrected depth
    
    baseline_log_path = os.path.join(project_root, 'mycode/experiment/single_channel/feature_filterbank_v1/HandStart/run_exp.log')
    optimized_dir_path = os.path.join(script_dir)

    # --- Parse Data ---
    print("1. Parsing baseline results from 'feature_filterbank_v1'...")
    baseline_data = parse_baseline_log(baseline_log_path)
    if not baseline_data:
        print("[ERROR] Could not parse any baseline data. Exiting.")
        return

    print("2. Parsing optimized results from 'optimize_filterbank_freqs'...")
    optimized_data = parse_optimized_logs(optimized_dir_path)
    if not optimized_data:
        print("[ERROR] Could not parse any optimized data. Exiting.")
        return
        
    # --- Combine and Compare Data ---
    print("3. Combining and comparing results...")
    comparison_list = []
    for (subject, channel), baseline_auc in baseline_data.items():
        optimized_result = optimized_data.get((subject, channel))
        
        if optimized_result:
            optimized_auc = optimized_result['auc']
            best_freqs = optimized_result['freqs']
            improvement = optimized_auc - baseline_auc
            
            comparison_list.append({
                'Subject': subject,
                'Channel': channel,
                'Baseline AUC': baseline_auc,
                'Optimized AUC': optimized_auc,
                'Improvement': improvement,
                'Best Frequencies': best_freqs
            })

    if not comparison_list:
        print("[ERROR] No matching (subject, channel) pairs found between the two experiments.")
        return

    df = pd.DataFrame(comparison_list)
    df['Improvement (%)'] = (df['Improvement'] / df['Baseline AUC']) * 100
    
    # Sort by subject and channel for consistent ordering
    df_sorted = df.sort_values(by=['Subject', 'Channel']).reset_index(drop=True)

    # --- Display Report ---
    print("\n\n" + "="*80)
    print("          Comparison: Default FilterBank vs. Optimized Frequencies")
    print("="*80)
    
    # Configure pandas to display all rows and format floats
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)
    pd.options.display.float_format = '{:,.4f}'.format
    
    print(df_sorted[['Subject', 'Channel', 'Baseline AUC', 'Optimized AUC', 'Improvement', 'Improvement (%)', 'Best Frequencies']])
    
    print("\n" + "="*80)
    print("                           Summary Statistics")
    print("="*80)
    
    avg_improvement = df_sorted['Improvement'].mean()
    avg_pct_improvement = df_sorted['Improvement (%)'].mean()
    
    print(f"Total Channels Compared: {len(df_sorted)}")
    print(f"Average Absolute AUC Improvement: {avg_improvement:+.4f}")
    print(f"Average Percentage AUC Improvement: {avg_pct_improvement:+.2f}%")
    
    print("\nTop 5 Channels by Absolute Improvement:")
    print(df_sorted.nlargest(5, 'Improvement')[['Subject', 'Channel', 'Improvement', 'Improvement (%)', 'Best Frequencies']])
    
    print("\n" + "="*80)

if __name__ == '__main__':
    main()
