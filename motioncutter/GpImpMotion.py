#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, errno, ConfigParser, math, logging, traceback, shutil
import sys, os, traceback, httplib
import GpLog, GpUtils
from GpImpExcel import ImpExcel

from GpCutMotion import CutMotion
#from GpMongoDao import MongoDao
from GpConfig import GpConfig
from converter_new import Converter

class ImpMotion:       
    ie = ImpExcel()
    cm = CutMotion()
    #sean md = MongoDao()
#####################################################

    def __init__(self):
        pass

    def __del__(self):
        pass

    def imp(self,xdata,desStorageId,desPath,currPid):
        fileName = xdata['FileName']
        motionFile = xdata['MotionAbsFileName']
        extName = xdata['MotionExtName']
        gaopinId = ''
        try:
            #insert into import_images table
            gaopinId = self.ie.procRow(xdata)
            #xdata['gaopinId']=gaopinId
            GpLog.debug('generate gaopinId=%s' % gaopinId)   
                                         
            md5Path = GpUtils.md5Str(gaopinId)                
            if desPath == '':
                GpLog.error("notfound des path, storageId=%s" % desStorageId)
                return
            
            previewflvpath = desPath + 'PreviewFLV' + md5Path + '/'
            previewflvfile = previewflvpath + gaopinId + '.flv'
            previewflvthumbnailfile = previewflvpath + gaopinId + '.jpg'
            
            previewmp4path = desPath + 'PreviewMP4' + md5Path + '/'
            previewmp4file = previewmp4path + gaopinId + '.mp4'
            previewmp4thumbnailfile = previewmp4path + gaopinId + '.jpg'
            
            previewwebmpath = desPath + 'PreviewWebm' + md5Path + '/'
            previewwebmfile = previewwebmpath + gaopinId + '.webm'
            previewwebmthumbnailfile = previewwebmpath + gaopinId + '.jpg'
            
            detailmp4path = desPath + 'DetailMP4' + md5Path + '/'
            detailmp4file = detailmp4path + gaopinId + '.mp4'
            detailmp4thumbnailfile = detailmp4path + gaopinId + '.jpg'
            
            detailwebmpath = desPath + 'DetailWebm' + md5Path + '/'
            detailwebmfile = detailwebmpath + gaopinId + '.webm'
            detailwebmthumbnailfile = detailwebmpath + gaopinId + '.jpg'
            
            self.mkdir_p(previewflvpath)
            self.mkdir_p(previewmp4path)
            self.mkdir_p(previewwebmpath)
            self.mkdir_p(detailmp4path)
            self.mkdir_p(detailwebmpath)
            
            xdata['SourcePreFlvPath'] = previewflvpath
            xdata['SourcePreMp4Path'] = previewmp4path
            xdata['SourcePreWebmPath'] = previewwebmpath
            xdata['SourceDetMp4Path'] = detailmp4path
            xdata['SourceDetWebmPath'] = detailwebmpath
            #cut motion
            c = Converter()
            info = c.probe(motionFile)
            w=float(info.video.video_width)
            h=float(info.video.video_height)
            
            d=float(info.format.duration)
            if(d>=10):
                tt=5
            if(d<10):
                tt=1

            GpLog.debug("wwwwwww is %f" % w)
            GpLog.debug("hhhhhhh is %f" % h)
            GpLog.debug("wwwwwwwwwwwwwwwwwwwxxxxx  is   %s" % xdata['Width'])
            GpLog.debug("wwwwwwwwwwwwwwwwwwwxxxxx  is   %s" % xdata['Height'])
            
            if(w>h):
                ratio=h/float(w)
                if abs((h/w) - 0.75)<0.1:
                    GpLog.debug("h/w is 3/4")
                    w_p=240
                    h_p=180
                    w_d=640
                    h_d=480
                elif abs((h/w) - 0.56)<0.1:
                    GpLog.debug("h/w is 9/16")
                    w_p=240
                    h_p=136
                    w_d=640
                    h_d=360
                else:
                    GpLog.debug("h/w is NOT 3/4 NOT 9/16")
                    w_p=240
                    h_p=int(240*ratio)
                    w_d=640
                    h_d=int(640*ratio)
            else:
                ratio=w/float(h)
                if abs(w/h - 0.75)<0.1:
                    GpLog.debug("w/h is 3/4")
                    w_p=136
                    h_p=180
                    w_d=270
                    h_d=360
                elif abs(w/h - 0.56)<0.1:
                    GpLog.debug("w/h is 9/16")
                    w_p=102
                    h_p=180
                    w_d=202
                    h_d=360
                else:
                    GpLog.debug("w/h is NOT 3/4 NOT 9/16")
                    w_p=int(180*ratio)
                    h_p=180
                    w_d=int(360*ratio)
                    h_d=360 
                    
            if(w==h):  
                GpLog.debug("h/w is 3/4")
                w_p=180
                h_p=180
                w_d=480
                h_d=480 
                
            #self.cm.PreviewFlv(motionFile, previewflvfile, previewflvthumbnailfile)
            self.cm.PreviewMp4(motionFile, previewmp4file, previewmp4thumbnailfile,w_p,h_p,tt)
            self.cm.PreviewWebm(motionFile, previewwebmfile, previewwebmthumbnailfile,w_p,h_p,tt)
            self.cm.DetailMp4(motionFile, detailmp4file, detailmp4thumbnailfile,w_d, h_d,tt)
            self.cm.DetailWebm(motionFile, detailwebmfile, detailwebmthumbnailfile,w_d, h_d,tt)
            return 1
            
            
            #iptcMsg = self.ci.procImg(desPath,corbisId,imgFile)
            #xlsData = {}
            #xlsData['corbisId'] = corbisId
            #xlsData['id'] = xdata['id']
            #xlsData['data'] = xdata
            #corbisId
            #iptcMsg['corbisId'] = corbisId
            #iptcMsg['storageId'] = desStorageId
            #iptcMsg['id'] = xdata['id']
            #iptcMsg['originalFilename'] = fileName+'.'+extName
            #iptcMsg['extName'] = extName
            #self.md.insertImageExcel(xlsData)
            #self.md.insertImageMeta(iptcMsg)
            #self.md.addCorbisId(currPid,corbisId)
        except Exception, e:
            if 'ExcelFileName' in xdata:
                xlsFile = xdata['ExcelFileName'] 
                GpLog.error(' procCutImgError fileName=%s at excel %s; error msg: %s' 
                        % (fileName,xlsFile,e))
                return -1
            else:
                GpLog.error(' procCutImgError fileName=%s; error msg: %s' 
                        % (fileName,e))
                return -1
            #self.md.addCutErrorMsg(fileName,gaopinId,traceback.format_exc())

                
    def mkdir_p(self, path):
                try:
                        os.makedirs(path)
                except OSError as exc:  # Python >2.5
                        if exc.errno == errno.EEXIST and os.path.isdir(path):
                                pass
                        else:
                                raise
