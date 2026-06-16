# HelpDesk Case Assistant

HelpDesk Case Assistant is a Flask web application that analyzes IT help desk support messages and generates structured troubleshooting guidance.

## Live Demo

Try the live project here:

PASTE-YOUR-LIVE-LINK-HERE

## Project Overview

This project was built as a help desk training and productivity tool. I created a custom analyzer that contains common support policies, troubleshooting guidance, and instructions that users may need when submitting a ticket. In this project, the analyzer is designed for general help desk scenarios, but the concept can easily be adapted for a company’s internal support environment. For example, it could help onboard new employees by providing consistent guidance, directing requests to the appropriate team, and suggesting standard responses based on company procedures. A user can paste a support ticket or email into the website, and the system analyzes the message to return:

* Issue category
* Priority level
* Suggested support team
* Professional email reply
* Recent ticket history
* Dashboard view
* Search and filter options
* CSV export option

## Features

* Analyze IT support messages
* Detect common help desk issues
* Generate professional suggested replies
* Track recent tickets during the session
* View dashboard statistics
* Search and filter tickets
* Export ticket data as CSV
* Copy suggested replies quickly

## Example Issues the App Can Detect

* MFA / authenticator issue
* Password reset issue
* Account locked issue
* Email access issue
* Learning platform issue
* Software access issue
* Cloud storage issue
* VPN or Wi-Fi issue
* Suspicious email / phishing issue
* Unclear requests that need more information

## Example Messages to Test

```text
I need MFA reset because I changed my phone.
I forgot my password.
My account is locked.
I cannot access my course.
My cloud storage is full.
I received a suspicious email.
The app is not opening.
I can't get in, it says error.
```

## Technologies Used

* Python
* Flask
* HTML
* CSS
* Gunicorn
* Render

## How to Run Locally

### Mac

```bash
git clone https://github.com/imahrassi-design/helpdesk-case-assistant.git
cd helpdesk-case-assistant
python3 -m pip install -r requirements.txt
python3 app.py
```

Then open:

```text
http://127.0.0.1:5000
```

### Windows

```bash
git clone https://github.com/imahrassi-design/helpdesk-case-assistant.git
cd helpdesk-case-assistant
py -m pip install -r requirements.txt
py app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Deployment

This project is deployed using Render.

Since the live demo uses Render’s free plan, the website may take a few seconds to load if it has been inactive.

## What I Learned

Through this project, I practiced:

* Building a web application with Flask
* Connecting Python logic to an HTML form
* Creating reusable analyzer logic
* Designing a clean user interface
* Handling form submissions
* Generating structured support replies
* Deploying a Python web app online
* Preparing a project for GitHub and interviews

## Author

Created by Ines Mahrassi.
