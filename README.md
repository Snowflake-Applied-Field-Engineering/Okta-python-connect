# Snowflake OAuth Client Credentials Connector

A Python script that establishes an automated connection to Snowflake using OAuth 2.0 client credentials flow with token auto-renewal.

## Overview

This script:
1. Requests an OAuth access token from an identity provider (e.g., Okta)
2. Establishes a connection to Snowflake using the token
3. Automatically refreshes the token every 5 minutes in the background
4. Executes a sample query to verify the connection

## Prerequisites

- Python 3.6+
- Required Python packages:
  - `requests`
  - `schedule`
  - `snowflake-connector-python`
  - `threading` (standard library)
  - `os` (standard library)
  - `time` (standard library)

## Configuration

Before running this script, you need to:

1. Configure an OAuth application in your identity provider (e.g., Okta)
2. Set up a client credentials flow for service-to-service authentication
3. Set the environment variable for your client secret:
   ```bash
   export OKTA_CLIENT_SECRET="your-client-secret"
   ```
4. Update the script with your specific values:
   - `TOKEN_URL`: Your identity provider's token endpoint
   - `CLIENT_ID`: Your OAuth client ID
   - `SCOPE`: The appropriate scope for your Snowflake role
   - Snowflake connection parameters (account, warehouse, database, schema)

## Usage

```bash
python snowflake_oauth_connector.py
```

The script will:
- Acquire an initial OAuth token
- Connect to Snowflake
- Run a test query to verify credentials and connection
- Refresh the token every 5 minutes in the background

## Security Considerations

- Store your client secret as an environment variable, never hardcode it
- Ensure the client credentials have appropriate permissions
- The script uses a daemon thread that will terminate when the main program exits

## Troubleshooting

If you encounter connection issues:
- Verify your client ID and secret are correct
- Check that the TOKEN_URL is accessible
- Ensure the requested scope is authorized for your client credentials
- Verify your Snowflake account parameters are correct

## Example Output

```
Initial token acquired: eyJraWQiOiJ1...
Connected to Snowflake via OAuth
[('EXAMPLE_USER', 'SYSADMIN', datetime.datetime(2023, 4, 1, 12, 0, 0))]
Snowflake connection closed.
```

## License

[Your License Here]
