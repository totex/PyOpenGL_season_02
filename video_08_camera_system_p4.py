import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
from pyrr import matrix44, Vector3
import TextureLoader
from Camera import Camera


def window_resize(window, width, height):
    glViewport(0, 0, width, height)

cam = Camera()
keys = [False] * 1024
lastX, lastY = 960, 540
first_mouse = True


def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key >= 0 and key < 1024:
        if action == glfw.PRESS:
            keys[key] = True
        elif action == glfw.RELEASE:
            keys[key] = False


def do_movement():
    if keys[glfw.KEY_W]:
        cam.process_keyboard("FORWARD", 0.05)
    if keys[glfw.KEY_S]:
        cam.process_keyboard("BACKWARD", 0.05)
    if keys[glfw.KEY_A]:
        cam.process_keyboard("LEFT", 0.05)
    if keys[glfw.KEY_D]:
        cam.process_keyboard("RIGHT", 0.05)


def mouse_callback(window, xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)


def main():
    # initialize glfw
    if not glfw.init():
        return

    w_width, w_height = 1920, 1080
    aspect_ratio = w_width / w_height

    window = glfw.create_window(w_width, w_height, "My OpenGL window", None, None)
    #window = glfw.create_window(w_width, w_height, "My OpenGL window", glfw.get_primary_monitor(), None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    #        positions        texture_coords
    cube = [-0.5, -0.5, 0.5, 0.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            -0.5, 0.5, -0.5, 0.0, 1.0,

            0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, -0.5, 0.5, 0.0, 1.0,

            -0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 1.0, 0.0,
            -0.5, -0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 1.0,

            0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, 0.5, -0.5, 1.0, 0.0,
            -0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 0.0, 1.0]

    cube = numpy.array(cube, dtype=numpy.float32)

    indices = [0, 1, 2, 2, 3, 0,
               4, 5, 6, 6, 7, 4,
               8, 9, 10, 10, 11, 8,
               12, 13, 14, 14, 15, 12,
               16, 17, 18, 18, 19, 16,
               20, 21, 22, 22, 23, 20]

    indices = numpy.array(indices, dtype=numpy.uint32)

    vertex_shader = """
    #version 330
    in layout(location = 0) vec3 position;
    in layout(location = 1) vec2 texture_cords;
    in layout(location = 2) vec3 offset;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 proj;

    out vec2 textures;

    void main()
    {
        vec3 final_pos = vec3(position.x + offset.x, position.y + offset.y, position.z + offset.z);
        gl_Position =  proj * view * model * vec4(final_pos, 1.0f);
        textures = texture_cords;
    }
    """

    fragment_shader = """
    #version 330
    in vec2 textures;

    out vec4 color;
    uniform sampler2D tex_sampler;

    void main()
    {
        color = texture(tex_sampler, textures);
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

    # position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube.itemsize * 5, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # textures
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube.itemsize * 5, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    # instances
    instance_array = []
    offset = 1

    for z in range(0, 100, 2):
        for y in range(0, 100, 2):
            for x in range(0, 100, 2):
                translation = Vector3([0.0, 0.0, 0.0])
                translation.x = x + offset
                translation.y = y + offset
                translation.z = z + offset
                instance_array.append(translation)

    instance_array = numpy.array(instance_array, numpy.float32).flatten()

    instanceVBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, instanceVBO)
    glBufferData(GL_ARRAY_BUFFER, instance_array.itemsize * len(instance_array), instance_array, GL_STATIC_DRAW)

    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(2)
    glVertexAttribDivisor(2, 1)

    crate = TextureLoader.load_texture("res/crate.jpg")

    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)

    model = matrix44.create_from_translation(Vector3([-14.0, -8.0, 0.0]))
    projection = matrix44.create_perspective_projection_matrix(45.0, aspect_ratio, 0.1, 100.0)

    model_loc = glGetUniformLocation(shader, "model")
    view_loc = glGetUniformLocation(shader, "view")
    proj_loc = glGetUniformLocation(shader, "proj")

    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        do_movement()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        glDrawElementsInstanced(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None, 125000)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()