# SAP BTP Deployment Instructions

## Prerequisites
1. Install CF CLI: https://docs.cloudfoundry.org/cf-cli/install-go-cli.html
2. Login to your SAP BTP space:
   ```
   cf login -a <api-endpoint> -o <org> -s <space>
   ```

## Redis Service Setup
You mentioned you already have the Redis service created. If not, create it with:
```bash
cf create-service redis-enterprise-cloud <plan-name> requestbin-redis
```

Bind it manually if needed:
```bash
cf bind-service requestbin-app requestbin-redis
```

## Deployment Steps

1. **Ensure all dependencies are listed in requirements.txt**
2. **Deploy the application:**
   ```bash
   cf push
   ```

## Environment Variables
The app is configured to automatically detect SAP BTP Redis service via VCAP_SERVICES.

Your Redis service details:
- Host: master.rg-ef83f777-8965-4ef9-b9ab-8bb1e87043a5.iroxbd.euc1.cache.amazonaws.com
- Port: 1608
- TLS: Enabled
- Password: (from service key)

## Troubleshooting

1. **Check app logs:**
   ```bash
   cf logs requestbin-app --recent
   ```

2. **Check service binding:**
   ```bash
   cf env requestbin-app
   ```

3. **Check Redis connectivity:**
   ```bash
   cf ssh requestbin-app
   ```

## Important Notes
- The app automatically detects SAP BTP environment via VCAP_SERVICES
- SSL/TLS is enabled for Redis connections
- DB 0 is used by default for SAP BTP Redis
- Certificate hostname verification is disabled for SAP BTP compatibility