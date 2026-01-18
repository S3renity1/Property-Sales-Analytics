import zipfile
import os
import pandas as pd
from pathlib import Path

zip_folder = "#insert path" 
excel_output_dir = "#insert path"


os.makedirs(excel_output_dir, exist_ok=True)


for zip_name in os.listdir(zip_folder):
    if zip_name.lower().endswith(".zip"):
        zip_path = os.path.join(zip_folder, zip_name)
        extract_dir = os.path.join(zip_folder, Path(zip_name).stem)

      
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

   
        for root, dirs, files in os.walk(extract_dir):
            for file_name in files:
                if file_name.lower().endswith(".dat"):
                    dat_path = os.path.join(root, file_name)
                    try:
                    
                        df = pd.read_csv(
                            dat_path,
                            sep=';',
                            header=None,
                            dtype=str,
                            engine='python',
                            names=[f'col{i + 1}' for i in range(30)]
                        )
             
                        excel_filename = f"{Path(zip_name).stem}_{Path(file_name).stem}.xlsx"
                        excel_path = os.path.join(excel_output_dir, excel_filename)
             
                        df.to_excel(excel_path, index=False, engine='openpyxl')
                        print(f"Converted {file_name} from {zip_name} -> {excel_filename}")

                    except Exception as e:
                        print(f" Error converting {file_name} from {zip_name}: {e}")
