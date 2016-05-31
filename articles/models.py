from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsearch import index

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, StreamFieldPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey

from utils.models import RelatedLink
from utils.models import Post


class ArticleRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('articles.ArticlePage', related_name='related_links')


class ArticlePage(Page, Post):
    search_fields = Page.search_fields + (
        index.SearchField('body'),
        index.SearchField('subtitle'),
    )


ArticlePage.content_panels = Page.content_panels + [
    ImageChooserPanel('feed_image'),
    FieldPanel('subtitle'),
    StreamFieldPanel('body'),
    FieldPanel('date'),
    InlinePanel('related_links', label="Related Links"),
]
