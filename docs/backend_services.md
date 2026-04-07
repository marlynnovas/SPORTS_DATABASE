# Backend Services Integration Guide

This document describes the functions available in the `services/` layer for the frontend to consume.

## 1. Member Service (`member_service.py`)

| Function | Parameters | Returns | Description |
| :--- | :--- | :--- | :--- |
| `create_member` | `full_name, phone, email` | `int (id)` or `None` | Registers a new member. |
| `get_all_members` | None | `list[dict]` | Returns all members ordered by name. |
| `search_members` | `query` (str) | `list[dict]` | Searches members by name or email. |

## 2. Plan Service (`plan_service.py`)

| Function | Parameters | Returns | Description |
| :--- | :--- | :--- | :--- |
| `create_plan` | `name, duration_days, price` | None | Creates a new membership plan. |
| `get_all_plans` | None | `list[dict]` | Returns all storage plans. |

## 3. Membership Service (`membership_service.py`)

| Function | Parameters | Returns | Description |
| :--- | :--- | :--- | :--- |
| `create_membership` | `member_id, plan_id, duration_days` | None | Assigns a plan to a member. |
| `get_active_membership` | `member_id` | `dict` or `None` | Gets the most recent membership. |
| `refresh_membership_status`| `membership_dict` | `str (status)`| Checks if expired and **updates DB**. |
| `auto_expire_memberships`  | None | `int` (count) | Batch update of all expired memberships. |

## 4. Payment Service (`payment_service.py`)

| Function | Parameters | Returns | Description |
| :--- | :--- | :--- | :--- |
| `register_payment` | `member_id, membership_id, amount` | `bool` | Records a payment and activates membership. |
| `get_payments_by_member` | `member_id` | `list[dict]` | Returns payment history for a member. |

## 5. Access Service (`access_service.py`)

| Function | Parameters | Returns | Description |
| :--- | :--- | :--- | :--- |
| `validate_access` | `member_id` | `dict` | Validates status, logs entry, and returns `{result, message}`. |

## 6. Report Service (`report_service.py`)

| Function | Returns | Description |
| :--- | :--- | :--- |
| `get_monthly_revenue` | `list[dict]` | Revenue grouped by `{month, total_revenue, payment_count}`. |
| `get_membership_distribution` | `list[dict]` | Counts grouped by `{status, count}`. |
| `get_denied_access_stats` | `list[dict]` | Denied reasons grouped by `{message, count}`. |

---

## Data Model (Dictionary Structure)

All service functions return data as Python dictionaries for ease of use in Flet:

```python
# Member example
{
    "id": 1,
    "full_name": "Juan Perez",
    "phone": "123456789",
    "email": "juan@example.com",
    "join_date": "2024-04-07"
}

# Access result example
{
    "result": "granted", # or "denied"
    "message": "Acceso Permitido"
}
```
