from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message

@login_required
def chat_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat_list.html', {'users': users})

@login_required
def chat_detail(request, username):
    other_user = get_object_or_404(User, username=username)
    
    # Отримуємо всі повідомлення між двома користувачами
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('created_at')

    # Позначаємо повідомлення, які адресовані поточному користувачу, як прочитані
    unread_messages = messages.filter(receiver=request.user, is_read=False)
    unread_messages.update(is_read=True)

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
