from analyzer import analyze_ticket

test_tickets = [
    "My OneDrive says storage is full but I only have a few files.",
    "I cannot access my cFlex course in Blackboard.",
    "I did not receive my OntarioLearn temporary password.",
    "I am getting an SSO error when trying to log into Blackboard.",
    "Blackboard says 404 file not found when I open my PowerPoint.",
    "My Microsoft Authenticator is not working because I changed my phone.",
    "I changed my phone number and cannot approve the MFA request.",
    "CAN-8 crashes after I enter the server, username, and password.",
    "Respondus says I am banned from LockDown Browser and shows a reference code.",
    "I cannot install LockDown Browser on my Chromebook.",
    "Adobe says Access Denied and asks me to contact my administrator.",
    "My ArcGIS Pro says the account is already configured for offline mode.",
    "I cannot launch MyApps because AppsAnywhere says initialization error.",
    "Cloudpaging Player is stuck on the loading screen.",
    "I forgot my student number.",
    "I did not receive my Seneca login credentials.",
    "My account says reference account is currently locked out.",
    "I received a suspicious email asking me to complete a survey.",
    "I am missing an email from my professor.",
    "I cannot upload my MS Project file to Blackboard.",
]

for ticket in test_tickets:
    result = analyze_ticket(ticket)

    print("=" * 80)
    print("TICKET:")
    print(ticket)
    print()
    print("CATEGORY:", result.get("category"))
    print("PRIORITY:", result.get("priority"))
    print("CONFIDENCE:", result.get("confidence_score"))
    print("MATCHED KEYWORDS:", result.get("matched_keywords"))
