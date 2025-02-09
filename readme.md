# 🔥 OpenAI Reverse Proxy with Guardian Filter

This project implements a **reverse proxy for OpenAI's API**, integrating **IBM Granite Guardian** to filter and modify API requests and responses in real-time.  

## **🎯 Features**
✅ **Intercepts API requests** before they reach OpenAI.  
✅ **Filters out harmful prompts** using IBM Granite Guardian.  
✅ **Modifies unsafe responses** before returning to the client.  
✅ **Works with MITMProxy, NGINX, and Guardian AI filtering.**  
✅ **Supports Docker for easy deployment.**  

---

## **📂 Project Structure**
```
reverse-proxy-openai/
📂 nginx/                      # NGINX configuration
📂    ├── nginx.conf              # NGINX reverse proxy config
📂 mitmproxy/                   # MITMProxy module
📂    ├── proxy.py                 # MITMProxy script for modifying requests
📂 models/                      # IBM Granite Guardian Model integration
📂    ├── guardian_filter.py       # Handles toxicity filtering & classification
📂 scripts/                     # Testing scripts
📂    ├── send_prompt.py           # Sends prompt to OpenAI (or proxy)
📂 docker/                      # Docker setup
📂    ├── Dockerfile               # Main Dockerfile
📂    ├── docker-compose.yml       # Docker Compose file
📂 certs/                       # SSL certificates (for NGINX & MITMProxy)
📂 logs/                        # Log files (created automatically)
📂 .env                         # Environment variables (API keys, etc.)
📂 README.md                    # Setup & usage instructions
📂 requirements.txt             # Python dependencies
📂 **start_services.sh**        # 🔥 Start all services
```
---

## **🚀 Setup & Usage**
### **1️⃣ Install Dependencies**
Before running the project, install all required Python dependencies:
```bash
pip install -r requirements.txt
```
This ensures you have all necessary libraries, including:
- **MITMProxy** for request interception
- **Requests** for API calls
- **FastAPI & Uvicorn** for serving the Guardian filter

---

### **2️⃣ Start All Services**
Run the shell script to start all necessary components:
```bash
bash start_services.sh
```
This will:
✅ Start **Guardian Filter** (`guardian_filter.py`)  
✅ Launch **MITMProxy** (`proxy.py`)  
✅ Start **NGINX** as a reverse proxy  

Check `logs/` for any error messages if a service fails to start.

---

### **3️⃣ Send a Test Request**
Use the testing script to send a prompt through the proxy:
```bash
python scripts/send_prompt.py
```
✅ If everything is working correctly, the script will:
- Send a request to OpenAI through the **reverse proxy**.
- Check if the prompt **passes the Guardian filter**.
- Return a **filtered or modified response**.

---

### **4️⃣ (Optional) Run via Docker**
For a **containerized deployment**, use Docker Compose:
```bash
docker-compose up --build -d
```
This will spin up:
- A **Guardian Filter API container**  
- A **MITMProxy container**  
- An **NGINX reverse proxy container**  

🚨 **Important:** This setup is heavily dependent on your environment.  
Ensure:
- Docker is installed  
- You have enough **VRAM & disk space**  

---

## **🔐 Setting Up SSL Certificates**
To enable HTTPS, you will need SSL certificates. There are two options:

### **Option 1: Use Let's Encrypt (Recommended for Production)**
1. Install Certbot:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```
2. Obtain a free SSL certificate:
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```
3. Certbot will automatically update your NGINX config and install the certificates in:
   ```
   /etc/letsencrypt/live/yourdomain.com/fullchain.pem
   /etc/letsencrypt/live/yourdomain.com/privkey.pem
   ```
4. Restart NGINX:
   ```bash
   sudo systemctl restart nginx
   ```

### **Option 2: Use Self-Signed Certificates (For Development Only)**
1. Generate a self-signed certificate:
   ```bash
   mkdir certs
   openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes
   ```
2. Update your `nginx.conf` to use the generated certificates:
   ```nginx
   ssl_certificate /certs/cert.pem;
   ssl_certificate_key /certs/key.pem;
   ```
3. Restart NGINX:
   ```bash
   sudo systemctl restart nginx
   ```
4. Your browser will show a **security warning** because the certificate is self-signed.

---

## **🔧 Configuration**
### **🛠 Environment Variables**
Update your `.env` file or set environment variables manually:
```bash
export OPENAI_API_KEY="your-api-key-here"
export GUARDIAN_API_URL="http://localhost:5000"
```

### **🔹 Configuring the Guardian Filter Model**
Guardian Filter is currently configured to **run locally**. If needed, modify `guardian_filter.py` to connect to an **external API** or **pretrained model**.

---

## **🛠 Troubleshooting**
### **Problem: MITMProxy Doesn't Start**
❌ **Error:** `Connection refused`  
✅ **Solution:**
1. Check if **port 8080** is already in use:
   ```bash
   netstat -tulnp | grep 8080
   ```
   If another service is using it, change the MITMProxy port in `proxy.py`.

2. Restart MITMProxy:
   ```bash
   mitmdump -s mitmproxy/proxy.py --mode transparent --listen-host 0.0.0.0 --listen-port 8080
   ```

---

### **Problem: Guardian Filter Isn't Working**
❌ **Error:** `404 Not Found for /v1/completions`  
✅ **Solution:**
1. Make sure the Guardian Filter API is running:
   ```bash
   curl -X GET "http://localhost:5000/health"
   ```
   Expected output: `{"status": "healthy"}`

2. Restart it manually:
   ```bash
   python models/guardian_filter.py
   ```

---

### **Problem: Docker Running Out of Memory**
❌ **Error:** `CUDA out of memory` or `No space left on device`  
✅ **Solution:**
1. Reduce GPU memory usage:
   ```bash
   export PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True"
   ```
2. Free up disk space:
   ```bash
   docker system prune -a
   ```

---

## **📜 License**
This project is licensed under the **MIT License**. Feel free to use, modify, and distribute it.


