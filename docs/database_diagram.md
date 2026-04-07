# Database Schema Diagram

This diagram represents the relational structure of the Sports Club Management System.

```mermaid
erDiagram
    MEMBERS ||--o{ MEMBERSHIPS : has
    MEMBERS ||--o{ PAYMENTS : pays
    MEMBERS ||--o{ ACCESS_LOGS : enters
    PLANS ||--o{ MEMBERSHIPS : defines
    MEMBERSHIPS ||--o{ PAYMENTS : is_for

    MEMBERS {
        int id PK
        string full_name
        string phone
        string email
        date join_date
    }

    PLANS {
        int id PK
        string name
        int duration_days
        float price
    }

    MEMBERSHIPS {
        int id PK
        int member_id FK
        int plan_id FK
        date start_date
        date end_date
        string status
    }

    PAYMENTS {
        int id PK
        int member_id FK
        int membership_id FK
        float amount
        date payment_date
        string payment_status
    }

    ACCESS_LOGS {
        int id PK
        int member_id FK
        date access_date
        time access_time
        string result
        string message
    }
```

## Special Views

- **active_members_view**: Combines Members and Memberships to provide real-time access status (Allowed/Denied).
- **monthly_revenue_view**: Aggregates payment amounts by month for financial reporting.
