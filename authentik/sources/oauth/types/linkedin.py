"""Linkedin OAuth Views"""
from typing import Any

from authentik.sources.oauth.types.manager import MANAGER, SourceType
from authentik.sources.oauth.views.callback import OAuthCallback
from authentik.sources.oauth.views.redirect import OAuthRedirect


class LinkedinOAuthRedirect(OAuthRedirect):
    """Linkedin OAuth2 Redirect"""

    def get_additional_parameters(self, source):  # pragma: no cover
        return {
            "scope": ["email", "profile"],
        }


class LinkedinOAuth2Callback(OAuthCallback):
    """Linkedin OAuth2 Callback"""

    def get_user_enroll_context(
        self,
        info: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "email": info.get("email"),
            "name": info.get("name"),
        }


@MANAGER.type()
class LinkedinType(SourceType):
    """Linkedin Type definition"""

    callback_view = LinkedinOAuth2Callback
    redirect_view = LinkedinOAuthRedirect
    name = "Linkedin"
    slug = "linkedin"

    authorization_url = "https://www.linkedin.com/oauth/v2/authorization"
    access_token_url = "https://www.linkedin.com/oauth/v2/accessToken"  # nosec
    profile_url = "https://www.linkedin.com/oauth/v2/me"
