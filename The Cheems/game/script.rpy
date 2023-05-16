define ch_ori = Character("Cheems")
define ch_true = Character("Cheemz")
define ref = Character("Referee")

image ori = "cheems_ori.png"
image true = "cheems_true.png"
image the_room = "the_room.png"
image the_true_end = "true_end.png"
image referee:
    "wong.png"
    #zoom 1.2
    #xalign 0.3

default persistent.true_eligible = False
default persistent.transition = False

init python:
    renpy.music.register_channel("crowd", "music", loop=True)
    chess_script = os.path.join(renpy.config.gamedir, THIS_PATH, 'chess_subprocess.py')
    # for importing libraries
    import_dir = os.path.join(renpy.config.gamedir, THIS_PATH, 'python-packages')

    startupinfo = None
    if renpy.windows:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW

    # remember to kill this process after use to prevent memory leak
    # but don't kill it unless there is no more chess game to play in your VN
    chess_subprocess = subprocess.Popen(
        [sys.executable, chess_script, import_dir],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        startupinfo=startupinfo)

screen mface():
    $theface = sprite
    imagebutton:
        idle theface + ".png"
        ypos 795
        xpos 35

label splashscreen:
    scene black
    with Pause(1)

    show text "CHEEMZ PRESENTS..." with dissolve
    with Pause(2)

    hide text with dissolve
    with Pause(1)

    return

# debugging purpose
# $ persistent.true_eligible = True

label start:


    scene hallway with dissolve

    "You are in a  hallway, walking slowly towards the door in front of you."

    "You feel like turning back, but you knew that this is the moment you've been waiting for."

    "Me" "Here I go..."

    "You reached the doorknob then opens it."
    play sound [door_open, door_close]
    $ renpy.pause(3.5)
    stop sound

    scene the_room with dissolve

    "This is a chess tournament room."

    play crowd crowd_ambiance volume 0.7

    "As you enter, you can hear people talking, albeit not so clear."

    "You are participating in this tournament, and today is the finals."

    "Your only option is to WIN."

    "Drawing, or losing won't help because your opponent has higher point than you, and by winning you can outscore them."

    "As you are thinking, someone greets you."

    show referee:
        zoom 1.2
        xalign 0.0
        yalign 0.8
        linear 1.0 xalign 0.3

    $sprite = "mk_wong"
    show screen mface
    voice isyou
    ref "Mr. ######?"

    hide screen mface
    "Me" "Yes, that's me."

    $sprite = "mk_wong"
    show screen mface
    voice kochira
    ref "Alright, follow me to the table."

    hide referee
    show referee:
        zoom 1.2
        xalign 0.3
        yalign 0.8
        parallel:
            linear 1.0 zoom 0.3
        parallel:
            linear 1.0 xalign 1.0
    hide referee with dissolve
    hide screen mface
    "As you approach the table, you decide to..."

    if(persistent.true_eligible == False):
        menu:
            "Sit down":
                jump the_game

    else:
        menu:
            "Sit down":
                jump the_game

            "Call your opponent":
                jump the_game_true

label the_game:

    "You sat down."

    "You looked at your opponent's face."

    show ori:
        yalign 1.0
        xalign 0.5
        linear 0.15 yalign 1.1
        linear 0.15 yalign 1.1
    $sprite = "mk_cheems_ori"
    show screen mface
    voice cheem_intro
    ch_ori "{i}Hello, I'm Cheems. Let's have a good game.{/i}"

    hide ori with dissolve
    hide screen mface
    "You nodded in acknowledgement, then starts the game."

    stop crowd fadeout 1
    "As you becoming more focused on the chessboard, the sounds of the crowd start to fade."

    window hide
    $ quick_menu = False
    $ renpy.block_rollback()

    $ fen = STARTING_FEN
    $ movetime = 2000
    $ player_color = WHITE
    $ depth = 2

    call screen chess(chess_subprocess, fen, player_color, movetime, depth)

    $ renpy.block_rollback()
    $ renpy.checkpoint()
    $ quick_menu = True
    window show

    $ chess_subprocess.kill()

    if _return == DRAW:

        play music neutral_theme volume 0.6

        "The game ended in a draw."

        show ori
        $sprite = "mk_cheems_ori"
        show screen mface
        voice cheem_gg
        ch_ori "Good game."

        hide ori
        show ori:
            yalign 1.0
            xalign 0.5
            linear 1 xalign 5
        hide ori
        hide screen mface
        "Cheems offered to shake hands, then you took his hand and shakes it."

        "Cheems left the table immediately after that."

        "The game ended in draw, and counting the previous points, you don't have enough point to win."

        "Although you didn't win, you put up a decent battle against Cheems."

        "Me" "Not bad at all, me."

        stop music

        "NEUTRAL ENDING"

        return
    else:
        $ winner = "White" if _return == WHITE else "Black"
        "[winner] won."
        if player_color is not None:
            if _return == player_color:
                jump winning_end
            else:
                jump losing_end

label the_game_true:

    "Me" "Cheemz."

    "Your opponent surprised."

    show ori with dissolve
    $sprite = "mk_cheems_ori"
    show screen mface
    ch_ori "How..."

    hide screen mface
    "Me" "I'm here to win, let's do our best!"

    "Cheemz smiled."

    "You looked to his eyes and noticed something unusual."

    "Cheemz's eyes, seemed to shine!."

    hide ori
    show true with dissolve

    "Cheemz's then... laughs!"

    hide true
    show true:
        yalign 1.0
        xalign 0.5
        linear 0.15 yalign 1.1
        linear 0.15 yalign 1.15
        linear 0.15 yalign 1.1
        linear 0.15 yalign 1.15

    $sprite = "mk_cheems_true"
    show screen mface
    voice cheem_best
    ch_true "Hahahaha! Yeah, let's do our best!"

    hide screen mface
    "You sat down, and start the game."
    stop crowd fadeout 1

    hide ori with dissolve
    "As you becoming more focused on the chessboard, the sounds of the crowd start to fade."

    "You know this is going to be the game of your life."

    window hide
    $ quick_menu = False
    $ renpy.block_rollback()
    $ fen = STARTING_FEN
    $ movetime = 2000
    $ player_color = WHITE
    $ depth = 10
    call screen chess(chess_subprocess, fen, player_color, movetime, depth)
    $ renpy.block_rollback()
    $ renpy.checkpoint()
    $ quick_menu = True
    window show

    $ chess_subprocess.kill()

    if _return == DRAW:
        play music neutral_theme volume 0.6

        "The game ended in a draw."

        show true
        $sprite = "mk_cheems_true"
        show screen mface
        voice cheem_gg
        ch_true "Good game, I must admit you're tough."

        hide true
        hide screen mface
        "Cheemz offered to shake hands, then you took his hand and shakes it."

        "The game ended in draw, and counting the previous points, you don't have enough point to win."

        "Although you didn't win, you put up a decent battle against Cheemz."

        "Me" "Not too bad, me."

        stop music

        "NEUTRAL ENDING 2"

        return
    else:
        $ winner = "White" if _return == WHITE else "Black"
        "[winner] won."
        if player_color is not None:
            if _return == player_color:
                jump winning_end_true
            else:
                jump losing_end

label winning_end:

    play music good_theme

    show ori with dissolve
    $sprite = "mk_cheems_ori"
    show screen mface
    ch_ori "Good game."

    "Cheems offered to shake hands, then you took his hand and shakes it."

    hide ori with dissolve
    "Cheems immediately stands up and leaves the room."

    "Me" "Ah.. what a relief."

    show referee
    $sprite = "mk_wong"
    show screen mface
    ref "Congratulations, the prize will be given to you later."

    hide referee
    hide screen mface
    "Me" "Alright, no problem."

    "You won the game, and this is the start of your journey to be the best the chess world."

    "You left the room, with pride."

    stop music

    "GOOD END"

    $persistent.true_eligible = True
    $persistent.transition = False

    return

label winning_end_true:

    play music true_theme

    show true
    $sprite = "mk_cheems_true"
    show screen mface
    ch_true "Good game, sir."

    "Cheemz offered to shake hands, then you took his hand and shakes it."

    "Cheemz immediately stands up, gazes at you for a split second, then leaves the room."

    hide true
    hide screen mface
    "He seems to spoke something, but you can't understand it."

    "Me" "Ah.. what a relief."

    "Your hands were shaking when you played Cheemz before. Now it started to calm down."

    show referee
    $sprite = "mk_wong"
    show screen mface
    ref "Congratulations, the prize will be given to you later."

    hide referee
    hide screen mface
    "Me" "Alright, no problem."

    "You won the game, and the news already went everywhere."

    "You are now known as the chess player to beat Cheemz, the super chess player."

    "You left the room, with pride and fame."

    show the_true_end with dissolve

    "The sunset greets you, and you raise your hand to partially cover your eyes."

    stop music

    "TRUE END"

label losing_end:

    play music losing_theme

    "You didn't win the final game."

    "Your opponent won with much higher total point compared to you."

    "You shook your opponent's hand then leaves the room."

    stop music

    "BAD END"

    return
