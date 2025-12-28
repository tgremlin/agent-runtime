# Keycloak Configuration

This directory contains the Keycloak realm configuration for Agent Runtime.

## Files

- `realm-export.json` - Exported realm configuration that is auto-imported on startup

## Default Configuration

### Realm: `agent-runtime`

### Clients

| Client ID | Type | Description |
|-----------|------|-------------|
| `agent-runtime` | Confidential | Main API client |
| `agent-runtime-cli` | Public | CLI client (device flow) |

### Roles

| Role | Description |
|------|-------------|
| `admin` | Platform administrator |
| `operator` | Tenant operator |
| `user` | Regular user |

### Default Users

| Username | Password | Roles | Notes |
|----------|----------|-------|-------|
| `admin` | `admin` | admin | Password change required on first login |

## Custom Claims

The `agent-runtime` client includes a custom protocol mapper that adds `tenant_id` to tokens:

```json
{
  "claim.name": "tenant_id",
  "user.attribute": "tenant_id"
}
```

## Development

### Access Keycloak Admin Console

1. Start the stack: `docker compose up -d`
2. Open http://localhost:8080
3. Login with `admin` / `admin` (set via `KEYCLOAK_ADMIN_PASSWORD`)

### Export Realm Changes

After making changes in the admin console, export the realm:

```bash
docker exec agent-runtime-keycloak /opt/keycloak/bin/kc.sh export \
  --dir /tmp/export \
  --realm agent-runtime

docker cp agent-runtime-keycloak:/tmp/export/agent-runtime-realm.json ./realm-export.json
```

## Production Considerations

1. **Change all default passwords**
2. **Use proper SSL/TLS certificates**
3. **Configure proper redirect URIs**
4. **Enable email verification**
5. **Review and harden security headers**
6. **Set up proper backup for the database**
