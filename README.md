# S3 File Management API

A serverless API to securely upload and download S3 files using Pre-signed URLs and HTTP 307 redirects.

## 🚀 Deployment

This repository is automated via **GitHub Actions**.

1. **Push** changes to the `main` branch.
2. **Monitor** the **Actions** tab in GitHub for build/deploy status.
3. **Retrieve** the `ApiEndpoint` from the deployment outputs.

---

## 🧪 Testing

### 1. Create a Mockup File

Before testing, create a local file to upload:

```bash
echo "Hello from my local machine" > hello.txt

```

### 2. Request Upload URL (POST)

```bash
# Replace "hello.txt" with your desired filename
curl -X POST <ENDPOINT>/files -H "Content-Type: application/json" -d "{\"filename\":\"hello.txt\"}"

```

*Returns a JSON containing the `uploadUrl`.*

### 3. Upload File (PUT)

```bash
# Use the URL returned from the step above (keep the quotes!)
curl -i -X PUT "<UPLOAD_URL>" --upload-file hello.txt

```

*Uploads the local file directly to S3.*

### 4. Verify Download Redirect (GET)

```bash
# Use the filename you uploaded. This command shows the redirect logic.
curl -v <ENDPOINT>/files/hello.txt

```

*Shows the **307 Temporary Redirect** and the signed S3 URL in the `location` header.*

---

## ⚙️ Technical Specs

* **Infrastructure:** API Gateway (HTTP API), Lambda (Python 3.12), S3.
* **Security:** Least-privilege IAM policies; SigV4 signing.
* **Redirection:** Uses **HTTP 307** to ensure the client preserves the `GET` method when redirected to S3.
* **Architecture:** Direct-to-S3 transfer bypasses Lambda execution and memory limits.

---

## 📄 Project Documentation

* [Project Report (Google Doc)](https://docs.google.com/document/d/1RJV_9Cfb35x-GWknntgHfZnE3a0l414_45PvGuDE5XE/edit?usp=sharing)

---

### A quick tip on the Google Doc link:

Make sure the Google Doc's share settings are set to **"Anyone with the link can view"** before you submit it, otherwise, your grader won't be able to open it!

**Would you like me to help you summarize the "Architecture Explanation" section for that Google Doc now?**
