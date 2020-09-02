import qi
import vision_definitions

import cv2
import numpy as np

def al_image_2_cv_mat(al_image):
    '''
        Convert from alImage to cvMat
        '''
    img_width = al_image[0]
    img_height = al_image[1]
    img_channels = al_image[2]
    np_img = np.reshape(al_image[6], (img_height, img_width, img_channels))
    np_img = np_img[..., ::-1]
    return np_img

class RobotSource(object):

    ## \details Function to start capturing both topImage and botImage from the robot. Should be called only once.
    #  \brief Function to start capturing both topImage and botImage from the robot.
    #  \param robot_ip String: robot address in the form of "xxx.xxx.xxx.xxx", such as "192.168.0.40".
    #  \param robot_port String: robot port in the form of "xxxxx", such as "9559".
    # \return Returns, in order, the qi session, the ALVideoDevice service, the top image client and the bottom image client.
    def __init__(self, robot_ip, robot_port):
        robot_ip = robot_ip.replace("robot-", "")
        self.robot_ip = robot_ip
        self.robot_port = robot_port
        self.isSubscribed = False

        self.session = qi.Session()
        self.session.connect("tcp://" + robot_ip + ":" + str(robot_port))

        # initialize a capture
        self.video_service = self.session.service("ALVideoDevice")
        self.resolution = vision_definitions.kVGA
        self.color_space = 12
        self.fps = 30
        self.exposure = 4000
        self.video_service.setParameter(0, vision_definitions.kCameraAutoExpositionID, 0)
        self.video_service.setParameter(1, vision_definitions.kCameraAutoExpositionID, 0)
        self.video_service.setParameter(0, vision_definitions.kCameraExposureID, self.exposure)
        self.video_service.setParameter(1, vision_definitions.kCameraExposureID, self.exposure)


    def subscribe_cameras(self):
        current_subscribers = self.video_service.getSubscribers()
        for subscriber in current_subscribers:
            if(subscriber.startswith(self.robot_ip + "_top_client") or subscriber.startswith(self.robot_ip + "_bottom_client")):
                self.video_service.unsubscribe(subscriber)
        self.top_img_client = self.video_service.subscribeCamera(
            self.robot_ip + "_top_client", 0, self.resolution,
            self.color_space, self.fps)
        self.bottom_img_client = self.video_service.subscribeCamera(
            self.robot_ip + "_bottom_client", 1, self.resolution,
            self.color_space, self.fps)
        self.isSubscribed = True

    def unsubscribe_cameras(self):
        self.video_service.unsubscribe(self.top_img_client)
        self.video_service.unsubscribe(self.bottom_img_client)
        self.isSubscribed = False

    #get a new image from top camera
    def get_top_image(self):
        al_image = self.video_service.getImageRemote(self.top_img_client)
        return al_image_2_cv_mat(al_image)

    #get a new image from bottom camera
    def get_bottom_image(self):
        al_image = self.video_service.getImageRemote(self.bottom_img_client)
        return al_image_2_cv_mat(al_image)

if __name__ == "__main__":
    source = RobotSource("192.168.0.40", 9559)
    source.subscribe_cameras()
    cv2.namedWindow("h")
    cv2.namedWindow("s")
    cv2.namedWindow("y")
    while 1:
        cv2.imshow("y", source.get_top_image()[:,:, 0])
        cv2.imshow("s", source.get_top_image()[:,:, 1])
        cv2.imshow("h", source.get_top_image()[:,:, 2])
        cv2.waitKey(1)
    
    cv2.destroyAllWindows()