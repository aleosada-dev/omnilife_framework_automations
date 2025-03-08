# Omnilife Framework Automations

A Python automation framework for personal productivity using the Polylith architecture pattern. This project connects various productivity tools (Notion, Google Calendar) and automates routine tasks through AWS Lambda functions.

## Features

- **Urgent Project Automation**: Automatically marks Notion projects as urgent based on their deadline
- **Weekly Planning**: Syncs events from Google Calendar to Notion tasks for upcoming week planning
- **Multiple Calendar Support**: Handles both work and personal calendars

## Architecture

This project follows the [Polylith](https://polylith.gitbook.io/polylith) architecture pattern, organizing code into:

- **Components**: Reusable modules with specific responsibilities
- **Bases**: Applications that use components
- **Projects**: Deployable units combining bases and components

### Key Components

- `notion`: Notion API integration
- `project`: Project-related entities and services
- `task`: Task-related entities and services
- `event`: Event-related entities for calendar integration
- `google`: Google Calendar API integration
- `parameter`: Configuration and secrets management
- `logger`: Structured logging

## Technical Stack

- **Python 3.11+**
- **AWS Lambda** for serverless execution
- **Terraform** for infrastructure as code
- **Poetry** for dependency management
- **Injector** for dependency injection
- **Pendulum** for date/time handling
- **Pytest** for testing

## Getting Started

### Prerequisites

- Python 3.11+
- Poetry
- Terraform
- AWS CLI configured

### Installation

1. Clone the repository:
   ```
   git clone [repository-url]
   cd omnilife-framework-automations
   ```

2. Install dependencies:
   ```
   poetry install
   ```

3. Configure environment variables:
   Create a `.env` file with:
   ```
   NOTION_APIKEY=your_notion_api_key
   NOTION_PROJECTS_DATABASE_ID=your_notion_projects_database_id
   NOTION_TASKS_DATABASE_ID=your_notion_tasks_database_id
   GOOGLE_CALENDAR_PROJECTID=your_google_calendar_project_id
   GOOGLE_CALENDAR_PRIVATEKEYID=your_google_calendar_private_key_id
   GOOGLE_CALENDAR_PRIVATEKEY=your_google_calendar_private_key
   GOOGLE_CALENDAR_CLIENTEMAIL=your_google_calendar_client_email
   GOOGLE_CALENDAR_CLIENTID=your_google_calendar_client_id
   GOOGLE_CALENDAR_CLIENTX509CERTURL=your_google_calendar_cert_url
   ```

### Deployment

1. Ensure you have AWS credentials configured:
   ```
   aws configure
   ```

2. Edit Terraform variables for your environment:
   ```
   cd projects/[project-name]/terraform
   vim terraform.tfvars
   ```

3. Deploy using the deploy script:
   ```
   ./deploy-script.sh [project-name]
   ```

## Project Structure

```
.
├── bases/                 # Application logic for Lambda functions
├── components/            # Reusable components
├── development/           # Development scripts and utilities
├── projects/              # Deployable projects combining bases and components  
│   ├── autofill_urgent_project/
│   └── plan_next_week/
└── test/                  # Test suite
```

## Development

### Testing

Run the test suite with:

```
poetry run pytest
```

### Adding a New Project

1. Create a new project directory:
   ```
   mkdir -p projects/new_project
   ```

2. Create a `pyproject.toml` file for your new project, listing the components it needs

3. Create a `terraform` subdirectory with deployment configuration

4. Add the project to the deploy script autocomplete:
   ```
   vim deploy-script-autocomplete
   ```

## License

[Your license information]

## Contributors

- [Your name or contributors]
