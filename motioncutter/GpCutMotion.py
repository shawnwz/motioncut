import sys, os, errno, ConfigParser, math, logging, traceback, shutil
import xlrd, sys, traceback, os, types, time
import GpLog
import GpUtils
from converter_new import Converter


class CutMotion():

    

    #GpLog.debug('codec: %s' % info.audio.codec)
    #GpLog.debug('audio_channels: %s' % info.audio.audio_channels)
    

    

    
    def PreviewFlv(self,inputfile, outputfile, jpg, w, h,tt):
        c = Converter()
        j=str(w)+'x'+str(h)
        conv = c.convert(inputfile, outputfile, {
                'format': 'flv',
                'audio': {
                    'codec': 'mp3',
                    'channels': 2
                },
                'video': {
                    'codec': 'h264',
                    'width': w,
                    'height': h
                }})
        c.thumbnail(inputfile,tt,jpg,j)
        for timecode in conv:
            GpLog.debug("current file is %s" % inputfile)
            GpLog.debug("Converting (%f) ...\r" % timecode)
            GpLog.debug("output file is (%s) ...\r" % outputfile)

            
    def PreviewMp4(self,inputfile, outputfile, jpg,w,h,tt):
        c = Converter()
        j=str(w)+'x'+str(h)
        #info = c.probe(inputfile)
        #if info.video.video_width < info.video.video_height :
        conv = c.convert(inputfile, outputfile, {
            'format': 'mp4',
            'audio': {
                'codec': 'mp3',
                'channels': 2
                },
                'video': {
                    'codec': 'h264',
                    'width': w,
                    'height': h,
                    'fps':24
                }})
        c.thumbnail(inputfile,tt,jpg, j)


        
        GpLog.debug("current file is %s" % inputfile)
        for timecode in conv:
            GpLog.debug("current file is %s" % inputfile)
            GpLog.debug("Converting (%f) ...\r" % timecode)
            GpLog.debug("output file is (%s) ...\r" % outputfile)
            
    def PreviewWebm(self,inputfile, outputfile, jpg,w,h,tt):
        c = Converter()
        j=str(w)+'x'+str(h)
        conv = c.convert(inputfile, outputfile, {
            'format': 'webm',
                'audio': {
                    'codec': 'vorbis',
                    'channels': 2
                    },
                'video': {
                    'codec': 'vp8',
                    'width': w,
                    'height': h,
                    'fps':24
                }})
        c.thumbnail(inputfile,tt,jpg, j)

        GpLog.debug("current file is %s" % inputfile)
        for timecode in conv:
            GpLog.debug("current file is %s" % inputfile)
            GpLog.debug("Converting (%f) ...\r" % timecode)
            GpLog.debug("output file is (%s) ...\r" % outputfile)
            
    def DetailMp4(self,inputfile, outputfile,jpg,w,h,tt):
        c = Converter()
        j=str(w)+'x'+str(h)
        if(w>h):
		k='h.png'
        else:
		k='v.png'  
        conv = c.convert(inputfile, outputfile, {
            'format': 'mp4',
                'audio': {
                    'codec': 'mp3',
                    'channels': 2
                    },
                'video': {
                    'codec': 'h264',
                    'width': w,
                    'height': h,
                    'fps':24
                    },
                'watermark':{
                        'file':k
                }})
        c.thumbnail(inputfile,tt,jpg, j)

        GpLog.debug("current file is %s" % inputfile)
        for timecode in conv:
            GpLog.debug("current file is %s" % inputfile)
            GpLog.debug("Converting (%f) ...\r" % timecode)
            GpLog.debug("output file is (%s) ...\r" % outputfile)
            
            
    def DetailWebm(self,inputfile, outputfile,jpg,w,h,tt):
        c = Converter()
        j=str(w)+'x'+str(h)
        if(w>h):
            k='h.png'
        else:
            k='v.png'    
        conv = c.convert(inputfile, outputfile, {
            'format': 'webm',
                'audio': {
                    'codec': 'vorbis',
                    'channels': 2
                },
                'video': {
                    'codec': 'vp8',
                    'width': w,
                    'height': h,
                    'fps':24
                },                              
                'watermark':{
                    'file':k
                }})
        c.thumbnail(inputfile,tt,jpg, j)

        GpLog.debug("current file is %s" % inputfile)
        for timecode in conv:
            GpLog.debug("current file is %s" % inputfile)
            GpLog.debug("Converting (%f) ...\r" % timecode)
            GpLog.debug("output file is (%s) ...\r" % outputfile)
            
    def mkdir_p(self, path):
                try:
                        os.makedirs(path)
                except OSError as exc:  # Python >2.5
                        if exc.errno == errno.EEXIST and os.path.isdir(path):
                                pass
                        else:
                                raise

    def __init__(self):
        '''
        Constructor
        '''
