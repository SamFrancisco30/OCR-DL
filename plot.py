import re
import pandas as pd
import plotly.express as px
import os

def parse_training_log(filepath):
    """
    Parse Tesseract training log file to extract BCER and BWER metrics
    Args:
        filepath: path to the training log file
    Returns:
        DataFrame containing iteration numbers and corresponding error rates
    """
    pattern = re.compile(
        r"At iteration\s+(\d+)[^\n]*?BCER train=([\d.]+)%[^\n]*?BWER train=([\d.]+)%"
    )
    records = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = pattern.search(line)
            if m:
                records.append((int(m.group(1)), float(m.group(2)), float(m.group(3))))
    df = pd.DataFrame(records, columns=['iteration','BCER','BWER'])
    df.sort_values('iteration', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def plot_training_metrics(log_dir='logs'):
    """
    Process all log files in the specified directory and generate interactive plots
    Args:
        log_dir: directory containing training log files
    """
    # Get all .log and .txt files in the logs directory
    log_files = [f for f in os.listdir(log_dir) if f.endswith(('.log', '.txt'))]
    
    if not log_files:
        print(f"No log files found in directory: {log_dir}")
        return
    
    for log_file in log_files:
        filepath = os.path.join(log_dir, log_file)
        try:
            # Parse the log file
            df = parse_training_log(filepath)
            
            # Create interactive plot using Plotly Express
            fig = px.line(
                df,
                x='iteration',
                y=['BCER', 'BWER'],
                markers=True,
                labels={'value':'Error Rate (%)', 'iteration':'Iteration', 'variable':'Metric'},
                title=f"Training Metrics: {log_file}"
            )
            fig.update_traces(mode='lines+markers')
            
            # Show the plot
            fig.show()
            
        except Exception as e:
            print(f"Error processing file {log_file}: {str(e)}")

# Process all log files in the logs directory
plot_training_metrics()