from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def urchin():
    urchin_id = getattr(settings, "URCHIN_ID", None)
    if urchin_id:
        return """
    <script src="http://www.google-analytics.com/urchin.js" type="text/javascript"></script>
    <script type="text/javascript">
        _uacct = "%s";
        urchinTracker();
    </script>
    """ % settings.URCHIN_ID
    else:
        return ""


@register.simple_tag
def ga():
    # Use new Google Analytics tracking code
    if not settings.DEBUG: # not to render GA tracking code if debug is True
        urchin_id = getattr(settings, "URCHIN_ID", None)
        if urchin_id:
            return """
    <script type="text/javascript">
        var _gaq = _gaq || [];
        _gaq.push(['_setAccount', '%s']);
        _gaq.push(['_trackPageview']);

        (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
        })();

    </script>
        """ % settings.URCHIN_ID
    else:
        return ""
