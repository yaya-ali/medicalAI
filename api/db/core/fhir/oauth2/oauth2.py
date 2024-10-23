import json
from fastapi import HTTPException
import httpx
import requests

from models.req import (
    FhirAuthorizeRequest,
    FhirRefreshTokenRequest,
    FhirRegistrationRequest,
    FhirTokenRequest,
)
from core.fhir.oauth2.utils import challenge, method, state
import urllib.parse
from core.config import settings


class FhirOauth2:
    def __init__(self) -> None:
        self.client_challenge_method = method()
        self.client_state = state()
        self.client_verifier, self.client_challenge = challenge()
        self.url = settings.FHIR_URL
        self.site = settings.FHIR_SITE

    def fhir_register(self, req: FhirRegistrationRequest) -> dict:
        """
        Create a new fhir client-app,
        users need to login manually to approve the app for it work

        Args:
            data (dict): client-app data see fhir client registration documentation for more info

        Returns:
            res (dict): client-app data
        """

        headers = {"Content-Type": "application/json"}
        data = {
            "application_type": req.application_type,
            "redirect_uris": req.redirect_uris,
            "client_name": req.client_name,
            "token_endpoint_auth_method": req.token_endpoint_auth_method,
            "scope": req.scope,
            "contacts": req.contacts,
            "post_logout_redirect_uris": req.post_logout_redirect_uris,
            "jwks_uri": req.jwks_uri,
            "jwks": [req.jwks],
        }

        with httpx.Client(
            headers=headers,
        ) as client:
            response = client.post(
                f"{self.url}/oauth2/{self.site}/registration",
                data=json.dumps(data),  # type: ignore
            )
        try:
            return json.loads(response.text)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Client Registration: Invalid Request",
            )

    def fhir_token(self, req: FhirTokenRequest) -> dict:
        """
        This method will get the token from the auth server,
        code will be parsed from oauth2 callback,
        the token returned will be valid for 3600 seconds (1 hour)

        Args:
            req (FhirTokenRequest): code, redirect_uri, client_id, client_secret

        Returns:
            dict: token data
        """

        payload = {
            "grant_type": req.grant_type,
            "code": req.code,
            "redirect_uri": req.redirect_uri,
            "client_id": req.client_id,
            "client_secret": req.client_secret,
            "code_verifier": self.client_verifier,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            f"{self.url}/oauth2/{self.site}/token",
            headers=headers,
            data=payload,
        )
        try:
            return json.loads(response.text)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid Request: {e}")

    def fhir_authorize(self, req: FhirAuthorizeRequest) -> dict:
        """
        This method will return the url to authorize the app
        we cant programmatically authorize the app, the user must do it
        /oauth2/{site}/authorize

        Args:
            req (FhirAuthorizeRequest): client_id, scope, redirect_uri, grant_type
            note: client_id, scope, redirect_uri, grant_type are optional
            because all of them are set in the .env file

        Returns:
            dict: url to authorize the app
        """

        url = f"{self.url}/oauth2/{self.site}/authorize?client_id={req.client_id}&scope={req.scope}&redirect_uri={req.redirect_uri}&state={self.client_state}&code_challenge={self.client_challenge}&code_challenge_method={self.client_challenge_method}&response_type=code"
        return {"url": urllib.parse.quote_plus(url, safe=":/?=&")}

    def fhir_refresh_token(self, req: FhirRefreshTokenRequest) -> dict:
        """
        /oauth2/{site}/token
        Fhir give only 3600 seconds per access_token.
        Note that a refresh token is only supplied if the
        offline_access scope is provided when requesting authorization or password grant

        Args:
            req (FhirRefreshTokenRequest): refresh_token, client_id

        Returns:
            dict: token data
        """

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": req.refresh_token,
            "client_id": req.client_id,
        }

        # we creating headers individually because some endpoints required json type
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            f"{self.url}/oauth2/{self.site}/token",
            headers=headers,
            data=payload,
        )
        try:
            return json.loads(response.text)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid Request: {e}")
