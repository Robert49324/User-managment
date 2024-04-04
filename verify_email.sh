#!/bin/bash
set -eo pipefail

awslocal ses verify-email-identity --email-address sender@example.com
echo "created email address: sender@example.com"
