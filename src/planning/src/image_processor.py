#!/usr/bin/env python
"""Segmentation skeleton code for Lab 6
Course: EECS C106A, Fall 2019
Author: Grant Wang

This Python file is the skeleton code for Lab 3. You are expected to fill in
the body of the incomplete functions below to complete the lab. The 'test_..'
functions are already defined for you for allowing you to check your 
implementations.

When you believe you have completed implementations of all the incompeleted
functions, you can test your code by running python segmentation.py at the
command line and step through test images
"""

import os
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt

from scipy import ndimage
from scipy.misc import imresize
from skimage import filters

from skimage.measure import block_reduce
import time
import pdb
from trans_new import calibration
import copy
from collections import deque

IMG_DIR = os.path.dirname(os.path.abspath(__file__))

fd0 = [(1, 0), (0, 1), (-1, 0), (0, -1)]
fdc = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
fd1 = set([(x, y) for x in range(-5, 6) for y in range(-5, 6) if abs(x) + abs(y) <= 1])
fd2 = set([(x, y) for x in range(-5, 6) for y in range(-5, 6) if abs(x) + abs(y) <= 2])
fd3 = set([(x, y) for x in range(-5, 6) for y in range(-5, 6) if abs(x) + abs(y) <= 3])
fd4 = set([(x, y) for x in range(-5, 6) for y in range(-5, 6) if abs(x) + abs(y) <= 4])
fd5 = set([(x, y) for x in range(-5, 6) for y in range(-5, 6) if abs(x) + abs(y) <= 5])

class imgProcess:
    def __init__(self):
        self.lower_thresh = 0
        self.upper_thresh = 145

    @staticmethod
    def read_image(img_name, grayscale=False):
        """ reads an image

        Parameters
        ----------
        img_name : str
            name of image
        grayscale : boolean
            true if image is in grayscale, false o/w
        
        Returns
        -------
        ndarray
            an array representing the image read (w/ extension)
        """

        if not grayscale:
            img = cv2.imread(img_name)
        else:
            img = cv2.imread(img_name, 0)

        return img

    @staticmethod
    def write_image(img, img_name):
        """writes the image as a file
        
        Parameters
        ----------
        img : ndarray
            an array representing an image
        img_name : str
            name of file to write as (make sure to put extension)
        """

        cv2.imwrite(img_name, img)

    @staticmethod
    def show_image(img_name, title='Fig', grayscale=False, paths=None, force=False):
        """show as a matplotlib figure
        
        Parameters
        ----------
        img_name : str
            name of image
        tile : str
            title to give the figure shown
        grayscale : boolean
            true if image is in grayscale, false o/w
        """
        if not force:
            return
        if paths is not None:
            for path in paths:
                for i in range(len(path) - 1):
                    plt.arrow(path[i][1], path[i][0], path[i+1][1] - path[i][1], path[i+1][0] - path[i][0])
        if not grayscale:
            plt.imshow(img_name)
            plt.title(title)
            plt.show()
        else:
            plt.imshow(img_name, cmap='gray')
            plt.title(title)
            plt.show()

    @staticmethod
    def threshold_segment_naive(gray_img, lower_thresh, upper_thresh):
        """perform grayscale thresholding using a lower and upper threshold by
        blacking the background lying between the threholds and whitening the
        foreground

        Parameter
        ---------
        gray_img : ndarray
            grayscale image array
        lower_thresh : float or int
            lowerbound to threshold (an intensity value between 0-255)
        upper_thresh : float or int
            upperbound to threshold (an intensity value between 0-255)

        Returns
        -------
        ndarray
            thresholded version of gray_img
        """
        # TODO: Implement threshold segmentation by setting pixels of gray_img inside the 
        # lower_thresh and upper_thresh parameters to 0
        # Then set any value that is outside the range to be 1 
        # Hints: make a copy of gray_img so that we don't alter the original image
        # Boolean array indexing, or masking will come in handy. 
        # See https://docs.scipy.org/doc/numpy-1.13.0/user/basics.indexing.html
        [n, m] = gray_img.shape
        newImage = np.zeros((n, m))
        for i in range(n):
            for j in range(m):
                if lower_thresh <= gray_img[i][j] <= upper_thresh:
                    newImage[i][j] = 0  # black
                else:
                    newImage[i][j] = 1  # white
        return newImage

    @staticmethod
    def edge_detect_naive(gray_img):
        """perform edge detection using first two steps of Canny (Gaussian blurring and Sobel
        filtering)

        Parameter
        ---------
        gray_img : ndarray
            grayscale image array

        Returns
        -------
        ndarray
            gray_img with edges outlined
        """

        img = gray_img.astype('int16') # convert to int16 for better img quality 
        # TODO: Blur gray_s using Gaussian blurring, convole the blurred image with
        # Sobel filters, and combine to compute the intensity gradient image (image with edges highlighted)
        # Hints: open-cv GaussianBlur will be helpful https://medium.com/analytics-vidhya/gaussian-blurring-with-python-and-opencv-ba8429eb879b 
        # the scipy.ndimage.filters class (imported already) has a useful convolve function

        # Steps
        # 1. apply a gaussian blur with a 5x5 kernel.
        # 2. define the convolution kernel Kx and Ky as defined in the doc.
        # 3. compute Gx and Gy by convolving Kx and Ky respectively with the blurred image.
        # 4. compute G = sqrt(Gx ** 2 + Gy ** 2)
        # 5. Return G
        
        # if our edge is bold, we need to blur first
        img_blur = img
        # img_blur = cv2.GaussianBlur(img, (31, 31), cv2.BORDER_DEFAULT)  # need to tune here
        
        Kx = np.array([[-1,0,1], [-2,0,2], [-1,0,1]])
        Ky = np.array([[-1,-2,-1], [0,0,0], [1,2,1]])

        Gx = ndimage.convolve(img_blur, Kx, mode='constant', cval=0.0)
        Gy = ndimage.convolve(img_blur, Ky, mode='constant', cval=0.0)

        G = np.sqrt(Gx ** 2 + Gy ** 2)

        return G

    @staticmethod
    def edge_detect_canny(gray_img):
        """perform Canny edge detection

        Parameter
        ---------
        gray_img : ndarray
            grayscale image array

        Returns
        -------
        ndarray
            gray_img with edges outlined
        """

        edges = cv2.Canny(gray_img, 100, 200)

        return edges

    @staticmethod
    def to_grayscale(rgb_img):
        return np.dot(rgb_img[... , :3] , [0.299 , 0.587, 0.114])

    @staticmethod
    def thresh_naive(img, lower_thresh, upper_thresh):
        thresh = imgProcess.threshold_segment_naive(img, lower_thresh, upper_thresh)
        imgProcess.show_image(thresh, title='thresh_naive', grayscale=True, force=True)
        cv2.imwrite(IMG_DIR + "/thresh.jpg", thresh.astype('uint8') * 255)
        return thresh  # 0, balck; 1, white

    @staticmethod
    def test_edge_naive(thresh):
        edges = imgProcess.edge_detect_naive(thresh)
        # write edgdes numpy array to file
        # np.savetxt(IMG_DIR + '/edge_naive', edges, fmt="%3f", delimiter=" ", newline='\n')

        # blur again, avoid hollow edge
        edges = cv2.GaussianBlur(edges, (7, 7), cv2.BORDER_DEFAULT)  # need to tune here
        imgProcess.show_image(edges, title='edge blur', grayscale=True)
        # np.savetxt(IMG_DIR + '/edge_blur', edges, fmt="%3f", delimiter=" ", newline='\n')
        
        # first flip the image
        imgProcess.flip(edges)  # now black -> edge; white -> space
        imgProcess.show_image(edges, title='edge flip', grayscale=True)
        # np.savetxt(IMG_DIR + '/edge_flip', edges, fmt="%3f", delimiter=" ", newline='\n')

        # then assign each area number
        count = imgProcess.assignAreaNumber(edges)
        print(count)
        imgProcess.show_image(edges, title='edge naive', grayscale=True)
        # np.savetxt(IMG_DIR + '/edge_naive_assigned', edges, fmt="%3f", delimiter=" ", newline='\n')

        # save the processed image
        cv2.imwrite(IMG_DIR + "/test_naive.jpg", edges)
        return edges, count

    @staticmethod
    def test_edge_canny(img):
        edges = edge_detect_canny(img)
        # np.savetxt(IMG_DIR + '/edge_canny', edges, fmt="%3f", delimiter=" ", newline='\n')
        # first maximize the edge
        boldEdge(edges)
        show_image(edges, title='edge canny bold', grayscale=True)
        # then assign the numbers
        count = assignAreaNumber(edges)
        print(count)
        # np.savetxt(IMG_DIR + '/edge_canny_assigned', edges, fmt="%3f", delimiter=" ", newline='\n')
        show_image(edges, title='edge canny', grayscale=True)
        cv2.imwrite(IMG_DIR + "/test_canny.jpg", edges)

    @staticmethod
    def flip(img):
        """flip the color of the image. 0 -> black -> edge; 1 -> white -> space.
        
        Parameters
        ----------
        img_name : ndarray
            image matrix
        """
        (m, n) = img.shape
        for i in range(m):
            for j in range(n):
                if img[i, j] != 0:  # white -> edge
                    img[i, j] = 0  # black -> edge
                else:  # original black space
                    img[i, j] = 1  # withe -> space
        return

    @staticmethod
    def assignAreaNumber(img):
        """This function will devide graph into several areas. Finally, 0 edge, >0 space.
        
        Parameters
        ----------
        img_name : ndarray
            image matrix

        Returns
        -------
        count : int
            number of areas
        """
        def DFS(i, j, count):
            stack = [(i, j)]
            while stack:
                (x, y) = stack[-1]  # top of the stack
                # up
                if x-1 >= 0 and img[x-1, y] == 1 and (x-1, y) not in visited:
                    stack.append((x-1, y))
                    visited.add((x-1, y))
                    continue
                # down
                if x+1 < m and img[x+1, y] == 1 and (x+1, y) not in visited:
                    stack.append((x+1, y))
                    visited.add((x+1, y))
                    continue
                # left
                if y-1 >= 0 and img[x, y-1] == 1 and (x, y-1) not in visited:
                    stack.append((x, y-1))
                    visited.add((x, y-1))
                    continue
                # right
                if y+1 < n and img[x, y+1] == 1 and (x, y+1) not in visited:
                    stack.append((x, y+1))
                    visited.add((x, y+1))
                    continue
                stack.pop()
                img[x, y] = (255-count)
            return  # stack empty
                    
        count = 0
        (m, n) = img.shape
        visited = set()  # keep all seen index
        for i in range(m):
            for j in range(n):
                if (i, j) not in visited and img[i, j] == 1:
                    DFS(i, j, count)  # assign white area number
                    count += 1
        return count

    @staticmethod
    def findStartandEnd(img, count):
        """This function will put all (start index, end index for each row) tuple in a dict.
        
        Parameters
        ----------
        img_name : ndarray
            image matrix

        Returns
        -------
        result : dict
            each element is a list of (start, end) tuples for a specific area number; each list is sorted
        """
        # result = {}  # {area number: [(starts, ends)]}
        # result = {
        #     1: [[(50, 50), (60, 50), (60, 60), (50, 60), (50, 50)]]
        # }

        # center = [100, 100]
        # radius = 100

        # circle_stroke = []
        # for x in np.linspace(0, np.pi * 4, num=30):
        #     circle_stroke.append((radius * np.cos(x) + center[0], center[1] + radius * np.sin(x)))
        # result[1].append(circle_stroke[:])

        # circle_stroke = []
        # for x in np.linspace(0, np.pi * 4, num=30):
        #     circle_stroke.append((radius * np.cos(x) + center[0], center[1] + radius * np.sin(x)))
        # result[1].append(circle_stroke[:])

        # circle_stroke = []
        # for x in np.linspace(0, np.pi * 4, num=30):
        #     circle_stroke.append((radius * np.cos(x) + center[0], center[1] + radius * np.sin(x)))
        # result[1].append(circle_stroke[:])


        (n, m) = img.shape
        print(img)
        result = [
            # (1, [[(0, 0), (0, m-1), (n-1, m-1), (n-1, 0), (0, 0)]]),
            # (2, [[(0, 0), (0, m-1), (n-1, m-1), (n-1, 0), (0, 0)]]),
            # (3, [[(0, 0), (0, m-1), (n-1, m-1), (n-1, 0), (0, 0)]])
        ]

        def dila(i, j, img, color = 0):
            # Let the pen stroke expand
            n, m = len(img), len(img[0])
            for fx, fy in fd2:
                di, dj = i + fx, j + fy
                if di >= 0 and di < n and dj >= 0 and dj < m:
                    if color == 0 or (color == 1 and img[di][dj] != 0):
                        img[di][dj] = color

        def has_zero(i, j, img):
            n, m = len(img), len(img[0])
            for fx, fy in fd0:
                di, dj = i + fx, j + fy
                if di >= 0 and di < n and dj >= 0 and dj < m:
                    if img[di][dj] == 0:
                        return True
            return False

        def draw_sub(start_y, end_y, longrange, img, color):
            empty_th = 10
            path = []
            for i in range(start_y, end_y, 3):
                path.append((i, longrange[i][0] + empty_th))
                path.append((i, longrange[i][1] - empty_th))

            for i in range(start_y, end_y, 1):
                for j in range(longrange[i][0] + empty_th, longrange[i][1] - empty_th + 1):
                    dila(i, j, img)

            return path[:]

        def draw_edge(sti, stj, img, color):

            if img[sti][stj] != color:
                print('COLOR WRONG')
                return []

            paths = []
            while True:
                vis = {}
                path = [(sti, stj)]

                while True:
                    # current_d, new_d = 0, 0
                    # new_d = current_d
                    # print('in', sti, stj, img[sti][stj])
                    dead_end = True
                    vis[(sti, stj)] = True
                    for fx, fy in fd0 + fdc:
                        newsti, newstj = sti + fx, stj + fy
                        # print('try', newsti, newstj, img[newsti][newstj])
                        if newsti >= 0 and newsti < n and newstj >= 0 and newstj < m and img[newsti][newstj] == 255 - area_number and (newsti, newstj) not in vis:
                            if has_zero(newsti, newstj, img):
                                sti, stj = newsti, newstj
                                path.append((sti, stj))
                                vis[(sti, stj)] = True
                                dead_end = False
                                break

                    if dead_end:
                        break

                if len(path) >= 1:
                    for x, y in path:
                        dila(x, y, img, color=1)
                    paths.extend(path)
                else:
                    break

                # BFS:

                q = deque()
                q.append(path[-1])
                sti = -1
                stj = -1
                vis = {}
                vis[path[-1]] = True
                while len(q) > 0:
                    i, j = q.popleft() 
                    for fx, fy in fd0:
                        ti, tj = i + fx, j + fy
                        if ti >= 0 and ti < n and tj >= 0 and tj < m and (ti, tj) not in vis:
                            if img[ti][tj] == 255 - area_number:
                                found = True
                                sti = ti
                                stj = tj
                                break
                            elif img[ti][tj] == 1:
                                q.append((ti, tj))
                                vis[(ti, tj)] = True
                    
                    if sti != -1:
                        break
                            
                if sti == -1:
                    break

            for i in range(0, n):
                for j in range(0, m):
                    if img[i][j] == 1:
                        img[i][j] = 0

            return paths[:]


        def floodfill_black(srcimg):
            img = copy.deepcopy(srcimg)  

            def DFS(i, j, count):
                stack = [(i, j)]
                while stack:
                    (x, y) = stack[-1]  # top of the stack
                    # up
                    if x-1 >= 0 and img[x-1, y] == 0 and (x-1, y) not in visited:
                        stack.append((x-1, y))
                        visited.add((x-1, y))
                        continue
                    # down
                    if x+1 < m and img[x+1, y] == 0 and (x+1, y) not in visited:
                        stack.append((x+1, y))
                        visited.add((x+1, y))
                        continue
                    # left
                    if y-1 >= 0 and img[x, y-1] == 0 and (x, y-1) not in visited:
                        stack.append((x, y-1))
                        visited.add((x, y-1))
                        continue
                    # right
                    if y+1 < n and img[x, y+1] == 0 and (x, y+1) not in visited:
                        stack.append((x, y+1))
                        visited.add((x, y+1))
                        continue
                    stack.pop()
                    img[x, y] = (150-count)
                return  # stack empty
                        
            count = 0
            (m, n) = img.shape
            visited = set()  # keep all seen index
            for i in range(m):
                for j in range(n):
                    if (i, j) not in visited and img[i, j] == 0:
                        DFS(i, j, count)  # assign white area number
                        count += 1
            black_data = {}
            for cnt in range(count):
                edges = [m-1, 0, n-1, 0]
                for i in range(0, m):
                    for j in range(0, n): 
                        if img[i][j] == 150 - cnt:
                            edges[0] = min(i, edges[0])
                            edges[1] = max(i, edges[1])
                            edges[2] = min(j, edges[2])
                            edges[3] = max(j, edges[3])
                black_data[cnt] = edges[:]
            return black_data

        def detect_number(edges, black_data, img, current_color):
            for black_number in black_data:
                if len(black_data[black_number]) > 0:
                    if black_data[black_number][0] > edges[0] and black_data[black_number][1] < edges[1] and black_data[black_number][2] > edges[2] and black_data[black_number][3] < edges[3]:
                        
                        # Found
                        for i in range(black_data[black_number][0], black_data[black_number][1]+1):
                            for j in range(black_data[black_number][2], black_data[black_number][3]+1):
                                img[i][j] = current_color

                        height = black_data[black_number][1] - black_data[black_number][0] + 1
                        width = black_data[black_number][3] - black_data[black_number][2] + 1
                        black_data[black_number] = []

                        print('Detected Number', width, height)
                        if width < 2 or height < 2:
                            return random.randint(1, 3) #Error

                        if width * 3 < height:
                            return 1
                        if width > height:
                            return 2
                        return 3

            return random.randint(1, 3)

        imgProcess.show_image(img)
        black_data = floodfill_black(img)
        print(black_data)
        for area_number in range(0, count):
            cnt = 0
            edges = [n-1, 0, m-1, 0]
            for i in range(0, n):
                for j in range(0, m): 
                    if img[i][j] == 255 - area_number:
                        cnt += 1
                        edges[0] = min(i, edges[0])
                        edges[1] = max(i, edges[1])
                        edges[2] = min(j, edges[2])
                        edges[3] = max(j, edges[3])
            if cnt <= 0.008 * n * m:
                continue

            if cnt >= 0.5 * n * m:
                continue

            paths = []
            current_color = 255 - area_number
            print(255 - area_number)

            number = detect_number(edges, black_data, img, current_color)

            TH = 22
            # Step 1
            found = True
            while found == True:
                found = False
                longrange = [0 for i in range(n)]
                for i in range(n):
                    start = -1
                    end = -1
                    for j in range(m):
                        if img[i][j] == current_color:
                            end = j
                            if start == -1:
                                start = j
                        else:
                            if start != -1:
                                break
                    longrange[i] = (start, end) # [start, end]

                i = 0
                while i < n:
                    # print(longrange[i])
                    if longrange[i][1] - longrange[i][0] + 1 >= TH:
                        j = i+1
                        while j < n and longrange[j][1] - longrange[j][0] + 1 >= TH:
                            j += 1
                        if i + 5 < j:
                            found = True
                            paths.append(draw_sub(i, j, longrange, img, current_color)) # [i, j)
                            # print(paths[-1])
                            imgProcess.show_image(img, paths=[paths[-1]])

                            st = []
                            for k in range(longrange[i][0], longrange[i][1] + 1):
                                st.append((i, k, img[i][k]))
                                img[i][k] = 0

                            for k in range(longrange[j-1][0], longrange[j-1][1] + 1):
                                st.append((j-1, k, img[j-1][k]))
                                img[j-1][k] = 0
                            imgProcess.show_image(img)

                            paths.append(draw_edge(i+1, longrange[i+1][0], img, current_color))
                            # print(paths[-1])
                            imgProcess.show_image(img, paths=[paths[-1]])

                            paths.append(draw_edge(i+1, longrange[i+1][1], img, current_color))
                            # print(paths[-1])
                            imgProcess.show_image(img, paths=[paths[-1]])

                            for x, y, v in st:
                                img[x][y] = v

                        i = j
                    i += 1
        

            found = True
            while found == True:
                found = False
                path = []
                sti = -1
                stj = -1
                # find 0
                for i in range(0, n):
                    for j in range(0, m):
                        if img[i][j] == current_color:
                            sti = i
                            stj = j
                            found = True
                            break
                    if sti != -1:
                        break
                
                if sti == -1 and stj == -1:
                    break

                # print(sti, stj)
                paths.append(draw_edge(sti, stj, img, current_color))
                # print(paths[-1])
                imgProcess.show_image(img, paths=[paths[-1]])

            def shorten_path(path):
                selected_path = [path[0]]
                for i in range(len(path)):
                    if abs(path[i][0] - selected_path[-1][0]) + abs(path[i][1] - selected_path[-1][1]) > 4:
                        selected_path.append(path[i])
                return selected_path[:]
            result.append((number, copy.deepcopy([shorten_path(p) for p in paths if len(p) > 3])))
            # imgProcess.show_image(img, paths=result[area_number])
            # print(result[area_number])

        (n, m) = img.shape
        print(img)
        result = [
            (1, [[(0, 0), (0, m-1), (n-1, m-1), (n-1, 0), (0, 0)]]),
            (2, [[(0, 0), (0, m-1), (n-1, m-1), (n-1, 0), (0, 0)]]),
            (3, [[(0, 0), (0, m-1), (n-1, m-1), (n-1, 0), (0, 0)]])
        ]

        def dila(i, j, img, color = 0):
            # Let the pen stroke expand
            n, m = len(img), len(img[0])
            for fx, fy in fd3:
                di, dj = i + fx, j + fy
                if di >= 0 and di < n and dj >= 0 and dj < m:
                    if color == 0 or (color == 1 and img[di][dj] != 0):
                        img[di][dj] = color

        def has_zero(i, j, img):
            n, m = len(img), len(img[0])
            for fx, fy in fd0:
                di, dj = i + fx, j + fy
                if di >= 0 and di < n and dj >= 0 and dj < m:
                    if img[di][dj] == 0:
                        return True
            return False

        def draw_sub(start_y, end_y, longrange, img, color):
            empty_th = 10
            path = []
            for i in range(start_y, end_y, 5):
                path.append((i, longrange[i][0] + empty_th))
                path.append((i, longrange[i][1] - empty_th))

            for i in range(start_y, end_y, 1):
                for j in range(longrange[i][0] + empty_th, longrange[i][1] - empty_th + 1):
                    dila(i, j, img)

            return path[:]

        def draw_edge(sti, stj, img, color):

            if img[sti][stj] != color:
                print('COLOR WRONG')
                return []

            paths = []
            while True:
                vis = {}
                path = [(sti, stj)]

                while True:
                    # current_d, new_d = 0, 0
                    # new_d = current_d
                    # print('in', sti, stj, img[sti][stj])
                    dead_end = True
                    vis[(sti, stj)] = True
                    for fx, fy in fd0 + fdc:
                        newsti, newstj = sti + fx, stj + fy
                        # print('try', newsti, newstj, img[newsti][newstj])
                        if newsti >= 0 and newsti < n and newstj >= 0 and newstj < m and img[newsti][newstj] == 255 - area_number and (newsti, newstj) not in vis:
                            if has_zero(newsti, newstj, img):
                                sti, stj = newsti, newstj
                                path.append((sti, stj))
                                vis[(sti, stj)] = True
                                dead_end = False
                                break

                    if dead_end:
                        break

                if len(path) >= 1:
                    for x, y in path:
                        dila(x, y, img, color=1)
                    paths.extend(path)
                else:
                    break

                # BFS:

                q = deque()
                q.append(path[-1])
                sti = -1
                stj = -1
                vis = {}
                vis[path[-1]] = True
                while len(q) > 0:
                    i, j = q.popleft() 
                    for fx, fy in fd0:
                        ti, tj = i + fx, j + fy
                        if ti >= 0 and ti < n and tj >= 0 and tj < m and (ti, tj) not in vis:
                            if img[ti][tj] == 255 - area_number:
                                found = True
                                sti = ti
                                stj = tj
                                break
                            elif img[ti][tj] == 1:
                                q.append((ti, tj))
                                vis[(ti, tj)] = True
                    
                    if sti != -1:
                        break
                            
                if sti == -1:
                    break

            for i in range(0, n):
                for j in range(0, m):
                    if img[i][j] == 1:
                        img[i][j] = 0

            return paths[:]


        def floodfill_black(srcimg):
            img = copy.deepcopy(srcimg)  

            def DFS(i, j, count):
                stack = [(i, j)]
                while stack:
                    (x, y) = stack[-1]  # top of the stack
                    # up
                    if x-1 >= 0 and img[x-1, y] == 0 and (x-1, y) not in visited:
                        stack.append((x-1, y))
                        visited.add((x-1, y))
                        continue
                    # down
                    if x+1 < m and img[x+1, y] == 0 and (x+1, y) not in visited:
                        stack.append((x+1, y))
                        visited.add((x+1, y))
                        continue
                    # left
                    if y-1 >= 0 and img[x, y-1] == 0 and (x, y-1) not in visited:
                        stack.append((x, y-1))
                        visited.add((x, y-1))
                        continue
                    # right
                    if y+1 < n and img[x, y+1] == 0 and (x, y+1) not in visited:
                        stack.append((x, y+1))
                        visited.add((x, y+1))
                        continue
                    stack.pop()
                    img[x, y] = (150-count)
                return  # stack empty
                        
            count = 0
            (m, n) = img.shape
            visited = set()  # keep all seen index
            for i in range(m):
                for j in range(n):
                    if (i, j) not in visited and img[i, j] == 0:
                        DFS(i, j, count)  # assign white area number
                        count += 1
            black_data = {}
            for cnt in range(count):
                edges = [m-1, 0, n-1, 0]
                for i in range(0, m):
                    for j in range(0, n): 
                        if img[i][j] == 150 - cnt:
                            edges[0] = min(i, edges[0])
                            edges[1] = max(i, edges[1])
                            edges[2] = min(j, edges[2])
                            edges[3] = max(j, edges[3])
                black_data[cnt] = edges[:]
            return black_data

        def detect_number(edges, black_data, img, current_color):
            for black_number in black_data:
                if len(black_data[black_number]) > 0:
                    if black_data[black_number][0] > edges[0] and black_data[black_number][1] < edges[1] and black_data[black_number][2] > edges[2] and black_data[black_number][3] < edges[3]:
                        
                        # Found
                        for i in range(black_data[black_number][0], black_data[black_number][1]+1):
                            for j in range(black_data[black_number][2], black_data[black_number][3]+1):
                                img[i][j] = current_color

                        height = black_data[black_number][1] - black_data[black_number][0] + 1
                        width = black_data[black_number][3] - black_data[black_number][2] + 1
                        black_data[black_number] = []

                        print('Detected Number', width, height)
                        if width < 2 or height < 2:
                            return random.randint(1, 3) #Error

                        if width * 3 < height:
                            return 1
                        if width > height:
                            return 2
                        return 3

            return random.randint(1, 3)

        imgProcess.show_image(img)
        black_data = floodfill_black(img)
        print(black_data)
        for area_number in range(0, count):
            cnt = 0
            edges = [n-1, 0, m-1, 0]
            for i in range(0, n):
                for j in range(0, m): 
                    if img[i][j] == 255 - area_number:
                        cnt += 1
                        edges[0] = min(i, edges[0])
                        edges[1] = max(i, edges[1])
                        edges[2] = min(j, edges[2])
                        edges[3] = max(j, edges[3])
            if cnt <= 0.01 * n * m:
                continue

            if cnt >= 0.5 * n * m:
                continue

            paths = []
            current_color = 255 - area_number
            print(255 - area_number)

            number = detect_number(edges, black_data, img, current_color)

            TH = 22
            # Step 1
            found = True
            while found == True:
                found = False
                longrange = [0 for i in range(n)]
                for i in range(n):
                    start = -1
                    end = -1
                    for j in range(m):
                        if img[i][j] == current_color:
                            end = j
                            if start == -1:
                                start = j
                        else:
                            if start != -1:
                                break
                    longrange[i] = (start, end) # [start, end]

                i = 0
                while i < n:
                    # print(longrange[i])
                    if longrange[i][1] - longrange[i][0] + 1 >= TH:
                        j = i+1
                        while j < n and longrange[j][1] - longrange[j][0] + 1 >= TH:
                            j += 1
                        if i + 5 < j:
                            found = True
                            paths.append(draw_sub(i, j, longrange, img, current_color)) # [i, j)
                            # print(paths[-1])
                            imgProcess.show_image(img, paths=[paths[-1]])

                            st = []
                            for k in range(longrange[i][0], longrange[i][1] + 1):
                                st.append((i, k, img[i][k]))
                                img[i][k] = 0

                            for k in range(longrange[j-1][0], longrange[j-1][1] + 1):
                                st.append((j-1, k, img[j-1][k]))
                                img[j-1][k] = 0
                            imgProcess.show_image(img)

                            paths.append(draw_edge(i+1, longrange[i+1][0], img, current_color))
                            # print(paths[-1])
                            imgProcess.show_image(img, paths=[paths[-1]])

                            paths.append(draw_edge(i+1, longrange[i+1][1], img, current_color))
                            # print(paths[-1])
                            imgProcess.show_image(img, paths=[paths[-1]])

                            for x, y, v in st:
                                img[x][y] = v

                        i = j
                    i += 1
        

            found = True
            while found == True:
                found = False
                path = []
                sti = -1
                stj = -1
                # find 0
                for i in range(0, n):
                    for j in range(0, m):
                        if img[i][j] == current_color:
                            sti = i
                            stj = j
                            found = True
                            break
                    if sti != -1:
                        break
                
                if sti == -1 and stj == -1:
                    break

                # print(sti, stj)
                paths.append(draw_edge(sti, stj, img, current_color))
                # print(paths[-1])
                imgProcess.show_image(img, paths=[paths[-1]])

            def shorten_path(path):
                selected_path = [path[0]]
                for i in range(len(path)):
                    if abs(path[i][0] - selected_path[-1][0]) + abs(path[i][1] - selected_path[-1][1]) > 5:
                        selected_path.append(path[i])
                return selected_path[:]
            result.append((number, copy.deepcopy([shorten_path(p) for p in paths if len(p) > 3])))
            # imgProcess.show_image(img, paths=result[area_number])
            # print(result[area_number])

        return result

    @ staticmethod
    def pixel2World(cali, areaPoints):
        worldPoints = []  # {area number: [(starts in world frame, ends in world frame)]}
        for data in areaPoints:
            tstore = []
            # (color, sto)
            for stroke in data[1]:
                temp = []  # [(starts in world frame, ends in world frame)]
                for (x, y) in stroke:
                    # startWorld = cali.transform_to_3d(np.array([start[0], start[1]]))
                    p = cali.transform_to_3d(np.array([x / 1.7, y / 1.7]))
                    temp.append(p)  # (np.array(2,), np.array(2))
                tstore.append(temp[:])
            worldPoints.append((data[0], copy.deepcopy(tstore)))
        # worldPoints[1] = [(cali.transform_to_3d(np.array([0, 499])),cali.transform_to_3d(np.array([0, 499])))]
        return worldPoints

    @ staticmethod
    def getPoints():
        # get th webcame image
        original_image = imgProcess.read_image(IMG_DIR + '/test.jpg', grayscale=True)
        
        # transform webcame image to standard image
        cali = calibration(original_image, (345, 500))
        standard_img = cali.calibrate()
        imgProcess.show_image(standard_img)
        # first, threshold the original image
        thresh = imgProcess.thresh_naive(standard_img, 0, 160)

        imgProcess.show_image(thresh)
        # then do the naive edge detection; also do area segmentation underlyingly
        count = imgProcess.assignAreaNumber(thresh)

        # thresh, count = imgProcess.test_edge_naive(thresh)
        # imgProcess.test_edge_canny(test_img)

        # get start points and corresponding end points
        areaPoints = imgProcess.findStartandEnd(thresh, count)  # {area number: [(starts, ends)]}

        # transfer index of the matrix to the coordinate in the world frame
        worldPoints = imgProcess.pixel2World(cali, areaPoints)
        # print(worldPoints)
        return worldPoints
        
if __name__ == '__main__':
    # TODO: to poptimize, no space allocation

    imgProcess.getPoints()