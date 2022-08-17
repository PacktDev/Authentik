"""google Type tests"""
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase
from django.test.client import RequestFactory

from authentik.lib.tests.utils import dummy_get_response
from authentik.sources.oauth.models import OAuthSource
from authentik.sources.oauth.types.linkedin import LinkedinOAuth2Callback, LinkedinOAuthRedirect

GOOGLE_USER = {
    "id": "1324813249123401234",
    "email": "foo@bar.baz",
    "verified_email": True,
    "name": "foo bar",
    "given_name": "foo",
    "family_name": "bar",
    "picture": "",
    "locale": "en",
}


class TestTypeLinkedin(TestCase):
    """OAuth Source tests"""

    def setUp(self):
        self.source: OAuthSource = OAuthSource.objects.create(
            name="test",
            slug="test",
            provider_type="linkedin",
            authorization_url="",
            profile_url="",
            consumer_key="foo",
        )
        self.request_factory = RequestFactory()

    def test_enroll_context(self):
        """Test Linkedin Enrollment context"""
        ak_context = LinkedinOAuth2Callback().get_user_enroll_context(LINKEDIN_USER)
        self.assertEqual(ak_context["email"], LINKEDIN_USER["email"])
        self.assertEqual(ak_context["name"], LINKEDIN_USER["name"])

    def test_authorize_url(self):
        """Test authorize URL"""
        request = self.request_factory.get("/")
        middleware = SessionMiddleware(dummy_get_response)
        middleware.process_request(request)
        request.session.save()
        redirect = LinkedinOAuthRedirect(request=request).get_redirect_url(
            source_slug=self.source.slug
        )
        self.assertEqual(
            redirect,
            (
                'login.packt.com/auth/linkedin'
            ),
        )
        self.source.additional_scopes = "foo"
        self.source.save()
        redirect = LinkedinOAuthRedirect(request=request).get_redirect_url(
            source_slug=self.source.slug
        )
        self.assertEqual(
            redirect,
            (
                'login.packt.com/auth/linkedin'
            ),
        )
