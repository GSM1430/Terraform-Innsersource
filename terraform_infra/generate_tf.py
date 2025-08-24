import pandas as pd

# Input CSV file
INPUT_FILE = "instances.csv"
OUTPUT_FILE = "main.tf"

# Read spreadsheet
df = pd.read_csv(INPUT_FILE)

# Terraform header
terraform_code = '''# Auto-generated Terraform code
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

'''

# Loop through each row and generate module blocks
for _, row in df.iterrows():
    module_block = f'''
module "{row["instance_name"]}" {{
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 5.0"

  name                   = "{row["instance_name"]}"
  instance_type          = "{row["instance_type"]}"
  ami                    = "{row["ami"]}"
  key_name               = "{row["key_name"]}"
  vpc_security_group_ids = {row["security_group_ids"]}
  subnet_id              = "{row["subnet_id"]}"

  tags = {{
    Environment = "{row["environment"]}"
    Owner       = "{row["owner"]}"
  }}
}}
'''
    terraform_code += module_block

# Write to main.tf
with open(OUTPUT_FILE, "w") as f:
    f.write(terraform_code)

print(f"Terraform code generated in {OUTPUT_FILE}")
