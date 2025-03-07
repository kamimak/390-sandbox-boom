import nibabel as nib
bold_file = r'C:\Users\neahs\Downloads\Connectomics_Project\OASIS_FIRSTBATCH\Oasis_first11\sub-OAS30001\ses-d3132\func\sub-OAS30001_ses-d3132_task-rest_run-01_bold.nii.gz'
img = nib.load(bold_file)
TR = img.header.get_zooms()[3]
print(f"RepetitionTime from NIfTI header: {TR} seconds")