# 🎯 SQUARESPACE DOMAINS DNS CONFIGURATION

## Your Domain Setup
- **Domain**: politicalequity.io
- **Registrar**: Squarespace Domains (formerly Google Domains)
- **Name Servers**: Google Cloud DNS ✅ (Perfect!)
- **Target IP**: 34.8.118.40

## 🚀 STEP-BY-STEP INSTRUCTIONS

### **Option 1: Squarespace Domains Dashboard**

1. **Login to Squarespace**
   - Go to: https://domains.squarespace.com
   - Login with your account

2. **Navigate to DNS**
   - Find `politicalequity.io` in your domain list
   - Click "Manage" or the domain name
   - Look for "DNS Settings" or "DNS Records"

3. **Add the A Record**
   ```
   Type: A
   Name: @ (or leave blank for root domain)
   Value: 34.8.118.40
   TTL: 300 seconds
   ```

4. **Delete Existing Records**
   - Remove any existing A records for `@` or the root domain
   - Keep other records (MX, TXT, etc.) unless they conflict

5. **Save Changes**
   - Click "Save" or "Update"
   - Changes typically take 5-15 minutes

### **Option 2: Google Cloud DNS (Recommended)**

Since you're using Google Cloud DNS name servers, you can manage DNS directly from Google Cloud Console:

1. **Access Google Cloud Console**
   ```bash
   # Check if DNS zone exists
   gcloud dns managed-zones list | grep politicalequity
   ```

2. **If DNS zone exists, add the record:**
   ```bash
   # Add A record
   gcloud dns record-sets create politicalequity.io. \
     --zone="YOUR_ZONE_NAME" \
     --type="A" \
     --ttl=300 \
     --rrdatas="34.8.118.40"
   ```

3. **If no DNS zone, create one:**
   ```bash
   # Create DNS zone
   gcloud dns managed-zones create politicalequity-zone \
     --description="DNS zone for politicalequity.io" \
     --dns-name="politicalequity.io."
   
   # Add A record
   gcloud dns record-sets create politicalequity.io. \
     --zone="politicalequity-zone" \
     --type="A" \
     --ttl=300 \
     --rrdatas="34.8.118.40"
   ```

## 🔍 VERIFICATION

**Check if Google Cloud DNS zone exists:**
```bash
gcloud dns managed-zones list
```

**Test DNS propagation:**
```bash
dig politicalequity.io A
```

**Monitor progress:**
```bash
python3 check_dns_progress.py
```

## ⚡ FASTEST METHOD

Since you're already using Google Cloud, the fastest approach is:

1. **Check for existing DNS zone**
2. **Add A record via gcloud command**
3. **Monitor with our script**

This bypasses any web interface delays and uses the same infrastructure as your load balancer.

## 🎯 EXPECTED TIMELINE

- **Google Cloud DNS**: 1-5 minutes propagation
- **Squarespace Interface**: 5-15 minutes
- **SSL Certificate**: 15-60 minutes after DNS
- **Domain Live**: 20-75 minutes total

---

**Which method would you prefer to use?**
1. **Google Cloud DNS** (fastest, via command line)
2. **Squarespace Dashboard** (web interface)

Let me know and I can walk you through the exact steps!