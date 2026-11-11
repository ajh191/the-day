################################################################################
## 아이템 도감 화면
################################################################################

## 1. 아이템 데이터
define ITEMS = [
    {
        "id": "umbrella",
        "name": "노란 우산의 기억",
        "route": "소은",
        "image": "images/items/item_umbrella.png",
        "desc": "비 오는 날, 처마 밑에 서 있던 내게 노란 우산이 다가왔다. 자기 쪽 어깨가 젖는 줄도 모르고 우산을 절반이나 기울여 주던 아이. 그 아이가 건넨 첫마디는 '같이 써'였다.",
    },
    {
        "id": "rooftop_key",
        "name": "옥상 열쇠",
        "route": "태은",
        "image": "images/items/item_key.png",
        "desc": "원래 잠겨 있어야 하는 문의 열쇠. 손때가 탄 금속이 햇빛을 받아 흐릿하게 빛난다. 또 올라오고 싶으면, 이라는 말과 함께 손바닥 위에 놓였다.",
    },
    {
        "id": "dain_photo",
        "name": "다인과 찍은 사진",
        "route": "다인",
        "image": "images/items/item_photo.png",
        "desc": "다인이 내 볼을 양쪽으로 잡아당기며 웃고 있다. 영문도 모르고 눈을 감은 나를 향해서. 지금은 잠금화면에 있다.",
    },
    {
        "id": "pencil",
        "name": "몽당연필",
        "route": "소은",
        "image": "images/items/item_pencil.png",
        "desc": "손가락 한 마디만 남은 연필. 끝이 둥글게 닳아 있다. 그날 쓰던 거라고, 그 뒤로 한 번도 깎지 않았다고 했다.",
    },
    {
        "id": "watch",
        "name": "멈춘 손목시계",
        "route": "태은",
        "image": "images/items/item_watch.png",
        "desc": "낡은 가죽 끈에, 바늘이 멈춘 시계. 누군가의 그날에서 멈춘 시간이다. 건네받았을 때, 금속은 아직 따뜻했다.",
    },
    {
        "id": "keyring",
        "name": "토끼 키링",
        "route": "다인",
        "image": "images/items/item_rabbit.png",
        "desc": "다인의 가방에 걸려 있던 토끼 키링. 나 까먹지 말라고, 웃으면서 내 가방 지퍼에 걸어 주었다. 걸음마다 흔들린다.",
    },
]

## 크기 조절 (프로젝트 해상도가 1280x720이면 ITEM_BOX 120, ITEM_DESC_WIDTH 300 정도로 줄이세요)
define ITEM_BOX = 160          # 아이템 칸 한 변 길이(px)
define ITEM_DESC_WIDTH = 420   # 오른쪽 설명 영역 너비(px)


## 2. 도감 기록 (회차가 바뀌어도 남는 영구 기록)
default persistent.items_found = set()

init python:

    def item_name(item_id):
        for i in ITEMS:
            if i["id"] == item_id:
                return i["name"]
        return item_id

    def get_item(item_id):
        ## 이번 회차용 변수 (엔딩 조건에 쓰는 item_umbrella 등)
        setattr(store, "item_" + item_id, True)
        ## 도감용 영구 기록
        persistent.items_found.add(item_id)
        ## 획득 알림
        renpy.notify("아이템 획득: " + item_name(item_id))


## 3. 도감 화면
screen collection():

    tag menu

    default selected = None

    $ found_count = len([i for i in ITEMS if i["id"] in persistent.items_found])

    use game_menu(_("도감")):

        hbox:
            spacing 50

            ## 왼쪽: 아이템 칸
            vbox:
                spacing 20

                text "수집 " + str(found_count) + " / " + str(len(ITEMS)) size 22 color "#ffffffaa"

                ## 아이템 개수를 바꾸면 여기 숫자(가로 3 × 세로 2)도 맞춰 주세요.
                grid 3 2:
                    spacing 20

                    for item in ITEMS:
                        $ found = item["id"] in persistent.items_found

                        button:
                            xysize (ITEM_BOX, ITEM_BOX)
                            background "#ffffff14"
                            hover_background "#ffffff33"
                            selected_background "#ffffff4d"
                            insensitive_background "#0000004d"
                            sensitive found
                            action SetScreenVariable("selected", item)

                            if found:
                                if renpy.loadable(item["image"]):
                                    add item["image"] fit "contain" xysize (ITEM_BOX - 24, ITEM_BOX - 24) align (0.5, 0.5)
                                else:
                                    text item["name"] size 20 text_align 0.5 align (0.5, 0.5)
                            else:
                                text "?" size 64 color "#ffffff55" align (0.5, 0.5)

            ## 오른쪽: 설명
            vbox:
                xsize ITEM_DESC_WIDTH
                spacing 16

                if selected:
                    text selected["name"] size 34
                    text selected["route"] + " 쪽으로 이어진 물건" size 20 color "#ffffff99"
                    null height 10
                    text selected["desc"] size 24
                else:
                    text "보고 싶은 물건을 고르세요." size 24 color "#ffffff88"