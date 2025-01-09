from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_named_model import baseTEMSNamedModel


class Trial1Label(baseTEMSNamedModel):
    class Meta(baseTEMSNamedModel.Meta):
        container_path = "/objects/labels/trial1/"
        verbose_name = _("TEMS Label")
        verbose_name_plural = _("TEMS Labels")
        rdf_type = "tems:Label"
