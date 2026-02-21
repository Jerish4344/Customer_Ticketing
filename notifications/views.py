"""JeyaRamaDesk — Notification Views"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Notification


@login_required
def notification_list(request):
    """Display user's notifications with read/unread filter."""
    qs = Notification.objects.filter(user=request.user)

    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'unread':
        qs = qs.filter(is_read=False)
    elif filter_type == 'read':
        qs = qs.filter(is_read=True)

    notifications = qs[:100]  # Latest 100
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'filter_type': filter_type,
        'unread_count': unread_count,
    })


@login_required
@require_POST
def mark_read(request, pk):
    """Mark a single notification as read (AJAX)."""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_read()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def mark_all_read(request):
    """Mark all of the user's unread notifications as read."""
    Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).update(is_read=True, read_at=timezone.now())
    return JsonResponse({'status': 'ok'})


@login_required
def unread_count_api(request):
    """Quick JSON endpoint returning the unread count for the topbar badge."""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})
