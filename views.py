# views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Content
from .forms import ContentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def shop(request):
    return render(request, 'shop.html')

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Content, Comment
from .forms import ContentForm, CommentForm
from django.contrib.auth.decorators import login_required

def content_list(request, content_type):
    contents = Content.objects.filter(content_type=content_type).order_by('-created_at')
    form=ContentForm()
    print(content_type)
    if content_type == 'blog':
        return render(request, 'blog.html', {'contents': contents, 'content_type': content_type})
    elif content_type == 'calligraphy':
        return render(request, 'calligraphy.html', {'contents': contents, 'content_type': content_type})
    elif content_type == 'quote':
        return render(request, 'quotes.html', {'contents': contents, 'content_type': content_type})
    elif content_type == 'essay':
        return render(request, 'essays.html', {'contents': contents, 'content_type': content_type})
    elif content_type == 'poem':
        return render(request, 'poems.html', {'contents': contents, 'content_type': content_type})

@login_required
def add_comment(request, content_id):
    if request.method == 'POST':
        content = Content.objects.get(id=content_id)
        Comment.objects.create(content=content, user=request.user, text=request.POST['comment'])
    return redirect('content_list', content_type='calligraphy')


@login_required  # Ensure the user is logged in
def upload_calligraphy(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')  # Get the uploaded image
        content_type = request.POST.get('content_type', 'calligraphy')  # Default to calligraphy if not set
        
        content = Content(
            title=title,
            description=description,
            image=image,
            content_type=content_type,
            author=request.user  # Use the currently logged-in user
        )
        content.save()  # Save the content to the database
        
        return JsonResponse({'success': True})  # Return a success response
    return JsonResponse({'success': False}, status=400)

@login_required
def post_content(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.author = request.user
            content.save()
            return redirect('home')
    else:
        form = ContentForm()
    return render(request, 'post_content.html', {'form': form})

@login_required
def like_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    if request.user in content.likes.all():
        content.likes.remove(request.user)
    else:
        content.likes.add(request.user)
    return redirect('content_list', content_type=content.content_type)

def signin(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request, username=uname, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('/')
        error = 'Username or password is incorrect'
        return render(request, 'login.html', {'error': error, 'username': uname})
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            error = 'Passwords do not match'
            return render(request, 'signup.html', {'error': error, 'username': uname, 'email': email})
        if User.objects.filter(username=uname).exists():
            error = 'Username already exists'
            return render(request, 'signup.html', {'error': error, 'username': uname, 'email': email})
        if User.objects.filter(email=email).exists():
            error = 'Email already registered'
            return render(request, 'signup.html', {'error': error, 'username': uname, 'email': email})
        user = User.objects.create(username=uname, email=email)
        user.set_password(pass1)
        user.save()
        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('signin')
    return render(request, 'signup.html')