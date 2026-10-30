# IT & Network Frequently Asked Questions (IT FAQ)

## I cannot connect to the Enterprise VPN
If a user reports they cannot connect to the VPN or are getting a "Gateway Timeout" error:
1. **Check System Status:** The agent MUST first use the system status tool to check the 'vpn' service.
2. **If VPN is Down:** Inform the user there is a known outage and IT is working on it. Do not create a ticket.
3. **If VPN is Operational:** Instruct the user to restart their router and flush their DNS cache. If they reply that it still does not work, create a MEDIUM Severity IT ticket.

## I need administrator rights to install software
Standard company policy prohibits giving local administrator rights to user laptops.
*   **Standard Users:** If they need specific software installed, create a LOW Severity ticket so the IT team can remotely push the software to their machine. 
*   **VIP Users:** VIPs (such as executives or lead developers) are exempt. Create a HIGH Severity ticket for IT to temporarily unlock admin privileges on the VIP's machine.

## My account is locked out
Accounts lock automatically after 5 failed password attempts.
*   **Action:** Instruct the user to wait 15 minutes for the automatic lockout timer to expire, then use the "Forgot Password" link. If they state it is an emergency, create a HIGH Severity ticket for IT Support.