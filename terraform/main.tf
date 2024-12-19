provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "ml_server" {
  ami = "ami-0d08c3b92d0f4250a"
  instance_type = "t2.micro"
}

output "instance_ip" {
  value = aws_instance.ml_server.public_ip
}
