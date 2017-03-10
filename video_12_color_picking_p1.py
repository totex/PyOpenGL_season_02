import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
from pyrr import matrix44, Vector3, Matrix44


def window_resize(window, width, height):
    glViewport(0, 0, width, height)

mouse_x, mouse_y = 0, 0
red_rot = False
green_rot = False
blue_rot = False


def cursor_pos_callback(window, xpos, ypos):
    global mouse_x, mouse_y
    mouse_x = xpos
    mouse_y = ypos


def mouse_button_callback(window, button, action, mods):
    global red_rot, green_rot, blue_rot

    data = glReadPixels(mouse_x, mouse_y, 1, 1, GL_RGB, GL_FLOAT)

    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        if data[0][0][0] == 1.0:
            print('red')
            red_rot = not red_rot
        elif data[0][0][1] == 1.0:
            print('green')
            green_rot = not green_rot
        elif data[0][0][2] == 1.0:
            print('blue')
            blue_rot = not blue_rot
        else:
            print('background')


def main():

    # initialize glfw
    if not glfw.init():
        return

    w_width, w_height = 1280, 720
    aspect_ratio = w_width / w_height

    window = glfw.create_window(w_width, w_height, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    #        positions
    cube = [-0.5, -0.5,  0.5,
             0.5, -0.5,  0.5,
             0.5,  0.5,  0.5,
            -0.5,  0.5,  0.5,

            -0.5, -0.5, -0.5,
             0.5, -0.5, -0.5,
             0.5,  0.5, -0.5,
            -0.5,  0.5, -0.5,

             0.5, -0.5, -0.5,
             0.5,  0.5, -0.5,
             0.5,  0.5,  0.5,
             0.5, -0.5,  0.5,

            -0.5,  0.5, -0.5,
            -0.5, -0.5, -0.5,
            -0.5, -0.5,  0.5,
            -0.5,  0.5,  0.5,

            -0.5, -0.5, -0.5,
             0.5, -0.5, -0.5,
             0.5, -0.5,  0.5,
            -0.5, -0.5,  0.5,

             0.5,  0.5, -0.5,
            -0.5,  0.5, -0.5,
            -0.5,  0.5,  0.5,
             0.5,  0.5,  0.5]

    cube = numpy.array(cube, dtype=numpy.float32)

    indices = [ 0,  1,  2,  2,  3,  0,
                4,  5,  6,  6,  7,  4,
                8,  9, 10, 10, 11,  8,
               12, 13, 14, 14, 15, 12,
               16, 17, 18, 18, 19, 16,
               20, 21, 22, 22, 23, 20]

    indices = numpy.array(indices, dtype=numpy.uint32)

    vertex_shader = """
    #version 330
    in layout(location = 0) vec3 position;

    uniform mat4 vp;
    uniform mat4 model;

    void main()
    {
        gl_Position =  vp * model * vec4(position, 1.0f);
    }
    """

    fragment_shader = """
    #version 330

    out vec4 outColor;
    uniform vec3 color;

    void main()
    {
        outColor = vec4(color, 1.0);
    }
    """
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, cube.itemsize * len(cube), cube, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)

    #position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)

    view = matrix44.create_from_translation(Vector3([0.0, 0.0, -4.0]))
    projection = matrix44.create_perspective_projection_matrix(45.0, aspect_ratio, 0.1, 100.0)

    vp = matrix44.multiply(view, projection)

    vp_loc = glGetUniformLocation(shader, "vp")
    model_loc = glGetUniformLocation(shader, "model")

    color_loc = glGetUniformLocation(shader, "color")

    cube_positions = [(-2.0, 0.0, 0.0), (0.0, 0.0, 0.0), (2.0, 0.0, 0.0)]
    cube_colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]

    glUniformMatrix4fv(vp_loc, 1, GL_FALSE, vp)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        rot_y = Matrix44.from_y_rotation(glfw.get_time() * 2)

        for i in range(len(cube_positions)):
            model = matrix44.create_from_translation(cube_positions[i])
            if i == 0:
                glUniform3fv(color_loc, 1, cube_colors[i])
                if red_rot:
                    glUniformMatrix4fv(model_loc, 1, GL_FALSE, rot_y * model)
                else:
                    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            elif i == 1:
                glUniform3fv(color_loc, 1, cube_colors[i])
                if green_rot:
                    glUniformMatrix4fv(model_loc, 1, GL_FALSE, rot_y * model)
                else:
                    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            else:
                glUniform3fv(color_loc, 1, cube_colors[i])
                if blue_rot:
                    glUniformMatrix4fv(model_loc, 1, GL_FALSE, rot_y * model)
                else:
                    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

            glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()