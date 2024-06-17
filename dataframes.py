import pandas as pd
from logger import info_logger, error_logger


def save_to_excel(devices, filename='output.xlsx'):
    """
    Save device information to an Excel file.

    Args:
        devices (list): A list of device objects.
        filename (str, optional): The name of the output Excel file. Defaults to 'output.xlsx'.
    """
    
    all_data = []

    for device in devices:
        device_dict = device.to_dict()
        licenses = device_dict.pop('licenses')
        
        device_df = pd.json_normalize(device_dict, sep='_')
        
        for i, license in enumerate(licenses):
            license_df = pd.json_normalize(license, sep='_')
            license_df.columns = [f'license_{i}_{col}' for col in license_df.columns]
            device_df = pd.concat([device_df, license_df], axis=1)
        
        all_data.append(device_df)

    try:
        # Combine all individual DataFrames into one
        final_df = pd.concat(all_data, ignore_index=True)

        # Save the combined DataFrame to Excel
        final_df.to_excel(filename, index=False)
        # Log the information
        info_logger.info(f"All devices information saved to {filename}")
    except Exception as e:
        error_logger.error(f"Error saving device information to Excel: {e}")
