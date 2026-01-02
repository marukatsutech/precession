""" Three precessions """
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
from tkinter import ttk
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import proj3d

""" Global variables """

""" Animation control """
is_play = False

""" Axis vectors """
vector_x_axis = np.array([1., 0., 0.])
vector_y_axis = np.array([0., 1., 0.])
vector_z_axis = np.array([0., 0., 1.])

""" Other parameters """
phase_init_x_deg = 0.
phase_init_y_deg = 0.
phase_init_z_deg = 0.

dir_rot_x = 1.
dir_rot_y = 1.
dir_rot_z = 1.

""" Create figure and axes """
title_ax0 = "Three precessions"
# title_ax1 = "AAA"
title_tk = title_ax0

x_min = 0.
x_max = 4.
y_min = -1.
y_max = 1.
z_min = -1.
z_max = 1.

fig = Figure()
# fig = Figure(facecolor='black')
ax0 = fig.add_subplot(111, projection='3d')
ax0.set_box_aspect((1, 1, 1))
ax0.grid()
ax0.set_title(title_ax0)
ax0.set_xlabel("x")
ax0.set_ylabel("y")
ax0.set_zlabel("z")
ax0.set_xlim(-1., 1.)
ax0.set_ylim(y_min, y_max)
ax0.set_zlim(z_min, z_max)

# ax0.set_facecolor('black')
# ax0.axis('off')


""" Embed in Tkinter """
root = tk.Tk()
root.title(title_tk)
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

""" Global objects of Tkinter """
var_time_op = tk.IntVar()

""" Classes and functions """


class Counter:
    def __init__(self, is3d=None, ax=None, xy=None, z=None, label="", color=None):
        self.is3d = is3d if is3d is not None else False
        self.ax = ax
        self.x, self.y = xy[0], xy[1]
        self.z = z if z is not None else 0
        self.label = label
        self.color = color

        self.count = 0

        if not is3d:
            self.txt_step = self.ax.text(self.x, self.y, self.label + str(self.count), color=color)
        else:
            self.txt_step = self.ax.text2D(self.x, self.y, self.label + str(self.count), color=color)
            self.xz, self.yz, _ = proj3d.proj_transform(self.x, self.y, self.z, self.ax.get_proj())
            self.txt_step.set_position((self.xz, self.yz))

    def count_up(self):
        self.count += 1
        self.txt_step.set_text(self.label + str(self.count))

    def reset(self):
        self.count = 0
        self.txt_step.set_text(self.label + str(self.count))

    def get(self):
        return self.count


class Arrow3d:
    def __init__(self, ax, x, y, z, u, v, w, color, alpha, line_width, line_style, arrow_length_ratio):
        self.ax = ax
        self.x, self.y, self.z = x, y, z
        self.u, self.v, self.w = u, v, w
        self.color = color
        self.alpha = alpha
        self.line_width = line_width
        self.line_style = line_style
        self.arrow_length_ratio = arrow_length_ratio

        self.qvr = self.ax.quiver(self.x, self.y, self.z, self.u, self.v, self.w,
                                  length=1, color=self.color, alpha=self.alpha, normalize=False,
                                  linewidth=self.line_width, linestyle=self.line_style,
                                  arrow_length_ratio=self.arrow_length_ratio)

    def _update_quiver(self):
        self.qvr.remove()
        self.qvr = self.ax.quiver(self.x, self.y, self.z, self.u, self.v, self.w,
                                  length=1, color=self.color, alpha=self.alpha, normalize=False,
                                  linewidth=self.line_width, linestyle=self.line_style,
                                  arrow_length_ratio=self.arrow_length_ratio)

    def set_vector(self, u, v, w):
        self.u, self.v, self.w = u, v, w
        self._update_quiver()

    def get_vector(self):
        return np.array([self.u, self.v, self.w])


def set_phase_init_x_deg(value):
    global phase_init_x_deg
    phase_init_x_deg = value
    update_diagrams()


def set_phase_init_y_deg(value):
    global phase_init_y_deg
    phase_init_y_deg = value
    update_diagrams()


def set_phase_init_z_deg(value):
    global phase_init_z_deg
    phase_init_z_deg = value
    update_diagrams()


def set_reverse_x(value):
    global dir_rot_x
    if value:
        dir_rot_x = - 1.
    else:
        dir_rot_x = 1.


def set_reverse_y(value):
    global dir_rot_y
    if value:
        dir_rot_y = - 1.
    else:
        dir_rot_y = 1.


def set_reverse_z(value):
    global dir_rot_z
    if value:
        dir_rot_z = - 1.
    else:
        dir_rot_z = 1.


def create_parameter_setter():
    frm_phase = ttk.Labelframe(root, relief='ridge', text="Initial phase (deg)", labelanchor='n', width=100)
    frm_phase.pack(side='left')

    lbl_x = tk.Label(frm_phase, text="x")
    lbl_x.pack(side='left')
    var_phase_init_x_deg = tk.StringVar(root)
    var_phase_init_x_deg.set(str(phase_init_x_deg))
    spn_phase_init_x_deg = tk.Spinbox(
        frm_phase, textvariable=var_phase_init_x_deg, format='%.0f', from_=-360, to=360, increment=1,
        command=lambda: set_phase_init_x_deg(float(var_phase_init_x_deg.get())), width=4
    )
    spn_phase_init_x_deg.pack(side='left')

    lbl_y = tk.Label(frm_phase, text="y")
    lbl_y.pack(side='left')
    var_phase_init_y_deg = tk.StringVar(root)
    var_phase_init_y_deg.set(str(phase_init_y_deg))
    spn_phase_init_y_deg = tk.Spinbox(
        frm_phase, textvariable=var_phase_init_y_deg, format='%.0f', from_=-360, to=360, increment=1,
        command=lambda: set_phase_init_y_deg(float(var_phase_init_y_deg.get())), width=4
    )
    spn_phase_init_y_deg.pack(side='left')

    lbl_z = tk.Label(frm_phase, text="z")
    lbl_z.pack(side='left')
    var_phase_init_z_deg = tk.StringVar(root)
    var_phase_init_z_deg.set(str(phase_init_x_deg))
    spn_phase_init_z_deg = tk.Spinbox(
        frm_phase, textvariable=var_phase_init_z_deg, format='%.0f', from_=-360, to=360, increment=1,
        command=lambda: set_phase_init_z_deg(float(var_phase_init_z_deg.get())), width=4
    )
    spn_phase_init_z_deg.pack(side='left')

    frm_reverse = ttk.Labelframe(root, relief="ridge", text="Reverse rotation", labelanchor='n')
    frm_reverse.pack(side='left', fill=tk.Y)

    var_reverse_x = tk.BooleanVar(root)
    chk_reverse_x = tk.Checkbutton(frm_reverse, text="x", variable=var_reverse_x,
                                   command=lambda: set_reverse_x(var_reverse_x.get()))
    chk_reverse_x.pack(side='left')
    var_reverse_x.set(False)

    var_reverse_y = tk.BooleanVar(root)
    chk_reverse_y = tk.Checkbutton(frm_reverse, text="y", variable=var_reverse_y,
                                   command=lambda: set_reverse_y(var_reverse_y.get()))
    chk_reverse_y.pack(side='left')
    var_reverse_y.set(False)

    var_reverse_z = tk.BooleanVar(root)
    chk_reverse_z = tk.Checkbutton(frm_reverse, text="z", variable=var_reverse_z,
                                   command=lambda: set_reverse_z(var_reverse_z.get()))
    chk_reverse_z.pack(side='left')
    var_reverse_z.set(False)


def create_animation_control():
    frm_anim = ttk.Labelframe(root, relief='ridge', text="Animation", labelanchor='n')
    frm_anim.pack(side='left', fill=tk.Y)
    btn_play = tk.Button(frm_anim, text="Play/Pause", command=switch)
    btn_play.pack(side='left')
    btn_reset = tk.Button(frm_anim, text="Reset", command=reset)
    btn_reset.pack(side='left')
    # btn_clear = tk.Button(frm_anim, text="Clear path", command=lambda: aaa())
    # btn_clear.pack(fill=tk.X)


def create_center_lines(ax, x_min, x_max, y_min, y_max, z_min, z_max):
    line_axis_x = art3d.Line3D([x_min, x_max], [0., 0.], [0., 0.], color='gray', ls='-.', linewidth=1)
    ax.add_line(line_axis_x)
    line_axis_y = art3d.Line3D([0., 0.], [y_min, y_max], [0., 0.], color='gray', ls='-.', linewidth=1)
    ax.add_line(line_axis_y)
    line_axis_z = art3d.Line3D([0., 0.], [0., 0.], [z_min, z_max], color='gray', ls='-.', linewidth=1)
    ax.add_line(line_axis_z)


def draw_static_diagrams():
    create_center_lines(ax0, -1., 1., y_min, y_max, z_min, z_max)

    c00 = Circle((0, 0), 1/np.sqrt(2), ec='red', fill=False)
    ax0.add_patch(c00)
    art3d.pathpatch_2d_to_3d(c00, z=1/np.sqrt(2), zdir='x')
    c01 = Circle((0, 0), 1/np.sqrt(2), ec='green', fill=False)
    ax0.add_patch(c01)
    art3d.pathpatch_2d_to_3d(c01, z=1/np.sqrt(2), zdir='y')
    c02 = Circle((0, 0), 1/np.sqrt(2), ec='blue', fill=False)
    ax0.add_patch(c02)
    art3d.pathpatch_2d_to_3d(c02, z=1/np.sqrt(2), zdir='z')


def update_diagrams():
    t = cnt.get()
    theta = np.deg2rad(t)

    phase_init_x = np.deg2rad(phase_init_x_deg)
    phase_init_y = np.deg2rad(phase_init_y_deg) + np.pi / 2.
    phase_init_z = np.deg2rad(phase_init_z_deg)

    ux = 1. / np.sqrt(2.)
    vx = 1. / np.sqrt(2.) * np.sin(phase_init_x + theta * dir_rot_x)
    wx = 1. / np.sqrt(2.) * np.cos(phase_init_x + theta * dir_rot_x)
    arrow_x.set_vector(ux, vx, wx)

    uy = 1. / np.sqrt(2.) * np.sin(phase_init_y + theta * dir_rot_y)
    vy = 1. / np.sqrt(2.)
    wy = 1. / np.sqrt(2.) * np.cos(phase_init_y + theta * dir_rot_y)
    arrow_y.set_vector(uy, vy, wy)

    uz = 1. / np.sqrt(2.) * np.sin(phase_init_z + theta * dir_rot_z)
    vz = 1. / np.sqrt(2.) * np.cos(phase_init_z + theta * dir_rot_z)
    wz = 1. / np.sqrt(2.)
    arrow_z.set_vector(uz, vz, wz)

    arrow_component_x_y.set_vector(0., vx, 0.)
    arrow_component_x_z.set_vector(0., 0., wx)

    arrow_component_y_x.set_vector(uy, 0., 0.)
    arrow_component_y_z.set_vector(0., 0., wy)

    arrow_component_z_x.set_vector(uz, 0., 0.)
    arrow_component_z_y.set_vector(0., vz, 0.)

    arrow_resultant_x.set_vector(1. / np.sqrt(2.) + uy + uz, 0., 0.)
    arrow_resultant_y.set_vector(0., 1. / np.sqrt(2.) + vx + vz, 0.)
    arrow_resultant_z.set_vector(0., 0., 1. / np.sqrt(2.) + wx + wy)


def reset():
    global is_play
    cnt.reset()
    update_diagrams()


def switch():
    global is_play
    is_play = not is_play


def update(f):
    if is_play:
        cnt.count_up()
        update_diagrams()


""" main loop """
if __name__ == '__main__':
    cnt = Counter(ax=ax0, is3d=True, xy=np.array([x_min, y_max]), z=z_max, label="Step=")
    draw_static_diagrams()
    create_animation_control()
    create_parameter_setter()

    arrow_x = Arrow3d(ax0, 0., 0., 0., 1. / np.sqrt(2.), 0., 1. / np.sqrt(2.), 'red', 1, 2,
                      '-', 0.2)
    arrow_y = Arrow3d(ax0, 0., 0., 0., 1. / np.sqrt(2.), 1. / np.sqrt(2.), 0., 'green', 1, 2,
                      '-', 0.2)
    arrow_z = Arrow3d(ax0, 0., 0., 0., 0., 1. / np.sqrt(2.), 1. / np.sqrt(2.), 'blue', 1, 2,
                      '-', 0.2)

    arrow_component_x_y = Arrow3d(ax0, 0., 0., 0., 0., 0., 1. / np.sqrt(2.), 'red', 1, 1,
                                  '--', 0.2)
    arrow_component_x_z = Arrow3d(ax0, 0., 0., 0., 0., 0., 0., 'red', 1, 1,
                                  '--', 0.2)

    arrow_component_y_x = Arrow3d(ax0, 0., 0., 0., 1. / np.sqrt(2.), 0., 0., 'green', 1, 1,
                                  '--', 0.2)
    arrow_component_y_z = Arrow3d(ax0, 0., 0., 0., 0., 0., 0., 'green', 1, 1,
                                  '--', 0.2)

    arrow_component_z_x = Arrow3d(ax0, 0., 0., 0., 0., 1. / np.sqrt(2.), 0., 'blue', 1, 1,
                                  '--', 0.2)
    arrow_component_z_y = Arrow3d(ax0, 0., 0., 0., 0., 0., 0., 'blue', 1, 1,
                                  '--', 0.2)

    arrow_resultant_x = Arrow3d(ax0, 0., 0., 0., 1. / np.sqrt(2.), 0., 1. / np.sqrt(2.), 'red', 0.3, 4,
                                '-', 0.2)
    arrow_resultant_y = Arrow3d(ax0, 0., 0., 0., 1. / np.sqrt(2.), 1. / np.sqrt(2.), 0., 'green', 0.3, 4,
                                '-', 0.2)
    arrow_resultant_z = Arrow3d(ax0, 0., 0., 0., 0., 1. / np.sqrt(2.), 1. / np.sqrt(2.), 'blue', 0.3, 4,
                                '-', 0.2)

    update_diagrams()


    # ax0.legend(loc='lower right', fontsize=8)
    # ax1.legend(loc='lower right', fontsize=8)

    anim = animation.FuncAnimation(fig, update, interval=100, save_count=100)
    root.mainloop()
