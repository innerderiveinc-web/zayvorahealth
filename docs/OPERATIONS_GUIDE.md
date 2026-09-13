# ZAYVORA Health OS — System Operations & Telemetry Guide
**Document ID**: `ZAY-OPS-002`  
**Classification**: Site Reliability Engineering Standard  
**Date**: September 2026  

---

## 1. Routine Operational Procedures

### 1.1 Health Probes & Monitoring
The live REST API server provides a real-time health probe:
- **Endpoint**: `GET /api/health`
- **Output**:
  ```json
  {
    "ok": true,
    "service": "zayvora_live_api",
    "environment": "live_local",
    "database": "connected",
    "registered_users": 5,
    "timestamp": "2026-09-13T16:30:00Z"
  }
  ```

### 1.2 Daily OPD Queue Initialization
Front desk staff initialize the daily outpatient department queue at start-of-day:
1. Open Receptionist Dashboard at `/receptionist`.
2. Verify attending clinical faculty roster.
3. Tokens are generated sequentially (`T-101`, `T-102`, etc.) automatically upon patient check-in.

### 1.3 Dispensary Stock Monitoring
Pharmacy custodians review expiring batches and low inventory every morning:
1. Open Pharmacy Dashboard at `/pharmacy`.
2. Sort inventory by FEFO (First-Expired First-Out).
3. Review items marked with `is_schedule_e1 = 1` and verify Mudabbar detoxification certificates.

