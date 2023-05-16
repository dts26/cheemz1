
transform hover_main_menu (yoff=-3, pausee=0):
    subpixel True
    alpha 0 xoffset 60
    pause pausee
    ease 0.7 alpha 1 xoffset 0

    on idle:
        ease 0.15 yoffset 0
    on hover:
        ease 0.15 yoffset yoff
