from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsearch import index

from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, CharBlock, RichTextBlock, RawHTMLBlock, URLBlock, PageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

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
    link_external = URLBlock(icon='link', label='External Link')
    link_page = PageChooserBlock(icon='link', label="Internal Link")


# Home Page

class HomePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('newspaper.HomePage', related_name='related_links')


class HomePage(Page):
    body = StreamField(Content())
    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    StreamFieldPanel('body'),
    InlinePanel('related_links', label="Related links"),
]

HomePage.promote_panels = Page.promote_panels
