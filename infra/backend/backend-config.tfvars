bucket         = "chrismlittle-terraform-state"
dynamodb_table = "terraform-lock"
encrypt        = true
key            = "${var.project}/terraform.tfstate"
region         = "eu-west-2"
