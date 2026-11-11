################################################################################
## 움직이는 타이틀 화면
################################################################################

## ── 이미지 ─────────────────────────────────────────

image title_bg       = "images/title/title_bg.png"
image title_lanterns = "images/title/title_lanterns.png"
image title_glow     = "images/title/title_glow.png"
image title_logo     = "images/title/logo.png"
image white          = Solid("#ffffff")

## 화면을 빈틈없이 덮도록 확대 비율을 자동으로 계산(1888x1056)합니다.
define title_w = 1888
define title_h = 1056
define title_cover = max(config.screen_width / 1888.0, config.screen_height / 1056.0)

## 거리 끝 하얀 빛의 중심 (그림 기준 비율). title_glow.png를 이 자리에 맞춰 만들었습니다.
define title_glow_center = (0.368, 0.625)


## ── 움직임 ─────────────────────────────────────────

## 화면 전체가 아주 천천히 다가왔다 물러납니다. (숨 쉬는 느낌)
## 확대의 기준점을 거리 끝 빛에 두어, 그 빛 쪽으로 다가가는 것처럼 보입니다.
transform title_drift(base=1.0):
    subpixel True
    align title_glow_center
    zoom base
    ease 25.0 zoom base * 1.03
    ease 25.0 zoom base
    repeat

## 등불 깜박임. 일부러 박자를 고르지 않게 해서 기계적으로 보이지 않게 합니다.
transform lantern_flicker:
    alpha 0.0
    block:
        ease 1.8 alpha 0.55
        ease 0.9 alpha 0.35
        ease 1.4 alpha 0.6
        ease 2.2 alpha 0.2
        repeat

## 거리 끝 하얀 빛이 천천히 밝아졌다 흐려집니다.
transform glow_breath:
    alpha 0.5
    block:
        ease 4.0 alpha 0.85
        ease 4.0 alpha 0.5
        repeat

## 떨어지는 잎이 돌면서 내려옵니다.
transform leaf_spin_cw:
    rotate 0
    linear 5.0 rotate 360
    repeat

transform leaf_spin_ccw:
    rotate 0
    linear 7.0 rotate -360
    repeat

## 로고가 살짝 떠오르며 나타납니다.
transform logo_in:
    alpha 0.0
    yoffset 10
    pause 0.6
    ease 1.5 alpha 1.0 yoffset 0


## ── 떨어지는 잎 (파티클) ───────────────────────────
## count: 화면에 동시에 있는 잎 수 / xspeed: 옆으로 흐르는 속도(음수면 왼쪽)
## yspeed: 떨어지는 속도 / fast=True: 처음부터 화면에 잎이 차 있는 상태로 시작

image title_leaves_ginkgo = SnowBlossom(
    At("images/title/leaf_ginkgo.png", leaf_spin_cw),
    count=6, xspeed=(20, 60), yspeed=(50, 110), fast=True)

image title_leaves_maple = SnowBlossom(
    At("images/title/leaf_maple.png", leaf_spin_ccw),
    count=4, xspeed=(10, 50), yspeed=(40, 90), fast=True)


## ── 타이틀 화면 레이어 ─────────────────────────────
## screens.rpy의 main_menu 화면에서 이 화면을 불러 씁니다.

screen title_layers():

    ## 배경·등불·빛은 한 묶음으로 같이 움직여야 위치가 어긋나지 않습니다.
    fixed:
        xysize (title_w, title_h)
        at title_drift(title_cover)
        add "title_bg"
        add "title_lanterns" at lantern_flicker
        add "title_glow" at glow_breath

    add "title_leaves_maple"
    add "title_leaves_ginkgo"

    ## 위쪽 등불 줄과 둘째 줄 사이의 하늘 자리입니다.
    add "title_logo" pos (110, 120) at logo_in


## ── "시작하기"를 눌렀을 때: 하얀 빛이 화면을 덮으며 시작 ──

transform whiteout_glow:
    align title_glow_center
    alpha 0.6
    zoom title_cover
    ease 1.0 zoom title_cover * 1.8 alpha 1.0

transform whiteout_fill:
    alpha 0.0
    pause 0.3
    ease 0.9 alpha 1.0

screen title_whiteout():
    modal True
    add "title_glow" at whiteout_glow
    add "white" at whiteout_fill
    timer 1.3 action Start()


## ── 타이틀 메뉴 ───────────────────────────────────
## 왼쪽 아래 길바닥 자리에 세로로 놓입니다.
## 밝은 안개(화면 가운데 높이)와 스케치북(오른쪽 아래)을 피한 자리입니다.

## 메뉴 위치와 간격. 그림 기준 좌표라 여기만 고치면 전체가 같이 움직입니다.
define title_menu_pos = (120, 400)
define title_menu_spacing = 24

## 글자 색
define title_menu_idle  = "#fff6ec"   # 평소: 따뜻한 흰색
define title_menu_hover = "#ffd68c"   # 마우스를 올렸을 때: 등불 같은 금빛
define title_menu_ink   = "#462834"   # 테두리: 로고와 같은 자두색 계열

style title_menu_button is button:
    background None
    padding (28, 4, 12, 4)
    hover_foreground Transform(
        Text("›", font=gui.interface_text_font, size=36, color=title_menu_hover,
            outlines=[ (3, title_menu_ink + "c8", 0, 0) ]),
        xpos=2, yalign=0.5)

style title_menu_button_text is button_text:
    font gui.interface_text_font
    size 42
    idle_color title_menu_idle
    hover_color title_menu_hover
    selected_color title_menu_hover
    insensitive_color "#fff6ec80"
    outlines [ (3, title_menu_ink + "c8", 0, 0), (8, "#28161e40", 0, 2) ]
    kerning 1.0

## 마우스를 올리면 오른쪽으로 살짝 밀리고, 앞에 작은 표시가 생깁니다.
transform title_menu_item:
    on idle:
        ease 0.18 xoffset 0
    on hover:
        ease 0.18 xoffset 10

transform title_menu_in(delay=0.0):
    alpha 0.0
    xoffset -12
    pause (1.2 + delay)
    ease 0.6 alpha 1.0 xoffset 0

screen title_menu():

    vbox:
        pos title_menu_pos
        spacing title_menu_spacing

        textbutton "시작하기":
            style "title_menu_button"
            action Show("title_whiteout")
            at title_menu_in(0.0), title_menu_item

        textbutton "불러오기":
            style "title_menu_button"
            action ShowMenu("load")
            at title_menu_in(0.1), title_menu_item

        textbutton "환경설정":
            style "title_menu_button"
            action ShowMenu("preferences")
            at title_menu_in(0.2), title_menu_item

        textbutton "크레딧":
            style "title_menu_button"
            action Start("ending_credit")
            at title_menu_in(0.3), title_menu_item
        
        if renpy.variant("pc"):
            textbutton "종료":
                style "title_menu_button"
                action Quit(confirm=True)
                at title_menu_in(0.4), title_menu_item