import numpy as np
import cv2
import time
import threading
from collections import deque
from . import Line
import warnings
class LaneDetector():
    '''
    This class finds the road lines using warpPerspective and Canny method, and then
    polyfit them in order to find their curvature parameters.
    '''
    #Initializer
    def __init__(self):
        self.frame = None
        self.ret = None
        self.width = None               #Set to default value
        self.height = None              #Set to default value
        self.frameSize = (self.width,self.height)
        self.resolutionValue = None
        self.videoCapture = None
        self.src = None
        self.dst = None
        self.undistorted = None
        self.binary_warped = None
        self.canny = None
        self.warpedFrame = None
        self.left_line = Line.Line()
        self.right_line = Line.Line()
        self.XmperPix = 3.7/700         # meters per pixel in x dimension
        self.YmperPix = 30/720          # meters per pixel in y dimension
        self.errorCnt = 0
        self.prevErrorCnt = 0
        self.captureVideo("")
        warnings.simplefilter('ignore', np.RankWarning)
    #Mutators
    #region
    def setFrame(self, frame):
        self.frame = frame

    def setResolutionValue(self,resolutionValue):
        self.getResolutionValue = resolutionValue

    def setSrc(self, src):
        self.src = src

    def setDst(self, dst):
        self.dst = dst

    def setLeftFit(self,LeftFit):
        self.LeftFit = LeftFit

    def setLeftCurveRad(self,LeftCurveRad):
        self.LeftCurveRad = LeftCurveRad

    def setRightFit(self,RightFit):
        self.RightFit = RightFit

    def setRightCurveRad(self,RightCurveRad):
        self.RightCurveRad = RightCurveRad

    def setXmperPix(self,XmperPix):
        self.XmperPix = XmperPix

    def setYmperPix(self,YmperPix):
        self.YmperPix = YmperPix
    
    #endregion

    #Accessors 
    #region 
    def getFrame(self):
        return self.frame
    
    def getUndistortedFrame(self):
        return self.undistorted

    def getResolutionValue(self):
        return self.resolutionValue

    def getFrameSize(self):
        return self.frameSize

    def getSrc(self):
        return self.src

    def getDst(self):
        return self.dst
        
    def getUndistorted(self):
        return self.undistorted
    
    def getBinaryWarped(self):
        return self.binary_warped

    def getVideoCapture(self):
        return self.videoCapture

    def getLeftFit(self):
        return self.LeftFit

    def getRightFit(self):
        return self.RightFit

    def getLeftCurveRad(self):
        return self.LeftCurveRad

    def getRightCurveRad(self):
        return self.RightCurveRad

    def getXmperPix(self):
        return self.XmperPix

    def getYmperPix(self):
        return self.YmperPix

    def getCountedError(self):
        return self.errorCnt

    #endregion

    #Methods
    #region
    def captureVideo(self, source = ""):
        if(source==""):
            self.cap = cv2.VideoCapture('C:/Users/ASUS/Desktop/Yeniklasör/videoplayback.mp4')
        else:
            self.cap = cv2.VideoCapture(0)

    def setResolution(self, weight, height):
        self.width = width
        self.height = height
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def resizeFrame(self,frame,fx=0.5,fy=0.5):
        '''
        Resize the frame to defined size
        '''
        return cv2.resize(frame, None, fx, fy, interpolation = cv2.INTER_AREA )

    def colorFilter(self,frame):
        '''
        Applies predefiened color filter to frame
        '''
        #Create white line mask
        lowerW = np.uint8([150, 150, 150])
        upperW = np.uint8([255, 255, 255])
        #Apply mask on the frame
        maskedFrame = cv2.inRange(frame,lowerW,upperW)
        return maskedFrame

    def createTrapzoid(self, frame, bottomWidth, upperWidth, height, xbias=0, ybias=0):
        frame_size = (frame.shape[1],frame.shape[0])
        self.src = np.array([[frame_size[0]/2-upperWidth/2+xbias,frame_size[1]-height+ybias],[frame_size[0]/2+upperWidth/2+xbias,frame_size[1]-height+ybias],[frame_size[0]/2+bottomWidth/2+xbias,frame_size[1]+ybias],[frame_size[0]/2-bottomWidth/2+xbias,frame_size[1]+ybias]],np.float32)
        #dst = np.array([[frame_size[0]/2-BottomWidth/2,0], [frame_size[0]/2+BottomWidth/2,0], [frame_size[0]/2+BottomWidth/2,Height] , [frame_size[0]/2-BottomWidth/2,Height]  ],np.float32)
        if(bottomWidth>upperWidth):
            maxWidth = bottomWidth
        else:
            maxWidth = upperWidth
        self.dst = np.array([[frame_size[0]/2-bottomWidth/2,0], [frame_size[0]/2+bottomWidth/2,0], [frame_size[0]/2+bottomWidth/2,frame_size[1]] , [frame_size[0]/2-bottomWidth/2,frame_size[1]]  ],np.float32)

    def warpPerspective(self, frame):
        frame_size = (frame.shape[1],frame.shape[0])
    
        LaneDetector.createTrapzoid(self, frame, 570, 220, 100)
        M = cv2.getPerspectiveTransform(self.src,self.dst)
        #M = np.fliplr([M])[0]
        
        return cv2.warpPerspective(frame, M, frame_size, flags=cv2.INTER_LINEAR)
        
    def iWarpPerspective(self, frame):
        frame_size = (frame.shape[1],frame.shape[0])
    
        LaneDetector.createTrapzoid(self, frame,570,220,100)
        M = cv2.getPerspectiveTransform(self.dst,self.src)
        #M = np.fliplr([M])[0]
        
        return cv2.warpPerspective(frame, M, frame_size, flags=cv2.INTER_LINEAR)

    def slidingWindow(self, binary_warped):
        out_img = (np.dstack((binary_warped, binary_warped, binary_warped)) * 255).astype(np.uint8)
        histogram = np.sum(binary_warped[int(binary_warped.shape[0]/2):,:], axis=0)

        # Find the peak of the left and right halves of the histogram
        # These will be the starting point for the left and right lines
        midpoint = np.int(histogram.shape[0]/2)
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint

        # Choose the number of sliding windows
        nwindows = 9

        # Set height of windows
        window_height = np.int(binary_warped.shape[0]/nwindows)

        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        # Current positions to be updated for each window
        leftx_current = leftx_base
        rightx_current = rightx_base
        # Set the width of the windows +/- margin
        margin = 100
        # Set minimum number of pixels found to recenter window
        minpix = 50
        # Create empty lists to receive left and right lane pixel indices
        left_lane_inds = []
        right_lane_inds = []

        # Step through the windows one by one
        for window in range(nwindows):
            # Identify window boundaries in x and y (and right and left)
            win_y_low = binary_warped.shape[0] - (window+1)*window_height
            win_y_high = binary_warped.shape[0] - window*window_height
            win_xleft_low = leftx_current - margin
            win_xleft_high = leftx_current + margin
            win_xright_low = rightx_current - margin
            win_xright_high = rightx_current + margin
            # Draw the windows on the visualization image
            vi=cv2.rectangle(out_img, (win_xleft_low,win_y_low), (win_xleft_high,win_y_high), color=(0,255,0), thickness=2) # Green
            vi=cv2.rectangle(out_img, (win_xright_low,win_y_low), (win_xright_high,win_y_high), color=(0,255,0), thickness=2) # Green
            #cv2.imshow('aa',vi)
            # Identify the nonzero pixels in x and y within the window
            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]
            # Append these indices to the lists
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)
            # If you found > minpix pixels, recenter next window on their mean position
            if len(good_left_inds) > minpix:
                leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
            if len(good_right_inds) > minpix:
                rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

        # Generate x and y values for plotting
        ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0])
        # Calculate radii of curvature in meters
        y_eval = np.max(ploty)  # Where radius of curvature is measured

        
        

        
        
        # Define conversions in x and y from pixels space to meters
        ym_per_pix = 30.0/720 # meters per pixel in y dimension
        xm_per_pix = 3.7/700 # meters per pixel in x dimension

        try:
            # Concatenate the arrays of indices
            left_lane_inds = np.concatenate(left_lane_inds)
            # Extract left and right line pixel positions
            leftx = nonzerox[left_lane_inds]
            lefty = nonzeroy[left_lane_inds]
            # Fit a second order polynomial to each
            left_fit = np.polyfit(lefty, leftx, 2)
            # Stash away polynomials
            self.left_line.current_fit = left_fit
            # Generate x and y values for plotting
            left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
            out_img[nonzeroy[left_lane_inds], nonzerox[left_lane_inds]] = [255, 0, 0]
            out_img[ploty.astype('int'),left_fitx.astype('int')] = [0, 255, 255]
            # Fit new polynomials to x,y in world space
            left_fit_cr = np.polyfit(lefty*ym_per_pix, leftx*xm_per_pix, deg=2)
            # Calculate radii of curvature in meters
            left_curverad = ((1 + (2*left_fit_cr[0]*y_eval*ym_per_pix + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
             # Stash away the curvatures  
            self.left_line.radius_of_curvature = left_curverad
        except:
            self.left_line.radius_of_curvature = 0
            left_curverad = 0
            pass
        
        try:
            # Concatenate the arrays of indices
            right_lane_inds = np.concatenate(right_lane_inds)
            # Extract left and right line pixel positions
            rightx = nonzerox[right_lane_inds]
            righty = nonzeroy[right_lane_inds] 
            # Fit a second order polynomial to each
            right_fit = np.polyfit(righty, rightx, 2)
            # Stash away polynomials
            self.right_line.current_fit = right_fit
            # Generate x and y values for plotting
            right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
            out_img[nonzeroy[right_lane_inds], nonzerox[right_lane_inds]] = [0, 0, 255]
            out_img[ploty.astype('int'),right_fitx.astype('int')] = [0, 255, 255]
            # Fit new polynomials to x,y in world space
            right_fit_cr = np.polyfit(righty*ym_per_pix, rightx*xm_per_pix, deg=2)
            # Calculate radii of curvature in meters
            right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*ym_per_pix + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])
            # Stash away the curvatures
            self.right_line.radius_of_curvature = right_curverad
        except:
            self.right_line.radius_of_curvature = 0
            right_curverad = 0
            pass

        return left_fit, right_fit, left_curverad, right_curverad, out_img

    def nonSliding(self, binary_warped, left_fit, right_fit):
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        margin = 100

        left_lane_inds = ((nonzerox > (left_fit[0]*(nonzeroy**2) + left_fit[1]*nonzeroy + left_fit[2] - margin))
            & (nonzerox < (left_fit[0]*(nonzeroy**2) + left_fit[1]*nonzeroy + left_fit[2] + margin)))
        right_lane_inds = ((nonzerox > (right_fit[0]*(nonzeroy**2) + right_fit[1]*nonzeroy + right_fit[2] - margin))
            & (nonzerox < (right_fit[0]*(nonzeroy**2) + right_fit[1]*nonzeroy + right_fit[2] + margin)))

        # Extract left and right line pixel positions
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds]
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]

        # Define conversions in x and y from pixels space to meters
        ym_per_pix = 30.0/720 # meters per pixel in y dimension
        xm_per_pix = 3.7/700 # meters per pixel in x dimension

        # Fit a second order polynomial to each
        
        try:
            left_fit = np.polyfit(lefty, leftx, 2)
            # Check difference in fit coefficients between last and new fits  
            self.left_line.diffs = self.left_line.current_fit - left_fit
            if (self.left_line.diffs[0]>0.001 or self.left_line.diffs[1]>0.4 or self.left_line.diffs[2]>150):
                return self.left_line.current_fit, self.right_line.current_fit, self.left_line.radius_of_curvature, self.right_line.radius_of_curvature, None
            # Stash away polynomials
            self.left_line.current_fit = left_fit

        except:
            self.left_line.current_fit = 0
            self.left_line.radius_of_curvature = 0

        try:
            right_fit = np.polyfit(righty, rightx, 2)
            self.right_line.diffs = self.right_line.current_fit - right_fit

            if (self.right_line.diffs[0]>0.001 or self.right_line.diffs[1]>0.4 or self.right_line.diffs[2]>150):
                return self.left_line.current_fit, self.right_line.current_fit, self.left_line.radius_of_curvature, self.right_line.radius_of_curvature, None
            # Stash away polynomials
            self.right_line.current_fit = right_fit
        except:
            #return self.left_line.current_fit, self.right_line.current_fit, self.left_line.radius_of_curvature, self.right_line.radius_of_curvature, None
            # Generate x and y values for plotting
            ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0])
            # Calculate radii of curvature in meters
            y_eval = np.max(ploty)  # Where radius of curvature is measured

        try:
            # Fit new polynomials to x,y in world space
            left_fit_cr = np.polyfit(lefty*ym_per_pix, leftx*xm_per_pix, deg=2)
            # Generate x and y values for plotting
            left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
            # Calculate radii of curvature in meters
            left_curverad = ((1 + (2*left_fit_cr[0]*y_eval*ym_per_pix + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
            # Stash away the curvatures  
            self.left_line.radius_of_curvature = left_curverad
            setLeftFit(self,left_fit)
            setLeftCurveRad(self,left_curverad)
        except:
            left_fit_cr = 0
            left_curverad = 0

        try:
            # Fit new polynomials to x,y in world space
            right_fit_cr = np.polyfit(righty*ym_per_pix, rightx*xm_per_pix, deg=2)
            # Generate x and y values for plotting
            right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
            # Calculate radii of curvature in meters
            right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*ym_per_pix + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])     
            # Stash away the curvatures  
            self.right_line.radius_of_curvature = right_curverad
            setRightFit(self,right_fit)
            setRightCurveRad(self,right_curverad)
        except:
            right_fit = 0
            right_curverad = 0

        return left_fit, right_fit, left_curverad, right_curverad, None
    
    def drawLane(self, binary_warped, left_fit, right_fit, left_curverad, right_curverad):
    
        # Create an image to draw the lines on
        warped_zero = np.zeros_like(binary_warped).astype(np.uint8)
        color_warped = np.dstack((warped_zero, warped_zero, warped_zero))    
    
        # Generate x and y values for plotting
        ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0])
        left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
        right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]   
    
        # Define conversions in x and y from pixels space to meters
        ym_per_pix = self.YmperPix
        xm_per_pix = self.XmperPix
    
        midpoint = np.int(self.undistorted.shape[1]/2)
        middle_of_lane = (right_fitx[-1] - left_fitx[-1]) / 2.0 + left_fitx[-1]
        offset = (midpoint - middle_of_lane) * xm_per_pix

        # Recast the x and y points into usable format for cv2.fillPoly()
        pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
        pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
        pts = np.hstack((pts_left, pts_right))

        # Draw the lane onto the warped blank image
        cv2.fillPoly(color_warped, np.int_([pts]), (0,255, 0))

        # Warp the blank back to original image space using inverse perspective matrix (Minv)
        img_size = (self.undistorted.shape[1], self.undistorted.shape[0])
        unwarped = LaneDetector.iWarpPerspective(self, color_warped)
        # Combine the result with the original image
        result = cv2.addWeighted(self.undistorted, 1, unwarped, 0.3, 0)
        radius = np.mean([left_curverad, right_curverad])

        # Add radius and offset calculations to top of video
        cv2.putText(result,"L. Lane Radius: " + "{:0.2f}".format(left_curverad/1000) + 'km', org=(50,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1, color=(255,255,255), lineType = cv2.LINE_AA, thickness=2)
        cv2.putText(result,"R. Lane Radius: " + "{:0.2f}".format(right_curverad/1000) + 'km', org=(50,100), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1, color=(255,255,255), lineType = cv2.LINE_AA, thickness=2)
        cv2.putText(result,"C. Position: " + "{:0.2f}".format(offset) + 'm', org=(50,150), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1, color=(255,255,255), lineType = cv2.LINE_AA, thickness=2)
        
        self.left_curverad = left_curverad
        self.right_curverad = right_curverad
        self.offset = offset
        
        return result

    def showLane(self, nbins=10):
        bins = nbins
        l_params = deque(maxlen=bins)
        r_params = deque(maxlen=bins)
        l_radius = deque(maxlen=bins)
        r_radius = deque(maxlen=bins)
        weights = np.arange(1,bins+1)/bins

        if len(l_params)==0 & self.prevErrorCnt!=self.errorCnt:
            left_fit, right_fit, left_curverad, right_curverad, _ = LaneDetector.slidingWindow(self, self.warpedFrame)
        else:
            left_fit, right_fit, left_curverad, right_curverad, _ = LaneDetector.nonSliding(self, self.warpedFrame,
                                                                    np.average(l_params,0,weights[-len(l_params):]),
                                                                    np.average(r_params,0,weights[-len(l_params):]))
        
        l_params.append(left_fit)
        r_params.append(right_fit)
        l_radius.append(left_curverad)
        r_radius.append(right_curverad)
        
        annotatedFrame = LaneDetector.drawLane(self, self.warpedFrame,
                                        np.average(l_params,0,weights[-len(l_params):]),
                                        np.average(r_params,0,weights[-len(l_params):]),
                                        np.average(l_radius,0,weights[-len(l_params):]),
                                        np.average(r_radius,0,weights[-len(l_params):]))
        return annotatedFrame      

    def showLaneParameters(self):
        return (getLeftFit(self),
                getLeftCurveRad(self),
                getRightFit(self),
                getRightCurveRad(self))

    def toString(self):
        return ("LeftFit:"+str(getLeftFit(self))+" "+
                "LeftCurveRad:"+str(getLeftCurveRad(self))+" "+
                "RightFit:"+str(getRightFit(self))+" "+
                "RightCurveRad:"+str(getRightCurveRad(self)))
    
    def waitKey(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()

    def releaseCapture(self):
            self.cap.release()
            cv2.destroyAllWindows()

    def showFrame(self,targetFrameType="frame"):
        try:
            if (targetFrameType=="frame"):
                cv2.imshow('Frame',self.frame)
            elif(targetFrameType=="Undistorted"):
                cv2.imshow('Undistorted',self.undistorted)
            elif(targetFrameType=="WarpedFrame"):
                cv2.imshow('WarpedFrame',self.warpedFram)
            elif(targetFrameType=="AnnotedFrame"):
                cv2.imshow('AnnotedFrame',self.annotatedFrame)
        except:
            pass
        
    #endregion

    #Main Method
    def getLaneParameters(self):
        '''
        This method runs lane detection algorithm. Detects lines and returns road parameters.
        It passes all parameters as zero as the algorithm cannot read the lines on road.
        '''
        if(self.cap.isOpened()):
            try:
                #Read frame
                self.ret, self.frame = self.cap.read()
                self.undistorted = self.frame
                
                #Resize the frame
                #resizedFrame = LaneDetector.resizeFrame(self,self.undistorted,0.5,0.67) #640 x 360---->320 x 240

                #Apply color filter to the frame
                #filteredFrame = LaneDetector.colorFilter(self,resizedFrame)
                
                #Apply canny algorithm to detect lines
                canny = cv2.Canny(self.undistorted,200,255)
                
                #cv2.imshow('',canny)
                #cv2.waitKey(1)

                #Change perspective view
                self.warpedFrame = LaneDetector.warpPerspective(self, canny)
            
                #cv2.imshow('Canny',self.warpedFrame)

                self.annotatedFrame = LaneDetector.showLane(self)

                return (self.left_curverad,self.right_curverad,self.offset)
            
            except:
                self.prevErrorCnt=self.errorCnt
                self.errorCnt= self.errorCnt+1
                #print(str(self.errorCnt)+" of Error in reading")
                return (0,0,0)
        # When everything done, release the capture
        LaneDetector.releaseCapture()



    
