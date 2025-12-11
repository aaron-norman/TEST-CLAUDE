# Notary Invoice Generator - Windows Edition

**Windows-friendly version** using ReportLab (no complex dependencies!)

## Quick Start for Windows

### 1. Install Python

Download Python from https://www.python.org/downloads/ (Python 3.8 or higher)

**IMPORTANT**: During installation, check ✅ "Add Python to PATH"

### 2. Download This Repository

Download and extract the ZIP file to a folder, for example:
```
C:\Users\YourName\notary-invoices
```

### 3. Install Dependencies

Open Command Prompt in the folder (type `cmd` in the folder's address bar) and run:

```bash
pip install -r requirements-windows.txt
```

That's it! No complex system libraries needed.

### 4. Configure Your Business

Edit `config.yaml` with your information:
- Business name
- Your name and commission number
- Contact details
- Default rates

### 5. Generate Invoices

**Try the examples first:**
```bash
python example_usage_windows.py
```

**Create your own invoice:**
```bash
python invoice_generator_windows.py --interactive
```

## Usage Examples

### Interactive Mode (Easiest)

```bash
python invoice_generator_windows.py --interactive
```

Then follow the prompts to enter:
- Client information
- Services provided

### Command Line Mode

```bash
python invoice_generator_windows.py --client-json "{\"name\": \"John Smith\", \"email\": \"john@example.com\"}" --services-json "[{\"description\": \"Loan Signing\", \"quantity\": 1, \"rate\": 150.00}]"
```

### Python API

Create a script:

```python
from invoice_generator_windows import InvoiceGenerator

generator = InvoiceGenerator('config.yaml')

client_info = {
    'name': 'John Smith',
    'company': 'ABC Title',
    'email': 'john@abc.com'
}

services = [
    {'description': 'Loan Signing', 'quantity': 1, 'rate': 150.00},
    {'description': 'Travel Fee (20 miles)', 'quantity': 20, 'rate': 0.65}
]

invoice_data = generator.create_invoice(client_info, services)
pdf_file = generator.generate_pdf(invoice_data)
print(f"Invoice created: {pdf_file}")
```

## Common Notary Services

### Loan Signing Invoice
```python
services = [
    {'description': 'Loan Signing - Refinance', 'quantity': 1, 'rate': 150.00},
    {'description': 'Travel Fee (25 miles)', 'quantity': 25, 'rate': 0.65},
    {'description': 'Printing (120 pages)', 'quantity': 120, 'rate': 0.25}
]
```

### General Notarization
```python
services = [
    {'description': 'Notarization - Power of Attorney', 'quantity': 1, 'rate': 15.00},
    {'description': 'Notarization - Affidavit', 'quantity': 2, 'rate': 15.00},
    {'description': 'Mobile Notary Fee', 'quantity': 1, 'rate': 50.00}
]
```

### After-Hours Signing
```python
services = [
    {'description': 'Loan Signing', 'quantity': 1, 'rate': 150.00},
    {'description': 'After-Hours Fee', 'quantity': 1, 'rate': 50.00},
    {'description': 'Witness Service', 'quantity': 2, 'rate': 25.00}
]
```

## Features

✅ **Pure Python** - No GTK, Cairo, or other complex dependencies
✅ **Professional PDFs** - Clean, business-ready invoices
✅ **Auto-numbering** - Sequential invoice numbers
✅ **Customizable** - Your business info, rates, terms
✅ **Tax calculation** - Optional tax support
✅ **Easy to use** - Interactive mode or command-line

## Troubleshooting

**"Python not found"**
- Reinstall Python and check "Add Python to PATH"
- Or use full path: `C:\Python312\python.exe`

**"pip not found"**
- Try `python -m pip install -r requirements-windows.txt`

**Wrong invoice number?**
- Check or delete `invoice_counter.txt` to reset

**Need to change invoice starting number?**
- Edit `invoice:starting_number` in `config.yaml`

## File Locations

After running, you'll find:
- **Invoices**: `invoice_####.pdf` in the same folder
- **Counter**: `invoice_counter.txt` tracks next number
- **Config**: `config.yaml` has your settings

## Advanced Usage

### Custom Output Location
```bash
python invoice_generator_windows.py --interactive --output "C:\Invoices\client_name.pdf"
```

### Batch Processing
Create a Python script to process multiple invoices:

```python
from invoice_generator_windows import InvoiceGenerator

generator = InvoiceGenerator('config.yaml')

# List of clients and services
jobs = [
    {
        'client': {'name': 'Client 1', 'email': 'client1@example.com'},
        'services': [{'description': 'Loan Signing', 'quantity': 1, 'rate': 150}]
    },
    {
        'client': {'name': 'Client 2', 'email': 'client2@example.com'},
        'services': [{'description': 'Notarization', 'quantity': 3, 'rate': 15}]
    }
]

for job in jobs:
    invoice_data = generator.create_invoice(job['client'], job['services'])
    generator.generate_pdf(invoice_data)
    print(f"Created invoice {invoice_data['invoice_number']} for {job['client']['name']}")
```

## Customization

### Change Colors

Edit `invoice_generator_windows.py` and change color values:
- Header color: `colors.HexColor('#2c3e50')` (dark blue)
- Payment box: `colors.HexColor('#fff3cd')` (yellow)
- Border: `colors.HexColor('#ffc107')` (orange)

### Add Logo

Add this to the header section in `generate_pdf()`:
```python
from reportlab.platypus import Image
logo = Image('logo.png', width=1*inch, height=1*inch)
```

### Change Font Sizes

Modify the style definitions:
- `fontSize=28` for title
- `fontSize=10` for normal text
- `fontSize=9` for small text

## Why Two Versions?

This repository has two invoice generators:

1. **invoice_generator.py** - Uses WeasyPrint (Linux/Mac friendly, complex Windows setup)
2. **invoice_generator_windows.py** - Uses ReportLab (Windows friendly, pure Python)

**Windows users**: Use the `_windows.py` version - it's simpler!
**Linux/Mac users**: Either version works, but WeasyPrint may look slightly better.

## Support

Common questions:

**Q: Can I use this for my notary business?**
A: Yes! It's designed specifically for notary signing agents.

**Q: How do I backup my invoices?**
A: Copy all `invoice_*.pdf` files and `invoice_counter.txt` to another location.

**Q: Can I email invoices automatically?**
A: Yes! You can extend the code to use Python's `smtplib` for email sending.

**Q: Is my data secure?**
A: Everything runs locally on your computer. No data is sent anywhere.

## Next Steps

1. ✅ Generate test invoices with `example_usage_windows.py`
2. ✅ Edit `config.yaml` with your real business info
3. ✅ Create your first invoice with `--interactive`
4. ✅ Organize your PDFs in a dedicated folder
5. ✅ Consider creating a desktop shortcut for quick access

Enjoy your new invoice generator! 📄✨
