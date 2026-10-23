"""UI-Tests: Frontend im echten Browser (Playwright/Chromium) gegen einen echten Server."""
import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.ui


@pytest.fixture
def app(page: Page, server):
    page.goto(server.base)
    expect(page.locator("#count")).to_have_text("0 offen von 0")
    return page


def add(page: Page, text: str, wait: bool = True):
    """Legt eine Aufgabe an und wartet auf die Serverantwort (Eingabefeld wird geleert)."""
    page.fill("#input", text)
    page.press("#input", "Enter")
    if wait:
        expect(page.locator("#input")).to_have_value("")


def items(page: Page):
    return page.locator("#list li")


def edit(page: Page, index: int, text: str, key: str = "Enter"):
    page.locator("#list li span").nth(index).dblclick()
    field = page.locator("#list li input[type=text]")
    field.fill(text)
    field.press(key)


# --- Seite laden ---

def test_seite_laedt_leer(app: Page):
    expect(app).to_have_title("Todo App")
    expect(app.locator("h1")).to_have_text("Todos")
    expect(items(app)).to_have_count(0)
    expect(app.locator("#input")).to_be_focused()
    expect(app.locator("#filters button[data-f=all]")).to_have_class("active")


# --- Hinzufügen ---

def test_hinzufuegen_per_enter(app: Page):
    add(app, "Milch kaufen")
    expect(items(app)).to_have_count(1)
    expect(items(app).first).to_contain_text("Milch kaufen")
    expect(app.locator("#input")).to_have_value("")
    expect(app.locator("#count")).to_have_text("1 offen von 1")


def test_hinzufuegen_per_button(app: Page):
    app.fill("#input", "Brot")
    app.click("form button")
    expect(items(app)).to_have_count(1)


def test_reihenfolge_bleibt_erhalten(app: Page):
    for t in ["eins", "zwei", "drei"]:
        add(app, t)
    expect(app.locator("#list li span")).to_have_text(["eins", "zwei", "drei"])


def test_leere_eingabe_legt_nichts_an(app: Page):
    app.click("form button")  # HTML5 "required" blockiert
    expect(items(app)).to_have_count(0)


def test_nur_leerzeichen_legt_nichts_an(app: Page):
    add(app, "     ", wait=False)
    expect(items(app)).to_have_count(0)
    expect(app.locator("#count")).to_have_text("0 offen von 0")


def test_text_wird_getrimmt(app: Page):
    add(app, "   Rand   ")
    expect(app.locator("#list li span")).to_have_text("Rand")


# --- Abhaken ---

def test_abhaken_und_wieder_oeffnen(app: Page):
    add(app, "a")
    add(app, "b")
    box = items(app).first.locator("input[type=checkbox]")
    box.check()
    expect(items(app).first).to_have_class("done")
    expect(app.locator("#count")).to_have_text("1 offen von 2")
    box.uncheck()
    expect(items(app).first).not_to_have_class("done")
    expect(app.locator("#count")).to_have_text("2 offen von 2")


def test_erledigte_aufgabe_ist_durchgestrichen(app: Page):
    add(app, "a")
    items(app).first.locator("input[type=checkbox]").check()
    expect(items(app).first.locator("span")).to_have_css("text-decoration-line", "line-through")


# --- Löschen ---

def test_loeschen(app: Page):
    add(app, "a")
    add(app, "b")
    items(app).first.locator("button").click()
    expect(app.locator("#list li span")).to_have_text(["b"])
    expect(app.locator("#count")).to_have_text("1 offen von 1")


def test_alle_loeschen(app: Page):
    add(app, "a")
    add(app, "b")
    items(app).first.locator("button").click()
    items(app).first.locator("button").click()
    expect(items(app)).to_have_count(0)
    expect(app.locator("#count")).to_have_text("0 offen von 0")


# --- Filter ---

def test_filter(app: Page):
    add(app, "offen")
    add(app, "fertig")
    items(app).nth(1).locator("input[type=checkbox]").check()

    app.click("#filters button[data-f=open]")
    expect(app.locator("#list li span")).to_have_text(["offen"])
    expect(app.locator("#filters button[data-f=open]")).to_have_class("active")
    expect(app.locator("#filters button[data-f=all]")).not_to_have_class("active")

    app.click("#filters button[data-f=done]")
    expect(app.locator("#list li span")).to_have_text(["fertig"])

    app.click("#filters button[data-f=all]")
    expect(items(app)).to_have_count(2)


def test_zaehler_ignoriert_filter(app: Page):
    add(app, "a")
    add(app, "b")
    items(app).first.locator("input[type=checkbox]").check()
    app.click("#filters button[data-f=done]")
    expect(app.locator("#count")).to_have_text("1 offen von 2")


def test_filter_wird_nach_neuladen_zurueckgesetzt(app: Page):
    add(app, "a")
    app.click("#filters button[data-f=done]")
    app.reload()
    expect(app.locator("#filters button[data-f=all]")).to_have_class("active")
    expect(items(app)).to_have_count(1)


# --- Bearbeiten ---

def test_bearbeiten_mit_enter(app: Page):
    add(app, "alt")
    edit(app, 0, "neu")
    expect(app.locator("#list li span")).to_have_text("neu")
    expect(app.locator("#list li input[type=text]")).to_have_count(0)


def test_bearbeiten_feld_enthaelt_alten_text_und_hat_fokus(app: Page):
    add(app, "alt")
    app.locator("#list li span").dblclick()
    field = app.locator("#list li input[type=text]")
    expect(field).to_have_value("alt")
    expect(field).to_be_focused()


def test_bearbeiten_escape_verwirft(app: Page):
    add(app, "alt")
    edit(app, 0, "neu", key="Escape")
    expect(app.locator("#list li span")).to_have_text("alt")


def test_bearbeiten_klick_daneben_speichert(app: Page):
    add(app, "alt")
    app.locator("#list li span").dblclick()
    app.locator("#list li input[type=text]").fill("neu")
    app.locator("h1").click()
    expect(app.locator("#list li span")).to_have_text("neu")


def test_bearbeiten_leerer_text_wird_verworfen(app: Page):
    add(app, "alt")
    edit(app, 0, "   ")
    expect(app.locator("#list li span")).to_have_text("alt")


def test_bearbeiten_behaelt_done_status(app: Page):
    add(app, "alt")
    items(app).first.locator("input[type=checkbox]").check()
    edit(app, 0, "neu")
    expect(items(app).first).to_have_class("done")
    expect(app.locator("#list li span")).to_have_text("neu")


def test_bearbeiten_unveraendert_sendet_keinen_request(app: Page):
    add(app, "alt")
    patches = []
    app.on("request", lambda r: patches.append(r) if r.method == "PATCH" else None)
    edit(app, 0, "alt")
    expect(app.locator("#list li span")).to_have_text("alt")
    assert patches == []


def test_bearbeiten_sendet_genau_einen_request(app: Page):
    add(app, "alt")
    patches = []
    app.on("request", lambda r: patches.append(r) if r.method == "PATCH" else None)
    edit(app, 0, "neu")  # Enter + anschließendes blur dürfen nicht doppelt senden
    expect(app.locator("#list li span")).to_have_text("neu")
    app.wait_for_timeout(300)
    assert len(patches) == 1


def test_bearbeiten_blur_waehrend_laufender_anfrage_sendet_nicht_doppelt(app: Page):
    add(app, "alt")
    patches = []
    pending = []

    def handler(route):
        if route.request.method == "PATCH":
            patches.append(route.request)
            pending.append(route)  # Antwort bewusst zurückhalten
        else:
            route.continue_()

    app.route("**/api/todos/*", handler)
    app.locator("#list li span").dblclick()
    field = app.locator("#list li input[type=text]")
    field.fill("neu")
    field.press("Enter")
    app.locator("h1").click()  # blur, bevor der Server geantwortet hat
    app.wait_for_timeout(300)
    assert len(patches) == 1
    pending[0].continue_()
    expect(app.locator("#list li span")).to_have_text("neu")
    assert len(patches) == 1


def test_bearbeiten_in_gefilterter_ansicht(app: Page):
    add(app, "a")
    add(app, "b")
    items(app).nth(1).locator("input[type=checkbox]").check()
    app.click("#filters button[data-f=done]")
    edit(app, 0, "b2")
    expect(app.locator("#list li span")).to_have_text(["b2"])


# --- Persistenz ---

def test_daten_bleiben_nach_neuladen(app: Page):
    add(app, "bleibt")
    items(app).first.locator("input[type=checkbox]").check()
    app.reload()
    expect(app.locator("#list li span")).to_have_text(["bleibt"])
    expect(items(app).first).to_have_class("done")
    expect(app.locator("#count")).to_have_text("0 offen von 1")


def test_zweiter_browserkontext_sieht_dieselben_daten(app: Page, browser, server):
    add(app, "geteilt")
    ctx = browser.new_context()
    try:
        other = ctx.new_page()
        other.goto(server.base)
        expect(other.locator("#list li span")).to_have_text(["geteilt"])
    finally:
        ctx.close()


# --- Sicherheit im Browser ---

def test_html_im_text_wird_nicht_ausgefuehrt(app: Page):
    dialogs = []
    app.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))
    payload = "<img src=x onerror=alert('xss')><b>fett</b>"
    add(app, payload)
    expect(app.locator("#list li span")).to_have_text(payload)
    expect(app.locator("#list img")).to_have_count(0)
    expect(app.locator("#list b")).to_have_count(0)
    app.reload()
    expect(app.locator("#list li span")).to_have_text(payload)
    assert dialogs == []


# --- Fehlerverhalten ---

def test_server_nicht_erreichbar_beim_laden(page: Page, server):
    page.route("**/api/todos", lambda route: route.abort())
    page.goto(server.base)
    expect(page.locator("#count")).to_have_text("Server nicht erreichbar")
    expect(items(page)).to_have_count(0)


def test_fehler_beim_anlegen_zeigt_hinweis_und_behaelt_eingabe(app: Page):
    app.route(
        "**/api/todos",
        lambda route: route.fulfill(status=500, body="{}") if route.request.method == "POST" else route.continue_(),
    )
    with app.expect_event("dialog") as dialog:
        add(app, "geht nicht", wait=False)
    assert dialog.value.message == "Serverfehler 500"
    dialog.value.accept()
    expect(app.locator("#input")).to_have_value("geht nicht")
    expect(items(app)).to_have_count(0)


def test_fehler_beim_loeschen_behaelt_aufgabe(app: Page):
    add(app, "bleibt")
    app.route(
        "**/api/todos/*",
        lambda route: route.fulfill(status=500, body="{}") if route.request.method == "DELETE" else route.continue_(),
    )
    app.on("dialog", lambda d: d.accept())
    items(app).first.locator("button").click()
    expect(app.locator("#list li span")).to_have_text(["bleibt"])


def test_fehler_beim_abhaken_stellt_zustand_wieder_her(app: Page):
    add(app, "a")
    app.route(
        "**/api/todos/*",
        lambda route: route.fulfill(status=500, body="{}") if route.request.method == "PATCH" else route.continue_(),
    )
    app.on("dialog", lambda d: d.accept())
    items(app).first.locator("input[type=checkbox]").check()
    expect(items(app).first.locator("input[type=checkbox]")).not_to_be_checked()
    expect(app.locator("#count")).to_have_text("1 offen von 1")
