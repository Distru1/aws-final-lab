# aws-final-lab
S3 File Management API
A serverless API to securely upload and download S3 files using Pre-signed URLs and HTTP 307 redirects.

🚀 Deployment
This repository is automated via GitHub Actions.
1. Push changes to the main branch.
2. Monitor the Actions tab in GitHub for build/deploy status.
3. Retrieve the ApiEndpoint from the deployment outputs.

🧪 Testing
1. Request Upload URL (POST)
  # Replace "hello.txt" with your desired filename
curl -X POST <ENDPOINT>/files -H "Content-Type: application/json" -d "{\"filename\":\"hello.txt\"}"
  * Returns a JSON containing the uploadUrl.

2. Upload File (PUT)
  # Use the URL returned from the step above
curl -i -X PUT "<UPLOAD_URL>" --upload-file hello.txt
  Uploads the local file directly to S3.

3. Verify Download Redirect (GET)
# Use the filename you uploaded. This command shows the redirect logic.
curl -v <ENDPOINT>/files/hello.txt
Shows the 307 Temporary Redirect and the signed S3 URL in the location header.

⚙️ Technical Specs
Infrastructure: API Gateway (HTTP API), Lambda (Python 3.12), S3.
Security: Least-privilege IAM policies; SigV4 signing.
Redirection: Uses HTTP 307 to ensure the browser/client preserves the GET method when redirected to S3.
Architecture: Direct-to-S3 transfer bypasses Lambda execution and memory limits.
