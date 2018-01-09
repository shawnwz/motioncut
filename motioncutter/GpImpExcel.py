#! /usr/bin/python
# -*- coding: utf-8 -*-

######################################
#gaopin read excel into import_images table
#coding licl
#20141201 
#beijing
######################################

import MySQLdb, sys, traceback, time, datetime, types

import GpLog, GpUtils
from GpConfig import GpConfig

class ImpExcel:
    config = GpConfig()        
    contentType={'659':'3','660':'3','662':'3'}
    contentType['664']='4'
    contentType['665']='4'
    contentType['666']='4'
    contentType['669']='4'
    contentType['680']='4'
    contentType['682']='4'
    contentType['683']='4'
    contentType['690']='4'
    contentType['661']='4'
    licModel={'RF':'1','RM':'2'}

    xlsId=['ProviderId','ContentTypeSecondaryId'
            ,'CollectionId','MarketingCollectionId'
            ,'ContentTypeId']

    ######collId map fr_image_collection
    icIds = {}
    ##var
    conn = None        
    ######calc id 000
    idLen={}
    iSql = 'insert into orgi_motions (OrgiID,remark) values(%s,%s)'        
    iOrgiSql = ''
    oColName = {}
#########################class fun###############################
    def __del__(self):
        self.dele()
             
    def __init__(self):
        ##################corbisId 000000############# 
        for i in range(1,9):
            tmp = ''
            for j in range(0,8-i):  
                tmp +='0'
            self.idLen[i]=tmp
        ################init conn#####################
        self.conn = MySQLdb.connect(host=self.config.host,user=self.config.user,
                passwd=self.config.pw,db=self.config.db,port=self.config.port,charset='utf8')
        
        ############load fr_image_collection
        self.loadCollection()
        
        ############ prepare sql ##########
        self.initIOrgiSql()

    def dele(self):
       if self.conn:
            self.conn.close()  

    ############load fr_image_collection
    def loadCollection(self):
        collSql = 'select id,category_id,cp_id from fr_motion_collection'
        cur = self.conn.cursor()
        cur.execute(collSql)
        for collId, catId, cpId in cur.fetchall():
            tmp = []
            tmp.append(catId)
            tmp.append(cpId)
            self.icIds[collId] = tmp                        
        cur.close()

    def genGaopinId(self,ctId,lic,Id):                
        gaopinId = '15'
        sctId = ''
        if type(ctId) is types.FloatType:
            sctId = str(int(ctId))
        else:
            sctId = str(ctId)
        if sctId in self.contentType:
            gaopinId += self.contentType[sctId]
        else:
            raise Exception('ContentTypeId %s error!' % ctId)               
        if lic in self.licModel:
            gaopinId +=self.licModel[lic]
        else:
            raise Exception('LicenseModel %s error!' % lic)
        sId = str(Id)
        gaopinId +=self.idLen[len(sId)]+sId
        return gaopinId

    def checkRow(self,xdata):
        collId = int(xdata['CollectionId'])
        if collId in self.icIds:
            if xdata['ContentTypeId'] == None or xdata['ContentTypeId'] == '':
                xdata['ContentTypeId'] = self.icIds[collId][0]
            if xdata['ProviderId'] == None or xdata['ProviderId'] == '':
                xdata['ProviderId'] = self.icIds[collId][1]

        ##excel => mysql so at proc
        #proc modelrelease
        mrs = xdata['ModelReleaseStatus']
        xdata['ExcelModelReleaseStatus'] = mrs
        if mrs.lower() == 'yes':
            xdata['ModelReleaseStatus']=2
        else:
            xdata['ModelReleaseStatus']=1
        #proc PropertyRelease
        prs = xdata['PropertyReleaseStatus']
        xdata['ExcelPropertyReleaseStatus'] = prs                                
        if prs.lower() == 'yes':
            xdata['PropertyReleaseStatus']=2
        else:
            xdata['PropertyReleaseStatus']=1

    def procRow(self,xdata):
        self.checkRow(xdata)
        dbParam = []
        dbParam.append(xdata['FileName'])
        dbParam.append(self.config.remark)
        cur = self.conn.cursor()
        cur.execute(self.iSql, dbParam)
        rowId = cur.lastrowid
        cur.close()
        self.conn.commit()
        ctId = xdata['ContentTypeId']
        lic = xdata['LicenseModel']
        gaopinId = self.genGaopinId(ctId,lic,rowId)
        xdata['id'] = str(rowId)
        xdata['gaopinId'] = gaopinId
        return gaopinId
    
    def initIOrgiSql(self):
        cfgFile = open(self.config.orgiCfgFile)
        for line in cfgFile.xreadlines():
            line = line.rstrip()
            index = line.find('=')
            self.oColName[line[0:index]]=line[index+1:]
        ###############gen insert sql#################
        ###orgi_image.remark,orgi_image.status
        iCol = 'Remark,Status'
        iParam = '%s,%s'
        for cn in self.oColName.keys():
            value = self.oColName[cn]
            if 'x'==value[0:1] or 'p'==value[0:1] or 'd'==value[0:1]:
                iCol = iCol + ','+cn
                iParam = iParam + ',%s'                
        self.iOrgiSql = 'insert into '+self.config.orgi_table+'('+iCol+') values ('+iParam+')'
