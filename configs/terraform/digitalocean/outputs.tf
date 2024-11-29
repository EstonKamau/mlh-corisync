output "droplet_ip" {
  description = "Public IP of the Droplet"
  value       = digitalocean_droplet.web.ipv4_address
}