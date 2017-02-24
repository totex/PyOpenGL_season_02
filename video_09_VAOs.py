import glfw
from OpenGL.GL import *
from pyrr import matrix44, Vector3
from ObjLoader import *
import TextureLoader
import ShaderLoader
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
    cube_shader = ShaderLoader.compile_shader("shaders/video_09_cube.vs", "shaders/video_09_cube.fs")
    cube_tex = TextureLoader.load_texture("res/cube/cube_texture.jpg")
    cube_texture_offset = len(cube.vertex_index) * 12

    monkey = ObjLoader()
    monkey.load_model("res/monkey/monkey.obj")
    monkey_shader = ShaderLoader.compile_shader("shaders/video_09_monkey.vs", "shaders/video_09_monkey.fs")
    monkey_tex = TextureLoader.load_texture("res/monkey/monkey.jpg")
    monkey_texture_offset = len(monkey.vertex_index) * 12

    monster = ObjLoader()
    monster.load_model("res/monster/monster.obj")
    monster_shader = ShaderLoader.compile_shader("shaders/video_09_monster.vs", "shaders/video_09_monster.fs")
    monster_tex = TextureLoader.load_texture("res/monster/monster.jpg")
    monster_texture_offset = len(monster.vertex_index) * 12

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

    glUseProgram(cube_shader)
    cube_model_loc = glGetUniformLocation(cube_shader, "model")
    cube_view_loc = glGetUniformLocation(cube_shader, "view")
    cube_proj_loc = glGetUniformLocation(cube_shader, "proj")
    glUniformMatrix4fv(cube_model_loc, 1, GL_FALSE, cube_model)
    glUniformMatrix4fv(cube_proj_loc, 1, GL_FALSE, projection)
    glUseProgram(0)

    glUseProgram(monkey_shader)
    monkey_model_loc = glGetUniformLocation(monkey_shader, "model")
    monkey_view_loc = glGetUniformLocation(monkey_shader, "view")
    monkey_proj_loc = glGetUniformLocation(monkey_shader, "proj")
    glUniformMatrix4fv(monkey_model_loc, 1, GL_FALSE, monkey_model)
    glUniformMatrix4fv(monkey_proj_loc, 1, GL_FALSE, projection)
    glUseProgram(0)

    glUseProgram(monster_shader)
    monster_model_loc = glGetUniformLocation(monster_shader, "model")
    monster_view_loc = glGetUniformLocation(monster_shader, "view")
    monster_proj_loc = glGetUniformLocation(monster_shader, "proj")
    glUniformMatrix4fv(monster_model_loc, 1, GL_FALSE, monster_model)
    glUniformMatrix4fv(monster_proj_loc, 1, GL_FALSE, projection)
    glUseProgram(0)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        do_movement()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = cam.get_view_matrix()

        glBindVertexArray(cube_vao)
        glUseProgram(cube_shader)
        glBindTexture(GL_TEXTURE_2D, cube_tex)
        glUniformMatrix4fv(cube_view_loc, 1, GL_FALSE, view)
        glDrawArrays(GL_TRIANGLES, 0, len(cube.vertex_index))
        glUseProgram(0)
        glBindVertexArray(0)

        glBindVertexArray(monkey_vao)
        glBindTexture(GL_TEXTURE_2D, monkey_tex)
        glUseProgram(monkey_shader)
        glUniformMatrix4fv(monkey_view_loc, 1, GL_FALSE, view)
        glDrawArrays(GL_TRIANGLES, 0, len(monkey.vertex_index))
        glUseProgram(0)
        glBindVertexArray(0)

        glBindVertexArray(monster_vao)
        glBindTexture(GL_TEXTURE_2D, monster_tex)
        glUseProgram(monster_shader)
        glUniformMatrix4fv(monster_view_loc, 1, GL_FALSE, view)
        glDrawArrays(GL_TRIANGLES, 0, len(monster.vertex_index))
        glUseProgram(0)
        glBindVertexArray(0)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()