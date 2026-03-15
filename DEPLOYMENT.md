# Deployment Guide

## Local Development

### 1. Setup
```bash
git clone <repo>
cd UFAC
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Gemini API key
```

### 2. Run CLI
```bash
python main.py
```

### 3. Run API Server
```bash
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

---

## Production Deployment

### Option 1: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t ufac-engine .
docker run -e GEMINI_API_KEY=your_key -p 8000:8000 ufac-engine
```

### Option 2: Heroku

Create `Procfile`:
```
web: uvicorn api.app:app --host 0.0.0.0 --port $PORT
```

Deploy:
```bash
heroku create ufac-engine
heroku config:set GEMINI_API_KEY=your_key
git push heroku main
```

### Option 3: AWS Lambda

Use AWS Lambda with API Gateway:
```bash
pip install -r requirements.txt -t package/
cd package
zip -r ../deployment.zip .
cd ..
zip deployment.zip -r . -x "*.git*" "package/*"
# Upload to Lambda
```

### Option 4: Google Cloud Run

```bash
gcloud run deploy ufac-engine \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=your_key
```

### Option 5: DigitalOcean App Platform

1. Connect GitHub repo
2. Set environment variable: `GEMINI_API_KEY`
3. Set run command: `uvicorn api.app:app --host 0.0.0.0 --port 8080`
4. Deploy

---

## Environment Variables

### Required
- `GEMINI_API_KEY`: Your Google Gemini API key

### Optional
- `API_HOST`: Server host (default: 0.0.0.0)
- `API_PORT`: Server port (default: 8000)
- `LOG_LEVEL`: Logging level (default: INFO)

---

## Performance Tuning

### For High Traffic

1. **Add Caching**:
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def run_ufac_cached(user_data_json):
    return run_ufac(json.loads(user_data_json))
```

2. **Use Gunicorn** (instead of Uvicorn):
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.app:app
```

3. **Add Redis Caching**:
```python
import redis
cache = redis.Redis(host='localhost', port=6379)
```

4. **Reduce LLM Calls**:
Edit `core/llm_utils.py`:
```python
def run_llm_council(prompt: str, num_runs: int = 2):  # Reduce from 3 to 2
```

### For Cost Optimization

1. **Use Gemini 1.5 Flash** (already configured - fastest & cheapest)
2. **Batch Requests**: Process multiple assessments together
3. **Cache Results**: Avoid duplicate assessments
4. **Monitor Usage**: Track API calls and costs

---

## Monitoring & Logging

### Add Monitoring

```python
# In api/app.py
from prometheus_client import Counter, Histogram
import time

request_count = Counter('ufac_requests_total', 'Total requests')
request_duration = Histogram('ufac_request_duration_seconds', 'Request duration')

@app.post("/check")
def check_eligibility(request: EligibilityCheckRequest):
    request_count.inc()
    start = time.time()
    try:
        result = run_ufac(request.model_dump(exclude_none=True))
        return result
    finally:
        request_duration.observe(time.time() - start)
```

### Log Aggregation

Use services like:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Datadog**
- **New Relic**
- **CloudWatch** (AWS)

---

## Security Checklist

- [ ] API key stored in environment variables
- [ ] HTTPS enabled in production
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Input validation enabled
- [ ] Error messages don't leak sensitive info
- [ ] Logging doesn't contain sensitive data
- [ ] Database credentials secured (if added)
- [ ] Regular security updates
- [ ] API authentication added (if needed)

---

## Scaling Strategy

### Phase 1: Single Server
- Single Uvicorn instance
- Local file storage
- Basic monitoring

### Phase 2: Load Balancing
- Multiple Uvicorn instances
- Nginx/HAProxy load balancer
- Shared cache (Redis)

### Phase 3: Microservices
- Separate agent services
- Message queue (RabbitMQ/Kafka)
- Distributed caching
- Database for persistence

### Phase 4: Serverless
- AWS Lambda / Google Cloud Functions
- API Gateway
- Managed databases
- Auto-scaling

---

## Backup & Recovery

### Database Backups
```bash
# If using PostgreSQL
pg_dump ufac_db > backup.sql
```

### Configuration Backups
```bash
# Backup .env (securely)
gpg -c .env
```

### Disaster Recovery Plan
1. Document all dependencies
2. Maintain backup API keys
3. Test recovery procedures
4. Keep deployment scripts in version control

---

## Rollback Procedure

```bash
# If deployment fails
git revert <commit-hash>
git push
# Redeploy

# Or use Docker tags
docker run -e GEMINI_API_KEY=key ufac-engine:v1.0.0
```

---

## Maintenance

### Regular Tasks
- [ ] Monitor API performance
- [ ] Review error logs
- [ ] Update dependencies monthly
- [ ] Test disaster recovery quarterly
- [ ] Review security settings
- [ ] Optimize database queries
- [ ] Clean up old logs

### Update Procedure
```bash
pip install --upgrade -r requirements.txt
python -m pytest tests/
git commit -am "Update dependencies"
git push
# Redeploy
```

---

## Support & Troubleshooting

### Common Issues

**API Key Error**
```
Solution: Check GEMINI_API_KEY environment variable
```

**Timeout Errors**
```
Solution: Increase timeout or reduce num_runs in llm_utils.py
```

**High Latency**
```
Solution: Add caching, reduce LLM calls, or upgrade server
```

**Out of Memory**
```
Solution: Reduce batch size, add more RAM, or use serverless
```

---

## Cost Estimation

### Monthly Costs (Rough Estimates)

**Low Volume** (100 assessments/day)
- Gemini API: ~$5
- Hosting: $10-20
- Total: ~$15-25/month

**Medium Volume** (1000 assessments/day)
- Gemini API: ~$50
- Hosting: $50-100
- Total: ~$100-150/month

**High Volume** (10000 assessments/day)
- Gemini API: ~$500
- Hosting: $200-500
- Total: ~$700-1000/month

---

## Next Steps

1. Choose deployment platform
2. Set up monitoring
3. Configure backups
4. Test disaster recovery
5. Document runbooks
6. Train team on deployment
7. Set up CI/CD pipeline
8. Monitor costs
9. Plan scaling strategy
10. Schedule regular reviews

---

## Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker Documentation](https://docs.docker.com/)
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [AWS Lambda](https://docs.aws.amazon.com/lambda/)
- [Heroku Deployment](https://devcenter.heroku.com/)
