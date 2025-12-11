#!/usr/bin/env python3
"""
Notary Signing Agent Invoice Generator - Windows Compatible Version
Generates professional PDF invoices for notary services using ReportLab
"""

import argparse
import os
import yaml
from datetime import datetime
from decimal import Decimal
import json

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER


class InvoiceGenerator:
    def __init__(self, config_file='config.yaml'):
        """Initialize the invoice generator with configuration."""
        self.config = self.load_config(config_file)
        self.invoice_counter_file = 'invoice_counter.txt'

    def load_config(self, config_file):
        """Load configuration from YAML file."""
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def get_next_invoice_number(self):
        """Get the next invoice number."""
        if os.path.exists(self.invoice_counter_file):
            with open(self.invoice_counter_file, 'r') as f:
                counter = int(f.read().strip())
        else:
            counter = self.config['invoice']['starting_number']

        # Save the next counter
        with open(self.invoice_counter_file, 'w') as f:
            f.write(str(counter + 1))

        return counter

    def create_invoice(self, client_info, services, invoice_date=None,
                      invoice_number=None, custom_notes=None):
        """
        Create an invoice.

        Args:
            client_info: Dictionary with client details (name, address, email, phone)
            services: List of dictionaries with service details (description, quantity, rate)
            invoice_date: Date of invoice (defaults to today)
            invoice_number: Invoice number (auto-generated if not provided)
            custom_notes: Custom notes for this invoice

        Returns:
            Dictionary with invoice data
        """
        if invoice_date is None:
            invoice_date = datetime.now().strftime('%Y-%m-%d')

        if invoice_number is None:
            invoice_number = self.get_next_invoice_number()

        # Calculate totals
        subtotal = Decimal('0.00')
        for service in services:
            quantity = Decimal(str(service.get('quantity', 1)))
            rate = Decimal(str(service['rate']))
            service['amount'] = float(quantity * rate)
            subtotal += quantity * rate

        tax_rate = Decimal(str(self.config['invoice'].get('tax_rate', 0)))
        tax = subtotal * tax_rate
        total = subtotal + tax

        invoice_data = {
            'invoice_number': invoice_number,
            'invoice_date': invoice_date,
            'business': self.config['business'],
            'client': client_info,
            'services': services,
            'subtotal': float(subtotal),
            'tax_rate': float(tax_rate) * 100,
            'tax': float(tax),
            'total': float(total),
            'payment_terms': self.config['invoice']['payment_terms'],
            'notes': custom_notes or self.config['invoice']['notes']
        }

        return invoice_data

    def generate_pdf(self, invoice_data, output_file=None):
        """Generate PDF from invoice data using ReportLab."""
        if output_file is None:
            output_file = f"invoice_{invoice_data['invoice_number']}.pdf"

        # Create PDF document
        doc = SimpleDocTemplate(
            output_file,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )

        # Container for PDF elements
        elements = []

        # Define styles
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=10,
            alignment=TA_RIGHT,
            fontName='Helvetica-Bold'
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )

        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=3
        )

        small_style = ParagraphStyle(
            'CustomSmall',
            parent=styles['Normal'],
            fontSize=9,
            spaceAfter=2
        )

        # Header section with business info and invoice title
        business = invoice_data['business']

        header_data = [
            [
                Paragraph(f"<b>{business['name']}</b><br/>"
                         f"{business['notary_name']} - Notary Public<br/>"
                         f"Commission #{business['commission_number']}<br/>"
                         f"Commission Expires: {business['commission_expires']}<br/>"
                         f"{business['address']}<br/>"
                         f"{business['city_state_zip']}<br/>"
                         f"Phone: {business['phone']}<br/>"
                         f"Email: {business['email']}<br/>"
                         f"{business.get('website', '')}", small_style),
                Paragraph(f"<b>INVOICE</b><br/>"
                         f"<font size=10>Invoice #: {invoice_data['invoice_number']}<br/>"
                         f"Date: {invoice_data['invoice_date']}</font>", title_style)
            ]
        ]

        header_table = Table(header_data, colWidths=[4*inch, 3.5*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2c3e50')),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.3*inch))

        # Client information
        client = invoice_data['client']
        client_text = f"<b>{client['name']}</b><br/>"
        if client.get('company'):
            client_text += f"{client['company']}<br/>"
        if client.get('address'):
            client_text += f"{client['address']}<br/>"
        if client.get('city_state_zip'):
            client_text += f"{client['city_state_zip']}<br/>"
        if client.get('email'):
            client_text += f"{client['email']}<br/>"
        if client.get('phone'):
            client_text += f"{client['phone']}<br/>"

        client_data = [[Paragraph("<b>BILL TO:</b><br/>" + client_text, normal_style)]]
        client_table = Table(client_data, colWidths=[7.5*inch])
        client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LINEABOVE', (0, 0), (-1, 0), 3, colors.HexColor('#2c3e50')),
        ]))
        elements.append(client_table)
        elements.append(Spacer(1, 0.3*inch))

        # Services table
        service_data = [['Description', 'Quantity', 'Rate', 'Amount']]

        for service in invoice_data['services']:
            service_data.append([
                service['description'],
                str(service.get('quantity', 1)),
                f"${service['rate']:.2f}",
                f"${service['amount']:.2f}"
            ])

        service_table = Table(service_data, colWidths=[4*inch, 1*inch, 1.25*inch, 1.25*inch])
        service_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

            # Quantity, Rate, Amount columns alignment
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),

            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),

            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),

            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ]))
        elements.append(service_table)
        elements.append(Spacer(1, 0.2*inch))

        # Totals table
        totals_data = [
            ['Subtotal:', f"${invoice_data['subtotal']:.2f}"]
        ]

        if invoice_data['tax'] > 0:
            totals_data.append([
                f"Tax ({invoice_data['tax_rate']:.2f}%):",
                f"${invoice_data['tax']:.2f}"
            ])

        totals_data.append([
            'TOTAL:',
            f"${invoice_data['total']:.2f}"
        ])

        totals_table = Table(totals_data, colWidths=[2*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -2), 10),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#2c3e50')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f8f9fa')),
        ]))

        # Right-align the totals table
        totals_wrapper = Table([[totals_table]], colWidths=[7.5*inch])
        totals_wrapper.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ]))
        elements.append(totals_wrapper)
        elements.append(Spacer(1, 0.4*inch))

        # Payment terms
        payment_box_data = [[
            Paragraph(f"<b>PAYMENT TERMS</b><br/>{invoice_data['payment_terms']}", normal_style)
        ]]
        payment_table = Table(payment_box_data, colWidths=[7.5*inch])
        payment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff3cd')),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LINEABOVE', (0, 0), (-1, 0), 3, colors.HexColor('#ffc107')),
        ]))
        elements.append(payment_table)

        # Notes
        if invoice_data.get('notes'):
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph(f"<i>{invoice_data['notes']}</i>", small_style))

        # Build PDF
        doc.build(elements)

        return output_file


def main():
    parser = argparse.ArgumentParser(description='Notary Invoice Generator (Windows Compatible)')
    parser.add_argument('--config', default='config.yaml', help='Configuration file')
    parser.add_argument('--client-json', help='Client info as JSON string')
    parser.add_argument('--services-json', help='Services as JSON string')
    parser.add_argument('--output', help='Output PDF file name')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')

    args = parser.parse_args()

    generator = InvoiceGenerator(args.config)

    if args.interactive or not (args.client_json and args.services_json):
        # Interactive mode
        print("=== Notary Invoice Generator (Windows Edition) ===\n")

        # Client information
        print("CLIENT INFORMATION:")
        client_info = {
            'name': input("Client Name: "),
            'company': input("Company (optional): "),
            'address': input("Address (optional): "),
            'city_state_zip': input("City, State ZIP (optional): "),
            'email': input("Email (optional): "),
            'phone': input("Phone (optional): ")
        }

        # Services
        print("\nSERVICES:")
        print("Available default rates:")
        for service, rate in generator.config['default_rates'].items():
            print(f"  - {service.replace('_', ' ').title()}: ${rate}")

        services = []
        while True:
            print(f"\nService #{len(services) + 1}:")
            description = input("Description (or press Enter to finish): ")
            if not description:
                break

            quantity = input("Quantity (default 1): ") or "1"
            rate = input("Rate: $")

            services.append({
                'description': description,
                'quantity': float(quantity),
                'rate': float(rate)
            })

        if not services:
            print("No services added. Exiting.")
            return

        # Generate invoice
        invoice_data = generator.create_invoice(client_info, services)
        output_file = args.output or f"invoice_{invoice_data['invoice_number']}.pdf"

    else:
        # Command-line mode
        client_info = json.loads(args.client_json)
        services = json.loads(args.services_json)

        invoice_data = generator.create_invoice(client_info, services)
        output_file = args.output or f"invoice_{invoice_data['invoice_number']}.pdf"

    # Generate PDF
    generator.generate_pdf(invoice_data, output_file)
    print(f"\n✓ Invoice generated: {output_file}")
    print(f"  Invoice Number: {invoice_data['invoice_number']}")
    print(f"  Total: ${invoice_data['total']:.2f}")


if __name__ == '__main__':
    main()
