# My qtile config

from libqtile.dgroups import simple_key_binder
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile import hook, bar, layout, widget
from libqtile.config import Click, Drag, Group, Match, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration

mod = "mod4"
terminal = guess_terminal()

theme = {
    "background": "#000000",
    "foreground": "#ffffff"
}

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod], "r", lazy.layout.reset()),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], 'f', lazy.window.toggle_floating(), desc='Toggle floating'),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Change monitor keybinding
    Key([mod], 'period', lazy.next_screen(), desc='Next monitor'),
    # Launchers
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "shift"], "r", lazy.spawn('rofi -show run'), desc="Rofi run mode"),
    Key([mod], "space", lazy.spawn(
        'rofi -show combi -icon-theme "Papirus-Dark" -show-icons'), desc="Rofi combi mode"),
    Key([], "XF86Calculator", lazy.spawn('speedcrunch'),
        desc="Launch Speedcrunch calculator"),
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        'pulsemixer --change-volume -10', shell=True), desc="Decrease Volume by 10"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        'pulsemixer --change-volume +10 && pulsemixer --max-volume 100', shell=True), desc="Increase Volume by 10"),
    Key([], "XF86AudioMute", lazy.spawn(
        'pulsemixer --toggle-mute', shell=True), desc="Toggle Mute")
]


# Move windows between screens
def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)


def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)


keys.extend([
    Key([mod, "shift"],  "comma",  lazy.function(window_to_next_screen)),
    Key([mod, "shift"],  "period", lazy.function(window_to_previous_screen)),
    Key([mod, "control"], "comma",  lazy.function(
        window_to_next_screen, switch_screen=True)),
    Key([mod, "control"], "period", lazy.function(
        window_to_previous_screen, switch_screen=True)),
])

groups = [Group("DEV", layout='monadtall', matches=[Match(wm_class=["jetbrains-idea", "vscodium"])]),
          Group("WWW", layout='monadtall', matches=[
                Match(wm_class=["firefox"])]),
          Group("SYS", layout='monadtall', matches=[
                Match(wm_class=["thunar"])]),
          Group("DOC"),
          Group("SYS"),
          Group("CHAT", layout='monadtall', matches=[
                Match(wm_class=["slack", "ferdium"])]),
          Group("ZOOM", layout='floating', matches=[Match(wm_class=["zoom"])]),
          Group("MUS"),
          Group("VID"),
          Group("GFX")]

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {
    "border_width": 2,
    "border_focus": theme["foreground"],
    "border_normal": theme["background"]
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme)
]

widget_defaults = dict(
    font="Noto Sans",
    fontsize=12,
    padding=4,
)
extension_defaults = widget_defaults.copy()

groupsWidget = dict(
    highlight_method='block',
    block_highlight_text_color=theme["background"],
    this_current_screen_border=theme["foreground"],
)

systrayWidget = dict(
    icon_size=16,
    padding=10
)

clockWidget = dict(
    format="%y-%m-%d %a %H:%M"
)

spacerWidget = dict(
    length=10
)


def init_widgets_list():
    widgets_list = [
        widget.Spacer(**spacerWidget),
        widget.GroupBox(**groupsWidget),
        widget.Spacer(**spacerWidget),
        widget.CurrentLayout(),
        widget.Prompt(),
        widget.WindowName(),
        widget.Spacer(),
        widget.Systray(**systrayWidget),
        widget.Spacer(**spacerWidget),
        widget.Volume(
            mouse_callbacks={
                'Button3': lambda: qtile.cmd_spawn('pavucontrol')},
            fmt='Vol: {}',
        ),
        widget.Spacer(**spacerWidget),
        widget.Clock(**clockWidget),
        widget.Spacer(**spacerWidget),
        widget.QuickExit(),
    ]
    return widgets_list


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[7:11]
    del widgets_screen2[9:10]
    return widgets_screen2


screens = [
    Screen(
        wallpaper='~/Pictures/wallpapers/1000.jpg',
        wallpaper_mode='fill',
        top=bar.Bar(
            init_widgets_screen1(),
            28,
            background=theme["background"]
        ),
    ),
    Screen(
        wallpaper='~/Pictures/wallpapers/1000.jpg',
        wallpaper_mode='fill',
        top=bar.Bar(
            init_widgets_screen2(),
            28,
            background=theme["background"]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])


# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
