from flask import Flask, request, send_file, Response
import logging
from datetime import datetime
import os

app = Flask(__name__)

# Setup logging to file
LOG_FILE = "open_tracking.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

@app.route('/pixel.png')
def tracking_pixel():
    email = request.args.get('email', 'unknown')
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} - OPENED by {email}"
    
    # Log to file and console
    print(log_line)
    logging.info(log_line)
    
    # Return 1x1 pixel image
    return send_file("pixel.png", mimetype='image/png')

@app.route('/view-opens')
def view_opens():
    if not os.path.exists(LOG_FILE):
        return "<h2>No opens logged yet.</h2>"

    with open(LOG_FILE, "r") as f:
        logs = f.readlines()

    html = "<h2>📬 Email Opens</h2><ul>"
    for line in logs:
        html += f"<li>{line.strip()}</li>"
    html += "</ul>"

    return Response(html, mimetype='text/html')

if __name__ == "__main__":
    # For Render, use port 10000; for local use 5000
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
