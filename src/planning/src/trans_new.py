import numpy as np
import cv2
import matplotlib.pyplot as plt


class calibration():
    def __init__(self, img, table_size):
        self.img = img
        self.transform_matrix = None
        self.table_size = table_size
        self.M = None
        self.scale = 1
        # self.clicked = None

    def get_transform_matrix(self, objpoints, imgpoints):
        print([objpoints])
        ret, camera_matrix, dist, rvecs, tvecs = cv2.calibrateCamera([objpoints], [imgpoints], (self.img.shape[0],self.img.shape[1]), None, None)
        camera_matrix, rvecs, tvecs = np.array(camera_matrix), np.array(rvecs).reshape((3,1)), np.array(tvecs).T.reshape((3,1))
        # print('r: ', rvecs)
        # print('t: ', tvecs)
        rot = cv2.Rodrigues(rvecs)[0]
        print('rot:', rot)
        rot_trans_matrix = np.concatenate((rot, tvecs), axis=1)
        # print(rot_trans_matrix.shape)
        self.transform_matrix = np.matmul(camera_matrix, rot_trans_matrix)
        print('total transform matrix:',self.transform_matrix)
        calculated_first = np.matmul(self.transform_matrix, np.concatenate((objpoints[0], np.array([1]))))
        print('first scale', calculated_first[-1])
        print('get first imgpoints:', calculated_first / calculated_first[-1])
        print('true first imgpoints:', imgpoints[0])

        calculated_second = np.matmul(self.transform_matrix, np.concatenate((objpoints[1], np.array([1]))))
        print('second scale', calculated_second[-1])
        print('get second imgpoints:', calculated_second / calculated_second[-1])
        print('true second imgpoints:', imgpoints[1])

        calculated_third = np.matmul(self.transform_matrix, np.concatenate((objpoints[2], np.array([1]))))
        print('third scale', calculated_third[-1])
        print('get third imgpoints:', calculated_third / calculated_third[-1])
        print('true third imgpoints:', imgpoints[2])

        calculated_fourth = np.matmul(self.transform_matrix, np.concatenate((objpoints[3], np.array([1]))))
        print('fourth scale', calculated_fourth[-1])
        print('get fourth imgpoints:', calculated_fourth / calculated_fourth[-1])
        print('true fourth imgpoints:', imgpoints[3])

        self.scale = (calculated_first[-1] + calculated_second[-1] + calculated_third[-1] + calculated_fourth[-1]) / 4

    def calibrate(self):
        plt.figure()
        plt.imshow(self.img)

        # clicked = plt.ginput(4, timeout=0, show_clicks=True)
        # clicked = [tuple([round(x) for x in tup]) for tup in clicked]
        # print(clicked)
        clicked = [(377.0, 355.0), (796.0, 369.0), (907.0, 553.0), (342.0, 555.0)]
        # clicked = [(415.0, 482.0), (632.0, 472.0), (808.0, 463.0), (850.0, 547.0), (902.0, 639.0), (671.0, 655.0), (374.0, 675.0), (395.0, 562.0)]
        # objpoints = np.zeros((4,1,3))
        
        src = np.float32([clicked[0],
                  clicked[1],
                  clicked[2],
                  clicked[3]])


        dst = np.float32([(0, 0),
                          (self.table_size[1], 0),
                          (self.table_size[1], self.table_size[0]),
                          (0, self.table_size[0])])
        transformed = self.warp(src, dst, self.img)
        cv2.imwrite('result.jpg', transformed)

        std_clicked = []
        for click in clicked:
            cur_click = self.M.dot([[click[0]], [click[1]], [1]])
            cur_click = (cur_click / cur_click[-1])[:2]
            print('lolllll', cur_click, cur_click.shape, cur_click[0,0], cur_click[0][0])
            cur_y = cur_click[0][0]
            cur_x = cur_click[1][0]
            if cur_x > 344:
                cur_x = 344
            if cur_x < 0:
                cur_x = 0
            if cur_y > 499:
                cur_y = 499
            if cur_y < 0:
                cur_y = 0
            std_clicked.append([cur_y,cur_x])
        # std_clicked = clicked

        # objpoints = np.float32([[0.554,-0.240,0],
        #                     [0.549,0.319,0],
        #                     [0.944,0.316,0],
        #                     [0.952,-0.235,0]]) #alan

        objpoints = np.float32([[0.465,-0.262,0],
                            [0.486,0.279,0],
                            [0.863,0.259,0],
                            [0.842,-0.300,0]])

        imgpoints = np.float32([[std_clicked[0][0],std_clicked[0][1]],
                            [std_clicked[1][0],std_clicked[1][1]],
                            [std_clicked[2][0],std_clicked[2][1]],
                            [std_clicked[3][0],std_clicked[3][1]]])

        print('std clicked:',std_clicked)

        self.get_transform_matrix(objpoints, imgpoints)



        return transformed

    def warp(self, src, dst, img):
        h, w = img.shape[:2]
        M = cv2.getPerspectiveTransform(src, dst)
        self.M = M
        print('matrix', M)
        warped = cv2.warpPerspective(img, M, (self.table_size[1], self.table_size[0]))
        return warped

    def transform_to_3d(self, pt):
        # swap x, y
        pt[0], pt[1] = pt[1], pt[0]
        # pt = np.concatenate((pt.T.reshape((2,1)), np.array([[1]])), axis=0)
        # inv_M = np.linalg.inv(self.M)
        # gen_pt = inv_M.dot(pt)
        gen_pt = pt
        # gen_pt = (gen_pt / gen_pt[-1])[:2]

        A = np.array([[self.transform_matrix[0][0], self.transform_matrix[0][1], -gen_pt[0]],[self.transform_matrix[1][0], self.transform_matrix[1][1], -gen_pt[1]], [self.transform_matrix[2][0], self.transform_matrix[2][1], -1]])
        
        # A = np.array([[self.transform_matrix[0][0], self.transform_matrix[0][1]],[self.transform_matrix[1][0], self.transform_matrix[1][1]]])
        inv_A = np.linalg.inv(A)
        b = np.array([[-self.transform_matrix[0][3]], [-self.transform_matrix[1][3]], [-self.transform_matrix[2][3]]])

        world_pos = inv_A.dot(b)
        world_pos = world_pos[:2]
        # print('pt: ', pt, 'gen_pt is: ', gen_pt, 'world_pos is: ', world_pos)
        return world_pos
        


if __name__ == '__main__':
    im = cv2.imread("test.jpg")
    # plt.figure()
    # plt.imshow(im)
    # clicked = plt.ginput(1, timeout=0, show_clicks=True)


    cali = calibration(im, (345, 500))
    cali.calibrate()
    print('get point:',cali.transform_to_3d(np.array([344, 499])))