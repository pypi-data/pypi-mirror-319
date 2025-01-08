from django.utils.translation import gettext as _

from apps.keywords.admin import StepsInline
from apps.testcases.forms import TestStepsForm
from apps.testcases.models import TestStep, TestCase
from apps.windows.models import Window


class TestSteps(StepsInline):
    model = TestStep
    fields = ['window'] + StepsInline.fields
    form = TestStepsForm

    def get_formset(self, request, obj=None, **kwargs):
        testcase: TestCase = obj
        formset = super().get_formset(request, obj, **kwargs)

        systems_under_test = testcase.systems.all()
        windows = Window.objects.filter(systems__in=systems_under_test).distinct().order_by('name')

        formset.form.base_fields['window'].queryset = windows
        formset.form.base_fields['window'].widget.can_add_related = False
        formset.form.base_fields['window'].widget.can_change_related = False

        formset.form.base_fields['to_keyword'].widget.can_add_related = False
        formset.form.base_fields['to_keyword'].widget.can_change_related = False
        formset.form.base_fields['to_keyword'].widget.can_view_related = False
        formset.form.base_fields['to_keyword'].label = _('Sequenz')
        sequences = formset.form.base_fields['to_keyword'].queryset.sequences()
        formset.form.base_fields['to_keyword'].queryset = sequences

        return formset
