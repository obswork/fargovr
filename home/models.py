from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, \
    InlinePanel, StreamFieldPanel
from wagtail.wagtailcore.fields import BooleanField, RichTextField


from modelcluster.fields import ParentalKey

# from utils.models import RelatedLink
from articles.models import ArticlePage


"""
# home page related links needed?
class HomePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('home.HomePage', related_name='related_links')
"""


class HomePagePost(Orderable):
    link_page = models.ForeignKey(
        'articles.ArticlePage',
        null=True,
        blank=True,
        related_name='+'
    )
    page = ParentalKey('home.HomePage', related_name='home_posts')


class Feature(models.Model, Orderable)
    body = RichTextField()

    page = ParentalKey('home.HomePage', related_name='features')

    panels = [
        FieldPanel('body'),
    ]

    """
    # TODO: make feature an abstract model?
    class Meta:
        abstract = True
    """


class HomePage(Page):
    auto_post = BooleanField(default=True, label="Auto frontpage posts")
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
        # else front page posts will be those selected in the admin (inline panel) (+ enough recent articles to keep home page reasonably populated - default = 3)
        else:
            posts = self.home_posts
            num_posts = len(posts)
            if num_posts < count:
                count = count - num_posts
                more_posts = ArticlePage.objects.live().order_by('-date')[:count]
                # len(selected posts + recent posts) = count
                posts = posts + more_posts
                return posts
            else:
                return posts

    @property
    def mini_posts(self):
        """
        # number of sidebar miniposts to display
        count = 4
        # see above note about auto_sidebar 
        # if auto_sidebar is set on the homepage, front side bar posts will be a random selection of site content + embeds
        if self.auto_sidebar:
            posts =  
        """


    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('auto_post', label="Auto update home page?"),
    StreamFieldPanel('body'),
    # InlinePanel('related_links', label="Related links"),
    InlinePanel('features', label="Homepage Featured Content"),
    InlinePanel('home_posts', label="Homepage Posts")
]
