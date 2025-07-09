# 🚀 DNS QUICK REFERENCE: politicalequity.io

## ⚡ IMMEDIATE ACTION NEEDED

**Configure this A record at your domain registrar:**

```
Type: A
Name: @ (or politicalequity.io)  
Value: 34.8.118.40
TTL: 300
```

## 🔍 QUICK CHECK COMMANDS

**Test DNS propagation:**
```bash
dig politicalequity.io A
# Expected: 34.8.118.40
```

**Check SSL certificate:**
```bash
gcloud compute ssl-certificates describe politicalequity-ssl-cert --global
```

**Monitor progress automatically:**
```bash
python3 check_dns_progress.py
```

## 📋 COMMON REGISTRARS

| Registrar | Login URL | DNS Location |
|-----------|-----------|--------------|
| **Namecheap** | namecheap.com | Domain List → Manage → Advanced DNS |
| **GoDaddy** | godaddy.com | My Products → Domains → Manage DNS |
| **Google Domains** | domains.google.com | DNS tab |
| **Cloudflare** | cloudflare.com | DNS → Records |

## ⏰ TIMELINE

- **DNS Propagation**: 15 min - 2 hours (typically)
- **SSL Certificate**: 15-60 min after DNS  
- **Domain Live**: Total 30 min - 3 hours

## 🆘 HELP

**If stuck, check:**
1. Delete any existing A records first
2. Use `@` not `www` for the name
3. Verify IP is exactly: `34.8.118.40`
4. Set TTL to 300 (5 minutes)

**Questions?** Ask me anytime during the process!

---
**🎯 Once configured, your professional domain will be live at: https://politicalequity.io**