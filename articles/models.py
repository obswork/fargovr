from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField, CharField
from wagtail.wagtailsearch import index

from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, StreamFieldPanel, ImageChooserPanel
)

from modelcluster.fields import ParentalKey

from utils.models import RelatedLink

# Streamblocks/fields


class QuoteBlock(StructBlock):
    quote = TextBlock()
    attribution = CharBlock()


class Content(StreamBlock):
    paragraph = RichTextBlock(icon="pilcrow")
    quote = QuoteBlock()
    raw = RawHTMLBlock(icon="code", label='Reddit Embed')
    embed = EmbedBlock(icon="media")
    document = DocumentChooserBlock(icon="doc-full-inverse")


class ArticleRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('article.ArticlePage', related_name='related_links')


class ArticlePage(Page):
    subtitle = CharField(max_length=255, null=True, blank=True)
    body = StreamField(Content())
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    search_field = Page.search_fields + (
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
