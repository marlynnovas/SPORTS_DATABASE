# Sports Club Management System

A Python-based application using **Flet** for the UI and **SQLite** for the database.

## System Features
- **Member Management**: Create, update, and list members.
- **Plans & Memberships**: Assign plans to members and track validity.
- **Payment Processing**: Record payments and check status.
- **Access Control**: Log member access and validate permissions in real-time.

## Project Structure
- `main.py`: Entry point (Flet UI).
- `database/`: SQL schema and connection logic.
- `models/`: Data classes for core entities.
- `services/`: Business logic and database interactions.
- `views/`: UI components and page layouts.
- `components/`: Shared UI elements (sidebars, tables, forms).
- `utils/`: Helper functions and validators.

## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the virtual enviomment:
    ```bash
   source .venv/bin/activate
   ```

2. Run the application:
   ```bash
   python main.py
   ```
