"""API module for Kemono and Coomer.

Contains:
    🌟 Some useful str variables (url, services, period, status).
    🌟 The Date class for easy formatting.
    🌟 The API class, including all the relevant API calls (WIP).
"""

import requests
from os import getcwd, path

url = [coomer := "https://coomer.su/api/v1/", kemono := "https://kemono.su/api/v1"]

icons = [cicon := "https://img.coomer.su/icons", kicon := "https://img.kemono.su/icons"]

notif_icon_path = path.join(getcwd(),path.join('ui','kemono.png'))

services = [
    patreon := "patreon",
    fanbox := "fanbox",
    gumroad := "gumroad",
    fantia := "fantia",
    boosty := "boosty",
    substar := "subscribestar",
    dlsite := "dlsite",
    onlyfans := "onlyfans",
    fansly := "fansly",
    carfans := "candfans",
]

period = [recent := "recent", day := "day", week := "week", month := "month"]

status = [pending := "pending", ignored := "ignored"]


class Date:
    day: int
    month: int
    year: int

    def __init__(self, day: int, month: int, year: int) -> None:
        self.day, self.month, self.year = day, month, year

    def __repr__(self) -> str:
        return f"{self.year}-{self.month}-{self.day}"


class API:
    """API class for Kemono and Coomer."""

    def __init__(self, api: str = kemono) -> None:
        self.url = api

    def get_creators_list(self) -> list:
        """Get the list of creators.

        Returns:
            list: Response json with the list of creators.
        """

        return requests.get(f"{self.url}/creators.txt").json()

    def search_posts(self, q: str = "", tag: list[str] = [], page: int = 0) -> list:
        """Search posts by querry and tags.

        Args:
            q (str, optional): Querry string. Defaults to "".
            tag (list, optional): List of tags. Defaults to [].
            page (int, optional): Page offset. Defaults to 0.

        Returns:
            list: Response json with the list of posts that match the search.
        """

        return requests.get(
            f"{self.url}/posts", params={"q": q, "o": page, "tag": tag}
        ).json()

    def get_all_creator_posts(
        self, service: str, creator_id: str, q: str = "", page: int = 0
    ) -> list:
        """Get all the posts from a creator.

        Args:
            service (str): The service the creator is part of.
            creator_id (str): The creator id.
            q (str, optional): Querry string for post filtering. Defaults to "".
            page (int, optional): Page offset. Defaults to 0.

        Returns:
            list: Response json with the list of posts that match the search.
        """

        return requests.get(
            f"{self.url}/{service}/user/{creator_id}", params={"q": q, "o": page}
        ).json()

    def get_creator_announcements(self, service: str, creator_id: str) -> list:
        return requests.get(
            f"{self.url}/{service}/user/{creator_id}/announcements"
        ).json()

    def get_creator_fancards(self, creator_id: str) -> list:
        return requests.get(f"{self.url}/fanbox/user/{creator_id}/fancards").json()

    def get_creator_post(self, service: str, creator_id: str, post_id: str) -> list:
        return requests.get(f"{self.url}/{service}/user/{creator_id}/{post_id}").json()

    def get_creator_post_revisions(
        self, service: str, creator_id: str, post_id: str
    ) -> list:
        return requests.get(
            f"{self.url}/{service}/user/{creator_id}/{post_id}/revisions"
        ).json()

    def get_creator_profile(self, service: str, creator_id: str) -> list:
        return requests.get(f"{self.url}/{service}/user/{creator_id}/profile").json()

    def get_creator_linked_accounts(self, service: str, creator_id: str) -> list:
        return requests.get(f"{self.url}/{service}/user/{creator_id}/links").json()

    def get_creator_tags(self, service: str, creator_id: str) -> list:
        return requests.get(f"{self.url}/{service}/user/{creator_id}/tags").json()

    def get_comments(self, service: str, creator_id: str, post_id: str) -> list:
        return requests.get(
            f"{self.url}/{service}/user/{creator_id}/post/{post_id}/comments"
        ).json()

    def flag_post(self, service: str, creator_id: str, post_id: str) -> list:
        return requests.post(
            f"{self.url}/{service}/user/{creator_id}/post/{post_id}/flag"
        ).json()

    def check_flag(self, service: str, creator_id: str, post_id: str) -> int:
        return requests.get(
            f"{self.url}/{service}/user/{creator_id}/post/{post_id}/flag"
        ).status_code

    def get_discord(self, channel_id: str, page: int = 0) -> list:
        return requests.get(
            f"{self.url}/discord/channel/{channel_id}", params={"o": page}
        ).json()

    def lookup_channel(self, server_id: str) -> list:
        return requests.get(f"{self.url}/discord/channel/lookup/{server_id}").json()

    def get_favourites(self) -> list:
        return requests.get(f"{self.url}/account/favourites").json()

    def set_favourite_post(self, service: str, creator_id: str, post_id: str) -> int:
        return requests.post(
            f"{self.url}/favorites/post/{service}/{creator_id}/{post_id}"
        ).status_code

    def remove_favourite_post(self, service: str, creator_id: str, post_id: str) -> int:
        return requests.delete(
            f"{self.url}/favorites/post/{service}/{creator_id}/{post_id}"
        ).status_code

    def set_favourite_creator(self, service: str, creator_id: str) -> int:
        return requests.post(
            f"{self.url}/favorites/post/{service}/{creator_id}"
        ).status_code

    def remove_favourite_creator(self, service: str, creator_id: str) -> int:
        return requests.delete(
            f"{self.url}/favorites/post/{service}/{creator_id}"
        ).status_code

    def lookup_filehas(self, file_hash: str) -> list:
        return requests.get(f"{self.url}/search_hash/{file_hash}").json()

    def get_appversion(self) -> str:
        return requests.get(f"{self.url}/app_version").text

    def get_random_post(self) -> list:
        return requests.get(f"{self.url}/posts/random").json()

    def get_popular_posts(self, date: Date | str, period: str, page: int = 0) -> list:
        return requests.get(
            f"{self.url}/posts/popular",
            params={"date": date, "period": period, "o": page},
        ).json()

    def get_tags(self) -> list:
        return requests.get(f"{self.url}/posts/tags").json()

    def get_archive_file(self, file_hash: str) -> list:
        return requests.get(f"({self.url}/posts/archives/{file_hash})").json()

    def get_post(self, service: str, post_id: str) -> list:
        return requests.get(f"{self.url}/posts/archives/{file_hash}").json()

    def get_add_link(self, service: str, creator_id: str) -> list:
        return requests.get(f"{self.url}/{service}/user/{creator_id}/links/new").json()

    def add_link(self, service: str, creator_id: str) -> list:
        return requests.post(f"{self.url}/{service}/user/{creator_id}/links/new").json()

    def get_shares(self, service: str, creator_id: str, page: int = 0) -> list:
        return requests.get(
            f"{self.url}/{service}/user/{creator_id}/shares", params={"o": page}
        ).json()

    def get_dms(self, service: str, creator_id: str) -> list:
        return requests.get(f"{self.url}/{service}/user/{creator_id}/dms").json()

    def get_post_revisions(
        self, service: str, creator_id: str, post_id: str, revision_id: str
    ) -> list:
        return requests.get(
            f"{self.url}/{service}/user/{creator_id}/post/{post_id}/revision/{revision_id}"
        ).json()

    def register(self, username: str, pw: str, cpw: str, favs: dict) -> str:
        return requests.post(
            f"{self.url}/authentication/register",
            json={
                "username": username,
                "password": pw,
                "confirm_password": cpw,
                "favorites_json": favs,
            },
        ).status_code

    def login(self, username: str, pw: str) -> list:
        return requests.post(
            f"{self.url}/authentication/login",
            json={"username": username, "password": pw},
        ).json()

    def logout(self) -> str:
        return requests.post(f"{self.url}/authentication/logout").status_code

    def account(self) -> list:
        return requests.get(f"{self.url}/account").json()

    def change_password(self, pw: str, npw: str, cnpw: str) -> str:
        return requests.post(
            f"{self.url}/account/change_password",
            json={
                "current-password": pw,
                "new-password": npw,
                "new-password-confirmation": cnpw,
            },
        ).status_code

    def get_notification(self) -> list:
        return requests.get(f"{self.url}/account/notifications").json()

    def get_keys(self) -> list:
        return requests.get(f"{self.url}/account/keys").json()

    def revoke_keys(self) -> list:
        return requests.post(f"{self.url}/account/keys", json={"revoke": [1]}).json()

    def upload_posts(self) -> list:
        return requests.get(f"{self.url}/account/posts/upload").json()

    def get_dms_review(self, status: str) -> list:
        return requests.get(
            f"{self.url}/account/review_dms", params={"status": status}
        ).json()

    def approve_dms_review(
        self, approved_hashes: list[str, ...], delete_ignored: bool
    ) -> list:
        return requests.post(
            f"{self.url}/account/review_dms",
            json={"approved_hashes": approved_hashes, "delete_ignored": delete_ignored},
        ).json()

    def get_random_artist(self) -> list:
        return requests.get(f"{self.url}/artists/random").json()

    def get_shares(self, page: int = 0) -> list:
        return requests.get(f"{self.url}/shares", params={"o": page}).json()

    def get_share_detail(self, share_id: str) -> list:
        return requests.get(f"{self.url}/share/{share_id}").json()

    def get_list_dms(self, q: str, page: int = 0) -> list:
        return requests.get(f"{self.url}/dms", params={"q": q, "o": page}).json()

    def check_pending_dms(self) -> bool:
        return requests.get(f"{self.url}/has_pending_dms").json()

    def create_import(
        self,
        session_key: str,
        auto_import: str,
        save_session_key: str,
        save_dms: str,
        channel_ids: str,
        x_bc: str,
        auth_id: str,
        user_agent: str,
    ) -> list:
        return requests.post(
            f"{self.url}/importer/submit",
            json={
                "session_key": session_key,
                "auto_import": auto_import,
                "save_session_key": save_session_key,
                "save_dms": save_dms,
                "channel_ids": channel_ids,
                "x-bc": x_bc,
                "auth_id": auth_id,
                "user_agent": user_agent,
            },
        ).json()
