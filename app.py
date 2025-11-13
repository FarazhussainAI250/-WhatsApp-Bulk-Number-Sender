import streamlit as st
import time
import pandas as pd
import urllib.parse
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# ------------------ Helper: Remove non-BMP chars (emojis etc) ------------------
def remove_non_bmp_chars(s: str) -> str:
    if not s:
        return s
    try:
        return re.sub(r'[^\u0000-\uFFFF]', '', s)
    except Exception:
        return s

# ------------------ Selenium helper class ------------------
class WhatsAppBulkSender:
    def __init__(self, wait_after_open=20):
        self.driver = None
        self.wait_after_open = wait_after_open

    def open_whatsapp(self):
        if self.driver is not None:
            return
        try:
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.get("https://web.whatsapp.com")
            st.info("WhatsApp Web opened. Please scan QR code if not already logged in.")
            time.sleep(self.wait_after_open)
        except WebDriverException as e:
            st.error(f"Chrome driver error: {str(e)}")
            raise
        except Exception as e:
            st.error(f"Failed to open WhatsApp: {str(e)}")
            raise

    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None

    def send_message(self, phone, message, wait_between=3):
        """Send message by phone number (must be in international format, e.g. 923001112233)."""
        if not self.driver:
            raise RuntimeError("WebDriver not started. Call open_whatsapp() first.")

        safe_message = remove_non_bmp_chars(message)
        url = f"https://web.whatsapp.com/send?phone={phone}&text={urllib.parse.quote(safe_message)}"
        try:
            self.driver.get(url)

            # Wait for either chat box or invalid number error
            try:
                msg_box = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab]"))
                )
            except Exception as e:
                try:
                    # Check for invalid number messages
                    invalid_msgs = [
                        "//div[contains(text(),'phone number shared via url is invalid')]",
                        "//div[contains(text(),'Phone number does not exist')]",
                        "//div[contains(text(),'not registered on WhatsApp')]"
                    ]
                    for msg_xpath in invalid_msgs:
                        try:
                            self.driver.find_element(By.XPATH, msg_xpath)
                            return False, "Invalid/unregistered number"
                        except NoSuchElementException:
                            continue
                    return False, f"Message box not found: {str(e)}"
                except Exception as inner_e:
                    return False, f"Error checking number validity: {str(inner_e)}"

            # Clear and type message with retry
            try:
                msg_box.clear()
                time.sleep(0.5)
                msg_box.send_keys(safe_message)
                time.sleep(1)
                
                # Verify message was typed
                if not msg_box.get_attribute('textContent'):
                    msg_box.send_keys(safe_message)
                    time.sleep(0.5)
            except Exception as e:
                return False, f"Failed to type message: {str(e)}"

            # Try multiple send button selectors
            send_selectors = [
                '//button[@aria-label="Send"]',
                '//span[@data-icon="send"]',
                '//button[contains(@class,"send")]'
            ]
            
            sent = False
            for selector in send_selectors:
                try:
                    send_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    send_btn.click()
                    sent = True
                    break
                except Exception as e:
                    continue
            
            if not sent:
                try:
                    # Fallback: press ENTER
                    msg_box.send_keys(Keys.ENTER)
                    sent = True
                except Exception as e:
                    return False, f"Failed to send message: {str(e)}"

            # Wait a bit and verify message was sent
            time.sleep(2)
            
            # Check if message box is empty (indicates message was sent)
            try:
                current_text = msg_box.get_attribute('textContent') or ''
                if current_text.strip() == '':
                    time.sleep(wait_between - 2)
                    return True, None
                else:
                    time.sleep(wait_between - 2)
                    return True, "Message sent (verification uncertain)"
            except:
                time.sleep(wait_between - 2)
                return True, None

        except Exception as e:
            return False, str(e)


# ----------- Custom CSS with Header & Footer ------------
st.markdown("""
<style>
/* Background Image */
.stApp {
    background-image: url("https://glance-web.glance-cdn.com/AI_Technology_Transforming_Daily_Life_Effortlessly0_3198dffcae.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

/* Top-right Header */
#top-header {
    position: fixed;
    top: 80px;
    right: 20px;
    background-color: rgba(0,0,0,0.5);
    padding: 8px 16px;
    border-radius: 8px;
    color: white;
    font-size: 18px;
    font-weight: bold;
    z-index: 100;
}

/* Bottom-left Footer */
#bottom-footer {
    position: fixed;
    bottom: 10px;
    left: 20px;
    background-color: rgba(0,0,0,0.5);
    padding: 6px 14px;
    border-radius: 6px;
    color: white;
    font-size: 14px;
    z-index: 100;
}
</style>

<div id="top-header">Respected Sir Shahzaib & Sir Ali Hamza</div>
<div id="bottom-footer">Developed by Faraz Hussain</div>
""", unsafe_allow_html=True)

# -------------------------


# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="WhatsApp Bulk Number Sender", layout="wide")
st.title("📲 WhatsApp Bulk Number Sender")

app_state = st.session_state
if 'wa' not in app_state:
    app_state['wa'] = None

# Sidebar controls
st.sidebar.header("Controls")

if st.sidebar.button("Open WhatsApp Web"):
    try:
        if app_state['wa'] is None:
            app_state['wa'] = WhatsAppBulkSender(wait_after_open=20)
        app_state['wa'].open_whatsapp()
    except Exception as e:
        st.sidebar.error(f"Failed: {e}")

if st.sidebar.button("Close WhatsApp Browser"):
    if app_state['wa']:
        app_state['wa'].close()
        app_state['wa'] = None
        st.sidebar.info("Browser closed.")

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

delay = st.slider("Delay between messages (seconds)", 2, 10, 5)

if st.button("🚀 Send to All"):
    if not numbers:
        st.warning("Upload a file with numbers first.")
    elif not message.strip():
        st.warning("Write a message first.")
    elif app_state['wa'] is None:
        st.warning("Open WhatsApp Web first from sidebar.")
    else:
        success, failed = [], []
        progress = st.progress(0)
        for i, num in enumerate(numbers, start=1):
            st.write(f"[{i}/{len(numbers)}] Sending to {num}...")
            ok, err = app_state['wa'].send_message(num, message, wait_between=delay)
            if ok:
                success.append(num)
            else:
                failed.append(num)
                st.error(f"Failed for {num}: {err}")
            progress.progress(i/len(numbers))

        st.success(f"✅ Done! Sent to {len(success)} numbers, Failed: {len(failed)}")
        if failed:
            st.warning(f"Failed numbers: {failed}")
