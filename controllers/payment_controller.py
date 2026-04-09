from services.payment_service import register_payment

def make_payment(data: dict):
    try:
        member_id = int(data.get("member_id"))
        membership_id = int(data.get("membership_id"))
        amount = float(data.get("amount"))
    except:
        return {"error": "Invalid data"}

    if amount <= 0:
        return {"error": "Amount must be positive"}

    register_payment(member_id, membership_id, amount)

    return {"success": "Payment registered"}