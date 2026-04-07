from services.plan_service import create_plan, get_all_plans
from models import Plan

def add_plan(data: dict):
    try:
        plan = Plan(
            name=data.get("name"),
            duration_days=int(data.get("duration_days")),
            price=float(data.get("price"))
        )
    except:
        return {"error": "Invalid data"}

    if plan.duration_days <= 0 or plan.price <= 0:
        return {"error": "Invalid values"}

    create_plan(plan)
    return {"success": "Plan created"}


def list_plans():
    return get_all_plans()