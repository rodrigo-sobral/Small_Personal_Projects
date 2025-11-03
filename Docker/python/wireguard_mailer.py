import os, time, smtplib, qrcode, yagmail, base64
from dotenv import load_dotenv

load_dotenv()

# Get environment variables
peers = os.getenv("WG_PEERS", "").split(",")
emails = os.getenv("WG_PEERS_EMAILS", "").split(",")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT", "587"))
smtp_user = os.getenv("SMTP_USER")
# SMTP_PASS is base64 encoded. Decode it.
smtp_pass = base64.b64decode(os.getenv("SMTP_PASS", "").encode()).decode("utf-8")
from_email = os.getenv("FROM_EMAIL")

# Wait for WireGuard configs
config_dir = "/config"
for _ in range(30):
    if os.path.exists(config_dir) and any(os.listdir(config_dir)):
        break
    time.sleep(5)

# Initialize mailer
yag = yagmail.SMTP(user=smtp_user, password=smtp_pass, host=smtp_server, port=smtp_port, smtp_starttls=True)

# Iterate over peers
for peer, email in zip(peers, emails):
    peer = peer.strip()
    email = email.strip()
    conf_path = f"{config_dir}/{peer}/{peer}.conf"
    if not os.path.exists(conf_path):
        print(f"⚠️ Config not found for {peer}")
        continue

    # Generate QR code
    with open(conf_path, "r") as f:
        conf_data = f.read()
    img = qrcode.make(conf_data)
    qr_path = f"/tmp/{peer}.png"
    img.save(qr_path)

    # Compose email
    subject = f"Your WireGuard VPN Configuration ({peer})"
    body = f"""
    Hi {peer},

    Attached is your WireGuard VPN configuration QR code.

    📱 **Setup instructions:**
    1. Install the WireGuard app from the App Store or Google Play.
    2. Open the app and tap “+”.
    3. Choose *Scan from QR Code*.
    4. Scan the attached QR image.
    5. That's it — your secure VPN is ready!

    If you prefer manual setup, here's your config file content:
    {conf_data}

    Stay secure! 🛡️
    """

    # Send email
    print(f"📤 Sending config for {peer} to {email}...")
    yag.send(to=email, subject=subject, contents=[body, qr_path])
    print(f"✅ Sent to {email}")
