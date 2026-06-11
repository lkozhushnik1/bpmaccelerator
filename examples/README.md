# Examples

This directory contains sample process payloads and generated output artefacts.

## Cloud Cost Anomaly Detection and Remediation

The **golden example** for the BPM Accelerator — a real-world FinOps process from the Financial Services / Insurance domain.

### Files

| File | Description |
|------|-------------|
| `cloud-cost-anomaly/intake.json` | Structured BYOP intake payload |
| `cloud-cost-anomaly/normalized-process.json` | Generated NormalizedProcess output |

### How to use

You can POST the intake file directly to the API:

```bash
curl -X POST http://localhost:8000/api/process/pipeline \
  -H "Content-Type: application/json" \
  -d @cloud-cost-anomaly/intake.json
```

Or run the full pipeline and save all outputs:

```bash
curl -X POST http://localhost:8000/api/process/pipeline \
  -H "Content-Type: application/json" \
  -d @cloud-cost-anomaly/intake.json \
  | python -m json.tool > cloud-cost-anomaly/pipeline-output.json
```
