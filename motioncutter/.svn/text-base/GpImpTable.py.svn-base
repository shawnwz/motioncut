#! /usr/bin/python
# -*- coding: utf-8 -*-

######################################
#gaopin read excel into import_images table
#coding licl
#20141201 
#beijing
######################################

import MySQLdb, sys, traceback, time, datetime, types, xlrd

import GpLog, GpUtils
from GpConfig import GpConfig
from GpECKey import ECKey
from _mysql import NULL

class ImpTable:
    #####config file name
    config = GpConfig()
    #####en => cn
    eckey = ECKey()

    #50 and 50+ =>558
    #32 =>559
    #14=>561
    #2=>64
    sizeCode={'100M':100,'50M':558,'32M':559,'14M':561,'2M':64,'HOVER':640}

    #illuKey = 'Illustration'.lower()
    
    ##var
    conn = None        
    ######enKey cnKey fr_keyword_collection
    e2c = {}
    c2e = {}
    ######collId map fr_image_collection
    icIds = {}
    ######fr_photographer
    pg = {}
    ######calc id 000        
    idLen={}
    ######import col name map,orgi col name map
    iColName = {}
    oColName = {}

    #
    errorMsg = {}

    ######sql 
    iOrgiSql = ''
    uOrgiSql = ''
    uImportSql=''

    sOrgiSql = 'select CorbisID from orgi_images where CorbisID=%s limit 2'

    iJobOnlineSql  = 'insert into job_image_online'
    iJobOnlineSql += '(image_id,corbis_id,status,type,user_id,try_times,create_time,update_time,valid_time) '
    iJobOnlineSql += 'values(%s,%s,1,0,-1,0,now(),now(),date_add(NOW(), interval 10 minute))'

    iPgSql = 'insert into fr_photographer(name,show_name,create_time) value(%s,%s,now())'
    sPgSql = 'select id from fr_photographer where name=%s'

    iFrMotionInfo = 'insert into fr_motion_info()'
    iFrMotionInfo += '(`id`, `gaopin_id`, `storage_id`, `title`, `caption`, `photographer_id`, `collection_id`, `category_id`, `shot_date`, `shot_date_des`, `status`, `mode_status`, `property_status`, `location`, `credit_line`, `license_type`, `max_size`, `is_in_cd`, `is_in_motion_set`, `is_in_motion_group`, `publish_date`, `restriction_ids`, `sort_id`, `create_time`, `update_time`, `pricing`)'
    iFrMotionInfo += 'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now(), %s)'
#########################class fun###############################
    def __del__(self):
        self.dele()

    def __init__(self):
        ##################corbisId 0000000############# 
        for i in range(1,9):
            tmp = ''
            for j in range(0,8-i):  
                tmp +='0'
            self.idLen[i]=tmp
        ################init conn#####################
        self.conn = MySQLdb.connect(host=self.config.host,user=self.config.user,
                passwd=self.config.pw,db=self.config.db,port=self.config.port,charset='utf8')
        ###############gen Sql########################
        self.initIOrgiSql()
        #self.initUOrgiSql()
        #self.initUImportSql()        
        ############load fr_image_collection##########
        self.loadCollection()
        ############load fr_photographer##############
        self.loadPg()

    def dele(self):
        if self.conn:
            self.conn.close() 
    # to delete
    def initUImportSql(self):
        cfgFile = open(self.config.impCfgFile)
        for line in cfgFile.xreadlines():
            line = line.rstrip()
            index = line.find('=')
            self.iColName[line[0:index]]=line[index+1:]
        ###import_image.status
        tmpSql = 'Status=%s' 
        for cn in self.iColName.keys():
            value = self.iColName[cn]
            if 'x'==value[0:1] or 'p'==value[0:1] or 'd'==value[0:1]:
                tmpSql+=','+cn+'=%s'
        self.uImportSql='update '+self.config.imp_table+' set '+tmpSql+' where Id=%s'
    
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
        uParam = 'Remark=%s, Status=%s'
        for cn in self.oColName.keys():
            value = self.oColName[cn]
            if 'x'==value[0:1] or 'p'==value[0:1] or 'd'==value[0:1]:
                iCol = iCol + ','+cn
                iParam = iParam + ',%s'  
                uParam = uParam + ',' + cn +'=%s'              
        self.iOrgiSql = 'insert into '+self.config.orgi_table+'('+iCol+') values ('+iParam+')'
        self.uOrgiSql = 'update '+self.config.orgi_table+' set '+uParam+' where Id =%s'
        
    def initUOrgiSql(self):
        cfgFile = open(self.config.orgiCfgFile)
        for line in cfgFile.xreadlines():
            line = line.rstrip()
            index = line.find('=')
            self.iColName[line[0:index]]=line[index+1:]
        ###import_image.status
        tmpSql = 'Status=%s' 
        for cn in self.iColName.keys():
            value = self.iColName[cn]
            if 'x'==value[0:1] or 'p'==value[0:1] or 'd'==value[0:1]:
                tmpSql+=','+cn+'=%s'
        self.uOrgiSql='update '+self.config.orgi_table+' set '+tmpSql+' where Id=%s'
        
    def loadPg(self):
        pgSql = 'select name,id from fr_photographer'
        cur = self.conn.cursor()
        cur.execute(pgSql)
        for name, pgid in cur.fetchall():
            self.pg[name.lower().strip()] = pgid
        cur.close()
        self.pg[''] = 0

    def addPg(self,name):
        u8Name = name.encode('utf8')
        cur = self.conn.cursor()
        rowId = 0
        try:
            cur.execute(self.iPgSql,(u8Name,u8Name))
            rowId = cur.lastrowid
            self.conn.commit()
        except Exception,ex:
            try:
                cur.execute(self.sPgSql, u8Name)
                for pid, in cur.fetchall():
                    rowId = pid
                    break
            except Exception,ex1:
                pass
        cur.close()
        self.pg[name.lower()] = rowId
        if rowId == 0:
            #add Photographer error
            self.procError('e07','add Photographer error,name:%s' % name)
        return rowId

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
    ###############################################
    def procColType(self,t,v):
        if ''==v or v == None:
            return None
        if '@d'==v:
            return datetime.datetime.now()
        if 'i'==t:
            return int(v)
        elif 'b'==t:
            return int(v)
        elif 'd'==t:            
            if type(v) == datetime.datetime:
                return v
            try:                        
                return xlrd.xldate.xldate_as_datetime(v,0)
            except Exception,ex:
                try:
                    return datetime.datetime.strptime(v,"%Y-%m-%d")
                except Exception,ex1:
                    try:
                        pdate = datetime.datetime.strptime(v,"%Y/%m/%d")
                    except Exception,ex1:
                        #excel datetime isn't 2014-11-11
                        self.procError('e06','date is not Y-m-d or Y/m/d')
                        return None
        elif 'f'==t:
            return float(v)
        else:
            if type(v) is types.UnicodeType:
                return v.encode('utf8')
            if 'v'==t:
                return str(v)
            return v

    def procEnCnKey(self,xdata):                
        cnsrc = xdata[self.config.cnKeyName]
        ensrc = xdata[self.config.enKeyName]
        endes = ''
        cndes = ''
        enm = False
        cnm = False                
        if cnsrc == None or cnsrc == '':
            cnm = True
        if ensrc == None or ensrc == '':
            enm = True

        if enm == False and cnm == False:
            cndes = cnsrc.replace(',','|')
            endes = ensrc.replace(',','|')
        else:
            endes,cndes=self.eckey.enMapcn(ensrc,',')
            if endes == '':
                #endes,cndes=self.eckey.cnMapen(cdsrc,',')
                endes,cndes=self.eckey.cnMapen(cnsrc,',')
        xdata[self.config.cnKeyName] = cndes
        xdata[self.config.enKeyName] = endes

    def procPgid(self,pger):
        #Photographer => photographerId
        pgid = 0
        if type(pger) == types.UnicodeType or type(pger) == types.StringType:
            pger = pger.strip()
            pgerLower = pger.lower()
            if pgerLower in self.pg.keys():
                pgid = self.pg[pgerLower]
            else:
                #insert 
                pgid = self.addPg(pger)
        return pgid

    def procImageDirection(self,ratio):
        imageDirection = 1
        if 0.5>=ratio and ratio>0:
            imageDirection = 1
        elif 0.9>=ratio and ratio>0.5:
            imageDirection = 2
        elif 1.1>=ratio and ratio>0.9:
            imageDirection = 3
        elif 2>=ratio and ratio>1.1:
            imageDirection = 4
        else:
            imageDirection = 5
        return imageDirection

    def procMediaRatingText(self,orgiLevel):
        #orgiLevel => orgi_MediaRatingText
        if orgiLevel == None or orgiLevel == '':
            return 5
        try:
            tmpLevel = int(orgiLevel)
            return tmpLevel
        except Exception,ex:
            #excel.orgiLevel not number
            self.procError('e04',traceback.format_exc())
            return 0

    def procPhotographedDate(self,photographedDate):
        if photographedDate == None or photographedDate == '':
            return (None,None,None)
        pdate = None
        if type(photographedDate) == types.UnicodeType or type(photographedDate) == types.StringType:
            try:
                pdate = datetime.datetime.strptime(photographedDate,"%Y-%m-%d")
            except Exception,ex:
                try:
                    pdate = datetime.datetime.strptime(photographedDate,"%Y/%m/%d")
                except Exception,ex1:
                #excel.DatePhotographed error
                    self.procError('e03','date is not Y-m-d or Y/m/d')
                    return (None,None,None)
        elif type(photographedDate) == datetime.datetime:
            pdate = photographedDate
        else:
            try:
                pdate = xlrd.xldate.xldate_as_datetime(photographedDate,0)
            except Exception,ex1:
                #excel.DatePhotographed type error
                self.procError('e02',str(type(photographedDate))+',value:'+str(photographedDate))
                return (None,None,None)
        sdate = pdate.strftime('%Y-%m-%d')
        smxdate = sdate + ' 23:59:59'
        smndate = sdate + ' 00:00:00'
        mxdate = datetime.datetime.strptime(smxdate,'%Y-%m-%d %H:%M:%S')
        mndate = datetime.datetime.strptime(smndate,'%Y-%m-%d %H:%M:%S')
        return (mndate,mxdate,smndate)
    
    def procSS(self,xdata):
        #en cn key                
        self.procEnCnKey(xdata)
        ##################
        #"maxSizeName"
        #xdata['sizeCode'] = 0
        #if xdata['SizeCode'] == None or xdata['SizeCode'] == '':
        #    ms = xdata['maxSizeName']
        #    if ms in self.sizeCode.keys():
        #        xdata['sizeCode'] = self.sizeCode[ms]
        ###################
        #Photographer => photographerId        
        pger = xdata['Photographer']
        pgid = self.procPgid(pger)
        xdata['photographerId'] = pgid
        ######################
        #ratio =>iptc_image_direction
        #ratio = xdata['ratio']
        #imageDirection = self.procImageDirection(ratio)
        #iptc['iptc_image_direction'] = imageDirection
        #######################
        #orgiLevel => MediaRatingText, orgi_MediaRatingText
        orgiLevel = xdata['orgiLevel']
        orgiMediaRatingText = self.procMediaRatingText(orgiLevel)
        #mediaRatingText = str(orgiMediaRatingText * 10)
        xdata['orgiMediaRatingText'] = orgiMediaRatingText
        #xdata['mediaRatingText'] = mediaRatingText
        #######################
        #datePhotographed = > LeftPhotographedDate,RightPhotographedDate
        dateShot = xdata['DateShot']
        dateShotApprox = xdata['DateShotApprox']
        #tmpDate = dateShotApprox
        #if tmpDate == None or tmpDate == '':
        #    tmpDate = dateShot         
        #lpd,rpd,sdpa = self.procPhotographedDate(tmpDate)
        #xdata['leftPhotographedDate'] = lpd
        #xdata['rightPhotographedDate'] = rpd
        #xdata['DateShotApprox'] = sdpa
        ########################
        #iptc_media_type
        xdata['MediaType'] = xdata['MediaType']
        enKeyLower = xdata[self.config.enKeyName].lower()
        #if enKeyLower.find(self.illuKey) > -1:
        #    iptc['iptc_media_type'] = 1
        #######################
        ###colorAppearance
        #if iptc['channel'] == 1:
        #    iptc['colorAppearance'] = 'B&W'
        #else:
        #    iptc['colorAppearance'] = 'Color'
        #######################
        ###ModelReleaseStatus
        #if xdata['ModelReleaseStatus']==2:
        #    iptc['modelReleaseRequired'] = 1
        #else:
        #    iptc['modelReleaseRequired'] = 0
        #######################
        ###PropertyReleaseStatus
        #if xdata['PropertyReleaseStatus']==1:
        #    iptc['propertyReleaseRequired'] = 1
        #else:
        #    iptc['propertyReleaseRequired'] = 0

    def checkOrgiExist(self,corbisId,cur):
        count = cur.execute(self.sOrgiSql,corbisId)
        if count>0:
            return True
        return False

    def procError(self,eCode,msg):
        code = self.errorMsg['code'] + 1
        #print 'code is --',code         
        self.errorMsg['code'] = code
        self.errorMsg[eCode] = msg

    def keepMysqlConn(self):
        try:
            cur = self.conn.cursor()
            cur.execute('select 1 from dual')
            cur.close()
        except MySQLdb.OperationalError:
            if self.conn:
                try:
                    self.conn.close()
                except Exception:
                    pass
            self.conn = MySQLdb.connect(host=self.config.host,user=self.config.user,
                passwd=self.config.pw,db=self.config.db,port=self.config.port,charset='utf8')
        except Exception:
            pass

    def procData(self,xdata):
        self.procDataWithCheck(xdata,False)

    def procDataWithCheck(self,xdata,check):
        self.errorMsg = {}
        self.errorMsg['code'] = 0
        gaopinId = xdata['gaopinId']        
        self.errorMsg['gaopinId'] = gaopinId
        self.procSS(xdata)
        
        cur = self.conn.cursor()
        try:
            if check:
                ###corbisId exist at orgi_images
                exist = self.checkOrgiExist(gaopinId,cur)
                if exist:
                    GpLog.debug('gaopinId %s exist' % gaopinId)
                    return
            ####insert orgi
            orgiParam = []
            orgiParam.append(self.config.remark)
            orgiParam.append(self.config.status)
            for cn in self.oColName.keys():
                #GpLog.debug('ooocolname = %s' % cn)
                value = self.oColName[cn]
                t = value[2:3]
                if 'x' == value[0:1]:   
                    xname = value[4:]                                
                    v = self.procColType(t,xdata[xname])
                    orgiParam.append(v)
                elif 'p' == value[0:1]:
                    xname = value[4:]
                    v = self.procColType(t,xdata[xname])
                    orgiParam.append(v)
                elif 'd' == value[0:1]:
                    v = value[4:]
                    v = self.procColType(t,v)
                    orgiParam.append(v)
                    
            orgiParam.append(xdata['id'])
            orgiId = 0
            try:                        
                cur.execute(self.uOrgiSql, orgiParam)
                orgiId = cur.lastrowid
            except MySQLdb.IntegrityError:
                GpLog.debug('gaopinId=%s exist at orgi_motions' % gaopinId)
                pass
            
            #try:
                #cur.execute(self.iFrMotionInfo, (orgiId,xdata['gaopinId'],xdata['storageId'],xdata['Title'],xdata['Caption'],xdata['photographerId'],xdata['CollectionId'],NULL,xdata['DateShot'],xdata['DateShot'],NULL,'0',xdata['ModelReleaseStatus'],xdata['PropertyReleaseStatus'],xdata['Displaylocation'],xdata['CustomCreditLine'],xdata['LicenseModel'],NULL,NULL,NULL,NULL,xdata) )
            self.conn.commit()                        
        except Exception,ex:
            self.conn.rollback()                        
            GpLog.error('gaopinId=%s, error=%s' % (gaopinId,ex))
            self.procError('e01',traceback.format_exc())
            raise
        finally:
            if cur:
                cur.close()                
                
