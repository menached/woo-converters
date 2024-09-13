import mysql.connector
import vobject
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get database connection details from environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Parse ADR field into street, city, and zip
def parse_address(adr):
    address_parts = adr.split(';')
    street = address_parts[0] if len(address_parts) > 0 else ''
    city = address_parts[1] if len(address_parts) > 1 else ''
    zip_code = address_parts[3] if len(address_parts) > 3 else ''
    return street, city, zip_code

# Insert one vCard into MySQL table
def insert_vcard_into_db(vcard):
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # SQL query to insert data
        insert_query = """
            INSERT INTO contacts (full_name, email, phone_number, street_address, city, zip_code, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # Prepare data
        full_name = vcard.get('FN', '')
        email = vcard.get('EMAIL', '')
        phone_number = vcard.get('TEL', '')
        street, city, zip_code = parse_address(vcard.get('ADR', ';;;'))
        category = vcard.get('CATEGORY', '')

        # Execute the SQL insert query for each vCard
        cursor.execute(insert_query, (full_name, email, phone_number, street, city, zip_code, category))

        # Commit the transaction
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Error inserting vCard {full_name}: {err}")
    finally:
        # Close the cursor and connection after each insert
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to parse the .vcf file one card at a time and insert into the DB
def parse_and_insert_vcf_file(vcf_file_path):
    with open(vcf_file_path, 'r') as f:
        vcard_data = f.read()

    # Use vobject to read and process each vCard one-by-one
    for vcard in vobject.readComponents(vcard_data):
        fn = vcard.fn.value if hasattr(vcard, 'fn') else ''
        email = vcard.email.value if hasattr(vcard, 'email') else ''
        tel = vcard.tel.value if hasattr(vcard, 'tel') else ''
        
        # Handle address fields
        if hasattr(vcard, 'adr'):
            adr = vcard.adr.value
            street = adr.street if adr.street else ''
            city = adr.city if adr.city else ''
            zip_code = adr.code if adr.code else ''
            full_address = f"{street};{city};;{zip_code}"
        else:
            full_address = ';;;'

        category = 'Unknown'  # Assign a default category if needed
        
        # Prepare the vCard data
        vcard_data = {
            'FN': fn,
            'EMAIL': email,
            'TEL': tel,
            'ADR': full_address,
            'CATEGORY': category
        }

        # Insert the vCard into the database
        insert_vcard_into_db(vcard_data)

# Main execution
vcf_file = 'vcards.vcf'  # Replace with the actual path to your .vcf file
parse_and_insert_vcf_file(vcf_file)

