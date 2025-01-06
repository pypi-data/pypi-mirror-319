"""Views."""

from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from orientation.models import NewMembers


@login_required
@permission_required("orientation.basic_access")
def index(request):
    """List all NewMembers ordered by creation date."""
    members = NewMembers.all_new_members_in_corp()
    return render(request, "orientation/index.html", {"members": members})


@require_POST
@permission_required("orientation.basic_access")
def mark_talked(request):
    """Mark a member as 'talked to'."""
    member_id = request.POST.get("member_id")
    print(request.POST)
    try:
        member = NewMembers.objects.get(id=member_id)
        member.member_talked_state = NewMembers.MembershipStates.TALKED
        member.save()
        return JsonResponse({"success": True})
    except NewMembers.DoesNotExist:
        return JsonResponse({"success": False, "error": "Member not found"})
