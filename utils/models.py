from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    PageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock


# Abstract classes with commonly used fields

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


class Post(models.Model):
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    body = StreamField(Content())
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    class Meta:
        abstract = True


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


# Related links


class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


class ContactFields(models.Model):
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=10, blank=True)

    panels = [
        FieldPanel('telephone'),
        FieldPanel('email'),
        FieldPanel('address_1'),
        FieldPanel('address_2'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('post_code'),
    ]

    class Meta:
        abstract = True
