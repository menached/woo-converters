import pandas as pd

def convert_to_nextcloud_format(input_csv, output_csv):
    # Load the GoAutodial CSV, skipping bad lines
    df = pd.read_csv(input_csv, on_bad_lines='skip')

    # Fill NaN values with empty strings
    df = df.fillna('')

    # Create the necessary columns for Nextcloud format
    df['FN'] = df['first_name'] + ' ' + df['last_name']
    df['TEL;TYPE=voice'] = '+1' + df['phone_number'].astype(str)
    df['ADR'] = df['address1'] + ';' + df['city'] + ';;' + df['postal_code'].astype(str) + ';' + df['country_code']

    # Select only the columns needed for Nextcloud
    df_nextcloud = df[['FN', 'email', 'TEL;TYPE=voice', 'ADR']]
    df_nextcloud.columns = ['FN', 'EMAIL', 'TEL;TYPE=voice', 'ADR']

    # Save the new CSV
    df_nextcloud.to_csv(output_csv, index=False)
    print(f"Converted CSV saved as: {output_csv}")

# Usage:
input_csv = 'LIST.csv'  # Path to your GoAutodial CSV file
output_csv = 'nextcloud_contacts.csv'  # Path to save the Nextcloud CSV
convert_to_nextcloud_format(input_csv, output_csv)

