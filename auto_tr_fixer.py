import os
import json
import nibabel as nib

# Path to your dataset
dataset_dir = r"C:\Users\neahs\Downloads\Connectomics_Project\OASIS_FIRSTBATCH\Oasis_first2"

updated = 0
created = 0

for root, dirs, files in os.walk(dataset_dir):
    for file in files:
        if file.endswith("_bold.nii.gz"):
            bold_path = os.path.join(root, file)
            json_filename = file.replace(".nii.gz", ".json")
            json_path = os.path.join(root, json_filename)

            # Get TR from NIfTI header
            img = nib.load(bold_path)
            TR = float(round(img.header.get_zooms()[3], 4))
  # Round to 4 decimal places

            # Extract TaskName from filename
            try:
                task_name = file.split("task-")[1].split("_")[0]
            except IndexError:
                task_name = "unknown"

            # Create or update JSON sidecar
            if os.path.exists(json_path):
                with open(json_path, 'r') as json_file:
                    try:
                        data = json.load(json_file)
                    except json.JSONDecodeError:
                        data = {}
            else:
                data = {}

            data["TaskName"] = task_name
            data["RepetitionTime"] = TR

            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            updated += 1
            print(f"✅ Updated {json_path} with TaskName '{task_name}' and RepetitionTime {TR} seconds")

# Create README if missing
readme_path = os.path.join(dataset_dir, "README")
if not os.path.exists(readme_path):
    with open(readme_path, 'w') as readme_file:
        readme_file.write(
            "This dataset contains resting-state fMRI and anatomical MRI data in BIDS format.\n"
            "RepetitionTime values were extracted from the NIfTI headers.\n"
        )
    print(f"✅ Created README at {readme_path}")
else:
    print(f"⚠️ README already exists at {readme_path}")

print(f"\n🎉 Done! Updated {updated} functional JSON files with TR from the NIfTI headers.")
