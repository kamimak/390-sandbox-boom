import os
import json

# 🔹 Path to your dataset
dataset_dir = r"C:\Users\neahs\Downloads\Connectomics_Project\OASIS_FIRSTBATCH\Oasis_first11"

for root, dirs, files in os.walk(dataset_dir):
    for file in files:
        if file.endswith("_bold.nii.gz"):
            bold_path = os.path.join(root, file)
            
            # Get corresponding JSON filename
            json_filename = file.replace(".nii.gz", ".json")
            json_path = os.path.join(root, json_filename)

            # Extract task name from filename (after 'task-')
            try:
                task_name = file.split("task-")[1].split("_")[0]
            except IndexError:
                task_name = "unknown"

            # If JSON doesn't exist, create it
            if not os.path.exists(json_path):
                sidecar_content = {
                    "TaskName": task_name
                }
                with open(json_path, 'w') as json_file:
                    json.dump(sidecar_content, json_file, indent=4)
                print(f"✅ Created JSON: {json_path} with TaskName '{task_name}'")

            else:
                # If JSON exists, check and add TaskName if missing
                with open(json_path, 'r+') as json_file:
                    try:
                        data = json.load(json_file)
                    except json.JSONDecodeError:
                        data = {}
                    if "TaskName" not in data:
                        data["TaskName"] = task_name
                        json_file.seek(0)
                        json.dump(data, json_file, indent=4)
                        json_file.truncate()
                        print(f"✅ Updated JSON: {json_path} with TaskName '{task_name}'")
                    else:
                        print(f"⚠️ JSON already has TaskName in {json_path}, skipped.")

print("\n🎉 Done! All missing sidecars created and existing ones updated.")

