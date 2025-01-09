from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_object import baseTEMSObject
from djangoldp_tems.models.provider import TEMSProvider, register_catalog
from djangoldp_tems_trial1.models.category import Trial1Category
from djangoldp_tems_trial1.models.label import Trial1Label


class Trial1Object(baseTEMSObject):
    providers = models.ManyToManyField(
        TEMSProvider, blank=True, related_name="catalog_trial1"
    )
    owners = models.OneToOneField(
        Group,
        related_name="owned_trial1",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Trial1Category, blank=True, null=True, on_delete=models.SET_NULL
    )
    label = models.ForeignKey(
        Trial1Label, blank=True, null=True, on_delete=models.SET_NULL
    )
    hub = models.CharField(max_length=255, blank=True, null=True, default="")
    lang = models.CharField(max_length=255, blank=True, null=True, default="")
    publication_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.title or self.urlid

    class Meta(baseTEMSObject.Meta):
        container_path = "/objects/trial1/"
        verbose_name = _("TEMS Trial 1 Object")
        verbose_name_plural = _("TEMS Trial 1 Objects")

        serializer_fields = [
            "@id",
            "creation_date",
            "update_date",
            "title",
            "description",
            "copyright",
            "website",
            "licences",
            "images",
            "assets",
            "owners",
            "providers",
            "category",
            "label",
            "hub",
            "lang",
            "publication_date",
        ]
        nested_fields = [
            "licences",
            "assets",
            "images",
            "providers",
            "category",
            "label",
        ]
        rdf_type = ["tems:Object", "tems:Article"]


register_catalog("trial1", Trial1Object)
