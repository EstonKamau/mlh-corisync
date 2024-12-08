# Vaultwarden Docker Setup

This folder contains a `docker-compose.vaultwarden.yml` file to deploy Vaultwarden, a lightweight alternative implementation of Bitwarden for managing and storing passwords securely.

---

## **Setup Overview**

Vaultwarden is deployed as a Docker container with the following features:
- Accessible through a custom port mapped to `9445` by default.
- Persistent storage using a volume (`./bitwarden:/data`).
- Environment variables to configure SMTP for email notifications, admin access, and domain settings.

---

## **Setup Instructions**

### 1. **Prerequisites**
- Install [Docker](https://www.docker.com/products/docker-desktop) and [Docker Compose](https://docs.docker.com/compose/install/).
- Ensure the required environment variables are defined in a `.env` file or your shell.

---

### 2. **Environment Variables**
Add the following variables to a `.env` file or export them in your shell:

```env
ADMIN_TOKEN=<your_admin_token>         # Token for admin panel access
WEBSOCKET_ENABLED=true                 # Enable WebSocket support
SIGNUPS_ALLOWED=true                   # Allow new user signups
SMTP_HOST=<smtp_server>                # SMTP server for emails
SMTP_FROM=<from_email_address>         # Sender email address
SMTP_PORT=<smtp_port>                  # SMTP server port (e.g., 587)
SMTP_SECURITY=<security_protocol>      # SMTP security (e.g., starttls, none)
SMTP_USERNAME=<smtp_username>          # SMTP login username
SMTP_PASSWORD=<smtp_password>          # SMTP login password
DOMAIN=<your_domain>                   # Vaultwarden's accessible domain
```

---

### 3. **Run the Container**

Start Vaultwarden using Docker Compose:
```bash
docker-compose up -d
```

---

### 4. **Access Vaultwarden**
- Open a web browser and go to: `http://<your_domain>:9445` (replace `<your_domain>` with your domain or IP address).
- Use the admin panel token (`ADMIN_TOKEN`) for administrative access.

---

## **Volumes**

- The `./bitwarden:/data:rw` volume ensures all Vaultwarden data (users, passwords, etc.) is stored persistently.

---

## **Ports**

- The container listens on port `80`, which is mapped to `9445` (or a custom port) on the host. Update the `ports` section in `docker-compose.yml` if you want to use a different port.

---

## **Stopping the Service**

To stop and remove the Vaultwarden container:
```bash
docker-compose down
```

---

## **TLS Configuration**

Vaultwarden can be configured to use HTTPS by setting the `ROCKET_TLS` environment variable with paths to your certificate and private key:
```env
ROCKET_TLS={certs="/path/to/certs.pem",key="/path/to/key.pem"}
```

---

## **References**
- [Vaultwarden Documentation](https://github.com/dani-garcia/vaultwarden/wiki)
- [Docker Hub: Vaultwarden](https://hub.docker.com/r/vaultwarden/server)