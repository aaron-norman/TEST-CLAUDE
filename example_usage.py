#!/usr/bin/env python3
"""
Example usage of the Notary Invoice Generator
"""

from invoice_generator import InvoiceGenerator

# Initialize the generator
generator = InvoiceGenerator('config.yaml')

# Example 1: Basic loan signing invoice
print("Generating Example 1: Loan Signing Invoice...")

client_info = {
    'name': 'John Smith',
    'company': 'ABC Title Company',
    'address': '456 Oak Avenue',
    'city_state_zip': 'Springfield, IL 62701',
    'email': 'jsmith@abctitle.com',
    'phone': '(555) 987-6543'
}

services = [
    {
        'description': 'Loan Signing Service - Refinance Package',
        'quantity': 1,
        'rate': 150.00
    },
    {
        'description': 'Travel Fee (25 miles)',
        'quantity': 25,
        'rate': 0.65
    },
    {
        'description': 'Document Printing (120 pages)',
        'quantity': 120,
        'rate': 0.25
    }
]

invoice_data = generator.create_invoice(client_info, services)
pdf_file = generator.generate_pdf(invoice_data, 'example_loan_signing.pdf')
print(f"✓ Created: {pdf_file}")


# Example 2: General notarization services
print("\nGenerating Example 2: General Notarization Invoice...")

client_info = {
    'name': 'Jane Doe',
    'email': 'jane.doe@email.com',
    'phone': '(555) 234-5678'
}

services = [
    {
        'description': 'General Notarization - Power of Attorney',
        'quantity': 3,
        'rate': 15.00
    },
    {
        'description': 'General Notarization - Affidavit',
        'quantity': 2,
        'rate': 15.00
    },
    {
        'description': 'Mobile Notary Service',
        'quantity': 1,
        'rate': 50.00
    }
]

invoice_data = generator.create_invoice(client_info, services)
pdf_file = generator.generate_pdf(invoice_data, 'example_general_notarization.pdf')
print(f"✓ Created: {pdf_file}")


# Example 3: After-hours signing with witness
print("\nGenerating Example 3: After-Hours Signing Invoice...")

client_info = {
    'name': 'Robert Johnson',
    'company': 'XYZ Escrow Services',
    'address': '789 Pine Street, Suite 200',
    'city_state_zip': 'Chicago, IL 60601',
    'email': 'rjohnson@xyzescrow.com',
    'phone': '(555) 456-7890'
}

services = [
    {
        'description': 'Loan Signing Service - Purchase Package',
        'quantity': 1,
        'rate': 150.00
    },
    {
        'description': 'After-Hours Fee (Evening Signing)',
        'quantity': 1,
        'rate': 50.00
    },
    {
        'description': 'Witness Service',
        'quantity': 2,
        'rate': 25.00
    },
    {
        'description': 'Travel Fee (15 miles)',
        'quantity': 15,
        'rate': 0.65
    }
]

invoice_data = generator.create_invoice(
    client_info,
    services,
    custom_notes="Thank you for choosing our after-hours notary services!"
)
pdf_file = generator.generate_pdf(invoice_data, 'example_after_hours.pdf')
print(f"✓ Created: {pdf_file}")

print("\n✓ All example invoices generated successfully!")
