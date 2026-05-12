# Async Task Queue → AWS Deployment Progress

**Date:** 2026-05-11
**Status:** App is live on AWS, end-to-end working. Need to verify worker via systemd tonight.
**Resume at:** Run the systemd sanity check + curl tests below.

---

## 🎯 What You Accomplished Today

You took your local FastAPI + Redis async task queue and:

1. ✅ Provisioned **AWS ElastiCache for Redis** (managed Redis cluster) — free tier
2. ✅ Provisioned a **t3.micro EC2** in the same VPC — free tier
3. ✅ Configured **security group** so EC2 ↔ Redis ↔ your laptop all work
4. ✅ Installed Python 3.11 + cloned repo + created virtualenv on EC2
5. ✅ Created a `.env` pointing your app to AWS Redis
6. ✅ Verified Redis connectivity from EC2 (got `True` from Python ping)
7. ✅ Ran `uvicorn` and successfully hit the API from inside the EC2
8. ✅ Set up **systemd services** for both FastAPI and worker (auto-start, auto-restart)

---

## 📋 Your AWS Resource Inventory (memorize these)

| Resource | Value | Notes |
|---|---|---|
| **AWS Region** | `ap-south-1` (Mumbai) | All resources are here |
| **VPC** | `vpc-0ebde86675e46a4cc` | Default VPC |
| **Security Group** | `sg-01ed5a626173bedc0` | Used by both Redis + EC2 |
| **ElastiCache name** | `my-redis` | Redis OSS, t3.micro, single node |
| **Redis endpoint** | `my-redis.neoll0.ng.0001.aps1.cache.amazonaws.com` | Port 6379 |
| **EC2 name** | `Async Task Queue` | Amazon Linux 2023, t3.micro |
| **EC2 Public IP** | `3.108.227.109` | ⚠️ May change if you stop/start the EC2 |
| **EC2 username** | `ec2-user` | For SSH |
| **SSH key file** | `C:\Users\anime\OneDrive\Desktop\my-app-key.pem` | ⚠️ DO NOT lose or share |
| **Project path on EC2** | `/home/ec2-user/Async-Task-Queue` | |

---

## 🔓 Security Group Inbound Rules (current)

| Type | Port | Source | Purpose |
|---|---|---|---|
| Custom TCP | 6379 | sg-01ed5a626173bedc0 | EC2 → Redis |
| SSH | 22 | My IP | Your laptop → EC2 |
| Custom TCP | 8000 | 0.0.0.0/0 (or My IP) | Internet → FastAPI |

⚠️ **If your home IP changes**, the SSH rule will stop working. Re-edit and pick "My IP" again.

---

## 🛠️ All Commands You Ran (in order)

### On your laptop (PowerShell)

```powershell
# Move SSH key to safe location (you ended up keeping it on Desktop)
mkdir "$env:USERPROFILE\.ssh" -ErrorAction SilentlyContinue
move "$env:USERPROFILE\Downloads\my-app-key.pem" "$env:USERPROFILE\.ssh\"

# Lock down key file permissions (Windows requires this for SSH)
icacls "$env:USERPROFILE\OneDrive\Desktop\my-app-key.pem" /inheritance:r
icacls "$env:USERPROFILE\OneDrive\Desktop\my-app-key.pem" /grant:r "$($env:USERNAME):(R)"

# SSH into EC2
ssh -i "$env:USERPROFILE\OneDrive\Desktop\my-app-key.pem" ec2-user@3.108.227.109
```

### On the EC2 (Linux shell, after SSH)

```bash
# Update OS + install basics
sudo dnf update -y
sudo dnf install -y python3 python3-pip git

# (Hit Python version error → installed Python 3.11)
sudo dnf install -y python3.11 python3.11-pip

# Clone the project
cd ~
git clone https://github.com/animeshrick/Async-Task-Queue.git
cd Async-Task-Queue

# Create virtualenv with Python 3.11
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file pointing to AWS Redis
cat > .env <<'EOF'
APP_NAME=Async-Task-Queue
APP_VERSION=1.0.0
APP_DESCRIPTION=Async task queue on AWS
APP_ENV=production
APP_HOST=0.0.0.0
APP_PORT=8000
REDIS_HOST=my-redis.neoll0.ng.0001.aps1.cache.amazonaws.com
REDIS_PORT=6379
REDIS_DB=0
EOF

# Test Redis connection (got True = working)
python -c "from redis import Redis; r = Redis(host='my-redis.neoll0.ng.0001.aps1.cache.amazonaws.com', port=6379); print(r.ping())"

# Manual run of FastAPI (worked, then stopped with Ctrl+C)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Created systemd service for FastAPI
sudo tee /etc/systemd/system/fastapi.service > /dev/null <<'EOF'
[Unit]
Description=FastAPI app (Async Task Queue)
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/Async-Task-Queue
EnvironmentFile=/home/ec2-user/Async-Task-Queue/.env
ExecStart=/home/ec2-user/Async-Task-Queue/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Created systemd service for worker
sudo tee /etc/systemd/system/worker.service > /dev/null <<'EOF'
[Unit]
Description=Async Task Queue Worker
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/Async-Task-Queue
EnvironmentFile=/home/ec2-user/Async-Task-Queue/.env
ExecStart=/home/ec2-user/Async-Task-Queue/venv/bin/python scripts/start_worker.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable + start both services
sudo systemctl daemon-reload
sudo systemctl enable --now fastapi.service worker.service
```

---

## 🌙 Resume Tonight (9 PM) — Do These in Order

### Step 1: SSH back into EC2

```powershell
ssh -i "$env:USERPROFILE\OneDrive\Desktop\my-app-key.pem" ec2-user@3.108.227.109
```

⚠️ If the public IP has changed, get the new one from AWS Console → EC2 → Instances.

### Step 2: Confirm both services are alive

```bash
sudo systemctl is-active fastapi worker
# Should print:
#   active
#   active
```

If either shows `inactive` or `failed`:
```bash
sudo journalctl -u fastapi.service -n 50 --no-pager
sudo journalctl -u worker.service -n 50 --no-pager
```

### Step 3: Fix the worker's debug sleep (still TODO)

You haven't done this yet. Edit the file:

```bash
cd ~/Async-Task-Queue
nano app/workers/worker.py
```

Find `time.sleep(120)` → delete that line. Save with Ctrl+O, Enter, Ctrl+X.

Then restart the worker:
```bash
sudo systemctl restart worker.service
```

### Step 4: End-to-end test

In one SSH window, watch logs:
```bash
sudo journalctl -u worker.service -f
```

In another SSH window, submit a task:
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_type":"email","payload":{"to":"animesh@example.com","subject":"It works!"}}'
```

Copy the `task_id`, then check status:
```bash
curl http://localhost:8000/tasks/<PASTE-TASK-ID>
```

✅ Should show `status: "success"` if everything works.

### Step 5: Test from your laptop browser

Visit:
- http://3.108.227.109:8000/ → JSON message
- http://3.108.227.109:8000/docs → Swagger UI (clickable API)

---

## 🧪 Real-World cURL Tests (paste into PowerShell on laptop OR SSH on EC2)

```bash
# Health check
curl http://3.108.227.109:8000/

# Submit email task
curl -X POST http://3.108.227.109:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_type":"email","payload":{"to":"test@x.com","subject":"hi","body":"hello"}}'

# Submit image task
curl -X POST http://3.108.227.109:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_type":"image","payload":{"filename":"cat.jpg","size_kb":245}}'

# Submit doc task
curl -X POST http://3.108.227.109:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_type":"doc","payload":{"title":"Plan","pages":12}}'

# Get task status (replace TASK_ID)
curl http://3.108.227.109:8000/tasks/TASK_ID

# Submit invalid task type (should return Failure)
curl -X POST http://3.108.227.109:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_type":"video","payload":{"url":"x"}}'

# Stress test: submit 10 tasks
for i in {1..10}; do
  curl -s -X POST http://3.108.227.109:8000/tasks \
    -H "Content-Type: application/json" \
    -d "{\"task_type\":\"email\",\"payload\":{\"to\":\"u$i@x.com\"}}"
  echo ""
done

# Inspect Redis directly
python3 -c "
from redis import Redis
r = Redis(host='my-redis.neoll0.ng.0001.aps1.cache.amazonaws.com', port=6379, decode_responses=True)
print('Queue length:', r.llen('/tasks/queue'))
print('All keys:', r.keys('/tasks/*'))
"
```

---

## 📝 Useful systemd Cheat Sheet

| Goal | Command |
|---|---|
| Status | `sudo systemctl status fastapi` |
| Live logs | `sudo journalctl -u fastapi -f` |
| Last 100 log lines | `sudo journalctl -u fastapi -n 100` |
| Restart after code change | `sudo systemctl restart fastapi worker` |
| Stop | `sudo systemctl stop fastapi worker` |
| Start | `sudo systemctl start fastapi worker` |

---

## 💸 Cost Status

If your AWS account is < 12 months old: **$0/month** (free tier covers everything).

After free tier expires: ~$22-25/month for both EC2 + ElastiCache running 24/7.

⚠️ **Set a zero-spend budget alarm** if you haven't:
AWS Console → Billing → Budgets → "Zero spend budget" template → email yourself.

---

## 🚧 Outstanding TODOs

- [ ] Remove `time.sleep(120)` from `app/workers/worker.py:35`
- [ ] Confirm `sudo systemctl is-active fastapi worker` returns `active` for both
- [ ] Run end-to-end curl test → see status reach `success`
- [ ] Verify browser access at http://3.108.227.109:8000/docs
- [ ] (Optional) Set up zero-spend budget alarm in AWS Billing
- [ ] (Optional) Open PR for the `chore/note-elasticache-endpoint` branch — already pushed, see https://github.com/animeshrick/Async-Task-Queue/pull/new/chore/note-elasticache-endpoint
- [ ] (Future) Set up domain name + HTTPS (would need ALB + ACM cert)
- [ ] (Future) Move EC2 to Auto Scaling Group for true production

---

## 🚨 Things to Remember

- **Never share or commit** `my-app-key.pem` — it's the only key to your EC2
- **`http://`** not `https://` (no SSL set up yet)
- **Redis is VPC-only** — your laptop cannot directly connect; always go through the EC2
- **EC2 stop/start changes the public IP** — use Elastic IP later if you need it stable (but Elastic IPs cost $3.60/mo when not attached to a running instance)
- **Free tier = 750 hrs/month** — exactly one of each running 24/7. Don't launch a second one.

---

## 🔗 Quick Links

- AWS Console: https://console.aws.amazon.com/
- ElastiCache: https://console.aws.amazon.com/elasticache/home?region=ap-south-1
- EC2 Instances: https://console.aws.amazon.com/ec2/home?region=ap-south-1#Instances
- Security Groups: https://console.aws.amazon.com/ec2/home?region=ap-south-1#SecurityGroups
- Billing: https://console.aws.amazon.com/billing/home
- Your repo: https://github.com/animeshrick/Async-Task-Queue
- API: http://3.108.227.109:8000/
- API docs: http://3.108.227.109:8000/docs

---

**See you at 9 PM. You got this. 🐴**
