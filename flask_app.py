from flask import Flask, render_template_string, request
import math

app = Flask(__name__)

# Constants
g = 9.81  # Gravity (m/s²)
rho_water = 1000  # Density of water (kg/m³)
mu_water = 0.001  # Viscosity of water (Pa·s)

def calculate_friction_factor(Re):
    warning = ""
    if Re < 2100:
        warning = "Warning: Laminar flow (Re < 2100). Formula may not apply accurately."
    f = 0.3164 / (Re ** 0.25)  # Blasius formula for turbulent flow
    return f, warning

@app.route('/', methods=['GET', 'POST'])
def calculator():
    results = None
    if request.method == 'POST':
        try:
            L = float(request.form['L'])
            D = float(request.form['D'])
            Q = float(request.form['Q'])
            rho = float(request.form.get('rho', rho_water))
            mu = float(request.form.get('mu', mu_water))
            
            A = math.pi * (D / 2) ** 2  # Cross-sectional area
            V = Q / A  # Velocity
            Re = (rho * V * D) / mu  # Reynolds number
            f, warning = calculate_friction_factor(Re)
            hf = f * (L / D) * (V ** 2 / (2 * g))  # Head loss
            delta_P = rho * g * hf  # Pressure drop
            
            results = {
                'V': f"{V:.3f} m/s",
                'Re': f"{Re:.0f}",
                'f': f"{f:.4f}",
                'hf': f"{hf:.3f} m",
                'delta_P': f"{delta_P:.0f} Pa ({delta_P/1000:.2f} kPa)",
                'warning': warning
            }
        except ValueError:
            results = {'error': 'Please enter valid numbers.'}
    
    # Improved HTML template with Bootstrap for professional look
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pipe Hydraulics Calculator</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; }
            .container { max-width: 600px; margin-top: 50px; }
            .card { box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            .btn-primary { background-color: #007bff; border: none; }
            .result-box { background-color: #e9ecef; padding: 10px; border-radius: 5px; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card p-4">
                <h1 class="text-center mb-4">Pipe Hydraulics Calculator</h1>
                <p class="text-muted text-center">Calculate pressure drop due to friction in a pipe using the Darcy-Weisbach equation.</p>
                <form method="post">
                    <div class="mb-3">
                        <label for="L" class="form-label">Pipe length (m)</label>
                        <input type="number" step="0.01" class="form-control" id="L" name="L" value="100" required>
                    </div>
                    <div class="mb-3">
                        <label for="D" class="form-label">Pipe diameter (m)</label>
                        <input type="number" step="0.01" class="form-control" id="D" name="D" value="0.1" required>
                    </div>
                    <div class="mb-3">
                        <label for="Q" class="form-label">Flow rate (m³/s)</label>
                        <input type="number" step="0.01" class="form-control" id="Q" name="Q" value="0.01" required>
                    </div>
                    <div class="mb-3">
                        <label for="rho" class="form-label">Fluid density (kg/m³)</label>
                        <input type="number" step="0.01" class="form-control" id="rho" name="rho" value="1000">
                    </div>
                    <div class="mb-3">
                        <label for="mu" class="form-label">Dynamic viscosity (Pa·s)</label>
                        <input type="number" step="0.0001" class="form-control" id="mu" name="mu" value="0.001">
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Calculate</button>
                </form>
                {% if results %}
                    <div class="mt-4">
                        <h3>Results</h3>
                        {% if results.error %}
                            <div class="alert alert-danger">{{ results.error }}</div>
                        {% else %}
                            <div class="result-box">
                                <p><strong>Velocity (V):</strong> {{ results.V }}</p>
                                <p><strong>Reynolds number (Re):</strong> {{ results.Re }}</p>
                                <p><strong>Friction factor (f):</strong> {{ results.f }}</p>
                                <p><strong>Head loss (hf):</strong> {{ results.hf }}</p>
                                <p><strong>Pressure drop (ΔP):</strong> {{ results.delta_P }}</p>
                                {% if results.warning %}<div class="alert alert-warning mt-2">{{ results.warning }}</div>{% endif %}
                            </div>
                        {% endif %}
                    </div>
                {% endif %}
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
    return render_template_string(html, results=results)

if __name__ == '__main__':
    app.run(debug=True)
