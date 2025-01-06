# Copyright (C) 2023-2025 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>
#
# Transkribus Metagrapho API Client
#
# This file is part of transkribus-metagrapho-api.
#
# transkribus-metagrapho-api is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# transkribus-metagrapho-api is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar. If not, see <http://www.gnu.org/licenses/>
"""Transkribus Metagrapho API Client."""

import base64
import logging
import re
import requests
import time

from contextlib import contextmanager
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from PIL import Image
from typing import Dict, List, Literal, Final, Generator, Type, TypeVar


class TranskribusMetagraphoAPI:
    """Transkribus metagrapho API.

    https://www.transkribus.org/metagrapho/documentation
    """

    T = TypeVar("T", bound="TranskribusMetagraphoAPI")

    BASE_URL: Final[str] = "https://transkribus.eu/processing/v1"
    access_token: "TranskribusMetagraphoAPI.AccessToken"

    class AccessToken:
        """API access token."""

        T = TypeVar("T", bound="TranskribusMetagraphoAPI.AccessToken")
        BASE_URL: Final[str] = (
            "https://account.readcoop.eu/auth/realms/readcoop/protocol/openid-connect"
        )

        access_token: str
        expires: datetime
        refresh_expires: datetime
        refresh_token: str
        token_type: str
        not_before_policy: int
        session_state: str
        scope: str

        def __init__(
            self,
            access_token: str,
            expires: datetime,
            refresh_expires: datetime,
            refresh_token: str,
            token_type: str,
            not_before_policy: int,
            session_state: str,
            scope: str,
        ) -> None:
            """Create new access token."""
            self.access_token = access_token
            self.expires = expires
            self.refresh_expires = refresh_expires
            self.refresh_token = refresh_token
            self.token_type = token_type
            self.not_before_policy = not_before_policy
            self.session_state = session_state
            self.scope = scope

        def get_auth_token(self) -> str:
            """Get auth token for Authentication header.

            Auto refreshes if token is expired.
            """
            self.refresh()
            return f"{self.token_type} {self.access_token}"

        def is_expired(self) -> bool:
            """Check if the access token is expired."""
            return datetime.now() > self.expires

        def is_refresh_expired(self) -> bool:
            """Check if the refresh token is expired."""
            return datetime.now() > self.refresh_expires

        def refresh(self, force: bool = False) -> bool:
            """Refresh access token."""
            if force or self.is_expired():
                if self.is_refresh_expired():
                    raise RuntimeError(
                        "Refresh token is expired, need to reauthenticate."
                    )
                logging.debug("Refresh access token.")
                r = requests.post(
                    f"{self.BASE_URL}/token",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data={
                        "grant_type": "refresh_token",
                        "client_id": "processing-api-client",
                        "refresh_token": self.refresh_token,
                    },
                )
                r.raise_for_status()
                data = r.json()
                now = datetime.now()
                self.access_token = data["access_token"]
                self.expires = now + timedelta(minutes=data["expires_in"])
                self.refresh_expires = now + timedelta(
                    minutes=data["refresh_expires_in"]
                )
                self.refresh_token = data["refresh_token"]
                self.token_type = data["token_type"]
                self.not_before_policy = data["not-before-policy"]
                self.session_state = data["session_state"]
                self.scope = data["scope"]
                return True
            return False

        def revoke(self) -> bool:
            """Revoke access token."""
            logging.debug("Revoke access token.")
            r = requests.post(
                f"{self.BASE_URL}/logout",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "client_id": "processing-api-client",
                    "refresh_token": self.refresh_token,
                },
            )
            r.raise_for_status()
            self.access_token = ""
            self.expires = datetime.now()
            self.refresh_expires = datetime.now()
            self.refresh_token = ""
            self.token_type = ""
            self.not_before_policy = -1
            self.session_state = ""
            self.scope = ""
            return True

        @classmethod
        def obtain(cls: Type[T], username: str, password: str) -> T:
            """Obtain access token."""
            logging.debug("Obtain access token.")
            r = requests.post(
                f"{cls.BASE_URL}/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "password",
                    "username": username,
                    "password": password,
                    "client_id": "processing-api-client",
                },
            )
            r.raise_for_status()
            data = r.json()
            now = datetime.now()
            return cls(
                access_token=data["access_token"],
                expires=now + timedelta(minutes=data["expires_in"]),
                refresh_expires=now + timedelta(minutes=data["refresh_expires_in"]),
                refresh_token=data["refresh_token"],
                token_type=data["token_type"],
                not_before_policy=data["not-before-policy"],
                session_state=data["session_state"],
                scope=data["scope"],
            )

    def __init__(self, username: str, password: str):
        """Init."""
        self.access_token = TranskribusMetagraphoAPI.AccessToken.obtain(
            username, password
        )

    def __call__(
        self,
        *args: Path,
        htr_id: int,
        line_detection: int | None = None,
        language_model: str | None = None,
        text: str | None = None,
        regions: List[Dict] | None = None,
        mode: Literal["alto", "page"] = "page",
        wait: int = 45,
        **kwargs: float | int,
    ) -> List[str | None]:
        """Run processing on several images and get ALTO or PAGE XML.

        Catches all exceptions that occur, the error are logged to stderr.

        Args:
         * args: image paths to process
         * htr_id: ID for the HTR model to use
         * line_detection: ID for the line detection model to use
         * language_model: ID for the language detection model to use
         * text:
         * regions:
         * mode: either `alto` or `page`, determenes the return XML
         * wait: wait between checking requests in seconds

        Returns:
         * list of XML, if an error occured for a given image `None` is returned
        """
        process_ids: Dict[int, Path] = {}
        for image_path in args:
            try:
                logging.debug("Send {image_path} to processing endpoint.")
                process_ids[
                    self.process(
                        image_path,
                        htr_id=htr_id,
                        line_detection=line_detection,
                        language_model=language_model,
                        text=text,
                        regions=regions,
                        **kwargs,
                    )
                ] = image_path
            except Exception as e:
                logging.error(
                    f"An error occurred while sending {image_path} to processing "
                    + "endpoint.",
                    exc_info=e,
                )

        xmls: List[str | None] = [None] * len(args)
        while len(process_ids) > 0:
            to_del = []
            counter = 0
            for process_id, image_path in process_ids.items():
                try:
                    status = self.status(process_id)
                    logging.debug(f"{image_path} [{process_id}] {status}")
                    match status.upper():
                        case "FINISHED":
                            if mode == "alto":
                                xmls[args.index(image_path)] = re.sub(
                                    r"<fileName>.+?</fileName>",
                                    f"<fileName>{image_path.name}</fileName>",
                                    self.alto(process_id),
                                )
                            elif mode == "page":
                                xmls[args.index(image_path)] = re.sub(
                                    r'<Page imageFilename="[^"]+"',
                                    f'<Page imageFilename="{image_path.name}"',
                                    self.page(process_id),
                                )
                            to_del.append(process_id)
                        case "FAILED":
                            to_del.append(process_id)
                        case _:
                            counter += 1
                            if counter >= 5:
                                break
                except Exception as e:
                    logging.error(
                        "An error occurred while checking the state and retriving "
                        + f"results for {image_path}.",
                        exc_info=e,
                    )
                    to_del.append(process_id)

            for process_id in to_del:
                del process_ids[process_id]
            time.sleep(wait)
        return xmls

    def alto(self, process_id: int) -> str:
        """Retrive ALTO XML.

        Args:
         * process_id: a process id

        Returns:
         * ALTO XML
        """
        logging.debug(f"Get ALTO XML for {process_id}.")
        r = requests.get(
            f"{self.BASE_URL}/processes/{process_id}/alto",
            headers={"Authorization": self.access_token.get_auth_token()},
        )

        logging.debug(f"Response: {r.text}")
        if r.status_code == 401:
            logging.debug("Lost authorization, refreshing token.")
            self.access_token.refresh(True)
            return self.alto(process_id)

        r.raise_for_status()
        return r.text

    def close(self) -> bool:
        """Close this API.

        Sends a requests to revoke the access token.

        Returns:
         * `True` if request was successful
        """
        return self.access_token.revoke()

    def page(self, process_id: int) -> str:
        """Retrive PAGE XML.

        Args:
         * process_id: a process id

        Returns:
         * PAGE XML
        """
        logging.debug(f"Get PAGE-XML for {process_id}.")
        r = requests.get(
            f"{self.BASE_URL}/processes/{process_id}/page",
            headers={"Authorization": self.access_token.get_auth_token()},
        )

        logging.debug(f"Response: {r.text}")
        if r.status_code == 401:
            logging.debug("Lost authorization, refreshing token.")
            self.access_token.refresh(True)
            return self.page(process_id)

        r.raise_for_status()
        return r.text

    def process(
        self,
        image_path: str | Path,
        htr_id: int,
        line_detection: int | None = None,
        language_model: str | None = None,
        text: str | None = None,
        regions: List[Dict] | None = None,
        **kwargs: float | int,
    ) -> int:
        """Send an image for processing.

        All the arguements are send to the API in the header.

        Args:
         * image_path: path of a image to be sind to the API
         * htr_id: ID for the HTR model to use
         * line_detection: ID for the line detection model to use
         * language_model: ID for the language detection model to use
         * text:
         * regions: text regions

        Returns:
         * the process ID return by the API
        """
        config: Dict = {
            "textRecognition": {
                "htrId": htr_id,
            }
        }
        if language_model is not None:
            config["textRecognition"]["languageModel"] = language_model
        if line_detection is not None:
            config["lineDetection"] = {
                "modelId": line_detection,
            }
            if "minimalBaselineLength" in kwargs:
                config["lineDetection"]["minimalBaselineLength"] = kwargs[
                    "minimalBaselineLength"
                ]
            if "baselineAccuracyThreshold" in kwargs:
                config["lineDetection"]["baselineAccuracyThreshold"] = kwargs[
                    "baselineAccuracyThreshold"
                ]
            if "maxDistForMerging" in kwargs:
                config["lineDetection"]["maxDistForMerging"] = kwargs[
                    "maxDistForMerging"
                ]
            if "numTextRegions" in kwargs:
                config["lineDetection"]["numTextRegions"] = kwargs["numTextRegions"]

        content: Dict[str, str | List[Dict]] = {}
        if text is not None:
            content["text"] = text
        if regions is not None:
            content["regions"] = regions

        if isinstance(image_path, str):
            image_path = Path(image_path).absolute()

        if not image_path.is_file():
            raise TypeError(f"{image_path} is not a file.")

        if image_path.stat().st_size > 19000000:
            logging.debug(
                "Open image {image_path}, convert (>19MB) and base64 encode it."
            )
            image = Image.open(image_path)
            buffered = BytesIO()
            image.save(buffered, format="JPEG", quality=95)
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
        else:
            logging.debug("Open image {image_path} (<19MB) and base64 encode it.")
            img_base64 = base64.b64encode(open(image_path, "rb").read()).decode()

        r = requests.post(
            f"{self.BASE_URL}/processes",
            headers={"Authorization": self.access_token.get_auth_token()},
            json={
                "config": config,
                "content": content,
                "image": {
                    "base64": img_base64,
                },
            },
        )

        logging.debug(f"Response: {r.text}")
        if r.status_code == 401:
            logging.debug("Lost authorization, refreshing token.")
            self.access_token.refresh(True)
            return self.process(
                image_path,
                htr_id,
                line_detection,
                language_model,
                text,
                regions,
                **kwargs,
            )

        r.raise_for_status()
        return r.json()["processId"]

    def status(self, process_id: int) -> str:
        """Make an API call to retrive the state for a process ID.

        Args:
         * process_id: a process id

        Returns:
         * JSON response from the API
        """
        logging.debug("Check status for {process_id}.")
        r = requests.get(
            f"{self.BASE_URL}/processes/{process_id}",
            headers={"Authorization": self.access_token.get_auth_token()},
        )

        logging.debug(f"Response: {r.text}")
        if r.status_code == 401:
            logging.debug("Lost authorization, refreshing token.")
            self.access_token.refresh(True)
            return self.status(process_id)

        return r.json()["status"]


@contextmanager
def transkribus_metagrapho_api(username: str, password: str) -> Generator:
    """Context manager for Transkribus metagrapho API.

    Args:
     * username: username for API authentication
     * password: password for API authentication

    Returns:
     * an instance of `TranskribusMetagraphoAPI`
    """
    api = TranskribusMetagraphoAPI(username, password)
    yield api
    api.close()
