## ─── 스토리라인 (분기 흐름도) ───────────────────────────────────
## 15개 label을 갈라지고 합쳐지는 흐름도로 보여 주고, 누르면 그 label로 이동합니다.
## 한 번 본 장면만 누를 수 있고, 아직 못 본 장면은 잠겨 있습니다.

################################################################################
## 1. 장면 목록
################################################################################
## label  : script.rpy에 있는 label 이름 (철자가 정확히 같아야 합니다)
## route  : 버튼 색을 정하는 인물 (이준 / 소은 / 태은 / 다인)
## ending : True면 그림이 들어가는 엔딩 카드
## image  : 엔딩 그림 경로. 지금은 None(그림 없음)입니다.

define STORYLINE = [
    {"label": "start",           "no": "1",   "route": "이준", "title": "그날로부터, 1년"},
    {"label": "ch2",             "no": "2",   "route": "이준", "title": "균열과 제안"},
    {"label": "ch2_keep_soeun",  "no": "2-1", "route": "소은", "title": "사진 한 장을 내놓다"},
    {"label": "ch2_keep_dain",   "no": "2-2", "route": "다인", "title": "첫 기억을 내놓다"},
    {"label": "ch3",             "no": "3",   "route": "이준", "title": "첫 번째 회귀"},
    {"label": "ch4",             "no": "4",   "route": "이준", "title": "두 번째 시도"},
    {"label": "ch4_stay_taeeun", "no": "4-1", "route": "태은", "title": "끝까지 듣다"},
    {"label": "ch4_go_dain",     "no": "4-2", "route": "다인", "title": "부르는 쪽으로"},
    {"label": "ch5",             "no": "5",   "route": "이준", "title": "옅어지는 것들"},
    {"label": "ch5_stay_taeeun", "no": "5-1", "route": "태은", "title": "내가 널 기억할게"},
    {"label": "ch5_go_soeun",    "no": "5-2", "route": "소은", "title": "용기를 낸 대가"},
    {"label": "ch6",             "no": "6",   "route": "이준", "title": "마지막 하루"},
    {"label": "end_soeun",       "no": "end", "route": "소은", "title": "다 그리면 알려줄게", "kind": "소은 엔딩", "ending": True, "image": "images/cg end_soeun.png"},
    {"label": "end_taeeun",      "no": "end", "route": "태은", "title": "오랜만의 평범함",    "kind": "태은 엔딩", "ending": True, "image": "images/cg end_taeeun.png"},
    {"label": "end_dain",        "no": "end", "route": "다인", "title": "여전히, 여기",       "kind": "다인 엔딩", "ending": True, "image": "images/cg end_dain.png"},
]

## 흐름도의 줄 구성 (위에서 아래로). 한 줄에 2개면 갈림길, 3개면 엔딩 갈림길.
## 갈림길 안에서는 왼쪽 → 오른쪽 순서로 놓입니다.
define SL_ROWS = [
    ["start"],
    ["ch2"],
    ["ch2_keep_soeun", "ch2_keep_dain"],
    ["ch3"],
    ["ch4"],
    ["ch4_stay_taeeun", "ch4_go_dain"],
    ["ch5"],
    ["ch5_stay_taeeun", "ch5_go_soeun"],
    ["ch6"],
    ["end_soeun", "end_taeeun", "end_dain"],
]

## 테스트용: True로 바꾸면 안 본 장면도 전부 열립니다. 배포 전에는 꼭 False로.
define STORYLINE_UNLOCK_ALL = True

## 색
define SL_ROUTE_COLOR = {"이준": "#6a8caf", "소은": "#c98a8a", "태은": "#8a7fb0", "다인": "#e0a040"}
define SL_ACCENT = "#6a8caf"      # 제목 탭 · 위쪽 띠
define SL_PAPER = "#f6f3ee"       # 패널 바탕
define SL_INK = "#3a3640"         # 글자
define SL_INK_SOFT = "#3a364099"  # 흐린 글자
define SL_LOCKED = "#e2e0e7"      # 잠긴 버튼 바탕
define SL_LOCKED_INK = "#3a364055"
define SL_LINE = "#b8b2c4"        # 연결선

## 크기 (1920x1080 기준. 다른 해상도에서는 자동으로 비율을 맞춥니다)
define SL_NODE_W = 380     # 텍스트 버튼 너비
define SL_NODE_H = 60      # 텍스트 버튼 높이
define SL_ROW_GAP = 64     # 줄 사이 간격 (연결선 길이)
define SL_PAIR_DX = 250    # 갈림길 버튼이 가운데서 벌어지는 거리
define SL_END_DX = 470     # 엔딩 카드가 가운데서 벌어지는 거리
define SL_CARD_W = 400     # 엔딩 카드 너비
define SL_CARD_HEAD = 52   # 엔딩 카드 제목 칸 높이
define SL_CARD_IMG = 225   # 엔딩 그림 높이 (너비 400과 16:9)
define SL_LINE_W = 4       # 연결선 두께


################################################################################
## 2. 기능
################################################################################

init python:

    SL_BY_LABEL = {e["label"]: e for e in STORYLINE}

    ## 1920x1080 기준 크기를 지금 해상도에 맞게 바꿔 줌
    def sl(n):
        return int(round(n * config.screen_width / 1920.0))

    ## 한 번이라도 본 label인지 (세이브와 상관없이 기록됨)
    def storyline_unlocked(entry):
        return STORYLINE_UNLOCK_ALL or renpy.seen_label(entry["label"])

    ## 버튼 위치와 연결선 계산
    ## 돌려주는 값: 캔버스 너비, 높이, [(장면, 가운데 x, 위쪽 y, 엔딩 여부)], [(x, y, 너비, 높이) 선]
    def storyline_layout():
        cw = sl(1500)
        cx = cw // 2
        t = max(2, sl(SL_LINE_W))

        nodes = []
        lines = []
        y = sl(50)
        prev = None

        for row in SL_ROWS:
            n = len(row)
            if n == 1:
                xs = [cx]
            elif n == 2:
                xs = [cx - sl(SL_PAIR_DX), cx + sl(SL_PAIR_DX)]
            else:
                xs = [cx - sl(SL_END_DX), cx, cx + sl(SL_END_DX)]

            is_end = all(SL_BY_LABEL[l].get("ending", False) for l in row)
            h = sl(SL_CARD_HEAD + SL_CARD_IMG) if is_end else sl(SL_NODE_H)

            ## 위 줄과 이어 주는 선: 내려오는 선 → 가로선 → 내려가는 선
            if prev:
                pxs, pbottom = prev
                mid = (pbottom + y) // 2
                for x in pxs:
                    lines.append((x - t // 2, pbottom, t, mid - pbottom))
                for x in xs:
                    lines.append((x - t // 2, mid, t, y - mid))
                allx = pxs + xs
                if min(allx) != max(allx):
                    lines.append((min(allx) - t // 2, mid - t // 2, max(allx) - min(allx) + t, t))

            for l, x in zip(row, xs):
                nodes.append((SL_BY_LABEL[l], x, y, is_end))

            prev = (xs, y + h)
            y = y + h + sl(SL_ROW_GAP)

        ch = y - sl(SL_ROW_GAP) + sl(60)
        return cw, ch, nodes, lines

    ## 이동하기 전에 아이템 상태 정리
    ## - 처음(start)부터 보면: 새 게임처럼 아이템 없이 시작
    ## - 그 외 장면에서 보면: 아이템을 모두 들고 시작 → 엔딩 선택지 3개가 모두 열림
    def storyline_prepare(target):
        grant = (target != "start")
        for item_id in ["umbrella", "pencil", "rooftop_key", "watch", "dain_photo", "keyring"]:
            setattr(store, "item_" + item_id, grant)

    ## 버튼을 눌렀을 때의 동작
    ## 타이틀 화면에서는 바로 이동, 게임 중에는 한 번 확인하고 이동
    def storyline_action(label):
        go = [SetField(persistent, "storyline_target", label), Start("storyline_jump")]
        if store.main_menu:
            return go
        return Confirm("지금 진행 중인 내용은 저장되지 않아요.\n이 장면으로 이동할까요?", go)


## 실제 이동은 여기를 거쳐서 합니다.
label storyline_jump:
    $ _sl_target = persistent.storyline_target or "start"
    $ storyline_prepare(_sl_target)

    ## 이전 장면의 연출(회상 톤, 음악 등)이 남지 않도록 정리
    camera
    scene black
    stop music fadeout 1.0
    stop sound
    window hide
    $ renpy.block_rollback()

    $ renpy.jump(_sl_target)


################################################################################
## 3. 스토리라인 화면
################################################################################

screen storyline():

    tag menu

    $ cw, ch, nodes, lines = storyline_layout()
    $ total = len(STORYLINE)
    $ seen_count = len([e for e in STORYLINE if storyline_unlocked(e)])

    key "game_menu" action Return()

    ## 배경 (뒤 화면을 어둡게)
    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background
    add Solid("#16131dcc")

    ## 왼쪽 위 제목 탭
    frame:
        pos (0, sl(40))
        padding (sl(110), sl(16), sl(44), sl(16))
        background SL_ACCENT

        hbox:
            spacing sl(22)
            text "스토리라인" size sl(36) color "#ffffff"
            text (str(seen_count) + " / " + str(total)) size sl(24) color "#ffffffbb" yalign 0.5

    ## 가운데 패널
    frame:
        xalign 0.5
        ypos sl(150)
        xysize (sl(1560), sl(800))
        padding (0, 0)
        background SL_PAPER

        fixed:

            ## 위쪽 색 띠
            add Solid(SL_ACCENT) xysize (sl(1560), sl(8))

            ## 흐름도 (마우스 휠 · 드래그로 위아래 이동)
            viewport id "sl_vp":
                pos (sl(30), sl(8))
                xysize (sl(1500), sl(792))
                mousewheel True
                draggable True

                fixed:
                    xysize (cw, ch)

                    ## 연결선
                    for r in lines:
                        add Solid(SL_LINE) pos (r[0], r[1]) xysize (r[2], r[3])

                    ## 버튼 · 엔딩 카드
                    for e, x, y, is_end in nodes:
                        if is_end:
                            use storyline_ending(e, x, y)
                        else:
                            use storyline_node(e, x, y)

            ## 오른쪽 스크롤바
            vbar value YScrollValue("sl_vp"):
                style "vscrollbar"
                xalign 1.0
                xoffset -sl(12)
                ypos sl(40)
                ysize sl(720)
                unscrollable "hide"

    ## 뒤로가기
    textbutton "< 뒤로가기":
        pos (sl(60), config.screen_height - sl(80))
        yanchor 0.5
        padding (sl(26), sl(10))
        background "#ffffff"
        hover_background "#e6ecf4"
        text_size sl(24)
        text_color SL_INK
        text_hover_color SL_ACCENT
        action Return()


## 텍스트 버튼 (본편 · 분기)
screen storyline_node(e, x, y):

    $ unlocked = storyline_unlocked(e)
    $ color = SL_ROUTE_COLOR.get(e["route"], SL_ACCENT)

    button:
        pos (x, y)
        xanchor 0.5
        xysize (sl(SL_NODE_W), sl(SL_NODE_H))
        padding (0, 0)
        background ("#ffffff" if unlocked else SL_LOCKED)
        hover_background (color + "33")
        sensitive unlocked
        action storyline_action(e["label"])

        fixed:
            ## 왼쪽 색 띠
            add Solid(color if unlocked else "#c9c5d1") xysize (sl(8), sl(SL_NODE_H))

            hbox:
                align (0.5, 0.5)
                spacing sl(14)
                text e["no"] size sl(22) color (color if unlocked else SL_LOCKED_INK) yalign 0.5
                text e["title"] size sl(26) color (SL_INK if unlocked else SL_LOCKED_INK) hover_color color yalign 0.5


## 엔딩 카드 (제목 + 그림)
screen storyline_ending(e, x, y):

    $ unlocked = storyline_unlocked(e)
    $ color = SL_ROUTE_COLOR.get(e["route"], SL_ACCENT)
    $ img = e.get("image")

    button:
        pos (x, y)
        xanchor 0.5
        xysize (sl(SL_CARD_W), sl(SL_CARD_HEAD + SL_CARD_IMG))
        padding (0, 0)
        background ("#ffffff" if unlocked else SL_LOCKED)
        hover_foreground Solid("#ffffff2e")
        sensitive unlocked
        action storyline_action(e["label"])

        vbox:
            ## 제목 칸
            frame:
                xysize (sl(SL_CARD_W), sl(SL_CARD_HEAD))
                padding (0, 0)
                background (color if unlocked else "#c9c5d1")

                hbox:
                    align (0.5, 0.5)
                    spacing sl(12)
                    text e["kind"] size sl(18) color "#ffffffcc" yalign 0.5
                    text e["title"] size sl(24) color "#ffffff" yalign 0.5

            ## 그림 칸
            fixed:
                xysize (sl(SL_CARD_W), sl(SL_CARD_IMG))

                if not unlocked:
                    text "?" size sl(96) color "#ffffffdd" align (0.5, 0.5)

                elif img and renpy.loadable(img):
                    add img fit "contain" xysize (sl(SL_CARD_W), sl(SL_CARD_IMG)) align (0.5, 0.5)

                else:
                    ## 그림이 아직 없을 때
                    vbox:
                        align (0.5, 0.5)
                        spacing sl(6)
                        text e["kind"] size sl(36) color color xalign 0.5
                        text "ENDING" size sl(18) color SL_INK_SOFT xalign 0.5