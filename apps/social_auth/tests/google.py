import re

from django.conf import settings

from social_auth.tests.base import SocialAuthTestsCase, FormParserByID, \
                                   FormParser, RefreshParser


class GoogleTestCase(SocialAuthTestsCase):
    def setUp(self, *args, **kwargs):
        super(GoogleTestCase, self).setUp(*args, **kwargs)
        self.user = getattr(settings, 'TEST_GOOGLE_USER', None)
        self.passwd = getattr(settings, 'TEST_GOOGLE_PASSWORD', None)
        # check that user and password are setup properly
        self.assertTrue(self.user)
        self.assertTrue(self.passwd)


REDIRECT_RE = re.compile('window.location.replace\("(.*)"\);')

class GoogleOpenIdTestLogin(GoogleTestCase):
    SERVER_NAME = 'myapp.com'
    SERVER_PORT = '8000'

    def test_login_succeful(self):
        response = self.client.get(self.reverse('begin', 'google'))

        parser = FormParserByID('openid_message')
        parser.feed(response.content)
        # Check that action and values were loaded properly
        self.assertTrue(parser.action)
        self.assertTrue(parser.values)
        content = self.get_content(parser.action, parser.values, use_cookies=True)

        parser = FormParserByID('gaia_loginform')
        parser.feed(content)
        auth = {'Email': self.user, 'Passwd': self.passwd}
        parser.values.update(auth)
        # Check that action and values were loaded properly
        self.assertTrue(parser.action)
        self.assertTrue(parser.values)

        content = self.get_content(parser.action, parser.values, use_cookies=True)
        parser = RefreshParser()
        parser.feed(content)

        # approved?
        result = self.get_redirect(parser.value, use_cookies=True)
        if result.headers.get('Location', ''):  # approved?
            # damn, google has a hell of redirects :-(
            result = self.get_redirect(result.headers['Location'], use_cookies=True)
            result = self.get_redirect(result.headers['Location'], use_cookies=True)
            result = self.get_redirect(result.headers['Location'], use_cookies=True)

        # app was not approved
        if self.SERVER_NAME not in result.headers.get('Location', ''):
            content = self.get_content(parser.value, use_cookies=True)
            parser = FormParser()
            parser.feed(content)
            parser.values['submit_true'] = 'yes'
            parser.values['remember_choices'] = 'yes'
            result = self.get_redirect(parser.action, parser.values, use_cookies=True)

        response = self.client.get(self.make_relative(result.headers['Location']))
        self.assertTrue(settings.LOGIN_REDIRECT_URL in self.make_relative(response['Location']))
