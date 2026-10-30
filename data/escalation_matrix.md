# Support Ticket Escalation Matrix

## Severity Definitions
When the agent creates a support ticket, it must assign one of the following severity levels based strictly on these definitions:

*   **LOW Severity:** General inquiries, feature requests, or out-of-warranty repair quotes (e.g., liquid damage). No immediate human intervention required.
*   **MEDIUM Severity:** Standard tier hardware damage (pending photo review), isolated login issues, or non-blocking software bugs. Human SLA is 48 hours.
*   **HIGH Severity:** Any VIP hardware damage, persistent software crashes preventing work, or security/data loss concerns. Human SLA is 4 hours.

## Human Manager Loop-in Rules
The AI agent operates autonomously but must involve a human manager via the Calendar Booking tool under these strict conditions:
1. **VIP Hardware Issue:** Automatically book a manager for any VIP experiencing hardware failure.
2. **Irate Customer Protocol:** If the customer explicitly demands to "speak to a manager," "talk to a human," or expresses extreme frustration, the agent must apologize and immediately book a calendar slot with a human manager, regardless of the user's tier. 

## Ticketing Requirements
When creating a ticket, the agent must provide a concise `summary` that includes the user's tier, the core issue, and the troubleshooting steps already attempted.