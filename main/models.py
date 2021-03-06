from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager

User = settings.AUTH_USER_MODEL #this is the user model, 'user_id' is how user is called in the model

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #many to one relationship where many posts can be tied to one user
    content = models.TextField(blank=True, null=True) 
    date_traded = models.DateTimeField(verbose_name= ('Date Traded'))
    image = models.ImageField(upload_to='trade_images', blank=True, null=True) #change blank = false later to be required
    upvotes = models.ManyToManyField(User, blank=True, related_name='upvotes')
    total_upvotes = models.IntegerField(default='0')
    ticker = models.CharField(blank=False, null=True, max_length=5)
    tags = TaggableManager(blank=True, help_text=('Press Enter or comma to seperate tags.')) #erased help text
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('main:post-detail', kwargs={'pk': self.pk}) #returns the url for individual posts

    def __str__(self):
        return self.content


class Upvote(models.Model):
    user = models.ForeignKey(User, related_name='upvoted_user', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='upvoted_post',  on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return str(self.user) + ':' + str(self.post)

 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics') 
    bio = models.TextField(max_length=1000, blank=True)

    @property
    def followers(self):
        return Follow.objects.filter(to_follow=self.user).count() #count of followers by filtering user and to_follow count

    @property
    def following(self):
        return Follow.objects.filter(user=self.user).count() #count of followers by filtering user and its user(following) count



    def __str__(self):
        return f"{self.user.username}'s Profile"



class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE) #tie follows to one user
    to_follow = models.ForeignKey(User, related_name='to_follow',  on_delete=models.CASCADE)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) #tie post model to comments as a one to many relationship using foreign key
    user = models.ForeignKey(User, related_name='commented_user', on_delete=models.CASCADE) #tie to user posting
    created_date = models.DateTimeField(default=timezone.now)
    content = models.TextField(max_length=120)

    def __str__(self):
        return self.content


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='participants')
    last_message = models.TextField(null=True)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE) #tie follows to one user
    recipient = models.ForeignKey(User, related_name = 'recipient', on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500)
    conversation = models.ForeignKey(Conversation, blank=False, null=True, on_delete=models.CASCADE) #ties conversation table to messages
    

    def __str__(self):
        return f"{self.sender} to {self.recipient} : {self.text}"

