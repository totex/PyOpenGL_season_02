import glfw
from OpenGL.GL import *
from pyrr import matrix44, Vector3, Matrix44
import ShaderLoader
import TextureLoader
from ObjLoader import *
from Camera import Camera


def window_resize(window, width, height):
    glViewport(0, 0, width, height)

cam = Camera()
keys = [False] * 1024
w_width, w_height = 1920, 1080
lastX, lastY = w_width / 2, w_height / 2
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

    aspect_ratio = w_width / w_height

    window = glfw.create_window(w_width, w_height, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    cube = ObjLoader()
    cube.load_model("res/cube/cube.obj")
    cube_tex = TextureLoader.load_texture("res/cube/cube_texture.jpg")
    cube_texture_offset = len(cube.vertex_index) * 12

    monkey = ObjLoader()
    monkey.load_model("res/monkey/monkey.obj")
    monkey_tex = TextureLoader.load_texture("res/monkey/monkey.jpg")
    monkey_texture_offset = len(monkey.vertex_index) * 12

    monster = ObjLoader()
    monster.load_model("res/monster/monster.obj")
    monster_tex = TextureLoader.load_texture("res/monster/monster.jpg")
    monster_texture_offset = len(monster.vertex_index) * 12

    generic_shader = ShaderLoader.compile_shader("shaders/generic_vertex_shader.vs", "shaders/generic_fragment_shader.fs")

    cube_vao = glGenVertexArrays(1)
    glBindVertexArray(cube_vao)
    cube_vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, cube_vbo)
    glBufferData(GL_ARRAY_BUFFER, cube.model.itemsize * len(cube.model), cube.model, GL_STATIC_DRAW)
    #position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    #textures
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube.model.itemsize * 2, ctypes.c_void_p(cube_texture_offset))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)

    monkey_vao = glGenVertexArrays(1)
    glBindVertexArray(monkey_vao)
    monkey_vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, monkey_vbo)
    glBufferData(GL_ARRAY_BUFFER, monkey.model.itemsize * len(monkey.model), monkey.model, GL_STATIC_DRAW)
    #position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, monkey.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    #textures
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, monkey.model.itemsize * 2, ctypes.c_void_p(monkey_texture_offset))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)

    monster_vao = glGenVertexArrays(1)
    glBindVertexArray(monster_vao)
    monster_vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, monster_vbo)
    glBufferData(GL_ARRAY_BUFFER, monster.model.itemsize * len(monster.model), monster.model, GL_STATIC_DRAW)
    #position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, monster.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    #textures
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, monster.model.itemsize * 2, ctypes.c_void_p(monster_texture_offset))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)

    glClearColor(0.13, 0.2, 0.15, 1.0)
    glEnable(GL_DEPTH_TEST)

    projection = matrix44.create_perspective_projection_matrix(45.0, aspect_ratio, 0.1, 100.0)
    cube_model = matrix44.create_from_translation(Vector3([-4.0, 0.0, -3.0]))
    monkey_model = matrix44.create_from_translation(Vector3([0.0, 0.0, -3.0]))
    monster_model = matrix44.create_from_translation(Vector3([0.0, 0.0, -10.0]))

    glUseProgram(generic_shader)
    model_loc = glGetUniformLocation(generic_shader, "model")
    view_loc = glGetUniformLocation(generic_shader, "view")
    proj_loc = glGetUniformLocation(generic_shader, "proj")

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        do_movement()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        rot_y = Matrix44.from_y_rotation(glfw.get_time() * 0.5)

        glBindVertexArray(cube_vao)
        glBindTexture(GL_TEXTURE_2D, cube_tex)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, rot_y * cube_model)
        glDrawArrays(GL_TRIANGLES, 0, len(cube.vertex_index))
        glBindVertexArray(0)

        glBindVertexArray(monkey_vao)
        glBindTexture(GL_TEXTURE_2D, monkey_tex)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, monkey_model)
        glDrawArrays(GL_TRIANGLES, 0, len(monkey.vertex_index))
        glBindVertexArray(0)

        glBindVertexArray(monster_vao)
        glBindTexture(GL_TEXTURE_2D, monster_tex)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, monster_model)
        glDrawArrays(GL_TRIANGLES, 0, len(monster.vertex_index))
        glBindVertexArray(0)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()