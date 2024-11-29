# Terraform Configuration

This folder contains Terraform configuration files for managing infrastructure on 
AWS.
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

## Files

- **`main.tf`**: Defines the resources to be created.
- **`provider.tf`**: Configures the provider (AWS in this case).
- **`variables.tf`**: Contains variable definitions for the configuration.
- **`outputs.tf`**: Specifies the outputs of the infrastructure.
- **`terraform.tfvars`**: Provides default values for the variables.

## Prerequisites

1. Install [Terraform](https://www.terraform.io/downloads).
2. Configure AWS CLI and ensure you have access to deploy resources:
   ```bash
   aws configure
   ```

## Usage

1. **Initialize the project**:
   ```bash
   terraform init
   ```

2. **Validate the configuration**:
   ```bash
   terraform validate
   ```

3. **Plan the infrastructure**:
   ```bash
   terraform plan
   ```

4. **Apply the configuration**:
   ```bash
   terraform apply
   ```

5. **Destroy the infrastructure** (when no longer needed):
   ```bash
   terraform destroy
   ```

## Notes

- Ensure your AWS credentials are configured before running the commands.
- Update the `terraform.tfvars` file to match your requirements.

## References

- [Terraform Documentation](https://www.terraform.io/docs)
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)


---

### How to Use
1. Copy the files into the `terraform/` directory.
2. Update the `terraform.tfvars` file with your specific AMI ID and other configurations.
3. Run Terraform commands as described in the `README.md`.
