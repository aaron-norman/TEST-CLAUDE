# Notary Signing Agent Invoice Generator

A professional invoice generator designed specifically for notary signing agents and mobile notary businesses. Generate beautiful, detailed PDF invoices with ease.

## Features

- **Professional PDF Invoices**: Clean, professional-looking invoices suitable for business use
- **Automatic Invoice Numbering**: Sequential invoice numbers with customizable starting point
- **Flexible Service Items**: Support for all common notary services:
  - Loan signings
  - General notarizations
  - Mobile notary fees
  - Travel fees
  - Printing/scanning fees
  - Witness fees
  - After-hours fees
- **Customizable Business Information**: Configure your business details once in the config file
- **Tax Calculation**: Automatic tax calculation (if applicable in your jurisdiction)
- **Multiple Usage Modes**:
  - Interactive command-line interface
  - Python API for automation
  - JSON input for integration with other systems

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Note: WeasyPrint requires some system dependencies. If you encounter issues:

**On Ubuntu/Debian:**
```bash
sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
```

**On macOS:**
```bash
brew install cairo pango gdk-pixbuf libffi
```

**On Windows:**
Follow the [WeasyPrint Windows installation guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows)

## Configuration

Edit `config.yaml` to set up your business information:

```yaml
business:
  name: "Your Notary Business Name"
  notary_name: "Your Full Name"
  commission_number: "12345678"
  commission_expires: "12/31/2025"
  address: "123 Main Street"
  city_state_zip: "Anytown, ST 12345"
  phone: "(555) 123-4567"
  email: "notary@example.com"
  website: "www.yournotary.com"

default_rates:
  loan_signing: 150.00
  general_notarization: 15.00
  travel_fee_per_mile: 0.65
  mobile_notary_fee: 50.00
  printing_per_page: 0.25
  witness_fee: 25.00
  after_hours_fee: 50.00

invoice:
  starting_number: 1001
  tax_rate: 0.0  # Set to your local tax rate if applicable
  payment_terms: "Payment due within 30 days"
  notes: "Thank you for your business!"
```

## Usage

### Interactive Mode

The easiest way to create an invoice:

```bash
python invoice_generator.py --interactive
```

This will prompt you for:
- Client information (name, company, address, contact details)
- Services provided (description, quantity, rate)

### Command-Line Mode

Create an invoice using JSON input:

```bash
python invoice_generator.py \
  --client-json '{"name": "John Smith", "company": "ABC Title", "email": "john@abc.com"}' \
  --services-json '[{"description": "Loan Signing", "quantity": 1, "rate": 150.00}]' \
  --output invoice_123.pdf
```

### Python API

Use the invoice generator in your own Python scripts:

```python
from invoice_generator import InvoiceGenerator

# Initialize
generator = InvoiceGenerator('config.yaml')

# Define client
client_info = {
    'name': 'John Smith',
    'company': 'ABC Title Company',
    'email': 'john@abc.com',
    'phone': '(555) 123-4567'
}

# Define services
services = [
    {
        'description': 'Loan Signing Service',
        'quantity': 1,
        'rate': 150.00
    },
    {
        'description': 'Travel Fee (20 miles)',
        'quantity': 20,
        'rate': 0.65
    }
]

# Create and generate invoice
invoice_data = generator.create_invoice(client_info, services)
pdf_file = generator.generate_pdf(invoice_data)
print(f"Invoice created: {pdf_file}")
```

## Examples

Run the example script to see sample invoices:

```bash
python example_usage.py
```

This will generate three example invoices:
1. **Loan Signing Invoice**: Complete loan signing package with travel and printing fees
2. **General Notarization Invoice**: Multiple notarizations with mobile service
3. **After-Hours Invoice**: Evening signing with witness services

### Common Service Examples

**Loan Signing:**
```python
services = [
    {'description': 'Loan Signing - Refinance', 'quantity': 1, 'rate': 150.00},
    {'description': 'Travel Fee', 'quantity': 25, 'rate': 0.65},
    {'description': 'Printing (120 pages)', 'quantity': 120, 'rate': 0.25}
]
```

**General Notarizations:**
```python
services = [
    {'description': 'Notarization - Power of Attorney', 'quantity': 1, 'rate': 15.00},
    {'description': 'Notarization - Affidavit', 'quantity': 2, 'rate': 15.00},
    {'description': 'Mobile Notary Fee', 'quantity': 1, 'rate': 50.00}
]
```

**Mobile Notary with Witnesses:**
```python
services = [
    {'description': 'Mobile Notary Service', 'quantity': 1, 'rate': 50.00},
    {'description': 'Witness Service', 'quantity': 2, 'rate': 25.00},
    {'description': 'After-Hours Fee', 'quantity': 1, 'rate': 50.00}
]
```

## Invoice Numbering

Invoices are automatically numbered sequentially. The system maintains a counter in `invoice_counter.txt`.

- First invoice starts at the number specified in `config.yaml` (default: 1001)
- Each subsequent invoice increments by 1
- To reset numbering, delete `invoice_counter.txt` or edit it manually

## Output Files

Generated invoices are saved as:
- `invoice_[NUMBER].pdf` (e.g., `invoice_1001.pdf`)
- Custom filename can be specified with `--output` flag

## Tips for Notary Businesses

1. **Track Your Expenses**: Use the travel fee calculator to ensure you're properly compensated for mileage
2. **Set Competitive Rates**: Update `default_rates` in config.yaml based on your local market
3. **Professional Presentation**: The invoices include your commission number and expiration for client confidence
4. **Stay Organized**: Use sequential invoice numbering for easy record-keeping
5. **Tax Compliance**: Set appropriate tax rate in config if your services are taxable in your jurisdiction

## Customization

### Modify Invoice Template

To customize the invoice appearance, edit the HTML template in `invoice_generator.py` (the `generate_html` method). You can change:
- Colors and fonts
- Layout and spacing
- Add your business logo
- Additional fields or sections

### Add New Service Types

Add new default rates in `config.yaml`:

```yaml
default_rates:
  # ... existing rates ...
  rush_fee: 75.00
  scanning_fee: 1.00
  certified_copy: 10.00
```

## Troubleshooting

**Issue: WeasyPrint installation fails**
- Solution: Install system dependencies (see Installation section)

**Issue: Fonts look different than expected**
- Solution: WeasyPrint uses system fonts. Install desired fonts on your system

**Issue: Invoice numbers are wrong**
- Solution: Check/edit `invoice_counter.txt` or delete it to reset

**Issue: PDF generation is slow**
- Solution: This is normal for the first PDF. Subsequent generations are faster

## License

This software is provided as-is for use in notary businesses. Feel free to modify and customize for your needs.

## Support

For issues or questions:
1. Check the examples in `example_usage.py`
2. Review the configuration in `config.yaml`
3. Ensure all dependencies are installed correctly

## Changelog

### Version 1.0.0
- Initial release
- PDF invoice generation
- Interactive and command-line modes
- Automatic invoice numbering
- Tax calculation
- Customizable business information
- Professional invoice template
