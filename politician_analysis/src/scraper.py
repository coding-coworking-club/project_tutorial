import json
import time
import requests


YOUTUBE_URL = "https://www.youtube.com/watch?v={youtube_id}"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
SORT_BY_POPULAR = 0
SORT_BY_RECENT = 1


def find_value(html, key, num_chars, separator='"'):
    pos_begin = html.find(key) + len(key) + num_chars
    pos_end = html.find(separator, pos_begin)
    return html[pos_begin:pos_end]


def ajax_request(session, endpoint, version, api_key, retries=5, sleep=20):

    component = endpoint["commandMetadata"]["webCommandMetadata"]["apiUrl"]

    url = f"https://www.youtube.com{component}"
    data = {
        "context": {
            "client": {
                "userAgent": USER_AGENT,
                "clientName": "WEB",
                "clientVersion": version,
            },
            "clickTracking": {"clickTrackingParams": endpoint["clickTrackingParams"]},
        },
        "continuation": endpoint["continuationCommand"]["token"],
    }

    for _ in range(retries):
        response = session.post(url, params={"key": api_key}, json=data)
        if response.status_code == 200:
            return response.json()
        elif response.status_code in [403, 413]:
            return {"You dont have authorization to access this page"}
        else:
            time.sleep(sleep)


def search_dict(partial, search_key):
    stack = [partial]
    while stack:
        current_item = stack.pop()
        if isinstance(current_item, dict):
            for key, value in current_item.items():
                if key == search_key:
                    yield value
                else:
                    stack.append(value)
        elif isinstance(current_item, list):
            stack += current_item


def download_comments(youtube_video_id, sort_by=SORT_BY_RECENT, sleep=0.1):

    """Download comments from youtube URL, send ajax request for dynamic webpages.
    Load the response JSON file and sorted the comments if it's not sorted by popularity.
    Lastly, save comment information as a dictionary.


    Parameters:
    youtube_id : youtube id for the selected video.
    sort_by : Has SORT_BY_RECENT and SORT_BY_POPULAR based on customers settings.
    sleep : wait for a given number of seconds.

    Returns:
    comment data: A dictionary with selected comments information.
    """

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    response = session.get(YOUTUBE_URL.format(youtube_video_id=youtube_id))

    if "uxe=" in response.request.url:
        session.cookies.set("CONSENT", "YES+cb", domain=".youtube.com")
        response = session.get(YOUTUBE_URL.format(youtube_video_id=youtube_id))

    html = response.text
    version = find_value(html, "client.version", 4, "'")
    api_key = find_value(html, "INNERTUBE_API_KEY", 3)

    data = json.loads(find_value(html, "var ytInitialData = ", 0, "};") + "}")
    section = next(search_dict(data, "itemSectionRenderer"), None)
    renderer = (
        next(search_dict(section, "continuationItemRenderer"), None)
        if section
        else None
    )
    if not renderer:
        return

    needs_sorting = sort_by != SORT_BY_POPULAR
    continuations = [renderer["continuationEndpoint"]]
    while continuations:
        continuation = continuations.pop()
        response = ajax_request(session, continuation, version, api_key)

        if not response:
            break
        if list(search_dict(response, "externalErrorMessage")):
            raise RuntimeError(
                "Error returned from server: "
                + next(search_dict(response, "externalErrorMessage"))
            )

        # sorted the comments if it's not sorted by popularity.
        if needs_sorting:
            sort_menu = next(
                search_dict(response, "sortFilterSubMenuRenderer"), {}
            ).get("subMenuItems", [])
            if sort_by < len(sort_menu):
                continuations = [sort_menu[sort_by]["serviceEndpoint"]]
                needs_sorting = False
                continue
            raise RuntimeError("Failed to set sorting")

        actions = list(search_dict(response, "reloadContinuationItemsCommand")) + list(
            search_dict(response, "appendContinuationItemsAction")
        )
        for action in actions:
            for item in action.get("continuationItems", []):
                if action["targetId"] == "comments-section":
                    # Process continuations for comments and replies.
                    continuations = [
                        ep for ep in search_dict(item, "continuationEndpoint")
                    ] + continuations
                if (
                    action["targetId"].startswith("comment-replies-item")
                    and "continuationItemRenderer" in item
                ):
                    # Process the 'Show more replies' button
                    continuations.append(
                        next(search_dict(item, "buttonRenderer"))["command"]
                    )

        # Save comment into dictionary format
        for comment in reversed(list(search_dict(response, "commentRenderer"))):
            yield {
                "cid": comment["commentId"],
                "text": "".join(
                    [c["text"] for c in comment["contentText"].get("runs", [])]
                ),
                "time": comment["publishedTimeText"]["runs"][0]["text"],
                "author": comment.get("authorText", {}).get("simpleText", ""),
                "channel": comment["authorEndpoint"]["browseEndpoint"].get(
                    "browseId", ""
                ),
                "votes": comment.get("voteCount", {}).get("simpleText", "0"),
                "photo": comment["authorThumbnail"]["thumbnails"][-1]["url"],
                "heart": next(search_dict(comment, "isHearted"), False),
            }

        time.sleep(sleep)
