#version 330
in layout(location = 0) vec3 position;
in layout(location = 1) vec2 textureCoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

out vec2 newTexture;

void main()
{
    gl_Position = proj * view * model * vec4(position, 1.0f);
    newTexture = vec2(textureCoords.x, 1 - textureCoords.y);
}