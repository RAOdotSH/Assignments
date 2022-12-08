import streamlit
from htbuilder import (
    HtmlElement,
    div,
    ul,
    li,
    br,
    hr,
    a,
    p,
    img,
    styles,
    classes,
    fonts,
)
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
    </style>
    """

    style_div = styles(
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        text_align="center",
        height="60px",
    )

    style_hr = styles()

    body = p()
    foot = div(style=style_div)(hr(style=style_hr), body)

    streamlit.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)

    streamlit.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        br(),
        "Created with ❤️ by<b> RAO.sh</b>",
        # link(
        #     "https://wcewlug.org",
        #     image("https://i.imgur.com/2xbJ8Zo.png", height=px(30)),
        # ),
    ]
    layout(*myargs)