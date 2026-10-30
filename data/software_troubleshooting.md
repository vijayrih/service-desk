# Software Troubleshooting Guidelines

## Issue: Crashing on Startup
If a user reports that their enterprise software crashes immediately upon opening:
1. **Initial Troubleshooting Steps:** The agent should ask the user to perform the following two steps:
   - Step 1: Clear the application cache folder.
   - Step 2: Ensure their operating system is updated to the latest version.
2. **Persistent Crashing Rule:** Ask the user if they have already tried these steps. If the user confirms the software still crashes after 2 attempts or after completing the steps, DO NOT continue troubleshooting.
3. **Action:** Create a High Severity support ticket for the Level 2 Engineering team and inform the user that a senior technician will investigate.

## Issue: Login Failures and Authentication
If a user reports they cannot log in or see an "Authentication Failed" error:
1. **Check Global Outages First:** The agent MUST check the global system status tool for the 'authentication' service. 
2. **If Global Outage Active:** Do NOT create a support ticket. Inform the user that there is a known global outage, engineers are working on it, and they should try again in 1 hour.
3. **If Systems are Operational:** Ask the user to reset their password using the "Forgot Password" link on the login portal. If they still cannot log in, create a Medium Severity ticket.