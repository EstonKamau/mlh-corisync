Below is a Terraform folder structure and configuration tailored for provisioning resources on **DigitalOcean**. This example demonstrates creating a Droplet (VM instance) on DigitalOcean.

---

### **Folder Structure**

```
terraform/
aws/
  ├── main.tf
  ├── variables.tf
  ├── outputs.tf
  ├── provider.tf
  ├── terraform.tfvars
  ├── README.md
```
---

# Terraform DigitalOcean Configuration

This folder contains Terraform configuration files to provision infrastructure on DigitalOcean.

## Files

- **`main.tf`**: Defines the Droplet resource and provisions basic software (e.g., Nginx).
- **`provider.tf`**: Configures the DigitalOcean provider using an API token.
- **`variables.tf`**: Contains variable definitions for the configuration.
- **`outputs.tf`**: Specifies the outputs of the infrastructure.
- **`terraform.tfvars`**: Provides default values for the variables.

## Prerequisites

1. Install [Terraform](https://www.terraform.io/downloads).
2. Install [doctl](https://github.com/digitalocean/doctl) (optional for easier management).
3. Obtain your DigitalOcean API token:
   - Log in to DigitalOcean.
   - Navigate to API > Tokens/Keys and generate a personal access token.

4. Add an SSH key to your DigitalOcean account:
   ```bash
   doctl compute ssh-key create "my-key" --public-key-file ~/.ssh/id_rsa.pub
   ```

## Usage

1. **Initialize Terraform**:
   ```bash
   terraform init
   ```

2. **Validate the Configuration**:
   ```bash
   terraform validate
   ```

3. **Plan the Infrastructure**:
   ```bash
   terraform plan
   ```

4. **Apply the Configuration**:
   ```bash
   terraform apply
   ```

5. **Access the Droplet**:
   - Once the configuration is applied, the public IP of the Droplet will be displayed.
   - SSH into the Droplet:
     ```bash
     ssh root@<DROPLET_IP>
     ```

6. **Destroy the Infrastructure**:
   ```bash
   terraform destroy
   ```

## Notes

- The SSH private key specified in `ssh_private_key_path` must match the public key added to DigitalOcean.
- Update `terraform.tfvars` with your desired Droplet configuration.

## References

- [Terraform Documentation](https://www.terraform.io/docs)
- [DigitalOcean Documentation](https://www.digitalocean.com/docs/)


### Steps to Use
1. **Install Prerequisites**: Terraform, DigitalOcean CLI (`doctl`), and a configured SSH key.
2. **Update Variables**: Edit `terraform.tfvars` to include your API token and SSH key fingerprint.
3. **Run Terraform Commands**: Follow the commands listed in the `README.md`.
