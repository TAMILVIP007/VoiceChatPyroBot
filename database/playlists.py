from database import db


c = db["playlists"]


def create_playlist(name: str) -> bool:
    if playlist := c.find_one({"name": name}):
        return False
    c.insert_one(
        {"name": name, "items": []}
    )
    return True


def get_playlist(name: str):
    playlist = c.find_one({"name": name})

    return False if not playlist else playlist


def add_item_to_playlist(name: str, item: dict) -> bool:
    if playlist := get_playlist(name):
        items = playlist["items"]
        urls = [i["url"] for i in items]

        if item["url"] in urls:
            return False

        items.append(item)

        c.update_one(
            {"name": name},
            {
                "$set": {"items": items}
            }
        )
        return True
    else:
        return False


def remove_item_from_playlist(name: str, item: dict) -> bool:
    if playlist := get_playlist(name):
        items = playlist["items"]
        urls = [i["url"] for i in items]

        if item["url"] not in urls:
            return False

        items.remove(item)

        c.update_one(
            {"name": name},
            {
                "$set": {"items": items}
            }
        )
        return True
    else:
        return False


def reset_playlist(name: str, items: list) -> bool:
    if playlist := get_playlist(name):
        if playlist["items"] == items:
            return False

        c.update_one(
            {"name": name},
            {
                "$set": {"items": items}
            }
        )
        return True
    else:
        return False


def delete_playlist(name: str) -> bool:
    if playlist := get_playlist(name):
        c.delete_one(
            {"name": name}
        )
        return True
    else:
        return False
