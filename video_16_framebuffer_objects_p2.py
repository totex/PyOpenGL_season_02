import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
import pyrr
from pyrr import matrix44, Vector3
from PIL import Image
from ObjLoader import *

new_width, new_height = 1280, 720


def window_resize(window, width, height):
    global new_width, new_height
    glViewport(0, 0, width, height)
    new_width, new_height = width, height


def main():
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

    cube = [-0.5, -0.5,  0.5, 0.0, 0.0,
             0.5, -0.5,  0.5, 1.0, 0.0,
             0.5,  0.5,  0.5, 1.0, 1.0,
            -0.5,  0.5,  0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
             0.5, -0.5, -0.5, 1.0, 0.0,
             0.5,  0.5, -0.5, 1.0, 1.0,
            -0.5,  0.5, -0.5, 0.0, 1.0,

             0.5, -0.5, -0.5, 0.0, 0.0,
             0.5,  0.5, -0.5, 1.0, 0.0,
             0.5,  0.5,  0.5, 1.0, 1.0,
             0.5, -0.5,  0.5, 0.0, 1.0,

            -0.5,  0.5, -0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 1.0, 0.0,
            -0.5, -0.5,  0.5, 1.0, 1.0,
            -0.5,  0.5,  0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
             0.5, -0.5, -0.5, 1.0, 0.0,
             0.5, -0.5,  0.5, 1.0, 1.0,
            -0.5, -0.5,  0.5, 0.0, 1.0,

             0.5, 0.5, -0.5,  0.0, 0.0,
            -0.5, 0.5, -0.5,  1.0, 0.0,
            -0.5, 0.5,  0.5,  1.0, 1.0,
             0.5, 0.5,  0.5,  0.0, 1.0]

    cube = numpy.array(cube, dtype=numpy.float32)

    cube_indices = [ 0,  1,  2,  2,  3,  0,
                     4,  5,  6,  6,  7,  4,
                     8,  9, 10, 10, 11,  8,
                    12, 13, 14, 14, 15, 12,
                    16, 17, 18, 18, 19, 16,
                    20, 21, 22, 22, 23, 20]

    cube_indices = numpy.array(cube_indices, dtype=numpy.uint32)

    monkey = ObjLoader()
    monkey.load_model("res/monkey/monkey.obj")
    monkey_texture_offset = len(monkey.vertex_index) * 12

    vertex_shader = """
    #version 330
    in layout(location = 0) vec3 position;
    in layout(location = 1) vec2 textCoords;

    uniform mat4 vp;
    uniform mat4 model;

    out vec2 outText;

    void main()
    {
        gl_Position =  vp * model * vec4(position, 1.0f);
        outText = textCoords;
    }
    """

    fragment_shader = """
    #version 330
    in vec2 outText;

    out vec4 outColor;
    uniform sampler2D renderedTexture;

    void main()
    {
        outColor = texture(renderedTexture, outText);
    }
    """

    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # cube VAO
    cube_vao = glGenVertexArrays(1)
    glBindVertexArray(cube_vao)
    cube_VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, cube_VBO)
    glBufferData(GL_ARRAY_BUFFER, cube.itemsize * len(cube), cube, GL_STATIC_DRAW)
    cube_EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cube_EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube_indices.itemsize * len(cube_indices), cube_indices, GL_STATIC_DRAW)
    # position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube.itemsize * 5, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    # textures
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube.itemsize * 5, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)


    # monkey VAO
    monkey_vao = glGenVertexArrays(1)
    glBindVertexArray(monkey_vao)
    monkey_VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, monkey_VBO)
    glBufferData(GL_ARRAY_BUFFER, monkey.model.itemsize * len(monkey.model), monkey.model, GL_STATIC_DRAW)
    # position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, monkey.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    # textures
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, monkey.model.itemsize * 2, ctypes.c_void_p(monkey_texture_offset))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)

    ###########################################################################################

    cube_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, cube_texture)
    # texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w_width, w_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
    glBindTexture(GL_TEXTURE_2D, 0)

    depth_buff = glGenRenderbuffers(1)
    glBindRenderbuffer(GL_RENDERBUFFER, depth_buff)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, w_width, w_height)

    FBO = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, FBO)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, cube_texture, 0)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depth_buff)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

    ###########################################################################################

    monkey_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, monkey_texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image
    image = Image.open("res/monkey/monkey.jpg")
    flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = numpy.array(list(flipped_image.getdata()), numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glBindTexture(GL_TEXTURE_2D, 0)

    ###########################################################################################

    glEnable(GL_DEPTH_TEST)

    view = matrix44.create_from_translation(Vector3([0.0, 0.0, -2.0]))
    projection = matrix44.create_perspective_projection_matrix(45.0, aspect_ratio, 0.1, 100.0)

    cube_position = matrix44.create_from_translation(Vector3([0.0, 0.0, 0.0]))
    monkey_position = matrix44.create_from_translation(Vector3([0.0, 0.0, -1.0]))

    vp = matrix44.multiply(view, projection)

    glUseProgram(shader)
    vp_loc = glGetUniformLocation(shader, "vp")
    model_loc = glGetUniformLocation(shader, "model")
    glUniformMatrix4fv(vp_loc, 1, GL_FALSE, vp)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClearColor(0.2, 0.25, 0.27, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        cube_rot_y = pyrr.Matrix44.from_y_rotation(glfw.get_time() * 0.1)
        cube_rot_x = pyrr.Matrix44.from_x_rotation(glfw.get_time() * 0.1)
        cube_rot_all = pyrr.matrix44.multiply(cube_rot_y, cube_rot_x)

        monkey_rot_y = pyrr.Matrix44.from_y_rotation(glfw.get_time())

        # draw to the custom frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, FBO)
        glViewport(0, 0, w_width, w_height)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBindVertexArray(monkey_vao)
        glBindTexture(GL_TEXTURE_2D, monkey_texture)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, monkey_rot_y * monkey_position)
        glDrawArrays(GL_TRIANGLES, 0, len(monkey.vertex_index))
        glBindVertexArray(0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # draw to the default frame buffer
        glBindVertexArray(cube_vao)
        glViewport(0, 0, new_width, new_height)
        glBindTexture(GL_TEXTURE_2D, cube_texture)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, cube_rot_all * cube_position)
        glDrawElements(GL_TRIANGLES, len(cube_indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
