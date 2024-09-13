import csv
import vobject

def csv_to_vcard(csv_file, vcf_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        with open(vcf_file, 'w') as vcf:
            for row in reader:
                vcard = vobject.vCard()
                
                # Add full name
                vcard.add('fn')
                vcard.fn.value = row['FN']
                
                # Add email
                if row['EMAIL']:
                    vcard.add('email')
                    vcard.email.value = row['EMAIL']
                    vcard.email.type_param = 'INTERNET'
                
                # Add phone number
                if row['TEL;TYPE=voice']:
                    vcard.add('tel')
                    vcard.tel.value = row['TEL;TYPE=voice']
                    vcard.tel.type_param = 'VOICE'
                
                # Add address
                if row['ADR']:
                    vcard.add('adr')
                    adr = row['ADR'].split(';')
                    vcard.adr.value = vobject.vcard.Address(street=adr[0], city=adr[1], code=adr[3], country=adr[4])
                    vcard.adr.type_param = 'HOME'
                
                # Write each contact to the vcf file
                vcf.write(vcard.serialize())

# Usage example
csv_file = 'nextcloud_contacts.csv'  # Your CSV file
vcf_file = 'nextcloud_contacts.vcf'  # Output vCard file
csv_to_vcard(csv_file, vcf_file)

