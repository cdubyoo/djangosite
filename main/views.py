from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Post, Profile, Follow, Comment
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.db.models import Count
from .forms import NewUserForm, PostForm, UserUpdateForm, ProfileUpdateForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# function based views handle the logic for the route and render the template.
# class based views handle backend logic using generic views and inherit from mixins

#home page
def homepage(request, *args, **kwargs):
     # render in the 'posts' with all the objects as post, to call it on the template
     context = {
          'posts': Post.objects.all() # calling all objects from the Post model
     }
     return render(request,
                  'main/home.html',
                  context)

# creating posts
class post_create_view(LoginRequiredMixin, CreateView):
     model = Post
     fields = ['content', 'image']
     #set user to logged in user then validate the form
     def form_valid(self, form):
          form.instance.user = self.request.user
          return super().form_valid(form)

# update view
class post_update_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
     model = Post
     fields = ['content', 'image']
     #set user to logged in user then validate the form
     def form_valid(self, form):
          form.instance.user = self.request.user
          return super().form_valid(form)

     def test_func(self):
          post = self.get_object() # get the post 
          if self.request.user == post.user:
               return True
          return False

# list of all posts, will be changed to discover page, showcasing top trades of the day instead
class post_list_view(ListView):
    
     model = Post
     template_name = 'main/home.html'
     context_object_name = 'posts' # this is called from the html as 'for post in posts'
     ordering = ['-date_posted'] # minus to reverse the date posted, so newer posts show up on top
     paginate_by = 5 #sets pagination per page


# feed of user's followings
class feed_list_view(LoginRequiredMixin, ListView):
    
     model = Post
     template_name = 'main/feed.html'
     context_object_name = 'posts' # this is called from the html as 'for post in posts'
     ordering = ['-date_posted'] # minus to reverse the date posted, so newer posts show up on top
     paginate_by = 5 #sets pagination per page

     def get_queryset(self): #function to return a queryset(list of items) 
          user = self.request.user #specify user as current user who is sending request
          qs = Follow.objects.filter(user=user) #query set filtering by current user's follow table
          follows = [user] # store following users as an array as 'follows'
          for users in qs: #iterate through the query set with a for loop
               follows.append(users.to_follow) #add to array the users who are in the to_follow list of the user's follow table model
          return Post.objects.filter(user__in=follows).order_by('-date_posted') 
          # ^^ using the '__in' syntax to make query to ask for posts with user = follows, which is array of users who is followed by current user


#individual post view
class post_detail_view(DetailView):
     model = Post
     template_name = 'main/post_detail.html'
     context_object_name = 'post'

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['form'] = CommentForm(instance=self.request.user)
          return context

     
     def post(self, request, *args, **kwargs):
          create_comment = Comment(content=request.POST.get('content'),
                                   user=self.request.user, post=self.get_object())
          create_comment.save()
     
          return self.get(self, request, *args, **kwargs)

class post_delete_view(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
     model = Post
     success_url = '/' #redirect to home if delete success
     def test_func(self):
          post = self.get_object() # get the post 
          if self.request.user == post.user:
               return True
          return False


class user_posts(LoginRequiredMixin, ListView):
    
     model = Post
     template_name = 'main/user_posts.html'
     context_object_name = 'posts'
     paginate_by = 5 #sets pagination per page

     def displayed_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username')) # user on display

     #get data from model and filter by user
     def get_queryset(self):
          user = get_object_or_404(User, username =self.kwargs.get('username'))
          return Post.objects.filter(user=user).order_by('-date_posted')

     #override and get data from another model
     def get_context_data(self, **kwargs):
          displayed_user = get_object_or_404(User, username =self.kwargs.get('username'))
          current_user = self.request.user

          if current_user is None:
               followable = False
          else:
               followable = (Follow.objects.filter(user=current_user, to_follow=displayed_user).count() == 0)

          context = super(user_posts, self).get_context_data(**kwargs)
          context['user_profile'] = Profile.objects.filter(user=displayed_user)
          context['followable'] = followable
          return context

     #post request, done as def post because its inside a class
     def post(self, request, *args, **kwargs):
          follows_between = Follow.objects.filter(user = request.user, to_follow = self.displayed_user()) # filter out current user and displayed user as a variable
          if 'follow' in request.POST: # calling the post request from html name=follow
               new_relation = Follow(user=request.user, to_follow=self.displayed_user()) #filter new relation with request user and displayed user using Follow model
               if follows_between.count() == 0: # if there is no count/relation between the 2, then save new relation
                    new_relation.save() 
          # doing the reverse for if the post request is from html name=unfollow
          elif 'unfollow' in request.POST: 
               new_relation = Follow(user=request.user, to_follow=self.displayed_user()) 
               if follows_between.count() > 0: # if  there is count/relation between the 2, then delete relation
                    follows_between.delete() 

          return self.get(self, request, *args, **kwargs)
     
          

     


# register
def register(request):
     if request.method == "POST":
          form = NewUserForm(request.POST)
          if form.is_valid():
               user = form.save() # saving the user 
               username = form.cleaned_data.get('username')
               messages.success(request, f"New user created: {username}")
               login(request, user)
               messages.info(request, f"Welcome, {username}.")
               return redirect("main:home")

          else:

               return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

     form = NewUserForm
     return render(request = request, 
                   template_name = "main/register.html", 
                   context = {"form":form})

# log out 
def logout_request(request):
     logout(request)
     messages.info(request, "You have been logged out.")
     return redirect("main:home")

# log in
def login_request(request):
     if request.method == "POST":
          form = AuthenticationForm(request, data=request.POST)
          if form.is_valid():
               username = form.cleaned_data.get('username')
               password = form.cleaned_data.get('password')
               user = authenticate(username=username, password=password)
               if user is not None:
                    login(request, user)
                    messages.info(request, f"Welcome, {username}.")
                    return redirect('/')
               else:
                    messages.error(request, "Invalid username or password.")
          else:
               messages.error(request, "Invalid username or password.")          
     form = AuthenticationForm()               
     return render(request = request,
                   template_name = "main/login.html",
                   context={"form":form})

@login_required
def profile(request):
     if request.method == "POST":
          u_form = UserUpdateForm(request.POST, instance=request.user)
          p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

          if u_form.is_valid and p_form.is_valid():
               u_form.save()
               p_form.save()
               messages.success(request, f'Your profile has been updated.')
               return redirect('main:profile')
     else:
          u_form = UserUpdateForm(instance=request.user)
          p_form = ProfileUpdateForm(instance=request.user.profile)

     context = {
          'u_form': u_form,
          'p_form': p_form
     }
     
     return render(request, 'main/profile.html', context)






