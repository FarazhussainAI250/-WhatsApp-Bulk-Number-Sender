import streamlit as st
import pandas as pd
import urllib.parse

# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="WhatsApp Bulk Message Generator", layout="wide")
st.title("📲 WhatsApp Bulk Message Generator")

st.info("⚠️ This app generates WhatsApp links. Click each link to send messages manually.")

# ------------------ Numbers Upload ------------------
st.subheader("📂 Upload Numbers File")
uploaded_file = st.file_uploader("Upload CSV/TXT file with numbers (international format, e.g. 923001112233)", type=["csv", "txt"])

numbers = []
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, dtype=str)
            if 'phone' in df.columns:
                numbers = df['phone'].dropna().astype(str).tolist()
            else:
                numbers = df.iloc[:,0].dropna().astype(str).tolist()
        else:
            content = uploaded_file.read().decode("utf-8")
            numbers = [line.strip() for line in content.splitlines() if line.strip()]
        st.success(f"✅ Loaded {len(numbers)} numbers")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# ------------------ Message Area ------------------
st.subheader("✍️ Write Message")
message = st.text_area("Message", height=200, value="Assalam o Alaikum,\nYeh ek test message hai.")

if st.button("🔗 Generate WhatsApp Links"):
    if not numbers:
        st.warning("Upload a file with numbers first.")
    elif not message.strip():
        st.warning("Write a message first.")
    else:
        st.subheader("📱 WhatsApp Links")
        st.info("Click each link below to open WhatsApp and send the message:")
        
        for i, num in enumerate(numbers, start=1):
            encoded_message = urllib.parse.quote(message)
            whatsapp_url = f"https://wa.me/{num}?text={encoded_message}"
            st.markdown(f"**{i}.** [{num}]({whatsapp_url}) - [Open WhatsApp]({whatsapp_url})")
        
        # Download links as HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>WhatsApp Bulk Links</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .link {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; }}
                a {{ color: #25D366; text-decoration: none; font-weight: bold; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>WhatsApp Bulk Message Links</h1>
            <p><strong>Message:</strong> {message}</p>
            <hr>
        """
        
        for i, num in enumerate(numbers, start=1):
            encoded_message = urllib.parse.quote(message)
            whatsapp_url = f"https://wa.me/{num}?text={encoded_message}"
            html_content += f'<div class="link">{i}. <a href="{whatsapp_url}" target="_blank">{num} - Open WhatsApp</a></div>\n'
        
        html_content += """
        </body>
        </html>
        """
        
        st.download_button(
            label="📥 Download HTML File",
            data=html_content,
            file_name="whatsapp_links.html",
            mime="text/html"
        )

# ------------------ Instructions ------------------
st.subheader("📋 How to Use")
st.markdown("""
1. **Upload Numbers**: Upload a CSV or TXT file with phone numbers in international format (e.g., 923001112233)
2. **Write Message**: Enter your message in the text area
3. **Generate Links**: Click the button to generate WhatsApp links
4. **Send Messages**: Click each link to open WhatsApp and send the message
5. **Download HTML**: Download the HTML file to use the links offline

**Note**: This version works on Streamlit Cloud but requires manual clicking for each message.
""")