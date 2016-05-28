from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, \
    InlinePanel, StreamFieldPanel
from wagtail.wagtailcore.fields import BooleanField


from modelcluster.fields import ParentalKey

from utils.models import RelatedLink
from articles.models import ArticlePage


class HomePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('home.HomePage', related_name='related_links')


class HomePagePost(Orderable):
    link_page = models.ForeignKey(
        'articles.ArticlePage',
        null=True,
        blank=True,
        related_name='+'
    )
    page = ParentalKey('home.HomePage', related_name='home_posts')


class HomePage(Page):
    auto = BooleanField(default=True, label="Auto Homepage")

    @property
    def posts(self):
        # number of posts to display on homepage
        count = 3
        # if auto is set on the homepage, front page posts will by 3 most recent articles from db
        if self.auto:
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

    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('auto', label="Auto update home page?"),
    StreamFieldPanel('body'),
    InlinePanel('related_links', label="Related links"),
    InlinePanel('home_posts', label="homepage posts")
]
