from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Max, Count
from .models import Message


@login_required
def chat_list(request):
    user = request.user

    # Знаходимо всіх користувачів, з якими був чат
    user_ids = (
        Message.objects.filter(Q(sender=user) | Q(receiver=user))
        .values_list("sender", "receiver")
    )

    ids = set()
    for s, r in user_ids:
        ids.add(s)
        ids.add(r)
    ids.discard(user.id)

    users = User.objects.filter(id__in=ids)

    # Підрахунок непрочитаних повідомлень
    unread_counts = (
        Message.objects.filter(receiver=user, is_read=False)
        .values("sender")
        .annotate(unread_count=Count("id"))
    )
    unread_dict = {item["sender"]: item["unread_count"] for item in unread_counts}

    # Дата останнього повідомлення
    last_times = (
        Message.objects.filter(Q(sender=user) | Q(receiver=user))
        .values("sender", "receiver")
        .annotate(last_time=Max("created_at"))
    )

    # Знаходимо останню дату спілкування для кожного користувача
    user_last_time = {}
    for record in last_times:
        s, r, t = record["sender"], record["receiver"], record["last_time"]
        if s == user.id:
            other = r
        elif r == user.id:
            other = s
        else:
            continue
        if other not in user_last_time or user_last_time[other] < t:
            user_last_time[other] = t

    # Прив'язуємо дані до користувачів
    for u in users:
        u.unread_count = unread_dict.get(u.id, 0)
        u.last_time = user_last_time.get(u.id, None)

    # Сортуємо — спочатку ті, що писали останні або мають непрочитані
    users = sorted(users, key=lambda x: (x.unread_count > 0, x.last_time or 0), reverse=True)

    return render(request, "chat_list.html", {"users": users})


@login_required
def chat_detail(request, username):
    other_user = get_object_or_404(User, username=username)

    # Отримуємо всі повідомлення між двома користувачами
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('created_at')

    # Позначаємо повідомлення, які адресовані поточному користувачу, як прочитані
    messages.filter(receiver=request.user, is_read=False).update(is_read=True)

    # Відправлення нового повідомлення
    if request.method == 'POST':
        text = request.POST.get('text')
        if text.strip():
            Message.objects.create(sender=request.user, receiver=other_user, text=text)
            return redirect('chat_detail', username=other_user.username)

    return render(request, 'chat_detail.html', {
        'other_user': other_user,
        'messages': messages
    })
