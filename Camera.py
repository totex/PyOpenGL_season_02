import pyrr

class Camera:

    def look_at(self, position, target, world_up):
        # 1.Position = known
        # 2.Calculate cameraDirection
        zaxis = pyrr.vector.normalise(position - target)
        # 3.Get positive right axis vector
        xaxis = pyrr.vector.normalise(pyrr.vector3.cross(pyrr.vector.normalise(world_up), zaxis))
        # 4.Caculate the camera up vector
        yaxis = pyrr.vector3.cross(zaxis, xaxis)

        # create translation and rotation matrix
        translation = pyrr.Matrix44.identity()
        translation[3][0] = -position.x
        translation[3][1] = -position.y
        translation[3][2] = -position.z
        #print(translation.T)
        rotation = pyrr.Matrix44.identity()
        rotation[0][0] = xaxis[0]
        rotation[1][0] = xaxis[1]
        rotation[2][0] = xaxis[2]
        rotation[0][1] = yaxis[0]
        rotation[1][1] = yaxis[1]
        rotation[2][1] = yaxis[2]
        rotation[0][2] = zaxis[0]
        rotation[1][2] = zaxis[1]
        rotation[2][2] = zaxis[2]
        #print(rotation)
        return translation * rotation

#cam = Camera()
#cam.look_at(pyrr.Vector3([2.0, 5.0, -2.0]), pyrr.Vector3([0.0, 0.0, 0.0]), pyrr.Vector3([0.0, 1.0, 0.0]))

