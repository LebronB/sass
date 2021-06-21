from django.forms import RadioSelect


class ColorRadioSelect(RadioSelect):
    # template_name = 'django/forms/widgets/radio.html'
    # option_template_name = 'django/forms/widgets/radio_option.html'

    template_name = 'radio.html'
    option_template_name = 'radio_option.html'
