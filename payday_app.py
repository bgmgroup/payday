
from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import tempfile
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def invoice():
    if request.method == 'POST':
        data = request.form
        items = [
            {
                "description": data.get("item_description_1"),
                "hours": float(data.get("item_hours_1", 0)),
                "rate": float(data.get("item_rate_1", 0)),
            },
            {
                "description": data.get("item_description_2"),
                "hours": float(data.get("item_hours_2", 0)),
                "rate": float(data.get("item_rate_2", 0)),
            }
        ]
        total_amount = sum(item["hours"] * item["rate"] for item in items)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="INVOICE", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Invoice #: {data.get('invoice_number')}", ln=True)
        pdf.cell(200, 10, txt=f"Date: {data.get('date')}  |  Due: {data.get('due_date')}", ln=True)
        pdf.ln(10)
        pdf.cell(100, 10, txt=f"From: {data.get('sender_name')} ({data.get('sender_email')})", ln=True)
        pdf.cell(100, 10, txt=f"To: {data.get('client_name')} ({data.get('client_email')})", ln=True)
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(100, 10, txt="Description", border=1)
        pdf.cell(30, 10, txt="Hours", border=1)
        pdf.cell(30, 10, txt="Rate", border=1)
        pdf.cell(30, 10, txt="Total", border=1)
        pdf.ln()

        pdf.set_font("Arial", size=12)
        for item in items:
            total = item["hours"] * item["rate"]
            pdf.cell(100, 10, txt=item["description"], border=1)
            pdf.cell(30, 10, txt=str(item["hours"]), border=1)
            pdf.cell(30, 10, txt=f"${item['rate']}", border=1)
            pdf.cell(30, 10, txt=f"${total}", border=1)
            pdf.ln()

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(160, 10, txt="Total Due", border=1)
        pdf.cell(30, 10, txt=f"${total_amount}", border=1)
        pdf.ln(15)

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=f"Notes: {data.get('notes')}")
        pdf.multi_cell(0, 10, txt=f"Payment Info: {data.get('payment_info')}")

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(tmp.name)
        tmp.close()

        return send_file(tmp.name, as_attachment=True, download_name="invoice.pdf")

    today = datetime.date.today().strftime("%Y-%m-%d")
    due = (datetime.date.today() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    return render_template('form.html', today=today, due=due)

if __name__ == '__main__':
    app.run(debug=True)
