from flask import Flask, jsonify
import stripe
from datetime import datetime

# Set the API key
stripe.api_key = "sk_test_51JjmCJSG4p0gu3ahRqeNbtUoeSCVtt51sISAwIGGQung1j5wgiegus6JLCbKpCzmdjhrHxYMjalwBVmRUZPYWLBa00dZAzBC2b"

# Create the Flask app
app = Flask(__name__)

# Define the API endpoint customer_id = "cus_L79c7ctX8Jl5GR"
@app.route("/billing/stripes/invoices/<customerID>")
def get_invoices(customerID):
    # Retrieve all invoices for the customer
    invoices = stripe.Invoice.list(customer=customerID)

    # Retrieve all payment receipts for the customer
    payment_receipts = stripe.Charge.list(customer=customerID, expand=["data.payment_intent"])

    # Extract the invoice and receipt information
    invoice_info = []
    for invoice in invoices.data:
        # Check if invoice has a payment receipt
        receipt_info = {}
        for payment in payment_receipts.data:
            if payment.payment_intent.invoice == invoice.id:
                receipt_info = {
                    "receipt_number": payment.receipt_number,
                    "receipt_link": payment.receipt_url,
                    "receipt_date": datetime.fromtimestamp(payment.created).strftime('%Y-%m-%d %H:%M:%S'),
                }
                break

        if receipt_info:
            invoice_info.append({
                "paid": True,
                "receipt_info": receipt_info,
                "invoice_info": None,
            })
        else:
            invoice_info.append({
                "paid": False,
                "receipt_info": None,
                "invoice_info": {
                    "invoice_number": invoice.number,
                    "invoice_date": datetime.fromtimestamp(invoice.created).strftime('%Y-%m-%d %H:%M:%S'),
                    "download_link": invoice.invoice_pdf,
                },
            })

    # Return the invoice and receipt information as JSON
    return jsonify(invoice_info)

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)



