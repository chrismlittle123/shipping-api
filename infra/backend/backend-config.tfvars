bucket         = "chrismlittle-terraform-state"
dynamodb_table = "terraform-lock"
encrypt        = true
key            = "lambda-template/terraform.tfstate"
region         = "eu-west-2"
