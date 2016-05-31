from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, \
    InlinePanel, StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail_embed_videos.edit_handlers import EmbedVideoChooserPanel
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailcore.blocks import StreamBlock, RawHTMLBlock
from modelcluster.fields import ParentalKey

# from utils.models import RelatedLink
from articles.models import ArticlePage


# custom streamblock for easy reddit & twitter embeds
class RedTwitBlock(StreamBlock):
    twitter = EmbedBlock(icon="site")
    reddit = RawHTMLBlock(icon="code")


# inline-able model to add site articles to the home page
class HomePagePost(Orderable):
    link_page = models.ForeignKey(
        'articles.ArticlePage',
        null=True,
        blank=True,
        related_name='+'
    )
    page = ParentalKey('home.HomePage', related_name='home_posts')


# easy video embeds using wagtail-embed-videos package
class EmbedVideo(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    video = models.ForeignKey(
        'wagtail_embed_videos.EmbedVideo',
        verbose_name="Video",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [FieldPanel('title'), FieldPanel('description'), EmbedVideoChooserPanel('video')]

    class Meta:
        abstract = True


# inline-able model to add videos to the featured sidebar on the home page
class HomePageVideo(EmbedVideo, Orderable):
    page = ParentalKey('home.HomePage', related_name='featured_video')


class HomePage(Page):
    auto_post = models.BooleanField(default=True)
    embed = StreamField(RedTwitBlock(), null=True, blank=True)
    # auto_sidebar not viable..for now..probably
    # auto_sidebar = BooleanField(default=True, label="Auto sidebar posts")

    @property
    def posts(self):
        # number of posts to display on homepage
        count = 3
        # if auto_post is set on the homepage, front page posts will be 3 most recent articles from db
        if self.auto_post:
            posts = ArticlePage.objects.live().order_by('-date')[:count]
            return posts
        # else front page posts will be those selected in the admin (inline panel)
        else:
            posts = self.home_posts
            num_posts = len(posts)
            # if fewer posts are selected than count, pad posts with some recent articles
            if num_posts < count:
                count = count - num_posts
                more_posts = ArticlePage.objects.live().order_by('-date')[:count]
                # len(selected posts + recent posts) = count
                posts = posts + more_posts
                return posts
            else:
                return posts

    """
    @property
    def mini_posts(self):
        # number of sidebar miniposts to display
        count = 4
        # see above note about auto_sidebar
        # if auto_sidebar is set on the homepage, front side bar posts will be a random selection of site content + embeds
        if self.auto_sidebar:
            posts =
    """

    # passing additional content to template via override of get_context method
    def get_context(self, request):
        posts = self.posts
        # Grab the original context dict
        context = super(HomePage, self).get_context(request)
        # Update the context w/ a blogs key:value
        context['posts'] = posts
        return context

    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('auto_post'),
    StreamFieldPanel('embed'),
    InlinePanel('featured_video', label="Featured Videos"),
    InlinePanel('home_posts', label="Homepage Posts")
]
