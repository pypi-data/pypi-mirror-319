from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.format import TEMSFormat


class Trial1Format(TEMSFormat):
    class Meta(TEMSFormat.Meta):
        container_path = "/objects/formats/trial1/"
