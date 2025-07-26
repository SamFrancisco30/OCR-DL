import os

# Path configuration
input_dir = "train_gt"          # Directory of original .gt.txt files
output_dir = "split_lines"      # Output directory for split files

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Iterate all .gt.txt files
for filename in os.listdir(input_dir):
    if filename.endswith(".gt.txt"):
        base_name = os.path.splitext(filename)[0]  # Remove .gt.txt suffix
        input_path = os.path.join(input_dir, filename)
        
        # Read original file content
        with open(input_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        # Create a separate file for each line
        for i, line in enumerate(lines):
            output_filename = f"{base_name}-{i:02d}.gt.txt"  # Use two-digit numbering
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(line)
            
            print(f"Created: {output_filename}")

print(f"\nDone! All split files are saved in the {output_dir} directory.")

# Rename files in split_lines folder
for filename in os.listdir(output_dir):
    if filename.endswith(".gt.txt") and ".gt-" in filename:
        new_filename = filename.replace(".gt-", "-")
        old_path = os.path.join(output_dir, filename)
        new_path = os.path.join(output_dir, new_filename)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")