variable "do_token" {
  description = "DigitalOcean API token"
  type        = string
}

variable "droplet_name" {
  description = "Name of the DigitalOcean Droplet"
  type        = string
  default     = "example-droplet"
}

variable "region" {
  description = "Region where the Droplet will be created"
  type        = string
  default     = "nyc3"
}

variable "size" {
  description = "Droplet size"
  type        = string
  default     = "s-1vcpu-1gb"
}

variable "image" {
  description = "Operating System image for the Droplet"
  type        = string
  default     = "ubuntu-20-04-x64"
}

variable "ssh_keys" {
  description = "List of SSH keys to associate with the Droplet"
  type        = list(string)
}

variable "ssh_private_key_path" {
  description = "Path to the private SSH key for provisioning"
  type        = string
  default     = "~/.ssh/id_rsa"
}