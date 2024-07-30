from flask import Flask, request, redirect, url_for, render_template, flash, send_file, session
import pandas as pd
import io

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def index():
    # Render the index.html template which includes the form for file upload and operation selection
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the file part is present in the request
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    selected_operation = request.form.getlist('operation')
    top_x = request.form.get('top_x')

    # Validate if at least one operation is selected
    if not selected_operation:
        flash('Please select at least one operation.')
        return redirect(request.url)

    # Validate the top X customers input if the 'top_customers' operation is selected
    if 'top_customers' in selected_operation:
        if not top_x or not top_x.isdigit() or int(top_x) <= 0:
            flash('Please enter a valid number greater than 1 for top X customers.')
            return redirect(request.url)
        top_x = int(top_x)
    else:
        top_x = None

    # Check if a file is selected
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file:
        file_content = file.read()
        outputs = process_file(file_content, selected_operation, top_x)
        session['outputs'] = outputs
        return render_template('results.html', outputs=outputs, selected_operation=selected_operation, top_x=top_x)

def process_file(file_content, selected_operation, top_x):
    # Read the uploaded CSV file content into a DataFrame
    df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
    
    # Calculate total revenue by multiplying product price and quantity for each row
    df['total_revenue'] = df['product_price'] * df['quantity']
    
    # Convert the order_date column to datetime format
    df['order_date'] = pd.to_datetime(df['order_date'])

    # Initialize a dictionary to store the outputs of the selected operations
    outputs = {}

    # Check if 'monthly_revenue' operation is selected
    if 'monthly_revenue' in selected_operation:
        # Group by month and sum the total revenue for each month
        monthly_revenue = df.groupby(df['order_date'].dt.to_period('M')).agg({'total_revenue': 'sum'}).reset_index()
        # Convert the period to string for HTML display
        monthly_revenue['order_date'] = monthly_revenue['order_date'].astype(str)
        # Store the monthly revenue table in HTML format and as a dictionary in the outputs
        outputs["monthly_revenue"] = monthly_revenue.to_html(index=False)
        outputs["monthly_revenue_df"] = monthly_revenue.to_dict()
    
    # Check if 'product_revenue' operation is selected
    if 'product_revenue' in selected_operation:
        # Group by product name and sum the total revenue for each product
        product_revenue = df.groupby('product_name').agg({'total_revenue': 'sum'}).reset_index()
        outputs["product_revenue"] = product_revenue.to_html(index=False)
        outputs["product_revenue_df"] = product_revenue.to_dict()

    # Check if 'customer_revenue' operation is selected
    if 'customer_revenue' in selected_operation:
        # Group by customer ID and sum the total revenue for each customer
        customer_revenue = df.groupby('customer_id').agg({'total_revenue': 'sum'}).reset_index()
        outputs["customer_revenue"] = customer_revenue.to_html(index=False)
        outputs["customer_revenue_df"] = customer_revenue.to_dict()

    # Check if 'top_customers' operation is selected and top_x is provided
    if 'top_customers' in selected_operation and top_x:
        # Group by customer ID, sum the total revenue, and select the top X customers by total revenue
        top_customers = df.groupby('customer_id').agg({'total_revenue': 'sum'}).nlargest(top_x, 'total_revenue').reset_index()
        outputs["top_customers"] = top_customers.to_html(index=False)
        outputs["top_customers_df"] = top_customers.to_dict()

    # Return the dictionary containing the results of the selected operations
    return outputs

@app.route('/download/<filename>')
def download_file(filename):
    # Retrieve the outputs stored in the session
    outputs = session.get('outputs', {})
    df_key = filename + '_df'
    
    # Check if the requested data exists in the outputs
    if df_key not in outputs:
        flash('File not found')
        return redirect(url_for('index'))

    # Convert the stored dictionary back to a DataFrame
    df_dict = outputs[df_key]
    df = pd.DataFrame.from_dict(df_dict)
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Convert the DataFrame to CSV format
    csv_content = df.to_csv(index=False)
    
    # Send the CSV file as a download
    return send_file(
        io.BytesIO(csv_content.encode()),
        as_attachment=True,
        download_name=f'{filename}.csv',
        mimetype='text/csv'
    )

if __name__ == '__main__':
    app.run(debug=True)
