from api import *
from mem import *
import threading, webview, json, queue, time
from notifypy import Notify

DEFAULT_TIMER: int = 1800  # 30 minutes


class Creator:
    def __init__(self, service: str, creator_id: str, name: str = "") -> None:
        self.service = service
        self.creator_id = creator_id
        self.name = name

    def string(self):
        return f"{self.service}_{self.creator_id}"


class Input:
    def __init__(self, text: str) -> None:
        self.text = text


class Click:
    def __init__(self, click: dict) -> None:
        self.click = click


def update_handler(
    event: Creator,
    kill_switch: queue.SimpleQueue,
    timeout: int,
    notification: Notify,
    api: API,
) -> None:
    while True:
        creator_file = get_file(event.string())
        creator_fetch = api.get_all_creator_posts(event.service, event.creator_id)
        if creator_file[0] != creator_fetch[0]:
            notification.message = creator_fetch[0]["title"]
            notification.title = f"New post from {event.name} ({event.service})"
            notification.icon = notif_icon_path
            notification.application_name = "KC"
            notification.send()
            write_file(event.string(), [creator_fetch[0]])
        try:
            kill_switch.get(timeout=timeout)
            break
        except queue.Empty:
            pass


def memory_handler(memory: queue.SimpleQueue) -> None:
    while True:
        saved_data = get_file("saved_data")[0]
        match event := memory.get():
            case Creator(service=_, creator_id=_) if isinstance(event, Creator):
                if (
                    event.string() not in saved_data.keys()
                    or saved_data[event.string()] == False
                ):
                    saved_data[event.string()] = True
                else:
                    saved_data[event.string()] = False
            case int(_):
                saved_data["timer"] = event
            case _:
                raise TypeError("Not a valid memory event type.")
        write_file("saved_data", [saved_data])


def spawn_handler(
    spawn: queue.SimpleQueue, notification: Notify, api: API, timer: int
) -> None:
    active_threads: dict[str, tuple[threading.Thread, queue.SimpleQueue]] = {}
    while True:
        match event := spawn.get():
            case Creator(service=_, creator_id=_) if isinstance(event, Creator):
                if event.string() in active_threads.keys():
                    active_threads.pop(event.string())[1].put(True)
                else:
                    kill_switch = queue.SimpleQueue()
                    active_threads[event.string()] = (
                        threading.Thread(
                            daemon=True,
                            target=update_handler,
                            args=[event, kill_switch, timer, notification, api],
                        ),
                        kill_switch,
                    )
                    active_threads[event.string()][0].start()
            case bool(_):
                [
                    kill_switch.put(True)
                    for kill_switch in active_threads.pop(thread)[1]
                    for thread in active_threads.keys()
                ]
            case _:
                raise TypeError("Not a valid spawn even type.")


def input_handler(
    ifield: webview.window.Element, root: queue.SimpleQueue, debounce: queue.SimpleQueue
):
    def logic(e):
        t = threading.Timer(
            0.2,
            lambda event: root.put(Input(event.get("target", {}).get("value", ""))),
            args=[e],
        )

        try:
            debounce.get(timeout=0.1).cancel()
            t.start()
            debounce.put(t)

        except queue.Empty:
            t.start()
            debounce.put(t)

    return logic


def click_handler(root: queue.SimpleQueue) -> None:
    def logic(e):
        if e["pointerId"] != 1:
            service, creator_id = e["currentTarget"]["id"].split("_")
            root.put(Creator(service, creator_id))

    return logic


def button_handler(root: queue.SimpleQueue) -> None:
    def logic(e):
        root.put(True)

    return logic


def obliteration_handler(root: queue.SimpleQueue) -> None:
    def logic():
        root.put("OBLTERATED")

    return logic


def root_handler(window: webview.window, api: API) -> None:
    # Timer
    timer = DEFAULT_TIMER

    # Get template elements
    ctemplate = window.dom.get_element("#ctemplate")

    # Get input elements
    ifield = window.dom.get_element("#ifield")
    button = window.dom.get_element("#button")

    # Setup thread queues
    memory = queue.SimpleQueue()
    spawn = queue.SimpleQueue()
    notification = Notify()
    debounce = queue.SimpleQueue()
    root = queue.SimpleQueue()
    favourites = False

    # Get data
    clist = get_clist(api)
    saved_data = gen_saved_data(timer)[0]

    # Start handlers
    threading.Thread(daemon=True, target=memory_handler, args=[memory]).start()
    threading.Thread(
        daemon=True,
        target=spawn_handler,
        args=[
            spawn,
            notification,
            api,
            saved_data["timer"] if "timer" in saved_data.keys() else DEFAULT_TIMER,
        ],
    ).start()
    ifield.events.input += input_handler(ifield, root, debounce)
    button.events.click += button_handler(root)
    window.events.closed += obliteration_handler(root)

    # Start saved threads
    [
        spawn.put(
            Creator(
                service,
                creator_id,
                api.get_creator_profile(service, creator_id)["name"],
            )
        )
        for (service, creator_id) in [
            creator.split("_")
            for creator in saved_data.keys()
            if creator != "timer" and saved_data[creator] is True
        ]
    ]

    # UI generation
    def generate_ui(search: str) -> None:
        saved_data = gen_saved_data(timer)
        [
            c.remove()
            for c in ctemplate.parent.children
            if c.attributes["id"] != ctemplate.attributes["id"]
        ]

        if favourites:
            csource = [
                creator
                for creator in clist
                if f"{creator["service"]}_{creator['id']}" in saved_data[0].keys()
                and saved_data[0][f"{creator["service"]}_{creator['id']}"] is True
            ]
        else:
            csource = clist

        for creator in [
            creator for creator in csource if search.lower() in creator["name"].lower()
        ][:50]:
            c = Creator(creator["service"], creator["id"])
            t = ctemplate.copy()
            del t.attributes["hidden"]
            t.children[0].attributes[
                "href"
            ] = f"https://kemono.su/{c.service}/user/{c.creator_id}"
            t.children[0].children[0].attributes[
                "src"
            ] = f"{kicon}/{c.service}/{c.creator_id}"
            t.children[1].attributes["id"] = c.string()
            if not t.children[1]._event_handlers:
                t.children[1].events.click += click_handler(root)
            if c.string() in saved_data[0].keys() and saved_data[0][c.string()]:
                t.children[1].children[0].attributes["checked"] = True
            t.children[0].children[1].children[0].text = creator["name"]
            t.children[0].children[1].children[1].text = c.service

    # First UI
    generate_ui("")

    # Root handler
    while True:
        match event := root.get():
            case Input(text=_) if isinstance(event, Input):
                generate_ui(event.text)
            case Creator(service=_, creator_id=_) if isinstance(event, Creator):
                event.name = api.get_creator_profile(event.service, event.creator_id)[
                    "name"
                ]
                spawn.put(event)
                memory.put(event)
            case bool(_):
                favourites = not favourites
                ifield.value = ""
                generate_ui("")
            case str(_):
                exit()
            case _:
                pass


if __name__ == "__main__":
    api = API()
    window = webview.create_window(
        "KC",
        "ui/index.html",
        text_select=True,
        resizable=False,
        width=400,
    )
    webview.start(root_handler, args=[window, api], gui="qt", icon="ui/kemono.png")
