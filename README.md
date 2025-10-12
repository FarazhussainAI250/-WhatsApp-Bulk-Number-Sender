# 📲 WhatsApp Bulk Number Sender
<img width="1888" height="960" alt="message sender" src="https://github.com/user-attachments/assets/cfef59f2-30ce-4a66-b7fd-b94cdd93bb2b" />

A modern **Streamlit-based WhatsApp automation app** that allows users to send custom messages to multiple contacts directly through **WhatsApp Web** — with just one click.

---

## 🚀 Features

- ✅ **Bulk Messaging:** Send messages to hundreds of numbers automatically.  
- 🧾 **CSV/TXT Upload:** Easily import phone numbers from files.  
- 💬 **Custom Message Support:** Write and send personalized messages.  
- ⏱️ **Smart Delay Control:** Set delay time between messages to avoid spam detection.  
- 🌐 **WhatsApp Web Integration:** No API needed — uses Selenium browser automation.  
- 🖥️ **Modern UI:** Beautiful Streamlit interface with header & footer branding.  
- 🧠 **Error Handling:** Detects invalid or non-WhatsApp numbers automatically.  

---

## ⚙️ Installation

Make sure you have **Python 3.9+** installed.

```bash
pip install streamlit selenium webdriver-manager pandas
```

---

## ▶️ How to Run

1. Clone or download this repository.  
2. Open a terminal in the project folder.  
3. Run the app using:

```bash
streamlit run app.py
```

4. In the sidebar, click **"Open WhatsApp Web"** and scan the QR code.  
5. Upload your CSV/TXT file containing phone numbers (e.g., 923001234567).  
6. Type your message, set delay, and click **"Send to All"**.  

---

## 📁 File Format

### Example `numbers.csv`
```csv
phone
923001112233
923009998877
```

### Example `numbers.txt`
```
923001112233
923009998877
```

---

## 🧑‍💻 Developer Info

**Developed by:** *Faraz Hussain*  
**Supervised by:** *Sir Shahzaib & Sir Ali Hamza*  
**Technology:** Python, Streamlit, Selenium, WebDriver Manager  
**Background:** AI-powered automation with modern UI design  

---

## ⚠️ Disclaimer

This tool is for **educational and personal use only**.  
The developer is **not responsible** for any misuse or violation of WhatsApp’s terms of service.  
Use responsibly and avoid spam messaging.  

---

⭐ *If you like this project, don’t forget to star it and share your feedback!*
