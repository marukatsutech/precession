""" Precession and phase """
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
from tkinter import ttk
from matplotlib.patches import Circle
from scipy.spatial.transform import Rotation
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import proj3d

from matplotlib.colors import Normalize

""" Global variables """
phase_step_deg = 1.
frequency = 1.
size_scatter = 6
tilt_deg = 0.

""" Animation control """
is_play = False
is_tilt = False
is_precession = False

""" Axis vectors """
vector_x_axis = np.array([1., 0., 0.])
vector_y_axis = np.array([0., 1., 0.])
vector_z_axis = np.array([0., 0., 1.])

""" Create figure and axes """
title_ax0 = "Precession and phase"
title_tk = title_ax0

x_min = -2.
x_max = 2.
y_min = -2.
y_max = 2.
z_min = -2.
z_max = 2.

fig = Figure()
ax0 = fig.add_subplot(111, projection="3d")
ax0.set_box_aspect((4, 4, 4))
ax0.grid()
ax0.set_title(title_ax0)
ax0.set_xlabel("x")
ax0.set_ylabel("y")
ax0.set_zlabel("z")
ax0.set_xlim(x_min, x_max)
ax0.set_ylim(y_min, y_max)
ax0.set_zlim(z_min, z_max)

""" Embed in Tkinter """
root = tk.Tk()
root.title(title_tk)
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill="both")

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

""" Global objects of Tkinter """
var_phase_stp = tk.StringVar(root)
var_freq = tk.StringVar(root)
var_cmap = tk.IntVar()
var_size = tk.StringVar(root)
var_tilt_deg = tk.StringVar(root)

""" Classes and functions """


class Counter:
    def __init__(self, is3d=None, ax=None, xy=None, z=None, label=""):
        self.is3d = is3d if is3d is not None else False
        self.ax = ax
        self.x, self.y = xy[0], xy[1]
        self.z = z if z is not None else 0
        self.label = label

        self.count = 0

        if not is3d:
            self.txt_step = self.ax.text(self.x, self.y, self.label + str(self.count))
        else:
            self.txt_step = self.ax.text2D(self.x, self.y, self.label + str(self.count))
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


class Circle3d:
    def __init__(self, ax, x, y, z, r, direction, line_width, line_style, color, alpha):
        self.ax = ax
        self.x, self.y, self.z = x, y, z
        self.r = r
        self.direction = direction
        self.line_width = line_width
        self.line_style = line_style
        self.color = color
        self.alpha = alpha

        self.angle_space = np.arange(0, 360)

        self.cos_data = self.r * np.cos(self.angle_space * np.pi / 180.) + self.x
        self.sin_data = self.r * np.sin(self.angle_space * np.pi / 180.) + self.y
        self.plain_data = self.angle_space * 0. + self.z

        if self.direction == "x":
            self.x_circle, self.y_circle, self.z_circle = self.plain_data, self.cos_data, self.sin_data
        elif self.direction == "y":
            self.x_circle, self.y_circle, self.z_circle = self.cos_data, self.plain_data, self.sin_data
        else:  # "z"
            self.x_circle, self.y_circle, self.z_circle = self.cos_data, self.sin_data, self.plain_data

        self.plt_circle, = self.ax.plot(self.x_circle, self.y_circle, self.z_circle,
                                        linewidth=self.line_width, linestyle=self.line_style,
                                        color=self.color, alpha=self.alpha)

    def rotate(self, angle, rotation_axis):
        # rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
        rot_matrix = Rotation.from_rotvec(angle * rotation_axis)
        x_circle_rotated = []
        y_circle_rotated = []
        z_circle_rotated = []
        for i in range(len(self.angle_space)):
            vector_point = np.array(
                [self.x_circle[i], self.y_circle[i], self.z_circle[i]])
            point_rotated = rot_matrix.apply(vector_point)
            x_circle_rotated.append(point_rotated[0])
            y_circle_rotated.append(point_rotated[1])
            z_circle_rotated.append(point_rotated[2])
            self.x_circle[i] = point_rotated[0]
            self.y_circle[i] = point_rotated[1]
            self.z_circle[i] = point_rotated[2]
        self.plt_circle.set_xdata(np.array(x_circle_rotated))
        self.plt_circle.set_ydata(np.array(y_circle_rotated))
        self.plt_circle.set_3d_properties(np.array(z_circle_rotated))

    def reset(self):
        self.cos_data = self.r * np.cos(self.angle_space * np.pi / 180.) + self.x
        self.sin_data = self.r * np.sin(self.angle_space * np.pi / 180.) + self.y
        self.plain_data = self.angle_space * 0. + self.z

        if self.direction == "x":
            self.x_circle, self.y_circle, self.z_circle = self.plain_data, self.cos_data, self.sin_data
        elif self.direction == "y":
            self.x_circle, self.y_circle, self.z_circle = self.cos_data, self.plain_data, self.sin_data
        else:  # "z"
            self.x_circle, self.y_circle, self.z_circle = self.cos_data, self.sin_data, self.plain_data

        self.plt_circle.set_xdata(self.x_circle)
        self.plt_circle.set_ydata(self.y_circle)
        self.plt_circle.set_3d_properties(self.z_circle)


class Arrow3d:
    def __init__(self, ax, x, y, z, u, v, w, scale, line_width, line_style, color, alpha):
        self.ax = ax
        self.x, self.y, self.z = x, y, z
        self.u, self.v, self.w = u, v, w
        self.scale = scale
        self.line_width = line_width
        self.line_style = line_style
        self.color = color
        self.alpha = alpha

        self.qvr = self.ax.quiver(self.x, self.y, self.z,
                                  self.u * self.scale, self.v * self.scale, self.w * self.scale,
                                  length=1, color=self.color, normalize=False,
                                  linewidth=self.line_width, linestyle=self.line_style)

        self.vector_init = np.array([self.u, self.v, self.w])

    def _update_quiver(self):
        self.qvr.remove()
        self.qvr = self.ax.quiver(self.x, self.y, self.z,
                                  self.u * self.scale, self.v * self.scale, self.w * self.scale,
                                  length=1, color=self.color, normalize=False,
                                  linewidth=self.line_width, linestyle=self.line_style)

    def rotate(self, angle, rotation_axis):
        rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
        rot_matrix = Rotation.from_rotvec(angle * rotation_axis)
        vector_rotated = rot_matrix.apply(self.vector_init)
        self.u, self.v, self.w = vector_rotated[0], vector_rotated[1], vector_rotated[2]
        self._update_quiver()
        self.vector_init = vector_rotated

    def set_vector(self, u, v, w):
        self.u, self.v, self.w = u, v, w
        self._update_quiver()

    def get_vector(self):
        return np.array([self.u, self.v, self.w])

    def set_scale(self, value):
        self.scale = value
        self._update_quiver()


class InternalPhase:
    def __init__(self, ax, phase_step):
        self.ax = ax
        self.phase_step = phase_step

        self.vector = np.array([0., 0., 1.])
        self.counter_vector = np.array([0., 0., 1.])
        self.vector_phase_center_axis = np.array([0., 1., 0.])
        self.vector_phase = np.array([0., 0., 1.])

        self.vector_tilt_center_axis = np.array([1., 0., 0.])

        self.resultant_vector = self.vector + self.counter_vector

        self.additional_circle = Circle3d(self.ax, 0., 0., 0., 1., "y",
                                     1, "--", "darkorange", 1)
        self.rotation_vector_spacial = Arrow3d(self.ax, 0., 0., 0.,
                                               self.vector[0], self.vector[1], self.vector[2],
                                               1, 2, "-", "red", 1)
        self.rotation_counter_vector = Arrow3d(self.ax, 0., 0., 0.,
                                            self.counter_vector[0], self.counter_vector[1], self.counter_vector[2],
                                            1, 2, "-", "gray", 1)
        self.rotation_vector_phase = Arrow3d(self.ax, 0., 0., 0.,
                                             self.vector_phase[0], self.vector_phase[1], self.vector_phase[2],
                                             1, 2, "--", "darkorange", 1)

        self.resultant_rotation_vector = Arrow3d(self.ax, 0., 0., 0.,
                                                 self.resultant_vector[0], self.resultant_vector[1],
                                                 self.resultant_vector[2],
                                                 1, 1, "-.", "black", 1)

        self.internal_phase = 0.

    def rotate_phase(self):
        rot_matrix = Rotation.from_rotvec(self.phase_step * self.vector_phase_center_axis)
        self.vector_phase = rot_matrix.apply(self.vector_phase)
        self.rotation_vector_phase.set_vector(self.vector_phase[0], self.vector_phase[1], self.vector_phase[2])

        self.internal_phase += self.phase_step

    def _rotate_all(self, angle, center_axis):
        self._rotate_vector_and_phase(angle, center_axis)
        self._rotate_counter_vector(angle, center_axis)

    def _rotate_vector_and_phase(self, angle, center_axis):
        rot_matrix = Rotation.from_rotvec(angle * center_axis)

        self.additional_circle.rotate(angle, center_axis)

        self.vector = rot_matrix.apply(self.vector)
        self.vector_phase_center_axis = rot_matrix.apply(self.vector_phase_center_axis)
        self.vector_phase = rot_matrix.apply(self.vector_phase)

        self.rotation_vector_spacial.set_vector(self.vector[0], self.vector[1], self.vector[2])
        self.rotation_vector_phase.set_vector(self.vector_phase[0], self.vector_phase[1], self.vector_phase[2])

    def _rotate_counter_vector(self, angle, center_axis):
        rot_matrix = Rotation.from_rotvec(angle * center_axis)

        self.counter_vector = rot_matrix.apply(self.counter_vector)
        self.rotation_counter_vector.set_vector(self.counter_vector[0], self.counter_vector[1], self.counter_vector[2])

    def tilt(self, angle_tilt):
        self._rotate_vector_and_phase(angle_tilt, self.vector_tilt_center_axis)
        self._rotate_counter_vector(- angle_tilt, self.vector_tilt_center_axis)
        self.resultant_vector = self.vector + self.counter_vector
        self.resultant_rotation_vector.set_vector(self.resultant_vector[0], self.resultant_vector[1],
                                                  self.resultant_vector[2])

    def rotate_z(self):
        self._rotate_all(self.phase_step, vector_z_axis)

    def rotate_z_scale(self, scale):
        self._rotate_all(self.phase_step * scale, vector_z_axis)

    def rotate_r(self):
        self._rotate_all(self.phase_step, self.resultant_vector)

    def reset(self):
        self.additional_circle.reset()

        self.vector = np.array([0., 0., 1.])
        self.counter_vector = np.array([0., 0., 1.])
        self.vector_phase_center_axis = np.array([0., 1., 0.])
        self.vector_phase = np.array([0., 0., 1.])

        self.vector_tilt_center_axis = np.array([1., 0., 0.])

        self.rotation_vector_spacial.set_vector(self.vector[0], self.vector[1], self.vector[2])
        self.rotation_counter_vector.set_vector(self.counter_vector[0], self.counter_vector[1], self.counter_vector[2])
        self.rotation_vector_phase.set_vector(self.vector_phase[0], self.vector_phase[1], self.vector_phase[2])

        self.internal_phase = 0.

    def show_rotation_counter_vector(self):
        self.rotation_counter_vector.set_scale(1)

    def hide_rotation_counter_vector(self):
        self.rotation_counter_vector.set_scale(0)

    def get_rotation_vector(self):
        vector = self.rotation_vector_phase.get_vector()
        return vector

    def get_internal_phase(self):
        return self.internal_phase

    def set_phase_step(self, angle):
        self.phase_step = angle


class Scatter3D:
    def __init__(self, ax, size_scat, cmap_scat, norm_vmin, norm_vmax):
        self.ax = ax
        self.size_scat = size_scat
        self.cmap_scat = cmap_scat
        self.norm = Normalize(vmin=norm_vmin, vmax=norm_vmax)

        self.points = [(0, 0, 0)]   # Dummy
        self.magnitude = [0]

        xs, ys, zs = zip(*self.points)
        self.scat_data = ax0.scatter(xs, ys, zs, c=self.magnitude, cmap=self.cmap_scat, s=self.size_scat, norm=self.norm)

    def append(self, x, y, z, value):
        self.points.append((x, y, z))
        self.magnitude.append(value)

        xs, ys, zs = zip(*self.points[1:])
        self.scat_data.remove()
        self.scat_data = ax0.scatter(xs, ys, zs, c=self.magnitude[1:], cmap=self.cmap_scat, s=self.size_scat, norm=self.norm)

    def clear_scatter(self):
        self.points = [(0, 0, 0)]  # Dummy
        self.magnitude = [0]

        xs, ys, zs = zip(*self.points)
        self.scat_data.remove()
        self.scat_data = ax0.scatter(xs, ys, zs, c=self.magnitude, cmap=self.cmap_scat, s=self.size_scat, norm=self.norm)

    def set_cmap(self, value):
        self.cmap_scat = value

    def set_size(self, value):
        self.size_scat = value


def tilt_vector(value):
    reset()
    internal_phase.tilt(np.deg2rad(value))


def set_phase_step_deg(value):
    global phase_step_deg
    phase_step_deg = value
    internal_phase.set_phase_step(np.deg2rad(phase_step_deg))


def set_is_precession(value):
    global is_precession
    is_precession = value


def set_frequency(value):
    global frequency
    frequency = value


def set_cmap(value):
    if value == 1:
        scatter_internal_phase.set_cmap("bwr")
    elif value == 2:
        scatter_internal_phase.set_cmap("plasma")
    elif value == 3:
        scatter_internal_phase.set_cmap("Reds")
    elif value == 4:
        scatter_internal_phase.set_cmap("spring")
    elif value == 5:
        scatter_internal_phase.set_cmap("hsv")


def set_size(value):
    global size_scatter
    size_scatter = value
    scatter_internal_phase.set_size(size_scatter)


def create_parameter_setter():
    frm_tilt = ttk.Labelframe(root, relief="ridge", text="Tilt (degree)", labelanchor="n")
    frm_tilt.pack(side="left", fill=tk.Y)

    # var_tilt_deg = tk.StringVar(root)
    var_tilt_deg.set(str(tilt_deg))
    spn_tilt = tk.Spinbox(
        frm_tilt, textvariable=var_tilt_deg, format="%.0f", from_=-360, to=360, increment=1,
        command=lambda: tilt_vector(float(var_tilt_deg.get())), width=5
    )
    spn_tilt.pack(side="left")

    # Phase per step
    frm_phase_step = ttk.Labelframe(root, relief="ridge", text="Phase(deg) per step", labelanchor='n')
    frm_phase_step.pack(side="left", fill=tk.Y)

    # var_phase_stp = tk.StringVar(root)
    var_phase_stp.set(str(phase_step_deg))
    spn_stp_angle = tk.Spinbox(
        frm_phase_step, textvariable=var_phase_stp, format="%.0f", from_=-360, to=360, increment=1,
        command=lambda: set_phase_step_deg(float(var_phase_stp.get())), width=5
    )
    spn_stp_angle.pack(side="left")

    # Precession on/off
    frm_precession = ttk.Labelframe(root, relief="ridge", text="Precession", labelanchor='n')
    frm_precession .pack(side="left", fill=tk.Y)
    var_chk_precession = tk.BooleanVar(root)
    chk_precession = tk.Checkbutton(frm_precession, text="On", variable=var_chk_precession,
                                    command=lambda: set_is_precession(var_chk_precession.get()))
    chk_precession.pack(anchor=tk.W)
    var_chk_precession.set(False)

    # Frequency
    frm_freq = ttk.Labelframe(root, relief="ridge", text="Frequency", labelanchor='n')
    frm_freq.pack(side="left", fill=tk.Y)

    # var_freq = tk.StringVar(root)
    var_freq.set(str(frequency))
    spn_freq = tk.Spinbox(
        frm_freq, textvariable=var_freq, format="%.0f", from_=-20, to=20, increment=1,
        command=lambda: set_frequency(float(var_freq.get())), width=5
    )
    spn_freq.pack(side="left")

    # Color map
    frm_cmap = ttk.Labelframe(root, relief="ridge", text="Phase color map", labelanchor='n')
    frm_cmap.pack(side="left", fill=tk.Y)
    # var_cmap = tk.IntVar()
    rd_op_cmap1 = tk.Radiobutton(frm_cmap, text="bwr", value=1, variable=var_cmap,
                                 command=lambda: set_cmap(1))
    rd_op_cmap1.pack(side="left")

    rd_op_cmap2 = tk.Radiobutton(frm_cmap, text="plasma", value=2, variable=var_cmap,
                                 command=lambda: set_cmap(2))
    rd_op_cmap2.pack(side="left")
    rd_op_cmap3 = tk.Radiobutton(frm_cmap, text="Reds", value=3, variable=var_cmap,
                                 command=lambda: set_cmap(3))
    rd_op_cmap3.pack(side="left")
    rd_op_cmap4 = tk.Radiobutton(frm_cmap, text="spring", value=4, variable=var_cmap,
                                 command=lambda: set_cmap(4))
    rd_op_cmap4.pack(side="left")
    rd_op_cmap5 = tk.Radiobutton(frm_cmap, text="hsv", value=5, variable=var_cmap,
                                 command=lambda: set_cmap(5))
    rd_op_cmap5.pack(side="left")

    var_cmap.set(1)

    # Size of scatter
    frm_size = ttk.Labelframe(root, relief="ridge", text="Scatter size", labelanchor='n')
    frm_size.pack(side="left", fill=tk.Y)

    # var_size = tk.StringVar(root)
    var_size.set(str(size_scatter))
    spn_size = tk.Spinbox(
        frm_size, textvariable=var_size, format="%.0f", from_=0, to=20, increment=1,
        command=lambda: set_size(float(var_size.get())), width=5
    )
    spn_size.pack(side="left")


def create_animation_control():
    frm_anim = ttk.Labelframe(root, relief="ridge", text="Animation", labelanchor="n")
    frm_anim.pack(side="left", fill=tk.Y)
    btn_play = tk.Button(frm_anim, text="Play/Pause", command=switch)
    btn_play.pack(side="left")
    btn_reset = tk.Button(frm_anim, text="Reset", command=reset)
    btn_reset.pack(side="left")
    btn_clear = tk.Button(frm_anim, text="Clear path", command=lambda: scatter_internal_phase.clear_scatter())
    btn_clear.pack(side="left")


def create_center_lines():
    ln_axis_x = art3d.Line3D([x_min, x_max], [0., 0.], [0., 0.], color="gray", ls="-.", linewidth=1)
    ax0.add_line(ln_axis_x)
    ln_axis_y = art3d.Line3D([0., 0.], [y_min, y_max], [0., 0.], color="gray", ls="-.", linewidth=1)
    ax0.add_line(ln_axis_y)
    ln_axis_z = art3d.Line3D([0., 0.], [0., 0.], [z_min, z_max], color="blue", ls="-.", linewidth=1)
    ax0.add_line(ln_axis_z)


def create_circle(ax, x, y, z, z_dir, edge_col, fill_flag, line_width, line_style, label):
    if label != "":
        c_spin_axis_guide = Circle((x, y), 1., ec=edge_col, fill=fill_flag,
                                   linewidth=line_width, linestyle=line_style, label=label)
    else:
        c_spin_axis_guide = Circle((x, y), 1., ec=edge_col, fill=fill_flag,
                                   linewidth=line_width, linestyle=line_style)
    ax.add_patch(c_spin_axis_guide)
    art3d.pathpatch_2d_to_3d(c_spin_axis_guide, z=z, zdir=z_dir)


def draw_static_diagrams():
    create_center_lines()


def update_diagrams():
    internal_phase.rotate_phase()
    if is_precession:
        internal_phase.rotate_r()

    magnitude_phase = (np.cos(frequency * internal_phase.get_internal_phase()) + 1) / 2.
    vector = internal_phase.get_rotation_vector()
    scatter_internal_phase.append(vector[0], vector[1], vector[2], magnitude_phase)


def reset():
    global is_play
    cnt.reset()
    if is_play:
        is_play = not is_play
    internal_phase.reset()


def switch():
    global is_play
    is_play = not is_play


def update(f):
    if is_play:
        cnt.count_up()
        update_diagrams()


""" main loop """
if __name__ == "__main__":
    cnt = Counter(ax=ax0, is3d=True, xy=np.array([x_min, y_max]), z=z_max, label="Step=")
    draw_static_diagrams()
    create_animation_control()
    create_parameter_setter()

    internal_phase = InternalPhase(ax0, np.deg2rad(phase_step_deg))

    scatter_internal_phase = Scatter3D(ax0, 6, "bwr", 0, 1)

    dummy1, = ax0.plot(np.array([0, 0]), np.array([0, 0]), np.array([0, 0]),
                       color="red", linewidth=2, linestyle="-", label="Rotation vector")
    dummy2, = ax0.plot(np.array([0, 0]), np.array([0, 0]), np.array([0, 0]),
                       color="gray", linewidth=2, linestyle="-", label="Counter rotation vector")
    dummy3, = ax0.plot(np.array([0, 0]), np.array([0, 0]), np.array([0, 0]),
                       color="black", linewidth=1, linestyle="-.", label="Resultant rotation vector (precession speed)")
    dummy4, = ax0.plot(np.array([0, 0]), np.array([0, 0]), np.array([0, 0]),
                       color="darkorange", linewidth=2, linestyle="--", label="Phase")

    ax0.legend(loc='lower right', fontsize=8)

    anim = animation.FuncAnimation(fig, update, interval=100, save_count=100)
    root.mainloop()