import os
import pandas as pd
import numpy as np

def normalise_area(row):
    try:
        area = float(row["Area"])
        unit = str(row["Area Type"]).strip().upper()
        if unit == "H":
            return area
        elif unit == "M":
            return round(area / 10000, 4)
        else:
            return np.nan
    except:
        return np.nan

def parse_ymd(val):
    try:
        val = str(val).strip().split('.')[0]  # Remove decimals if float
        if len(val) == 8 and val.isdigit():
            return pd.to_datetime(val, format="%Y%m%d")
    except:
        pass
    return pd.NaT  # Return missing if not parsable


def clean_and_combine(folder_path, output_path):
    all_cleaned = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_excel(file_path)

            df_filter = df[df["col1"] == "B"].copy()
            df_filter.drop(columns=['col1'], inplace=True)
            df_filter = df_filter.iloc[:, :24]

            df_filter.columns = [
                "District Code", "Property ID", "Sale Counter", "Download Datetime",
                "Property Name", "Unit Number", "House Number", "Street Name", "Locality", "Postcode",
                "Area", "Area Type", "Contract Date", "Settlement Date", "Purchase Price",
                "Zoning", "Nature of Property", "Primary Purpose", "Strata Lot Number",
                "Component Code", "Sale Code", "% Interest", "Dealing Number", "Blank",
            ]
            # Ensure date columns are in string format
            df_filter["Contract Date"] = df_filter["Contract Date"].apply(parse_ymd)
            df_filter["Settlement Date"] = df_filter["Settlement Date"].apply(parse_ymd)

            df_filter["Full Address"] = df_filter[
                ["Unit Number", "House Number", "Street Name"]
            ].fillna('').astype(str).agg(' '.join, axis=1).str.replace(r"\s+", " ", regex=True).str.strip()

            df_filter["Area (ha)"] = df_filter.apply(normalise_area, axis=1)
            df_filter.drop(columns=["Area", "Area Type" ], inplace=True)

            df_filter = df_filter[[
                "Property ID", "Sale Counter", "Contract Date", "Settlement Date", "Purchase Price",
                "Zoning", "Nature of Property", "Primary Purpose", "Full Address", "Locality", "Postcode", "Area (ha)",
                "Strata Lot Number", "Component Code", "Sale Code", "% Interest", "Dealing Number"
            ]]

            all_cleaned.append(df_filter)
            print(f" Cleaned and added: {filename}")

    combined_df = pd.concat(all_cleaned, ignore_index=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    combined_df.to_excel(output_path, index=False, engine='openpyxl')

    print(f" Combined data saved to {output_path}")


# Usage
input_folder = "#insert path"
output_folder = "#insert path"

clean_and_combine(input_folder, output_folder)