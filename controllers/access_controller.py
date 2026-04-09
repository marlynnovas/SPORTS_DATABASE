from services.access_service import validate_access

def check_access(member_id: int):
    try:
        member_id = int(member_id)
    except:
        return {"error": "Invalid member ID"}

    result = validate_access(member_id)

    return result