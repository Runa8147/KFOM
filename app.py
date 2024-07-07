from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/report')
def report():
    return render_template('index.html')

@app.route('/submit_report', methods=['POST'])
def submit_report():
    try:
        data = request.json
        # Validate data
        required_fields = ['latitude', 'longitude', 'waterLevel', 'description']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "error": f"Missing required field: {field}"}), 400
        
        # Insert data into Supabase
        response = supabase.table('flood_reports').insert(data).execute()
        
        if len(response.data) > 0:
            return jsonify({"success": True, "id": response.data[0]['id']})
        else:
            return jsonify({"success": False, "error": "Failed to insert data"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/get_reports', methods=['GET'])
def get_reports():
    try:
        response = supabase.table('flood_reports').select('*').execute()
        return jsonify({"success": True, "data": response.data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()