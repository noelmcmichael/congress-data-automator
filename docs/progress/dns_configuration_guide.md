# DNS Configuration Guide: politicalequity.io

## 🎯 Target Configuration
**Domain**: `politicalequity.io`  
**Static IP**: `34.8.118.40`  
**Record Type**: A Record  
**TTL**: 300 seconds (5 minutes) for quick changes

---

## 📋 Step-by-Step DNS Configuration

### **Step 1: Identify Your Domain Registrar**

First, find out where you registered `politicalequity.io`:

```bash
# Check current DNS servers
dig politicalequity.io NS

# Or use whois to find registrar
whois politicalequity.io | grep -i registrar
```

Common registrars include:
- **Namecheap**
- **GoDaddy** 
- **Google Domains** (now Squarespace)
- **Cloudflare**
- **Route 53** (AWS)

### **Step 2: Access Your DNS Management**

#### **For Namecheap:**
1. Log in to namecheap.com
2. Go to "Domain List" → Find `politicalequity.io`
3. Click "Manage" → "Advanced DNS"

#### **For GoDaddy:**
1. Log in to godaddy.com
2. Go to "My Products" → "Domains" 
3. Click `politicalequity.io` → "Manage DNS"

#### **For Google Domains/Squarespace:**
1. Log in to domains.google.com
2. Select `politicalequity.io`
3. Go to "DNS" tab

#### **For Cloudflare:**
1. Log in to cloudflare.com
2. Select `politicalequity.io` from dashboard
3. Go to "DNS" → "Records"

#### **For Route 53:**
1. Log in to AWS Console
2. Go to Route 53 → "Hosted zones"
3. Click on `politicalequity.io`

### **Step 3: Configure the A Record**

**Add/Update the following record:**

| Field | Value |
|-------|-------|
| **Type** | A |
| **Name/Host** | `@` or `politicalequity.io` |
| **Value/Points to** | `34.8.118.40` |
| **TTL** | `300` (5 minutes) |

#### **Important Notes:**
- Use `@` for the root domain (most registrars)
- Some registrars want the full domain name `politicalequity.io`
- **Delete any existing A records** for the same name
- Set TTL to 300 for quick changes during setup

### **Step 4: Optional - Add www Subdomain**

For `www.politicalequity.io` to also work, add:

| Field | Value |
|-------|-------|
| **Type** | CNAME |
| **Name/Host** | `www` |
| **Value/Points to** | `politicalequity.io` |
| **TTL** | `300` |

---

## 🔍 Verification Steps

### **Immediate Verification (5-15 minutes)**

```bash
# Check if DNS has propagated
dig politicalequity.io A

# Expected output:
# politicalequity.io.     300     IN      A       34.8.118.40
```

### **Global DNS Propagation Check**

Use online tools to check propagation worldwide:
- https://www.whatsmydns.net/#A/politicalequity.io
- https://dnschecker.org/#A/politicalequity.io

### **Test Domain Response**

```bash
# Test HTTP response (will fail until SSL provisions)
curl -I http://politicalequity.io

# Test HTTPS once SSL is ready (15-60 min after DNS)
curl -I https://politicalequity.io
```

---

## ⏰ Timeline Expectations

### **Phase 1: DNS Propagation (15 minutes - 48 hours)**
- **Local DNS**: 5-15 minutes
- **ISP DNS**: 1-4 hours  
- **Global DNS**: 4-48 hours
- **Average**: 1-2 hours for most users

### **Phase 2: SSL Certificate Provisioning (after DNS)**
- **Google detects DNS**: 5-15 minutes after propagation
- **Certificate issuance**: 15-60 minutes
- **Total SSL time**: 20 minutes - 2 hours

### **Phase 3: Domain Fully Active**
- **Frontend loads**: Once SSL is provisioned
- **API routing works**: After CORS update

---

## 🛠️ Troubleshooting Guide

### **DNS Not Propagating**

```bash
# Check if your local DNS sees the change
nslookup politicalequity.io

# Try different DNS servers
nslookup politicalequity.io 8.8.8.8    # Google DNS
nslookup politicalequity.io 1.1.1.1    # Cloudflare DNS
```

**Common Issues:**
- Old A record still exists (delete it)
- TTL set too high (change to 300)
- Wrong record type (must be A, not CNAME for root)

### **SSL Certificate Not Provisioning**

Check certificate status:
```bash
gcloud compute ssl-certificates describe politicalequity-ssl-cert --global
```

**Common Issues:**
- DNS not fully propagated yet
- Multiple A records causing confusion
- Domain validation failing

### **Load Balancer Not Responding**

Check load balancer status:
```bash
gcloud compute forwarding-rules describe politicalequity-https-rule --global
```

---

## 📱 Mobile/Browser Testing

### **Clear DNS Cache**

**On macOS:**
```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

**On Windows:**
```cmd
ipconfig /flushdns
```

**In Browsers:**
- Chrome: `chrome://net-internals/#dns` → "Clear host cache"
- Firefox: Restart browser
- Safari: Restart browser

### **Test from Different Networks**
- Your home WiFi
- Mobile data (different ISP)
- Public WiFi
- VPN from different location

---

## 🚨 Emergency Rollback

If something goes wrong, quickly revert:

```bash
# Set TTL back to low value (300)
# Change A record back to original IP
# Or delete the A record entirely to disable domain
```

**Original frontend URL** (always works):
https://storage.googleapis.com/congressional-data-frontend/index.html

---

## 📋 DNS Configuration Checklist

- [ ] **Access domain registrar account**
- [ ] **Locate DNS management section**  
- [ ] **Delete any existing A records for `@` or `politicalequity.io`**
- [ ] **Add new A record: `@` → `34.8.118.40`**
- [ ] **Set TTL to 300 seconds**
- [ ] **Save/Apply changes**
- [ ] **Wait 5-15 minutes, then test with `dig politicalequity.io A`**
- [ ] **Check global propagation with online tools**
- [ ] **Monitor SSL certificate provisioning**
- [ ] **Test HTTPS once SSL is ready**

---

## 🎯 Success Indicators

### **DNS Configured Successfully:**
```bash
$ dig politicalequity.io A
politicalequity.io.     300     IN      A       34.8.118.40
```

### **SSL Certificate Ready:**
```bash
$ gcloud compute ssl-certificates describe politicalequity-ssl-cert --global
name: politicalequity-ssl-cert
type: MANAGED
managed:
  status: ACTIVE
  domainStatus:
    politicalequity.io: ACTIVE
```

### **Domain Fully Functional:**
```bash
$ curl -I https://politicalequity.io
HTTP/2 200
content-type: text/html
# ... other headers showing successful response
```

---

## 📞 Next Steps After DNS Configuration

1. **Monitor propagation** with online tools
2. **Check SSL certificate status** every 15 minutes
3. **Update CORS configuration** once domain resolves
4. **Test all endpoints** once HTTPS works
5. **Update any hardcoded URLs** in your application

---

**🎯 Your mission: Configure that A record and we'll have a professional domain live within hours!**