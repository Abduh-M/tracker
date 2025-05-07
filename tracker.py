# from flask import Flask, request, send_file, Response
# import logging
# from datetime import datetime
# import os
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from collections import defaultdict

# app = Flask(__name__)

# # Setup logging to file
# LOG_FILE = "open_tracking.log"
# logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# # Google Sheets logger
# def log_to_google_sheets(email, timestamp):
#     print("⚙️ log_to_google_sheets triggered")

#     try:
#         scope = [
#             "https://spreadsheets.google.com/feeds",
#             "https://www.googleapis.com/auth/drive"
#         ]

#         print("🔑 Loading creds.json...")
#         creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
#         print("✅ creds.json loaded")

#         client = gspread.authorize(creds)
#         print("✅ gspread authorized")

#         sheet = client.open_by_key("1RW_6-9NKiwxWSc5rR5V7OJPnaR-uRL1sLN-Lf3r02kc").sheet1
#         print("✅ Sheet opened")

#         sheet.append_row([timestamp, email])
#         print(f"✅ Appended to Google Sheet: {timestamp}, {email}")

#     except Exception as e:
#         print(f"❌ Google Sheets logging failed: {str(e)}")
#         raise e




# @app.route('/pixel.png')
# def tracking_pixel():
#     email = request.args.get('email', 'unknown')
#     timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
#     log_line = f"{timestamp} - OPENED by {email}"

#     # Log to console and file
#     print(log_line)
#     logging.info(log_line)

#     # Log to Google Sheets
#     log_to_google_sheets(email, timestamp)

#     # Return transparent tracking pixel
#     return send_file("pixel.png", mimetype='image/png')

# @app.route('/view-opens')
# def view_opens():
#     if not os.path.exists(LOG_FILE):
#         return "<h2>No opens logged yet.</h2>"

#     with open(LOG_FILE, "r") as f:
#         logs = f.readlines()

#     html = "<h2>📬 Email Opens</h2><ul>"
#     for line in logs:
#         html += f"<li>{line.strip()}</li>"
#     html += "</ul>"
#     return Response(html, mimetype='text/html')

# @app.route('/dashboard')
# def dashboard():
#     counts = defaultdict(int)
#     try:
#         with open(LOG_FILE, "r") as f:
#             lines = f.readlines()
#             for line in lines:
#                 if "OPENED by" in line:
#                     email = line.strip().split("OPENED by ")[-1]
#                     counts[email] += 1
#     except FileNotFoundError:
#         return "<h2>No opens logged yet.</h2>"

#     html = "<h2>📊 Open Count Per Email</h2><table border='1' cellpadding='5'><tr><th>Email</th><th>Open Count</th></tr>"
#     for email, count in sorted(counts.items(), key=lambda x: -x[1]):
#         html += f"<tr><td>{email}</td><td>{count}</td></tr>"
#     html += "</table>"
#     return html

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 10000))
#     app.run(host="0.0.0.0", port=port)



from flask import Flask, request, send_file, Response
import logging
from datetime import datetime
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict

app = Flask(__name__)

# Setup logging to file
LOG_FILE = "open_tracking.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# Google Sheets logger
# def log_to_google_sheets(email, timestamp, name="unknown", title="unknown"):
#     print("⚙️ log_to_google_sheets triggered")

#     try:
#         scope = [
#             "https://spreadsheets.google.com/feeds",
#             "https://www.googleapis.com/auth/drive"
#         ]

#         creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
#         client = gspread.authorize(creds)
#         sheet = client.open_by_key("1RW_6-9NKiwxWSc5rR5V7OJPnaR-uRL1sLN-Lf3r02kc").sheet1

#         sheet.append_row([timestamp, email, name, title])
#         print(f"✅ Appended to Google Sheet: {timestamp}, {email}, {name}, {title}")

#     except Exception as e:
#         print(f"❌ Google Sheets logging failed: {str(e)}")
#         raise e

def log_to_google_sheets(email, timestamp, name="unknown", title="unknown", batch_number="unknown"):
    print("⚙️ log_to_google_sheets triggered")

    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1RW_6-9NKiwxWSc5rR5V7OJPnaR-uRL1sLN-Lf3r02kc").sheet1

        # ✅ Now include batch_6 in the row
        sheet.append_row([timestamp, email, name, title, batch_number])
        print(f"✅ Appended to Google Sheet: {timestamp}, {email}, {name}, {title}, {batch_number}")

    except Exception as e:
        print(f"❌ Google Sheets logging failed: {str(e)}")
        raise e





# @app.route('/pixel.png')
# def tracking_pixel():
#     email = request.args.get('email', 'unknown')
#     name = request.args.get('name', 'unknown')
#     title = request.args.get('title', 'unknown')
#     timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

#     log_line = f"{timestamp} - OPENED by {email} - Name: {name} - Title: {title}"
#     print(log_line)
#     logging.info(log_line)

#     log_to_google_sheets(email, timestamp, name, title)

#     return send_file("pixel.png", mimetype='image/png')

@app.route('/pixel.png')
def tracking_pixel():
    email = request.args.get('email', 'unknown')
    name = request.args.get('name', 'unknown')
    title = request.args.get('title', 'unknown')
    batch_number = request.args.get('batch_number', 'unknown')  # ✅ get batch

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    log_line = f"{timestamp} - OPENED by {email} - Name: {name} - Title: {title} - Batch: {batch_number}"
    print(log_line)
    logging.info(log_line)

    # ✅ Pass batch_6 to the log
    log_to_google_sheets(email, timestamp, name, title, batch_number)

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

@app.route('/dashboard')
def dashboard():
    counts = defaultdict(int)
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "OPENED by" in line:
                    email = line.strip().split("OPENED by ")[-1]
                    counts[email] += 1
    except FileNotFoundError:
        return "<h2>No opens logged yet.</h2>"

    html = "<h2>📊 Open Count Per Email</h2><table border='1' cellpadding='5'><tr><th>Email</th><th>Open Count</th></tr>"
    for email, count in sorted(counts.items(), key=lambda x: -x[1]):
        html += f"<tr><td>{email}</td><td>{count}</td></tr>"
    html += "</table>"
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

















