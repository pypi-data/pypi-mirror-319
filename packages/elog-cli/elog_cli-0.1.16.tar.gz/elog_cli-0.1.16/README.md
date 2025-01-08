# elog-cli

## Environment Variables

The following environment variables need to be set for the authentication manager to work:

- `CODE_FLOW_SERVER_URL`: The URL of the OAuth2 code flow server (e.g., `https://<hostname>/device/code`).
- `TOKEN_URL`: The URL to obtain the token (e.g., `https://<hostname>/token`).
- `CLIENT_ID`: The client ID for OAuth2 authentication.
- `CLIENT_SECRET`: The client secret for OAuth2 authentication.
- `ENPOINT_URL`: The base URL for the elog management backend client.

## Development

To set up the development environment, follow these steps:

1. Download the mock user authentication data:
    ```sh
    wget http://elog:8080/v1/mock/users-auth -O user.json
    ```

2. Generate the Python client from the OpenAPI specification:
    ```sh
    ~/.local/bin/openapi-python-client generate --url http://elog:8080/api-docs --output-path elog_management_backend_client --overwrite
    ```

3. Ensure all required environment variables are set:
    ```sh
    export ENPOINT_URL="http://elog:8080"
    ```

4. Run the application:
    ```sh
    python main.py login --login-type token
    ```
    and past one of the token found on the above downloaded `user.json`