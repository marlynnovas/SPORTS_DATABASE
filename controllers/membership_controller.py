from services.membership_service import create_membership, get_active_membership

def assign_membership(data: dict):
    try:
        member_id = int(data.get("member_id"))
        plan_id = int(data.get("plan_id"))
        duration_days = int(data.get("duration_days"))
    except:
        return {"error": "Invalid data"}

    create_membership(member_id, plan_id, duration_days)

    return {"success": "Membership assigned"}


def get_membership(member_id: int):
    membership = get_active_membership(member_id)

    if not membership:
        return {"error": "No membership found"}

    return membership