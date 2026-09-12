# Storage Schema

## Root

Default project-local root:

```text
.local-agent-pack/
```

## Artifact JSON

```text
.local-agent-pack/artifacts/{YYYYMMDD}/{id}.json
```

Required:

```json
{
  "id": "artifact-id",
  "type": "image-generation",
  "provider": "openrouter",
  "endpoint": "/images",
  "model": "model-slug",
  "input": {},
  "output": {},
  "artifacts": [],
  "usage": {},
  "provenance": {},
  "createdAt": "RFC3339"
}
```

## Video Jobs

```text
.local-agent-pack/jobs/videos/{jobId}.json
```

Required:

```json
{
  "id": "jobId",
  "provider": "openrouter",
  "endpoint": "/videos",
  "model": "model-slug",
  "status": "pending",
  "pollingUrl": "https://openrouter.ai/api/v1/videos/jobId",
  "request": {},
  "submittedAt": "RFC3339",
  "updatedAt": "RFC3339"
}
```

## Approval Records

```text
.local-agent-pack/approvals/{id}.json
```

Required:

```json
{
  "provider": "openrouter",
  "kind": "upload",
  "path": "absolute-path",
  "bytes": 123,
  "approvedAt": "RFC3339"
}
```