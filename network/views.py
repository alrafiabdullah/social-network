from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from .models import User, Post, Follow, Like, Comment
from .serializers import PostSerializer, LikeSerializer, FollowSerializer

from rest_framework import status, permissions, viewsets


def index(request):
    try:
        if request.method == "POST":
            post = request.POST["post_post"]

            post_obj = Post(
                post_owner=request.user,
                text_field=post
            )
            post_obj.save()

            like_obj = Like(
                liked_post=post_obj
            )
            like_obj.save()

            return HttpResponseRedirect(reverse('index'))
    except:
        pass
    all_post = Post.objects.order_by('-post_time')

    paginator = Paginator(all_post, per_page=10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        previous_url = f'?page={page.previous_page_number()}'
    else:
        previous_url = ''

    return render(request, "network/index.html", {
        "posts": page,
        "next_page_url": next_url,
        "previous_page_url": previous_url,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def profile_view(request):
    current_user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]

        current_user.first_name = first_name
        current_user.last_name = last_name

        current_user.save()
        return HttpResponseRedirect(reverse('profile_view'))

    follower_count = 0
    following_count = 0

    try:
        all_follow = Follow.objects.get(user=current_user)
        followers = all_follow.user_follower.all()
        for follower in followers:
            follower_count += 1

        followings = all_follow.user_following.all()
        for following in followings:
            following_count += 1
    except:
        pass

    return render(request, "network/profile.html", {
        "follower": follower_count,
        "following": following_count,
    })


@login_required
def click_profile(request, id):
    requested_user = User.objects.get(id=id)
    all_posts = Post.objects.filter(
        post_owner=requested_user).order_by('-post_time')

    follower_count = 0
    following_count = 0

    try:
        all_follow = Follow.objects.get(user_id=requested_user.id)
        followers = all_follow.user_follower.all()
        for follower in followers:
            follower_count += 1

        followings = all_follow.user_following.all()
        for following in followings:
            following_count += 1
    except:
        pass

    followed = False
    try:
        check_follower = Follow.objects.get(user_id=requested_user.id)
        follower_list = check_follower.user_follower.all()
        for foll in follower_list:
            if foll.username == request.user.username:
                followed = True
                break
            else:
                followed = False
    except:
        pass

    

    paginator = Paginator(all_posts, per_page=10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        previous_url = f'?page={page.previous_page_number()}'
    else:
        previous_url = ''

    return render(request, "network/click.html", {
        "requested": requested_user,
        "posts": page,
        "next_page_url": next_url,
        "previous_page_url": previous_url,
        "follower": follower_count,
        "following": following_count,
        "followed": followed,
    })


@login_required
def follow(request):
    if request.method == "POST":
        requested_user_id = request.POST["id"]

        requested_user = User.objects.get(id=requested_user_id)
        try:
            user_following = Follow.objects.get(user_id=requested_user.id)
            user_following.user_follower.add(request.user)
        except:
            follow_obj = Follow(
                user=requested_user
            )

            follow_obj.save()
            user_following = Follow.objects.get(user_id=requested_user.id)
            user_following.user_follower.add(request.user)

        try:
            user_follower = Follow.objects.get(user_id=request.user.id)
            user_follower.user_following.add(requested_user)
        except:
            follow_obj = Follow(
                user=request.user
            )

            follow_obj.save()
            user_follower = Follow.objects.get(user_id=request.user.id)
            user_follower.user_following.add(requested_user)

    return HttpResponseRedirect(reverse('click_profile', kwargs={
        'id': requested_user.id
    }))


@login_required
def unfollow(request):
    if request.method == "POST":
        requested_user_id = request.POST["id"]

    check_follower = Follow.objects.get(user_id=requested_user_id)
    check_follower.user_follower.remove(request.user.id)

    self = Follow.objects.get(user_id=request.user.id)
    self.user_following.remove(requested_user_id)

    return HttpResponseRedirect(reverse('click_profile', kwargs={
        'id': requested_user_id
    }))


@login_required
def following(request):
    following_list = []
    following_id_list = []

    check_following = Follow.objects.get(user_id=request.user.id)
    all_following = check_following.user_following.all()

    for following in all_following:
        following_id_list.append(following.pk)

    all_post = Post.objects.all().order_by('-post_time')
    for i in range(len(following_id_list)):
        posts = all_post.filter(
            post_owner_id=following_id_list[i])
        for post in posts:
            following_list.append(post)

    paginator = Paginator(following_list, per_page=10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        previous_url = f'?page={page.previous_page_number()}'
    else:
        previous_url = ''

    return render(request, 'network/following.html', {
        'posts': page,
        "next_page_url": next_url,
        "previous_page_url": previous_url,
    })


def edit(request, id):
    edit_post = Post.objects.get(id=id)

    if request.method == "POST":
        text = request.POST["post"]

        edit_post.text_field = text
        edit_post.is_edited = True
        edit_post.save()

        return HttpResponseRedirect(reverse('index'))

    return render(request, "network/edit.html", {
        "post": edit_post,
    })


def delete_post(request, id):
    tobe_deleted = Post.objects.get(id=id)
    tobe_deleted.delete()

    return HttpResponseRedirect(reverse('index'))


def comment(request):
    if request.method == "POST":
        post_comment = request.POST["comment"]
        post_id = request.POST["post_id"]

        comment_obj = Comment(
            post_comment=post_comment,
            of_post=Post.objects.get(id=post_id),
            comment_user=request.user
        )

        comment_obj.save()

        return HttpResponseRedirect(reverse('index'))


class LikeView(viewsets.ModelViewSet):

    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def get(self, request, id):
        try:
            model = Follow.objects.filter(user_id=id)
        except:
            return HttpResponse(f"Post with {id} is not found!", status=status.HTTP_400_BAD_REQUEST)

        serializer = FollowSerializer(model)
        return HttpResponse(serializer.data)

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            model = Like.objects.get(id=id)
        except:
            return HttpResponse(f"Post with {id} is not found!", status=status.HTTP_400_BAD_REQUEST)

        serializer = LikeSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeHandlerView(View):
    def post(self, request):

        if request.method == 'POST':
            text = request.POST.get('post_id')
            print(text)
        like_obj = Like.objects.get(liked_post_id=int(text))
        like_obj.liked_by.add(request.user)
        return JsonResponse({
            'count': len(like_obj.liked_by.all()),
        }, status=200)


class UnlikeHandlerView(View):
    def post(self, request):

        if request.method == 'POST':
            text = request.POST.get('post_id')
        like_obj = Like.objects.get(liked_post_id=int(text))
        like_obj.liked_by.remove(request.user)
        return JsonResponse({
            'count': len(like_obj.liked_by.all()),
        }, status=200)


class TotalLikeView(View):
    def post(self, request):

        if request.method == 'POST':
            text = request.POST.get('post_id')
        like_obj = Like.objects.get(liked_post_id=int(text))
        return JsonResponse({
            'count': len(like_obj.liked_by.all()),
        }, status=200)
