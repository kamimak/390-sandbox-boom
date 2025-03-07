import os
import re

dataset_dir = r"C:\Users\neahs\Downloads\Connectomics_Project\OASIS_FIRSTBATCH\Oasis_first11"

required_folders = ['anat', 'func']
errors = []

subject_pattern = re.compile(r"sub-\w+")
session_pattern = re.compile(r"ses-\w+")

print("\n🔍 Checking BIDS structure...\n")

for subject in os.listdir(dataset_dir):
    sub_path = os.path.join(dataset_dir, subject)
    if os.path.isdir(sub_path) and subject_pattern.match(subject):
        for session in os.listdir(sub_path):
            ses_path = os.path.join(sub_path, session)
            if os.path.isdir(ses_path) and session_pattern.match(session):
                folder_contents = os.listdir(ses_path)
                
                # Check for required folders
                for folder in required_folders:
                    if folder not in folder_contents:
                        errors.append(f"❌ Missing '{folder}/' folder in {sub_path}/{session}")
                
                # Check files in anat/ and func/
                for folder in required_folders:
                    folder_path = os.path.join(ses_path, folder)
                    if os.path.exists(folder_path):
                        for file in os.listdir(folder_path):
                            if not file.startswith(subject):
                                errors.append(f"❌ Invalid filename '{file}' in {folder_path} (does not start with {subject})")
                            if session not in file:
                                errors.append(f"❌ Invalid filename '{file}' in {folder_path} (missing {session})")
            else:
                errors.append(f"❌ Invalid or missing session folder under {subject}: {session}")
    else:
        if subject != "dataset_description.json" and subject != "README":
            errors.append(f"❌ Invalid or unexpected folder/file at top level: {subject}")

# Results
if errors:
    print("\n🚨 STRUCTURE ISSUES FOUND:")
    for e in errors:
        print(e)
else:
    print("✅ Dataset structure looks good!")

print(f"\n🔎 Checked dataset at: {dataset_dir}")
