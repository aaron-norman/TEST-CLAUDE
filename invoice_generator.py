#!/usr/bin/env python3
"""
Notary Signing Agent Invoice Generator
Generates professional PDF invoices for notary services
"""

import argparse
import os
import yaml
from datetime import datetime
from decimal import Decimal
from jinja2 import Template
from weasyprint import HTML
import json


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
        """Generate PDF from invoice data."""
        if output_file is None:
            output_file = f"invoice_{invoice_data['invoice_number']}.pdf"

        html_content = self.generate_html(invoice_data)
        HTML(string=html_content).write_pdf(output_file)

        return output_file

    def generate_html(self, invoice_data):
        """Generate HTML from invoice data."""
        template_str = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: letter;
            margin: 0.5in;
        }

        body {
            font-family: 'Helvetica', 'Arial', sans-serif;
            color: #333;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }

        .invoice-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #2c3e50;
        }

        .business-info {
            flex: 1;
        }

        .business-info h1 {
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 24px;
        }

        .business-info p {
            margin: 3px 0;
            font-size: 12px;
        }

        .invoice-title {
            text-align: right;
            flex: 1;
        }

        .invoice-title h2 {
            margin: 0;
            color: #2c3e50;
            font-size: 32px;
            font-weight: bold;
        }

        .invoice-meta {
            font-size: 12px;
            margin-top: 10px;
        }

        .invoice-meta p {
            margin: 3px 0;
        }

        .parties {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
        }

        .party-box {
            flex: 1;
            padding: 15px;
            background-color: #f8f9fa;
            border-left: 4px solid #2c3e50;
        }

        .party-box h3 {
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 14px;
            text-transform: uppercase;
        }

        .party-box p {
            margin: 3px 0;
            font-size: 12px;
        }

        .party-box:last-child {
            margin-left: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
        }

        thead {
            background-color: #2c3e50;
            color: white;
        }

        th {
            padding: 12px;
            text-align: left;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }

        th.right, td.right {
            text-align: right;
        }

        th.center, td.center {
            text-align: center;
        }

        tbody tr {
            border-bottom: 1px solid #dee2e6;
        }

        tbody tr:nth-child(even) {
            background-color: #f8f9fa;
        }

        td {
            padding: 12px;
            font-size: 12px;
        }

        .totals {
            margin-left: auto;
            width: 300px;
            margin-bottom: 30px;
        }

        .totals table {
            margin-bottom: 0;
        }

        .totals tbody tr {
            border: none;
            background-color: transparent !important;
        }

        .totals td {
            padding: 8px 12px;
            border: none;
        }

        .totals .total-row {
            font-weight: bold;
            font-size: 14px;
            border-top: 2px solid #2c3e50;
            background-color: #f8f9fa !important;
        }

        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #dee2e6;
        }

        .payment-terms {
            background-color: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin-bottom: 20px;
        }

        .payment-terms h3 {
            margin: 0 0 10px 0;
            color: #856404;
            font-size: 14px;
        }

        .payment-terms p {
            margin: 0;
            font-size: 12px;
            color: #856404;
        }

        .notes {
            font-size: 12px;
            color: #666;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="invoice-header">
        <div class="business-info">
            <h1>{{ business.name }}</h1>
            <p><strong>{{ business.notary_name }}</strong> - Notary Public</p>
            <p>Commission #{{ business.commission_number }}</p>
            <p>Commission Expires: {{ business.commission_expires }}</p>
            <p>{{ business.address }}</p>
            <p>{{ business.city_state_zip }}</p>
            <p>Phone: {{ business.phone }}</p>
            <p>Email: {{ business.email }}</p>
            {% if business.website %}
            <p>{{ business.website }}</p>
            {% endif %}
        </div>

        <div class="invoice-title">
            <h2>INVOICE</h2>
            <div class="invoice-meta">
                <p><strong>Invoice #:</strong> {{ invoice_number }}</p>
                <p><strong>Date:</strong> {{ invoice_date }}</p>
            </div>
        </div>
    </div>

    <div class="parties">
        <div class="party-box">
            <h3>Bill To:</h3>
            <p><strong>{{ client.name }}</strong></p>
            {% if client.company %}
            <p>{{ client.company }}</p>
            {% endif %}
            {% if client.address %}
            <p>{{ client.address }}</p>
            {% endif %}
            {% if client.city_state_zip %}
            <p>{{ client.city_state_zip }}</p>
            {% endif %}
            {% if client.email %}
            <p>{{ client.email }}</p>
            {% endif %}
            {% if client.phone %}
            <p>{{ client.phone }}</p>
            {% endif %}
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Description</th>
                <th class="center">Quantity</th>
                <th class="right">Rate</th>
                <th class="right">Amount</th>
            </tr>
        </thead>
        <tbody>
            {% for service in services %}
            <tr>
                <td>{{ service.description }}</td>
                <td class="center">{{ service.quantity|default(1) }}</td>
                <td class="right">${{ "%.2f"|format(service.rate) }}</td>
                <td class="right">${{ "%.2f"|format(service.amount) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div class="totals">
        <table>
            <tbody>
                <tr>
                    <td><strong>Subtotal:</strong></td>
                    <td class="right">${{ "%.2f"|format(subtotal) }}</td>
                </tr>
                {% if tax > 0 %}
                <tr>
                    <td><strong>Tax ({{ "%.2f"|format(tax_rate) }}%):</strong></td>
                    <td class="right">${{ "%.2f"|format(tax) }}</td>
                </tr>
                {% endif %}
                <tr class="total-row">
                    <td><strong>TOTAL:</strong></td>
                    <td class="right"><strong>${{ "%.2f"|format(total) }}</strong></td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="footer">
        <div class="payment-terms">
            <h3>Payment Terms</h3>
            <p>{{ payment_terms }}</p>
        </div>

        {% if notes %}
        <p class="notes">{{ notes }}</p>
        {% endif %}
    </div>
</body>
</html>
        """

        template = Template(template_str)
        return template.render(**invoice_data)


def main():
    parser = argparse.ArgumentParser(description='Notary Invoice Generator')
    parser.add_argument('--config', default='config.yaml', help='Configuration file')
    parser.add_argument('--client-json', help='Client info as JSON string')
    parser.add_argument('--services-json', help='Services as JSON string')
    parser.add_argument('--output', help='Output PDF file name')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')

    args = parser.parse_args()

    generator = InvoiceGenerator(args.config)

    if args.interactive or not (args.client_json and args.services_json):
        # Interactive mode
        print("=== Notary Invoice Generator ===\n")

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
