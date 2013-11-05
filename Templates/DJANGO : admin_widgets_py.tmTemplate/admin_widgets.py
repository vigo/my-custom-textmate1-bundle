# -*- coding: utf-8 -*-

# from django.contrib.admin.widgets import Admin-MY-Widget

# from django.utils.translation import ugettext as _
# from django.utils.translation import ugettext_lazy as _

from django.utils.safestring import mark_safe
from django.conf import settings
import os

# ???
# AdminCommaSeparatedIntegerFieldWidget
# AdminDateWidget
# AdminFileWidget
# AdminIntegerFieldWidget
# AdminRadioFieldRenderer
# AdminRadioSelect
# AdminSplitDateTime
# AdminTextInputWidget
# AdminTextareaWidget
# AdminTimeWidget
# AdminURLFieldWidget

class Admin-MY-Widget(???):
    def render(self, name, value, attrs=None):
        output = []
        # str(value) : field value
        output.append('<strong>hello</strong>')
        output.append("<p>%s</p>" % super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))