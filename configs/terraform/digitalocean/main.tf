resource "digitalocean_droplet" "web" {
  image    = var.image
  name     = var.droplet_name
  region   = var.region
  size     = var.size
  ssh_keys = var.ssh_keys
  tags     = ["web", "terraform"]

  connection {
    type        = "ssh"
    user        = "root"
    private_key = file(var.ssh_private_key_path)
  }

  provisioner "remote-exec" {
    inline = [
      "apt-get update -y",
      "apt-get install -y nginx",
    ]
  }
}