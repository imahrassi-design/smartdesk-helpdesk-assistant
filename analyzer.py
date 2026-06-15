"""
Public Analyzer for SmartDesk AI / HelpDesk Case Assistant

This file contains the main rule-based analyzer used by the web app.
It is written as a general IT help desk training tool, so it can be safely
shared on GitHub without exposing private school or company information.

The analyzer reads a user's support message and returns:
- category
- priority
- issue summary
- suggested reply
- support steps
- information to collect
- useful general links
- internal notes for the support agent
"""

import re


def normalize(text):
    """
    Convert the message to lowercase and remove extra spaces.
    This makes keyword matching easier and more reliable.
    """
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def has_any(text, keywords):
    """
    Check if the message contains any keyword from a list.
    """
    return any(keyword in text for keyword in keywords)


def make_result(
    category,
    priority,
    issue_summary,
    reply,
    support_steps,
    info_to_collect=None,
    useful_links=None,
    internal_notes=None,
):
    """
    Build a standard result dictionary.

    The website reads this dictionary and displays the result to the user.
    Keeping the same structure makes the project easier to maintain.
    """
    return {
        "category": category,
        "priority": priority,
        "issue_summary": issue_summary,
        "reply": reply,
        "student_reply": reply,
        "case_steps": support_steps,
        "support_steps": support_steps,
        "info_to_collect": info_to_collect or [],
        "useful_links": useful_links or [],
        "internal_notes": internal_notes or [],
        "team": "IT Service Desk",
    }


def password_reset_case():
    return make_result(
        category="Password Reset Issue",
        priority="Medium",
        issue_summary="The user is unable to reset their password or needs help creating a new password.",
        reply="""Subject: Password Reset Assistance

Hello,

Thank you for contacting the IT Service Desk.

Please try resetting your password using the password reset portal. Make sure your new password follows the required password rules, such as minimum length, complexity, and not reusing a recent password.

If you still cannot reset your password, please send us a screenshot of the error message you are receiving so we can review it further.

Kind regards,
IT Service Desk""",
        support_steps=[
            "Confirm whether the user is trying to reset a forgotten password or change a known password.",
            "Ask for a screenshot if the password reset fails.",
            "Remind the user to follow password complexity rules.",
            "Check whether the account is locked or inactive if the reset keeps failing.",
        ],
        info_to_collect=[
            "Screenshot of the error message",
            "Whether the user forgot the password or is changing an existing one",
            "Whether they can access their recovery email or phone",
        ],
        useful_links=[
            "Password reset portal",
            "Password rules page",
        ],
        internal_notes=[
            "Do not ask the user to send their password.",
            "If identity verification is required, follow the organization's approved process.",
        ],
    )


def mfa_case():
    return make_result(
        category="Multi-Factor Authentication Issue",
        priority="High",
        issue_summary="The user cannot complete MFA because they changed phones, lost access to the authenticator app, or cannot receive verification codes.",
        reply="""Subject: MFA Verification Assistance

Hello,

Thank you for contacting the IT Service Desk.

It looks like you may be having trouble with multi-factor authentication. Please confirm whether you recently changed your phone, lost access to your authenticator app, or are unable to receive verification codes.

Once we confirm the details, we can guide you through the next steps to restore access.

Kind regards,
IT Service Desk""",
        support_steps=[
            "Confirm the user’s identity using the approved verification process.",
            "Ask whether the user changed phones or lost access to the authenticator app.",
            "Check whether the issue is with the authenticator app, SMS, phone call, or recovery email.",
            "Escalate or reset MFA only if the user has been properly verified.",
        ],
        info_to_collect=[
            "Did the user change phones?",
            "Are they using an authenticator app, SMS, or phone call?",
            "Screenshot of the MFA error if available",
            "Best contact method",
        ],
        useful_links=[
            "MFA setup guide",
            "Authenticator app setup guide",
        ],
        internal_notes=[
            "MFA issues should be handled carefully because they involve account security.",
            "Never bypass MFA without proper identity verification.",
        ],
    )


def account_locked_case():
    return make_result(
        category="Account Locked",
        priority="High",
        issue_summary="The user's account may be locked due to repeated failed login attempts or security restrictions.",
        reply="""Subject: Account Lockout Assistance

Hello,

Thank you for contacting the IT Service Desk.

Your account may be temporarily locked due to multiple failed sign-in attempts or a security restriction. Please wait a short period and try again. If the issue continues, send us a screenshot of the message you see when signing in.

Kind regards,
IT Service Desk""",
        support_steps=[
            "Check if the account is locked due to repeated failed attempts.",
            "Ask for the exact error message.",
            "Confirm whether the user recently changed their password.",
            "Escalate if the account is disabled, compromised, or blocked by policy.",
        ],
        info_to_collect=[
            "Exact error message",
            "Screenshot",
            "When the issue started",
            "Whether the user recently changed their password",
        ],
        useful_links=[
            "Account recovery guide",
            "Password reset portal",
        ],
        internal_notes=[
            "Account lockout may be temporary, but repeated lockouts may indicate saved old passwords on a device.",
        ],
    )


def login_credentials_case():
    return make_result(
        category="Login Credentials Not Received",
        priority="Medium",
        issue_summary="The user has not received their username, temporary password, or account setup information.",
        reply="""Subject: Login Credentials Assistance

Hello,

Thank you for contacting the IT Service Desk.

If you have not received your login credentials, please check your personal email inbox, junk folder, and spam folder. If you still cannot find the message, please provide your full name and student or employee ID so we can review your account status.

Kind regards,
IT Service Desk""",
        support_steps=[
            "Ask the user to check inbox, junk, and spam folders.",
            "Confirm the user’s account status.",
            "Verify that the correct personal email address is on file.",
            "Escalate if credentials need to be resent by the proper department.",
        ],
        info_to_collect=[
            "Full name",
            "Student or employee ID",
            "Personal email address on file",
            "Program, department, or role if applicable",
        ],
        useful_links=[
            "Account activation guide",
            "New user login guide",
        ],
        internal_notes=[
            "Do not provide login credentials in an insecure way.",
        ],
    )


def email_issue_case():
    return make_result(
        category="Email Access Issue",
        priority="Medium",
        issue_summary="The user is having trouble accessing email, receiving emails, sending emails, or opening attachments.",
        reply="""Subject: Email Access Assistance

Hello,

Thank you for contacting the IT Service Desk.

Please confirm what issue you are experiencing with your email. For example, are you unable to sign in, not receiving emails, unable to send emails, or having trouble opening an attachment?

Please also send a screenshot of any error message you see.

Kind regards,
IT Service Desk""",
        support_steps=[
            "Identify whether the problem is login, sending, receiving, attachment, or mailbox storage.",
            "Ask for a screenshot of the error message.",
            "Check whether the user can access email from a web browser.",
            "Escalate if mail flow or account permissions need investigation.",
        ],
        info_to_collect=[
            "Email address affected",
            "Screenshot of the issue",
            "Can the user access email from webmail?",
            "Is the issue with sending, receiving, or attachments?",
        ],
        useful_links=[
            "Email login page",
            "Email troubleshooting guide",
        ],
        internal_notes=[
            "Email issues can be caused by storage limits, security filtering, browser cache, or account status.",
        ],
    )


def lms_case():
    return make_result(
        category="Learning Management System Issue",
        priority="Medium",
        issue_summary="The user is having trouble accessing courses, files, assignments, or content in the learning platform.",
        reply="""Subject: Learning Platform Access Assistance

Hello,

Thank you for contacting the IT Service Desk.

Please confirm what issue you are experiencing in the learning platform. Are you unable to log in, missing a course, unable to open a file, or receiving an error message?

Please send a screenshot of the issue and the course name or course code so we can review it further.

Kind regards,
IT Service Desk""",
        support_steps=[
            "Identify whether the issue is login, missing course, file access, assignment upload, or browser error.",
            "Ask for course name or course code.",
            "Ask for a screenshot of the error.",
            "Suggest trying another browser or clearing browser cache if the issue seems browser-related.",
        ],
        info_to_collect=[
            "Course name or course code",
            "Screenshot of the error",
            "Browser used",
            "Whether the issue happens with one course or all courses",
        ],
        useful_links=[
            "Learning platform login page",
            "Browser troubleshooting guide",
        ],
        internal_notes=[
            "Missing courses may depend on enrollment, instructor availability, or course start date.",
        ],
    )


def software_access_case():
    return make_result(
        category="Software Access Issue",
        priority="Medium",
        issue_summary="The user cannot access required software, virtual apps, or installed applications.",
        reply="""Subject: Software Access Assistance

Hello,

Thank you for contacting the IT Service Desk.

Please confirm the name of the software you are trying to access and describe what happens when you open it. If you receive an error message, please send us a screenshot.

Kind regards,
IT Service Desk""",
        support_steps=[
            "Ask for the software name.",
            "Ask whether the user is using a personal device, lab computer, or virtual app platform.",
            "Ask for the exact error message.",
            "Check if the software requires VPN, licensing, or special access.",
        ],
        info_to_collect=[
            "Software name",
            "Device type",
            "Screenshot of error",
            "Whether the user is on campus, remote, or using VPN",
        ],
        useful_links=[
            "Software access guide",
            "Virtual apps guide",
        ],
        internal_notes=[
            "Software issues may be caused by licensing, installation problems, VPN requirements, or expired access.",
        ],
    )


def storage_case():
    return make_result(
        category="Cloud Storage Issue",
        priority="Medium",
        issue_summary="The user is running out of cloud storage or cannot upload/sync files.",
        reply="""Subject: Cloud Storage Assistance

Hello,

Thank you for contacting the IT Service Desk.

If your cloud storage is full, please check large files, deleted files in the recycle bin, and older file versions. These can still take up storage space.

If you are still having issues, please send a screenshot showing your storage usage.

Kind regards,
IT Service Desk""",
        support_steps=[
            "Ask the user to check storage usage.",
            "Suggest deleting unnecessary large files.",
            "Suggest emptying the recycle bin.",
            "Suggest checking file version history if supported.",
            "Escalate if storage quota looks incorrect.",
        ],
        info_to_collect=[
            "Screenshot of storage usage",
            "Whether the issue affects upload, sync, or saving files",
            "Approximate storage used",
        ],
        useful_links=[
            "Cloud storage guide",
            "File cleanup guide",
        ],
        internal_notes=[
            "Storage issues are often caused by recycle bin items, synced folders, large media files, or version history.",
        ],
    )


def vpn_wifi_case():
    return make_result(
        category="Network / VPN Issue",
        priority="Medium",
        issue_summary="The user cannot connect to Wi-Fi, VPN, or a network-required service.",
        reply="""Subject: Network or VPN Assistance

Hello,

Thank you for contacting the IT Service Desk.

Please confirm whether you are having trouble with Wi-Fi, VPN, or a specific service that requires network access. Please include the error message you see and whether you are on campus or working remotely.

Kind regards,
IT Service Desk""",
        support_steps=[
            "Identify whether the issue is Wi-Fi, VPN, or access to a network-only service.",
            "Ask whether the user is on campus or remote.",
            "Ask for the device type and operating system.",
            "Ask for a screenshot of the error message.",
        ],
        info_to_collect=[
            "Wi-Fi or VPN?",
            "On campus or remote?",
            "Device type",
            "Screenshot of error",
        ],
        useful_links=[
            "VPN setup guide",
            "Wi-Fi troubleshooting guide",
        ],
        internal_notes=[
            "Some services only work when connected to VPN or a trusted network.",
        ],
    )


def suspicious_email_case():
    return make_result(
        category="Suspicious Email / Phishing",
        priority="High",
        issue_summary="The user received a suspicious email and needs guidance on how to handle it safely.",
        reply="""Subject: Suspicious Email Guidance

Hello,

Thank you for contacting the IT Service Desk.

Please do not click any links, open attachments, or reply to the suspicious email. If your email system has a report phishing option, please use it to report the message.

If you already clicked a link or entered your password, please let us know immediately so we can help secure your account.

Kind regards,
IT Service Desk""",
        support_steps=[
            "Tell the user not to click links or open attachments.",
            "Ask whether they interacted with the email.",
            "Advise them to report the message using the approved phishing report option.",
            "Escalate immediately if the user entered credentials or downloaded a file.",
        ],
        info_to_collect=[
            "Sender email address",
            "Screenshot of the email",
            "Did the user click a link?",
            "Did the user enter their password?",
        ],
        useful_links=[
            "Phishing awareness guide",
            "Report phishing guide",
        ],
        internal_notes=[
            "Treat credential entry or downloaded attachments as urgent security concerns.",
        ],
    )


def unclear_case():
    return make_result(
        category="Needs More Information",
        priority="Medium",
        issue_summary="The message is too unclear to confidently identify the issue.",
        reply="""Subject: Additional Information Required

Hello,

Thank you for contacting the IT Service Desk.

To help you further, could you please provide more details about the issue you are experiencing?

Please include:
1. What you are trying to access
2. The exact error message
3. A screenshot of the issue
4. The device and browser you are using
5. When the issue started

Kind regards,
IT Service Desk""",
        support_steps=[
            "Do not guess the issue if the message is unclear.",
            "Ask the user for more information.",
            "Request a screenshot and exact error message.",
            "Review the case again once more details are provided.",
        ],
        info_to_collect=[
            "What system or website the user is trying to access",
            "Exact error message",
            "Screenshot",
            "Device and browser",
            "When the issue started",
        ],
        useful_links=[],
        internal_notes=[
            "This is the safe fallback case. It prevents the support agent from giving incorrect instructions.",
        ],
    )


def analyze_ticket(message):
    """
    Main analyzer function.

    The order of the checks matters.
    Specific security and access issues are checked before general cases.
    """
    text = normalize(message)

    if not text:
        return unclear_case()

    if has_any(text, [
        "phishing", "suspicious email", "spam email", "scam email",
        "strange email", "clicked a link", "entered my password",
        "survey email", "fake email"
    ]):
        return suspicious_email_case()

    if has_any(text, [
        "mfa", "multi factor", "multifactor", "authenticator",
        "verification code", "changed my phone", "new phone",
        "cannot approve sign in", "two factor", "2fa"
    ]):
        return mfa_case()

    if has_any(text, [
        "password", "reset my password", "forgot my password",
        "change my password", "password does not meet",
        "temporary password"
    ]):
        return password_reset_case()

    if has_any(text, [
        "locked", "account locked", "too many attempts",
        "blocked", "sign in blocked", "reference account is locked"
    ]):
        return account_locked_case()

    if has_any(text, [
        "credentials", "temporary password", "username",
        "did not receive my login", "never received", "account setup"
    ]):
        return login_credentials_case()

    if has_any(text, [
        "email", "mailbox", "outlook", "cannot send",
        "not receiving emails", "attachment", "inbox"
    ]):
        return email_issue_case()

    if has_any(text, [
        "blackboard", "canvas", "moodle", "learning platform",
        "course", "assignment", "lms", "course shell",
        "missing course", "cannot open file"
    ]):
        return lms_case()

    if has_any(text, [
        "software", "application", "app", "virtual app",
        "cloudpaging", "appsanywhere", "license", "install",
        "program is not opening"
    ]):
        return software_access_case()

    if has_any(text, [
        "storage", "onedrive", "google drive", "cloud storage",
        "quota", "sync", "upload files", "storage full"
    ]):
        return storage_case()

    if has_any(text, [
        "vpn", "wifi", "wi-fi", "network", "remote access",
        "cannot connect", "connection error"
    ]):
        return vpn_wifi_case()

    return unclear_case()
