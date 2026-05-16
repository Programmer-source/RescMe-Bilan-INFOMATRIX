import flet as ft
import flet_map as fmap
import pyttsx3
from PIL import Image, ImageOps
import tf_keras as keras
import numpy as np
import tensorflow

model = keras.models.load_model("keras_model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()

engine = pyttsx3.init()

def main(page: ft.Page):
    page.title = "RescMe"
    page.window.width = 390
    page.window.height = 844
    page.window.resizable = False
    page.padding = 0

    # initializing the colors variables
    OUTER_BLUE = "#4A6FB5"
    INNER_BLUE = "#5B9BD5"
    TILE_BLUE = "#A8CCE6"
    INPUT_BG = "#C9C3BD"
    BUTTON_GREEN = "#7FB069"
    SOS_RED = "#E25C5C"
    TEXT_DARK = "#1A2E33"

    RISK_HIGH = "#E25C5C"
    RISK_MEDIUM = "#F4A261"
    RISK_LOW = "#7FB069"

    page.bgcolor = OUTER_BLUE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    user_data = {
        "full_name": "",
        "password": "",
        "logged_in": False,
    }

    def show_message(text):
        snack = ft.SnackBar(content=ft.Text(text), open=True)
        page.overlay.append(snack)
        page.update()

    # login input
    full_name = ft.TextField(
        hint_text="Full name",
        bgcolor=INPUT_BG,
        border_color="transparent",
        border_radius=30,
        content_padding=ft.Padding(left=24, top=18, right=24, bottom=18),
        text_style=ft.TextStyle(color=TEXT_DARK, size=18),
        hint_style=ft.TextStyle(color=TEXT_DARK, size=18),
        height=60,
    )

    password = ft.TextField(
        hint_text="Password",
        password=True,
        can_reveal_password=True,
        bgcolor=INPUT_BG,
        border_color="transparent",
        border_radius=30,
        content_padding=ft.Padding(left=24, top=18, right=24, bottom=18),
        text_style=ft.TextStyle(color=TEXT_DARK, size=18),
        hint_style=ft.TextStyle(color=TEXT_DARK, size=18),
        height=60,
    )

    def make_header(on_logo_click=None):
        name_display = user_data['full_name'] if user_data['full_name'] else "User"
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    on_click=on_logo_click,
                    ink=True if on_logo_click else False,
                    content=ft.Row(
                        spacing=6,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Image(src="logo.png", width=44, height=44, fit=ft.BoxFit.CONTAIN),
                            ft.Text(
                                spans=[
                                    ft.TextSpan("Resc", style=ft.TextStyle(size=22, weight=ft.FontWeight.BOLD,
                                                                           color=TEXT_DARK)),
                                    ft.TextSpan("Me", style=ft.TextStyle(size=22, weight=ft.FontWeight.W_300,
                                                                         color=TEXT_DARK)),
                                ],
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    bgcolor=INPUT_BG,
                    border_radius=20,
                    padding=ft.Padding(left=14, top=8, right=14, bottom=8),
                    content=ft.Text(f"Hey, {name_display}", size=15, color=TEXT_DARK, weight=ft.FontWeight.W_500),
                ),
            ],
        )

    # mental health assistant
    def show_mental_help_screen():
        page.controls.clear()
        chat_column = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=15)

        def add_chat_bubble(text, is_user=False):
            alignment = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
            bubble_color = BUTTON_GREEN if is_user else INPUT_BG
            text_color = "white" if is_user else TEXT_DARK

            b_radius = ft.BorderRadius(
                top_left=25,
                top_right=25,
                bottom_left=25 if is_user else 5,
                bottom_right=5 if is_user else 25
            )

            chat_column.controls.append(
                ft.Row(
                    alignment=alignment,
                    controls=[
                        ft.Container(
                            content=ft.Text(text, color=text_color, size=18),
                            bgcolor=bubble_color,
                            padding=ft.Padding(left=20, top=12, right=20, bottom=12),
                            border_radius=b_radius,
                            width=240 if len(text) > 25 else None,
                        )
                    ]
                )
            )
            page.update()


        def handle_send(e):
            val = message_input.value.strip()
            if not val: return
            add_chat_bubble(val, is_user=True)
            message_input.value = ""
            page.update()

            lower_val = val.lower()
            if any(k in lower_val for k in ["scared", "afraid", "panic"]):
                response = "Take a deep breath. You are safe now. I am here with you."
            elif any(k in lower_val for k in ["hurt", "pain", "doctor"]):
                response = "I'm sorry you're hurting. Please stay still while help arrives."
            elif any(k in lower_val for k in ["earthquake", "missile attack", "war", "armed", "drone"]):
                response = "It's getting serious. Stay calm and support neither side"
            else:
                response = "I hear you. Tell me more about how you're feeling."

            add_chat_bubble(response, is_user=False)

        message_input = ft.TextField(
            hint_text="Message",
            bgcolor="black",
            border_color="transparent",
            border_radius=30,
            expand=True,
            content_padding=ft.Padding(left=20, top=15, right=20, bottom=15),
            text_style=ft.TextStyle(color=TEXT_DARK, size=18),
            on_submit=handle_send,
        )

        chat_card = ft.Container(
            bgcolor=INNER_BLUE,
            border_radius=30,
            padding=ft.Padding(left=20, top=20, right=20, bottom=20),
            width=340,
            height=720,
            content=ft.Column(
                controls=[
                    make_header(on_logo_click=lambda e: show_home_screen()),
                    ft.Container(height=10),
                    ft.Text("Mental help", size=22, color=TEXT_DARK, weight=ft.FontWeight.BOLD, width=300,
                            text_align=ft.TextAlign.CENTER),
                    ft.Text("Cutie Pie Assistant", size=18, color="white", width=300),
                    ft.Container(content=chat_column, expand=True,
                                 padding=ft.Padding(top=10, bottom=10, left=0, right=0)),
                    ft.Row(
                        spacing=10,
                        controls=[
                            message_input,
                            ft.Container(
                                width=60, height=60,
                                bgcolor=BUTTON_GREEN,
                                border_radius=20,
                                on_click=handle_send,
                                content=ft.Icon(ft.Icons.SEND, color="white", size=24),
                                alignment=ft.Alignment(0, 0),  # Absolute Alignment
                                ink=True,
                            )
                        ]
                    )
                ]
            )
        )
        page.add(ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=chat_card))
        add_chat_bubble("What's wrong ?", is_user=False)


    # simulated map screen
    def show_map_screen():
        page.controls.clear()

        BUCHAREST = fmap.MapLatitudeLongitude(44.4268, 26.1025)
        #fictional data
        high_risk_zone = [
            fmap.MapLatitudeLongitude(44.4350, 26.0950),
            fmap.MapLatitudeLongitude(44.4350, 26.1100),
            fmap.MapLatitudeLongitude(44.4250, 26.1100),
            fmap.MapLatitudeLongitude(44.4250, 26.0950),
        ]
        medium_risk_zone = [
            fmap.MapLatitudeLongitude(44.4250, 26.0950),
            fmap.MapLatitudeLongitude(44.4250, 26.1100),
            fmap.MapLatitudeLongitude(44.4150, 26.1100),
            fmap.MapLatitudeLongitude(44.4150, 26.0950),
        ]
        low_risk_zone = [
            fmap.MapLatitudeLongitude(44.4350, 26.1100),
            fmap.MapLatitudeLongitude(44.4350, 26.1250),
            fmap.MapLatitudeLongitude(44.4250, 26.1250),
            fmap.MapLatitudeLongitude(44.4250, 26.1100),
        ]

        map_view = fmap.Map(
            initial_center=BUCHAREST,
            initial_zoom=13,
            layers=[
                fmap.TileLayer(url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png"),
                fmap.PolygonLayer(polygons=[
                    fmap.PolygonMarker(
                        coordinates=high_risk_zone,
                        color=RISK_HIGH + "66",
                        border_color=RISK_HIGH,
                        border_stroke_width=2,
                    ),
                    fmap.PolygonMarker(
                        coordinates=medium_risk_zone,
                        color=RISK_MEDIUM + "66",
                        border_color=RISK_MEDIUM,
                        border_stroke_width=2,
                    ),
                    fmap.PolygonMarker(
                        coordinates=low_risk_zone,
                        color=RISK_LOW + "66",
                        border_color=RISK_LOW,
                        border_stroke_width=2,
                    ),
                ]),
            ],
        )

        map_container = ft.Container(
            content=map_view,
            border_radius=20,
            height=300,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        def legend_row(color, label, description):
            return ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(width=20, height=20, bgcolor=color, border_radius=6),
                    ft.Column(
                        spacing=2,
                        expand=True,
                        controls=[
                            ft.Text(label, size=15, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                            ft.Text(description, size=12, color=TEXT_DARK),
                        ],
                    ),
                ],
            )

        key_points = ft.Column(
            spacing=12,
            controls=[
                ft.Text("Key points:", size=18, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                legend_row(RISK_HIGH, "High earthquake risk",
                           "Avoid older buildings. Have evacuation plan ready."),
                legend_row(RISK_MEDIUM, "Medium risk zone",
                           "Stay alert. Check building safety rating."),
                legend_row(RISK_LOW, "Low risk / Safe zone",
                           "Recommended evacuation destination."),
            ],
        )

        map_card = ft.Container(
            bgcolor=INNER_BLUE,
            border_radius=30,
            padding=ft.Padding(left=20, top=20, right=20, bottom=20),
            width=340,
            height=720,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                spacing=18,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    make_header(on_logo_click=lambda e: show_home_screen()),
                    map_container,
                    key_points,
                ],
            ),
        )

        page.add(
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=map_card,
            )
        )
        page.update()

    # SOS screen
    def show_sos_screen():
        page.controls.clear()

        emergency_type = ft.Dropdown(
            hint_text="What's happening?",
            bgcolor=INPUT_BG,
            border_color="transparent",
            border_radius=20,
            text_style=ft.TextStyle(color=TEXT_DARK, size=16),
            options=[
                ft.dropdown.Option("Earthquake"),
                ft.dropdown.Option("Fire"),
                ft.dropdown.Option("Flood"),
                ft.dropdown.Option("Injury / Bleeding"),
                ft.dropdown.Option("Trapped / Stuck"),
                ft.dropdown.Option("Armed conflict / Attack"),
                ft.dropdown.Option("Other / Unsure"),
            ],
        )

        people_count = ft.Dropdown(
            hint_text="Who's with you'?",
            bgcolor=INPUT_BG,
            border_color="transparent",
            border_radius=20,
            text_style=ft.TextStyle(color=TEXT_DARK, size=16),
            options=[
                ft.dropdown.Option("I'm alone"),
                ft.dropdown.Option("1-2 others"),
                ft.dropdown.Option("Group of 3+"),
                ft.dropdown.Option("I don't know"),
            ],
        )

        mobility = ft.Dropdown(
            hint_text="Can you move?",
            bgcolor=INPUT_BG,
            border_color="transparent",
            border_radius=20,
            text_style=ft.TextStyle(color=TEXT_DARK, size=16),
            options=[
                ft.dropdown.Option("Yes, safely"),
                ft.dropdown.Option("Yes, with difficulty"),
                ft.dropdown.Option("No, I'm stuck"),
                ft.dropdown.Option("Unsure"),
            ],
        )

        result_area = ft.Column(spacing=10, controls=[])
        # advices based on the user's answers
        def get_advice(etype, people, move):
            steps = []

            if etype == "Earthquake":
                if move == "No, I'm stuck":
                    steps = [
                        "Stay still. Do NOT shout — save oxygen.",
                        "Tap on a pipe or wall in groups of 3 to signal rescuers.",
                        "Cover mouth with cloth to avoid dust inhalation.",
                        "If you have a phone signal, share your location now.",
                    ]

                elif move == "Yes, safely":
                    steps = [
                        "Drop, Cover, Hold On — get under a sturdy table.",
                        "Stay away from windows, mirrors, and heavy furniture.",
                        "After shaking stops, exit using stairs — NEVER elevators.",
                        "Check for gas smell before lighting anything.",
                    ]

                else:
                    steps = [
                        "Move carefully to an interior wall or doorway.",
                        "Protect your head with arms or a bag.",
                        "Wait for shaking to fully stop before moving further.",
                    ]


            elif etype == "Fire":
                if move == "No, I'm stuck":
                    steps = [
                        "Stay LOW — smoke rises, cleaner air is near the floor.",
                        "Seal door cracks with wet cloth or clothing.",
                        "Signal from a window with a bright cloth or flashlight.",
                        "Call emergency services. Tell them your exact room.",
                    ]

                else:
                    steps = [
                        "Stay low and move toward the nearest exit.",
                        "Feel doors with the back of your hand before opening.",
                        "If door is hot, do NOT open it — find another way.",
                        "Once out, do NOT go back in for any reason.",
                    ]


            elif etype == "Flood":
                if move == "Yes, safely":
                    steps = [
                        "Move to higher ground immediately.",
                        "Avoid walking through moving water — 15cm can knock you down.",
                        "Stay away from power lines and electrical equipment.",
                        "Do NOT drive through flooded roads.",
                    ]

                else:
                    steps = [
                        "Get to the highest point you can reach safely.",
                        "Signal for help from a window or roof.",
                        "Do NOT enter rising water — wait for rescue.",
                    ]


            elif etype == "Injury / Bleeding":
                steps = [
                    "Apply firm, direct pressure on the wound with cloth.",
                    "Do not remove cloth if it soaks through — add more on top.",
                    "If bleeding is severe, elevate the wound above heart.",
                    "Keep the injured person warm and talking.",
                    "Call emergency services as soon as possible.",
                ]

                if people == "I'm alone":
                    steps.insert(0, "You are alone — use one hand to apply pressure, one to call.")

            elif etype == "Trapped / Stuck":
                steps = [
                    "Stay calm. Conserve energy and breath.",
                    "Tap on solid surfaces in groups of 3 — universal distress signal.",
                    "Do NOT shout unless you hear rescuers nearby.",
                    "Cover your nose and mouth from dust.",
                    "If you have a phone, send your location now while battery lasts.",
                ]


            elif etype == "Armed conflict / Attack":
                steps = [
                    "Move away from windows immediately.",
                    "Go to the most interior room — bathroom or hallway.",
                    "Lie flat on the floor. Cover head with arms.",
                    "Turn off all lights. Stay silent.",
                    "Do NOT use flashlights or phone screens visible from outside.",
                ]


            else:
                steps = [
                    "Take 3 slow breaths. You are not alone.",
                    "Get to the safest spot you can — interior, low, away from windows.",
                    "Call emergency services and describe what you see.",
                    "Stay on the line with someone if possible.",
                ]


            return steps
            #the function that simulates calling 911 with text to speech
        def handle_call_911(e):
            # collecting the user's answers
            etype = emergency_type.value or "unspecified emergency"
            people = people_count.value or "unknown"
            move = mobility.value or "unknown"

            # formatting the text to speech text
            speech_text = (
                f"Emergency call initiated. "
                f"Type of emergency: {etype}. "
                f"People situation: {people}. "
                f"Mobility status: {move}. "
                "Stay calm. Help is being contacted."
            )

            # tts mechanism
            speaker = pyttsx3.init()
            speaker.setProperty('rate', 160)
            speaker.say(speech_text)
            speaker.runAndWait()
            speaker.stop()

        def handle_get_help(e):
            if not emergency_type.value or not people_count.value or not mobility.value:
                show_message("Please answer all questions")
                return

            steps = get_advice(emergency_type.value, people_count.value, mobility.value)

            result_area.controls.clear()
            result_area.controls.append(
                ft.Text("What to do RIGHT NOW:", size=18, weight=ft.FontWeight.BOLD, color=TEXT_DARK)
            )

            # reading the steps out loud
            speech_text = f"Emergency instructions for {emergency_type.value}. "

            for i, step in enumerate(steps, 1):
                result_area.controls.append(
                    ft.Container(
                        bgcolor=INPUT_BG,
                        border_radius=15,
                        padding=ft.Padding(left=14, top=10, right=14, bottom=10),
                        content=ft.Row(
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                ft.Container(
                                    width=28, height=28,
                                    bgcolor=SOS_RED,
                                    border_radius=14,
                                    alignment=ft.Alignment(0, 0),
                                    content=ft.Text(str(i), color="white",
                                                    weight=ft.FontWeight.BOLD, size=14),
                                ),
                                ft.Text(step, size=14, color=TEXT_DARK, expand=True),
                            ],
                        ),
                    )
                )

                speech_text += f"Step {i}. {step}. "


            page.update()

            # saying the text out loud
            speaker = pyttsx3.init()
            speaker.setProperty('rate', 160)  # setting the properties up
            speaker.say(speech_text)
            speaker.runAndWait()
            speaker.stop()
            # end of tts

        get_help_button = ft.ElevatedButton(
            "Get Help",
            bgcolor=SOS_RED,
            color="white",
            width=250,
            height=55,
            on_click=handle_get_help,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15)),
        )
        call_911_button = ft.ElevatedButton(
            "Call 911",
            bgcolor=SOS_RED,
            color="white",
            width=200,
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15)),
            on_click = handle_call_911
        )

        sos_card = ft.Container(
            bgcolor=INNER_BLUE,
            border_radius=30,
            padding=ft.Padding(left=20, top=20, right=20, bottom=20),
            width=340,
            height=720,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    make_header(on_logo_click=lambda e: show_home_screen()),
                    ft.Container(height=4),
                    ft.Text("I need help NOW", size=22, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                    ft.Text("Answer 3 quick questions:", size=14, color=TEXT_DARK),
                    emergency_type,
                    people_count,
                    mobility,
                    ft.Container(height=4),
                    get_help_button,
                    ft.Container(height=8),
                    call_911_button,
                    ft.Container(height=8),
                    result_area,
                ],
            ),
        )

        page.add(ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=sos_card))
        page.update()

    # training data
    TRAINING_TOPICS = {
        "Bleeding Control": {
            "icon": ft.Icons.BLOODTYPE,
            "steps": [
                "Wear gloves if available, or use a plastic bag as a barrier.",
                "Apply firm, direct pressure on the wound with clean cloth.",
                "Do NOT remove the cloth if it soaks through — add more on top.",
                "If bleeding is severe, elevate the wound above heart level.",
                "Keep the person warm, calm, and talking.",
                "Call emergency services as soon as possible.",
            ],
        },
        "CPR (Adult)": {
            "icon": ft.Icons.FAVORITE,
            "steps": [
                "Check the scene is safe, then tap and shout to check responsiveness.",
                "If no response and no normal breathing — call emergency services.",
                "Place heel of one hand on center of chest, other hand on top.",
                "Push hard and fast: 5-6 cm deep, 100-120 compressions per minute.",
                "After 30 compressions, give 2 rescue breaths (if trained).",
                "Continue until help arrives or the person starts breathing.",
            ],
        },
        "Choking": {
            "icon": ft.Icons.AIR,
            "steps": [
                "Ask: 'Are you choking?' If they can't speak or cough — act fast.",
                "Stand behind them, lean them slightly forward.",
                "Give 5 sharp back blows between the shoulder blades.",
                "If that fails, do 5 abdominal thrusts (Heimlich maneuver).",
                "Alternate 5 back blows and 5 thrusts until object is dislodged.",
                "If they become unconscious, start CPR and call emergency services.",
            ],
        },
        "Burns": {
            "icon": ft.Icons.LOCAL_FIRE_DEPARTMENT,
            "steps": [
                "Remove the person from the heat source safely.",
                "Cool the burn under cool (not cold) running water for 20 minutes.",
                "Remove jewelry or tight clothing near burn BEFORE swelling starts.",
                "Do NOT apply ice, butter, toothpaste, or creams.",
                "Cover loosely with sterile non-stick dressing or cling film.",
                "Seek medical help for burns larger than a hand, or on face/joints.",
            ],
        },
        "Fractures": {
            "icon": ft.Icons.HEALING,
            "steps": [
                "Do NOT try to straighten the broken limb.",
                "Keep the person still and support the injury where it lies.",
                "Immobilize with a splint or rolled-up clothing if you must move them.",
                "Apply a cold pack wrapped in cloth to reduce swelling.",
                "Watch for shock: pale skin, fast breathing, confusion.",
                "Call emergency services — especially for spine, hip, or skull injuries.",
            ],
        },
        "Shock": {
            "icon": ft.Icons.MONITOR_HEART,
            "steps": [
                "Lay the person flat on their back.",
                "Raise their legs about 30 cm — unless you suspect spine/leg injury.",
                "Loosen tight clothing around neck, chest, and waist.",
                "Cover them with a blanket to keep warm.",
                "Do NOT give food or drink, even if they ask.",
                "Monitor breathing and stay with them until help arrives.",
            ],
        },
        "Heat Stroke": {
            "icon": ft.Icons.WB_SUNNY,
            "steps": [
                "Move the person to a cool, shaded place immediately.",
                "Remove excess clothing.",
                "Cool them down: cold wet cloths on neck, armpits, groin.",
                "Fan them and spray with cool water if possible.",
                "If conscious, give small sips of cool water.",
                "Call emergency services — heat stroke can be fatal.",
            ],
        },
        "Hypothermia": {
            "icon": ft.Icons.AC_UNIT,
            "steps": [
                "Move the person indoors or out of the cold.",
                "Remove any wet clothing carefully.",
                "Wrap them in dry blankets — cover head, leave face clear.",
                "Give warm (not hot) sweet drinks if fully conscious.",
                "Do NOT rub limbs or use direct heat like a heater on skin.",
                "Handle them gently — rough movement can trigger heart problems.",
            ],
        },
    }

    def show_training_screen():
        page.controls.clear()

        def make_training_button(topic_name, icon):
            return ft.Container(
                bgcolor=INPUT_BG,
                border_radius=18,
                padding=ft.Padding(left=16, top=14, right=16, bottom=14),
                on_click=lambda e, t=topic_name: show_training_topic_screen(t),
                ink=True,
                content=ft.Row(
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=42, height=42,
                            bgcolor=BUTTON_GREEN,
                            border_radius=12,
                            alignment=ft.Alignment(0, 0),
                            content=ft.Icon(icon, color="white", size=22),
                        ),
                        ft.Text(topic_name, size=17, weight=ft.FontWeight.W_500,
                                color=TEXT_DARK, expand=True),
                        ft.Icon(ft.Icons.CHEVRON_RIGHT, color=TEXT_DARK, size=22),
                    ],
                ),
            )

        topic_buttons = ft.Column(
            spacing=10,
            controls=[
                make_training_button(name, data["icon"])
                for name, data in TRAINING_TOPICS.items()
            ],
        )

        training_card = ft.Container(
            bgcolor=INNER_BLUE,
            border_radius=30,
            padding=ft.Padding(left=20, top=20, right=20, bottom=20),
            width=340,
            height=720,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                spacing=14,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    make_header(on_logo_click=lambda e: show_home_screen()),
                    ft.Container(height=4),
                    ft.Text("Training", size=22, weight=ft.FontWeight.BOLD,
                            color=TEXT_DARK, text_align=ft.TextAlign.CENTER),
                    ft.Text("Learn what to do BEFORE an emergency happens.",
                            size=14, color=TEXT_DARK),
                    ft.Container(height=4),
                    topic_buttons,
                ],
            ),
        )

        page.add(ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=training_card))
        page.update()

    def show_training_topic_screen(topic_name):
        page.controls.clear()
        topic = TRAINING_TOPICS[topic_name]
        steps = topic["steps"]

        step_widgets = []
        for i, step in enumerate(steps, 1):
            step_widgets.append(
                ft.Container(
                    bgcolor=INPUT_BG,
                    border_radius=15,
                    padding=ft.Padding(left=14, top=12, right=14, bottom=12),
                    content=ft.Row(
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Container(
                                width=30, height=30,
                                bgcolor=BUTTON_GREEN,
                                border_radius=15,
                                alignment=ft.Alignment(0, 0),
                                content=ft.Text(str(i), color="white",
                                                weight=ft.FontWeight.BOLD, size=14),
                            ),
                            ft.Text(step, size=15, color=TEXT_DARK, expand=True),
                        ],
                    ),
                )
            )

        back_button = ft.Container(
            bgcolor=INPUT_BG,
            border_radius=15,
            padding=ft.Padding(left=14, top=10, right=14, bottom=10),
            on_click=lambda e: show_training_screen(),
            ink=True,
            content=ft.Row(
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.ARROW_BACK, color=TEXT_DARK, size=20),
                    ft.Text("Back to topics", size=14, color=TEXT_DARK,
                            weight=ft.FontWeight.W_500),
                ],
            ),
        )

        topic_card = ft.Container(
            bgcolor=INNER_BLUE,
            border_radius=30,
            padding=ft.Padding(left=20, top=20, right=20, bottom=20),
            width=340,
            height=720,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    make_header(on_logo_click=lambda e: show_home_screen()),
                    ft.Container(height=4),
                    ft.Row(
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=44, height=44,
                                bgcolor=BUTTON_GREEN,
                                border_radius=14,
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(topic["icon"], color="white", size=24),
                            ),
                            ft.Text(topic_name, size=20, weight=ft.FontWeight.BOLD,
                                    color=TEXT_DARK, expand=True),
                        ],
                    ),
                    ft.Text("Step-by-step guide:", size=14, color=TEXT_DARK),
                    ft.Container(height=4),
                    *step_widgets,
                    ft.Container(height=10),
                    back_button,
                ],
            ),
        )

        page.add(ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=topic_card))
        page.update()
    def show_war_detection_screen():
        page.controls.clear()
        # prediction label
        pred_label = ft.Text("Waiting for scan...", size=18, color=TEXT_DARK, italic=True)

        # imported here, because we only use these modules here
        import cv2
        import os
        from datetime import datetime

        # preventing crashes by making sure if that folder exists
        os.makedirs("imgtest", exist_ok=True)

        # path of the captured photo
        captured_path_holder = {"path": None}

        selected_file_text = ft.Text("No photo captured yet", color="white", size=16)

        # putting the captured img on the screen
        captured_image = ft.Image(
            src="",
            width=280,
            height=200,
            fit=ft.BoxFit.CONTAIN,
            visible=False,
        )

        def handle_capture(e):
            try:
                #capturing func
                cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                if not cap.isOpened():
                    show_message("Cannot access webcam!")
                    return

                # first 5 frames neglected for better exposure
                for _ in range(5):
                    cap.read()

                ret, frame = cap.read()
                cap.release()

                if not ret or frame is None:
                    show_message("Failed to capture image!")
                    return

                # saving to img test folder
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"capture_{timestamp}.jpg"
                filepath = os.path.join("imgtest", filename)
                cv2.imwrite(filepath, frame)


                abs_path = os.path.abspath(filepath)
                captured_path_holder["path"] = abs_path

                selected_file_text.value = f"Captured: {filename}"
                captured_image.src = abs_path
                captured_image.visible = True
                page.update()

            except Exception as ex:
                show_message(f"Webcam error: {str(ex)}")


        def handle_detect(e):
            if captured_path_holder["path"] is None:
                show_message("Please capture a photo first!")
            else:
                image = Image.open(captured_path_holder["path"]).convert("RGB")
                image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)

                image_array = np.asarray(image)
                normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

                data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
                data[0] = normalized_image_array

                prediction = model.predict(data)

                index = np.argmax(prediction)
                class_name = class_names[index].strip()
                confidence_score = prediction[0][index]

                if class_name == "1 Safety":
                    pred_label.value = f"That's ({confidence_score:.2%} safety! Congratulations! You are in a safe enviroment)"
                    page.update()
                else:
                    pred_label.value = f"Thats {class_name} ({confidence_score:.2%}! Be careful! Go to I need help NOW tab and find out what to do)"
                    page.update()
                print("Class:", class_name, confidence_score)

        detection_card = ft.Container(
            bgcolor=INNER_BLUE,
            border_radius=ft.BorderRadius(30, 30, 30, 30),
            padding=ft.Padding(20, 20, 20, 20),
            width=340,
            height=720,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    make_header(on_logo_click=lambda e: show_home_screen()),
                    ft.Text("War Threat Detection", size=22, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                    ft.Container(
                        height=200, width=300, bgcolor=TILE_BLUE,
                        border_radius=ft.BorderRadius(20, 20, 20, 20),
                        alignment=ft.Alignment(0, 0),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.PHOTO_CAMERA, size=50, color=TEXT_DARK),
                                ft.ElevatedButton(
                                    "Capture Photo",
                                    on_click=handle_capture
                                ),
                            ]
                        )
                    ),
                    selected_file_text,
                    captured_image,
                    pred_label,
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "Send to Detect Threats",
                        bgcolor=SOS_RED,
                        color="white",
                        width=250,
                        height=60,
                        on_click=handle_detect,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=15)
                        )
                    ),
                ]
            )
        )
        page.add(ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=detection_card))
        page.update()
    # home screen
    def tile_click(name):
        if name == "Mental help":
            show_mental_help_screen()
        elif name == "Map":
            show_map_screen()
        elif name == "Threat Detection":
            show_war_detection_screen()
        elif name == "Training":
            show_training_screen()
        else:
            show_message(f"Opening {name}")

    def make_tile(label, icon, on_click):
        return ft.Container(
            bgcolor=TILE_BLUE, border_radius=24, width=140, height=140,
            on_click=on_click, ink=True,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[ft.Icon(icon, size=40, color=TEXT_DARK), ft.Text(label, size=18, color=TEXT_DARK)],
            ),
        )

    def show_home_screen():
        page.controls.clear()
        grid = ft.Column([
            ft.Row([
                make_tile("Mental help", ft.Icons.FAVORITE, lambda e: tile_click("Mental help")),
                make_tile("Map", ft.Icons.LOCATION_ON, lambda e: tile_click("Map")),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                make_tile("Threat Detection", ft.Icons.FIREPLACE, lambda e: tile_click("Threat Detection")),
                make_tile("Training", ft.Icons.SCHOOL, lambda e: tile_click("Training")),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ], spacing=14)

        sos_button = ft.Container(
            bgcolor=SOS_RED, border_radius=24, height=110, alignment=ft.Alignment(0, 0),
            content=ft.Text("I need help NOW", size=22, color="white", weight=ft.FontWeight.BOLD),
            on_click=lambda e: show_sos_screen(),
            ink=True,
        )

        home_card = ft.Container(
            bgcolor=INNER_BLUE, border_radius=30, padding=ft.Padding(20, 20, 20, 20),
            width=340, height=720,
            content=ft.Column([make_header(), ft.Container(height=10), grid, ft.Container(expand=True), sos_button]),
        )
        page.add(ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=home_card))
        page.update()

    # login screen
    def enter_click(e):
        if full_name.value and password.value:
            user_data["full_name"] = full_name.value
            show_home_screen()

    login_card = ft.Container(
        bgcolor=INNER_BLUE, border_radius=30, padding=ft.Padding(28, 40, 28, 40),
        width=340, height=720,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(src="logo.png", width=200, height=200),
                ft.Container(height=20),
                full_name, password,
                ft.Container(height=20),
                ft.ElevatedButton("Enter", on_click=enter_click, bgcolor=BUTTON_GREEN, color="white", width=200,
                                  height=50),
            ],
        ),
    )

    page.add(ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=login_card))


ft.run(main)
