
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal



# Start of my config: To increase and decrease volume
from libqtile.widget import TextBox
import subprocess

class VolumeWidget(TextBox):
    def __init__(self):
        super().__init__(text="Vol")
        self.update_volume()

        # Add callbacks to the widget
        self.add_callbacks({'Button1': self.on_left_click, 'Button3': self.on_right_click})

    def update_volume(self):
        # Run your volume.sh script to get the volume level or mute state
        result = subprocess.run(["/home/chris/.config/scripts/volume.sh"], capture_output=True, text=True)
        self.text = result.stdout.strip()

    def on_left_click(self):
        subprocess.run(["/home/chris/.config/scripts/volume.sh", "up"])
        self.update_volume()

    def on_right_click(self):
        subprocess.run(["/home/chris/.config/scripts/volume.sh", "down"])
        self.update_volume()

# Create an instance of VolumeWidget
volume_widget = VolumeWidget()

# End of my config: To increase and decrease volume

# Start of My Config: (Network Widget) A Script runs and displays a icon depending on if connected to wifi, ethernet or disconnected
def get_nmcli_output():
    return subprocess.check_output(["/home/chris/.config/scripts/nmcli.sh"]).decode("utf-8").strip()

script_widget = widget.GenPollText(
    func=get_nmcli_output,
    update_interval=1,
    fmt='{} ',  # You can customize the formatting here
    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("/home/chris/.config/scripts/rofi-wifi-menu.sh")}
    #foreground='#FF0000',  # You can customize the color here
)
# End of My Config: A Script runs and displays a icon depending on if connected to wifi, ethernet or disconnected

# Start of My Config: Adding a mod key for my personal scripts and lauching apps
alt = "mod1"
# End of My Config: Adding a mod key for my personal scripts and lauching apps

# Start of My Config: Script to launch things at login
import os
import subprocess
from libqtile import hook
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])
# End of My Config: Script to launch things at login

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
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
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Start of My Config: setting my own keys
     Key([alt], "q", lazy.spawn(os.path.expanduser("/home/chris/.config/scripts/power.sh")), desc="powermenu"), 
     Key([alt], "f", lazy.spawn("firefox")),
     Key([alt], "d", lazy.spawn("rofi -show drun")),
    # End of My Config: setting my own keys

]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
     # Start of My Config: Added margin of 15 to default layouts and move them up  
     layout.MonadTall(margin=15),
     layout.MonadWide(margin=15),
     layout.RatioTile(margin=15),
     layout.TreeTab(),
     # End Start of My Config: Added margin of 15 to default layouts and move them up  
    
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    #layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.Tile(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# Start of My Config: Added and moved widgets
screens = [
    Screen(
        top=bar.Bar(
            [
            widget.TextBox(
                text = "",
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("rofi -show drun")}
                ),
             widget.Spacer(
                 length=10, 
                 ),
            widget.Clock(
                format="  %a %d-%m-%Y",
                    ),
            widget.Clock(
                format="  %I:%M %p",
                    ),
             widget.Spacer(
                 length=10, 
                 ),
            widget.CPU(format = '   {load_percent}%'),
             widget.Spacer(
                 length=10, 
                 ),
            widget.Memory(format = '   {MemPercent}%'),
             widget.Spacer(
                 length=408, 
                 ),
            widget.GroupBox(),
            widget.WindowName(),
            widget.CurrentLayout(),
            widget.Spacer(
                length=10, 
                ),
            VolumeWidget(),
            widget.Spacer(
                length=10, 
                ),
            widget.CheckUpdates(distro = "Arch_checkupdates", display_format = '󰇚 {updates}'),
            widget.Spacer(
                length=10, 
                ),
            widget.Battery(battery = "BAT0", charge_char = "󰂄 ", discharge_char = "  ", format = "{char} {percent:2.0%}", full_char ="", update_interval = "1"),
            widget.Spacer(
                 length=10, 
                 ),
            script_widget, #(Network Widget) A Script runs and displays a icon depending on if connected to wifi, ethernet or disconnected
            widget.Spacer(
                 length=10, 
                 ),
            widget.TextBox(
                text = "⏻ ",
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("/home/chris/.config/scripts/power.sh")}
                ),
            # End of My Config: Added and moved widgets
                       
                # widget.Prompt(),
                
                # widget.Chord(
                #     chords_colors={
                #         "launch": ("#ff0000", "#ffffff"),
                #     },
                #     name_transform=lambda name: name.upper(),
                # ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # # widget.StatusNotifier(),
                # widget.Systray(),
                
                # widget.QuickExit(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
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
