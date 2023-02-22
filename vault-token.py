#!/bin/bash

# Get the current token from the environment variable
TOKEN="$VAULT_TOKEN"

# Lookup token information
TOKEN_INFO=$(vault token lookup "$TOKEN")

# Extract the expiration time from the token information
EXPIRATION_TIME=$(echo "$TOKEN_INFO" | jq -r '.data.expire_time')

# Calculate the time remaining until the token expires
CURRENT_TIME=$(date +%s)
EXPIRATION_TIMESTAMP=$(date -d "$EXPIRATION_TIME" +%s)
TIME_REMAINING=$((EXPIRATION_TIMESTAMP - CURRENT_TIME))

# Check if the token will expire in one week or less
if [ "$TIME_REMAINING" -le $((7 * 24 * 60 * 60)) ]; then
  # Create Jira ticket
  JIRA_SUMMARY="Vault token will expire in one week or less"
  JIRA_DESCRIPTION="The current Vault token will expire on $EXPIRATION_TIME. Please generate a new token before it expires."
  JIRA_PROJECT="MYPROJECT"
  JIRA_ISSUETYPE="Task"
  JIRA_ASSIGNEE="myusername"
  
  JIRA_API_URL="https://myjirainstance.com/rest/api/2/issue/"
  JIRA_AUTH=$(echo -n "myusername:mypassword" | base64)
  JIRA_HEADERS="Authorization: Basic $JIRA_AUTH"
  JIRA_DATA=$(cat <<EOF
{
  "fields": {
    "project": {
      "key": "$JIRA_PROJECT"
    },
    "issuetype": {
      "name": "$JIRA_ISSUETYPE"
    },
    "summary": "$JIRA_SUMMARY",
    "description": "$JIRA_DESCRIPTION",
    "assignee": {
      "name": "$JIRA_ASSIGNEE"
    }
  }
}
EOF
)
  curl -X POST \
       --header "Content-Type: application/json" \
       --header "$JIRA_HEADERS" \
       --data "$JIRA_DATA" \
       "$JIRA_API_URL"
fi
