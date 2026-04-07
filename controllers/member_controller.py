from services.member_service import create_member, get_all_members
from models import Member

def add_member(data: dict):
    member = Member(
        full_name=data.get("full_name"),
        phone=data.get("phone"),
        email=data.get("email")
    )

    if not member.full_name:
        return {"error": "Name is required"}

    create_member(member)
    return {"success": "Member created"}


def list_members():
    return get_all_members()