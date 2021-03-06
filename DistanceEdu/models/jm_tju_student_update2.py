#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
from passlib.context import CryptContext
import re
from openerp.exceptions import except_orm

class Tju_Student_update2(models.Model):
    #建表
    _name = 'jm.tju.student.update2'
    _description = 'tju student import2'

    name = fields.Char(u'姓名')
    card_type = fields.Char(u'有效身份证件名称', default='身份证')
    idcard = fields.Char(u'有效身份证件号码')
    sex = fields.Selection([[1, '男'], [2, '女']], string=u'性别', default=1)
    nation = fields.Char(u'民族', default="汉")
    native_place = fields.Char(u'生源地区', default='浙江省')
    birth = fields.Date(u'出生年月')
    phone = fields.Char(u'联系电话')
    qq = fields.Char(u'QQ')
    wchat = fields.Char(u'微信')
    political = fields.Char(u'政治面貌')
    work_time = fields.Date(u'参加工作时间')
    job = fields.Char(u'职务或工种')
    work_unit = fields.Char(u'工作单位')
    address = fields.Char(u'联系地址')
    email = fields.Char(u'电子信箱')
    letter_add = fields.Char(u'通知书邮寄地址')
    zip = fields.Char(u'邮编')

    reg_time = fields.Datetime(u'注册时间')
    reg_code = fields.Char(u'注册号')
    school_state = fields.Char(u'学籍状态')
    is_change = fields.Char(u'是否异动')
    warning = fields.Char(u'警告', default='正常')
    college_remark = fields.Char(u'学院备注')

    highest_degree = fields.Char(u'入学前国民教育最高学历层次')
    graduate_time = fields.Date(u'入学前学历毕业年份')
    graduate_major = fields.Char(u'专业')
    graduate_school = fields.Char(u'入学前学历学校名称')
    graduate_code = fields.Char(u'入学前学历学校代码')
    graduate_cer_code = fields.Char(u'入学前学历证书编号')


    # 报名信息
    study_center = fields.Char(string=u'注册学习中心名称')
    batch = fields.Char(string=u'招生批次号')
    level = fields.Char(string=u'报考层次')
    major = fields.Char(string=u'就读专业名称')
    study_code = fields.Char(u'学号')
    school_date = fields.Char(u'入学日期')
    inputer = fields.Char(string=u'中心备注')
    beschool = fields.Char(u'所属分校')
    firstcon = fields.Char(u'第一联系方式')

    state = fields.Char(u'状态')


    bm_fee = fields.Float(u'报名考试费')
    tuition = fields.Float(u'第一年学费')
    z_fee = fields.Float(u'第一年杂费')
    tuition2 = fields.Float(u'第二年学费')
    z_fee2 = fields.Float(u'第二年杂费')
    jc_fee = fields.Float(u'教材费')
    bys_fee = fields.Float(u'毕业生费')
    qcfd_fee = fields.Float(u'全程辅导费（不含论文）')
    qcfd_fee2 = fields.Float(u'全程辅导费（含论文）')
    lwcx_fee = fields.Float(u'论文重修费')
    yh_fee = fields.Float(u'优惠')
    sum_fee = fields.Float(string=u'费用总和', store=True)

    remarks = fields.Text(u'备注')

    @api.multi
    def check_id(self):
        idcard_list = list(self.idcard)
        area = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古",
                "21": "辽宁", "22": "吉林", "23": "黑龙江", "31": "上海", "32": "江苏",
                "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东",
                "41": "河南", "42": "湖北", "43": "湖南", "44": "广东", "45": "广西",
                "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南",
                "54": "西藏", "61": "陕西", "62": "甘肃", "63": "青海", "64": "宁夏",
                "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"}
        if (not (self.idcard[0:2] in area)):
            return 1
        if (len(self.idcard) == 15):
            if ((int(self.idcard[6:8]) + 1900) % 4 == 0 or
                    ((int(self.idcard[6:8]) + 1900) % 100 == 0 and
                                 (int(self.idcard[6:8]) + 1900) % 4 == 0)):
                ereg = re.compile('[1-9][0-9]{5}[0-9]{2}[0-9]{4}[0-9]{3}$')

            else:
                ereg = re.compile('[1-9][0-9]{5}[0-9]{2}[0-9]{4}[0-9]{3}$')
            if (re.match(ereg, self.idcard)):
                pass
            else:
                return 1
        elif (len(self.idcard) == 18):
            if (int(self.idcard[6:10]) % 4 == 0 or
                    (int(self.idcard[6:10]) % 100 == 0 and
                                 int(self.idcard[6:10]) % 4 == 0)):
                ereg = re.compile('[1-9][0-9]{5}[0-9]{8}[0-9]{3}[0-9Xx]$')
            else:
                ereg = re.compile('[1-9][0-9]{5}[0-9]{8}[0-9]{3}([0-9]|X|x])$')

            if (re.match(ereg, self.idcard)):
                S = ((int(idcard_list[0]) + int(idcard_list[10])) * 7 +
                     (int(idcard_list[1]) + int(idcard_list[11])) * 9 +
                     (int(idcard_list[2]) + int(idcard_list[12])) * 10 +
                     (int(idcard_list[3]) + int(idcard_list[13])) * 5 +
                     (int(idcard_list[4]) + int(idcard_list[14])) * 8 +
                     (int(idcard_list[5]) + int(idcard_list[15])) * 4 +
                     (int(idcard_list[6]) + int(idcard_list[16])) * 2 +
                     int(idcard_list[7]) * 1 + int(idcard_list[8]) * 6 +
                     int(idcard_list[9]) * 3)
                Y = S % 11
                M = "F"
                JYM = "10X98765432"
                M = JYM[Y]
                if (M == idcard_list[17]):
                    pass
                else:
                    return 1
            else:
                return 1
        else:
            return 1



    def student_update(self, cr, uid, allid, context):
        # search = ['id','create_date','write_uid','county','open_bank','create_uid','reg_address','area']
        same = {'GZ':'gz','SHUZI':'jmszyx','jm':'hzjm','gnjx':'gn','czc0573':'czc','czc1':'czc','czc2':'czc',
                'czc3': 'czc','czc4':'czc','czc5':'czc'}
        block = []
        count = 0
        if (len(allid) >= 80):
            platforms = self.pool.get('res.users').browse(cr, uid, uid).platform
            domain = [('study_center', 'in', [g.name.replace('天大', '') for g in platforms])]
            allid = self.pool.get('jm.tju.student.update2').search(cr, uid, domain)
        for id in allid:
            if type(id) <> int:
                id = id[0]
            # 插入到学生表
            # 字段列表  以便取得插入的字段是啥
            l = ['sname', 'idcard', 'sex', 'nation', 'native_place', 'birth', 'phone', 'qq', 'wchat', 'political',
                 'work_time', 'job', 'work_unit', 'address', 'email', 'letter_add', 'zip', 'card_type']
            # 从导入的表中选取所需字段的值
            cr.execute("SELECT name,idcard,sex,nation,native_place,birth,phone,qq,wchat,political,work_time,\
                job,work_unit,address,email,letter_add,zip,card_type from jm_tju_student_update2 where id=%s" % (id))
            stup = cr.fetchall()

            student = self.browse(cr, uid, [id], context=context)[0]
            if (student.check_id() == 1):
                cr.execute("UPDATE jm_tju_student_update2 set state='身份证号码错误' where id=%s" % (id))
                continue
            # 查看该学生信息是否已存在
            cr.execute("SELECT sname from jm_student where idcard='%s'" % (stup[0][1]))
            exist = cr.fetchall()
            # 如果存在 则更新
            if (exist):
                for index in range(0, len(stup[0])):
                    # 检索各个字段的值 若不为空 就将其进行更新
                    if (stup[0][index] != None):
                        pos = l[index]
                        cr.execute("UPDATE jm_student set %s='%s' where idcard='%s'" % (pos, stup[0][index], stup[0][1]))
            # 不存在 插入
            else:
                cr.execute("INSERT into jm_student(sname,idcard) values('%s','%s')" % (stup[0][0], stup[0][1]))
                # 为了缩短插入语句 用循环将其进行更新
                for i in range(2, len(l)):
                    if (stup[0][i] != None):
                        pos = l[i]
                        cr.execute("UPDATE jm_student set %s='%s' where idcard='%s'" % (pos, stup[0][i], stup[0][1]))

            # 插入到报名表
            # 报名基本信息
            l2 = ['idcard', 'graduate_time', 'graduate_major', 'graduate_school', 'graduate_code', 'graduate_cer_code',
                  'study_center', 'batch', 'level', 'major','school_date','beschool', 'firstcon',
                  'highest_degree','study_code','reg_time','reg_code','study_code','is_change','warning','college_remark','school_state']
            # 报名收费信息
            feelist = ['bm_fee', 'tuition', 'jc_fee', 'ptfw_fee', 'tuition2', 'jc_fee2', 'ptfw_fee2', 'qcfd_fee',
                       'qcfd_fee2', 'lwcx_fee', 'lwzd_fee', 'dzsx_fee']
            fee_sum = 0  # 收费总和
            # 从导入的表中选取报名信息
            cr.execute("SELECT idcard,graduate_time,graduate_major,graduate_school,graduate_code,graduate_cer_code, "
                       "study_center,batch,level,major,school_date,beschool,firstcon,highest_degree,"
                       "study_code,reg_time,reg_code,study_code,is_change,warning,college_remark,school_state"
                       " from jm_tju_student_update2 WHERE id=%s" % (id))
            ide = cr.fetchall()

            batch_name = ide[0][7]
            if ide[0][7][-1] == '1':
                batch_name = ide[0][7][0:4] + u'春'
            if ide[0][7][-1] == '2':
                batch_name = ide[0][7][0:4] + u'秋'
            # print batch_name
            level_name = ide[0][8]
            study_center_name = u'天大' + ide[0][6]
            major_name = ide[0][9]
            # print batch_name,level_name,s
            # 因为报名中的学生是Many2one 以id为检索  所以  先已身份证为凭借取得id
            cr.execute("SELECT id from jm_student where idcard = '%s'" % (ide[0][0]))
            No = cr.fetchall()
            # 检测批次的正确性
            cr.execute("select id from jm_tju_plan where name='%s'" % (batch_name))
            batch_id = cr.fetchall()
            if not batch_id:
                cr.execute("UPDATE jm_tju_student_update2 set state='批次错误' where id=%s" % (id))
                continue
            # 检测层次的正确性
            cr.execute("SELECT id from jm_tju_plan where name='%s' and batch='%s'" % (level_name, batch_name))
            level_id = cr.fetchall()
            if not level_id:
                cr.execute("UPDATE jm_tju_student_update2 set state='层次错误' where id=%s" % (id))
                continue
            # 检测学习中心
            cr.execute("SELECT id from jm_tju_plan where name='%s' and batch='%s' and type='%s'"
                       % (study_center_name, batch_name, level_name))
            study_center_id = cr.fetchall()
            if not study_center_id:
                cr.execute("UPDATE jm_tju_student_update2 set state='学习中心错误' where id=%s" % (id))
                continue
            # 检测专业
            cr.execute("SELECT id from jm_tju_plan where name='%s' and batch='%s' and type='%s' and study_center='%s'"
                       % (major_name, batch_name, level_name, study_center_name))
            major_id = cr.fetchall()
            if not major_id:
                cr.execute("UPDATE jm_tju_student_update2 set state='专业错误' where id=%s" % (id))
                continue
            # 因为报名中的学生是Many2one 以id为检索  所以  先已身份证为凭借取得id
            cr.execute("SELECT id from jm_student where idcard = '%s'" % (ide[0][0]))
            No = cr.fetchall()
            # 查看在报名表中  改学生是否以及报过改批次
            cr.execute("SELECT id from jm_tju_student where student=%s and batch=%s" % (No[0][0], batch_id[0][0]))
            exist = cr.fetchall()
            # 如果存在
            if (exist):
                # 对比导入信息与已存在信息
                for index in range(1, len(ide[0])):
                    # 若导入信息不为空  就将已存在信息更新
                    if (ide[0][index] != None):
                        # 更新的字段
                        if index in [6,7,8,9]:
                            continue
                        pos = l2[index]
                        cr.execute("UPDATE jm_tju_student set %s='%s' where student=%s and batch=%s"
                                    %(pos, ide[0][index], No[0][0], batch_id[0][0]))
                # 因为导入时Many2one存在多个匹配时只会将第一个匹配到的数据写入  所以  再进行插入到目的表时  需要选出正确的数据插入
                cr.execute("UPDATE jm_tju_student set level=%s where student=%s and batch=%s"
                            %(level_id[0][0], No[0][0], batch_id[0][0]))
                # 根据批次、层次更新学习中心
                cr.execute("UPDATE jm_tju_student set study_center=%s where student=%s and batch=%s"
                            %(study_center_id[0][0], No[0][0], batch_id[0][0]))
                # 根据批次、层次、学习中心更新专业
                cr.execute("UPDATE jm_tju_student set major=%s where student=%s and batch=%s"
                            %(major_id[0][0], No[0][0], batch_id[0][0]))
                cr.execute("select inputer_dpt from jm_tju_student where student=%s and batch=%s" %(No[0][0], batch_id[0][0]))
                inputer_id = cr.fetchall()[0][0]
                if(inputer_id == None):
                    pass
                else:
                    cr.execute("select code from jm_custom_code where cus_con = '%s'" %(inputer_id))
                    inputer_code = cr.fetchall()[0][0]
                    student_inputer = self.pool.get('jm.tju.student.update2').browse(cr, uid, [id], context=context)[0].inputer
                    if not student_inputer:
                        pass
                    else:
                        student_inputer = student_inputer.lower()
                        if(inputer_code == student_inputer or not student_inputer):
                            pass
                        else:
                            cr.execute("update jm_tju_student set inputer='%s' where student=%s and batch=%s" % (student_inputer,No[0][0], batch_id[0][0]))
                            cr.execute("select remarks from jm_tju_student where student=%s and batch=%s" %(No[0][0], batch_id[0][0]))
                            remarks = cr.fetchall()[0][0]
                            if(remarks == None):
                                if (not student_inputer):
                                    pass
                                else:
                                    remarks = u"中心备注:" + student_inputer
                                    cr.execute("update jm_tju_student set remarks='%s' where student=%s and batch=%s" %(remarks,No[0][0], batch_id[0][0]))
                            else:
                                if(not student_inputer):
                                    pass
                                else:
                                    remarks = remarks + u"中心备注:" + student_inputer
                                    cr.execute("update jm_tju_student set remarks='%s' where student=%s and batch=%s" %(remarks,No[0][0], batch_id[0][0]))
                cr.execute("UPDATE jm_tju_student set (create_uid, create_date)=(%s,'%s') where student=%s and batch=%s"
                           % (uid, fields.Datetime.now(), No[0][0], batch_id[0][0]))
                cr.execute("delete from jm_tju_student_update2 where id=%s" % (id))
            '''else:
                # 若在目的表中不存在  则插入（先插入关键字段  再对其进行更新 减少代码长度）
                cr.execute("INSERT into jm_tju_student(student,batch) values(%s, %s)" % (No[0][0], batch_id[0][0]))
                # 对其进行更新
                for index in range(1, len(ide[0])):
                    if (ide[0][index] != None):
                        pos = l2[index]
                        cr.execute("UPDATE jm_tju_student set %s='%s' where student=%s and batch=%s" % (
                        pos, ide[0][index], No[0][0], batch_id[0][0]))
                # 新增时 费用信息也需要添加进去
                cr.execute("SELECT bm_fee,tuition,jc_fee,ptfw_fee,tuition2,jc_fee2,ptfw_fee2,qcfd_fee,"
                           "qcfd_fee2,lwcx_fee,lwzd_fee,dzsx_fee from jm_tju_plan where id=%s" % (ide[0][9]))
                fee = cr.fetchall()
                # 依次更新其费用信息
                for i in range(0, len(fee[0])):
                    # 计算费用总和
                    fee_sum = fee_sum + fee[0][i]
                    pos = feelist[i]
                    cr.execute("UPDATE jm_tju_student set %s=%s where student=%s and batch=%s" % (
                    pos, fee[0][i], No[0][0], batch_id[0][0]))
                # 更新其费用总和
                cr.execute("UPDATE jm_tju_student set sum_fee=%s where student=%s and batch=%s" % (
                fee_sum, No[0][0], batch_id[0][0]))
                # 因为导入时Many2one存在多个匹配时只会将第一个匹配到的数据写入  所以  再进行插入到目的表时  需要选出正确的数据插入
                # 与上相同  依次寻找正确值  并目的表更新
                batch_name = self.pool.get('jm.tju.plan').browse(cr, uid, [batch_id[0][0]], context=context)[0].name
                level_name = self.pool.get('jm.tju.plan').browse(cr, uid, [ide[0][8]], context=context)[0].name
                study_center_name = self.pool.get('jm.tju.plan').browse(cr, uid, [ide[0][6]], context=context)[0].name
                major_name = self.pool.get('jm.tju.plan').browse(cr, uid, [ide[0][9]], context=context)[0].name
                cr.execute("SELECT id from jm_tju_plan where name='%s' and batch='%s'" % (level_name, batch_name))
                cr.execute("UPDATE jm_tju_student set level=%s where student=%s and batch=%s" % (
                    cr.fetchall()[0][0], No[0][0], batch_id[0][0]))
                cr.execute("SELECT id from jm_tju_plan where name='%s' and batch='%s' and type='%s'" % (
                    study_center_name, batch_name, level_name))
                cr.execute("UPDATE jm_tju_student set study_center=%s where student=%s and batch=%s" % (
                    cr.fetchall()[0][0], No[0][0], batch_id[0][0]))
                cr.execute(
                    "SELECT id from jm_tju_plan where name='%s' and batch='%s' and type='%s' and study_center='%s'" % (
                        major_name, batch_name, level_name, study_center_name))
                cr.execute("UPDATE jm_tju_student set major=%s where student=%s and batch=%s" % (
                cr.fetchall()[0][0], No[0][0], batch_id[0][0]))
                # 反馈学生状态为新增
                cr.execute("UPDATE jm_tju_student_update2 set state='新增' where id=%s" % (id))'''

            cr.commit()
        if (len(block) != 0):
            raise except_orm(u"错误", u"学生%s的身份证号码有误" % block[0])
        else:
            raise except_orm(u"成功", u"导入成功，共导入%s条数据" % len(allid))

    def delete(self, cr, uid, context):
        cr.execute("DELETE from jm_tju_student_update2 where 1=1")

class tju_confirm_import2(models.Model):
    _name = 'jm.tju.confirm.import2'
    _description = "confirm import tju student2"

    @api.multi
    def confirm_import(self):
        create = 0
        update = 0
        error = 0
        for id in self.env.context.get('active_ids'):
            import_info = self.env['jm.tju.student.update2'].browse(id)
            stu_base_info = self.env['jm.student'].search([('idcard','=',import_info.idcard)])
            if stu_base_info:
                pass
            else:
                base_info = {
                    'sname':import_info.name,
                    'idcard':import_info.idcard,
                    'sex':import_info.sex,
                    'nation':import_info.nation,
                    'native_place':import_info.native_place,
                    'birth':import_info.birth,
                    'phone':import_info.phone,
                    'qq':import_info.qq,
                    'wchat':import_info.wchat,
                    'political':import_info.political,
                    'work_time':import_info.work_time,
                    'job':import_info.job,
                    'work_unit':import_info.work_unit,
                    'address':import_info.address,
                    'email':import_info.email,
                    'letter_add':import_info.letter_add,
                    'zip':import_info.zip,
                    'card_type':import_info.card_type,
                }
                stu_base_info = self.env['jm.student'].create(base_info)

            batch_name = import_info.batch
            batch_name = batch_name[0:4] + u'春' if batch_name[-1] == '1' else batch_name[0:4] + u'秋'
            level_name = import_info.level
            study_center_name  = u'天大' + import_info.study_center
            major_name = import_info.major
            inputer_dpt_code = import_info.inputer.lower() if import_info.inputer else import_info.inputer

            batch = self.env['jm.tju.plan'].search(
                [('name','=',batch_name),
                 ('batch','=','1')],
                limit=1
            )
            if not batch:
                import_info.state = u'批次错误'
                error += 1
                continue
            level = self.env['jm.tju.plan'].search(
                [('name','=',level_name),
                 ('batch','=',batch_name),
                 ('type','=','1'),],
                limit=1
            )
            if not level:
                import_info.state = u'层次错误'
                error += 1
                continue
            study_center = self.env['jm.tju.plan'].search(
                [('name', '=', study_center_name),
                 ('batch', '=', batch_name),
                 ('type', '=', level_name),
                 ('study_center','=','1')],
                limit=1
            )
            if not study_center:
                import_info.state = u'学习中心错误'
                error += 1
                continue
            major = self.env['jm.tju.plan'].search(
                [('name', '=', major_name),
                 ('batch', '=', batch_name),
                 ('type', '=', level_name),
                 ('study_center', '=', study_center_name),
                 ('major', '=' ,'1')],
                limit=1
            )
            if not major:
                import_info.state = u'专业错误'
                error += 1
                continue
            inputer_dpt = self.env['jm.custom'].search(
                [('code.code','=',inputer_dpt_code)],
                limit = 1
            )


            info = {
                'student': stu_base_info.id,
                'graduate_time': import_info.graduate_time,
                'graduate_major': import_info.graduate_major,
                'graduate_school': import_info.graduate_school,
                'graduate_code': import_info.graduate_code,
                'graduate_cer_code': import_info.graduate_cer_code,
                'highest_degree':import_info.highest_degree,
                'study_code':import_info.study_code,
                'reg_time':import_info.reg_time,
                'college_remark':import_info.college_remark,
                'school_state':import_info.school_state,
                'batch': batch.id,
                'level': level.id,
                'study_center': study_center.id,
                'major': major.id,
            }
            stu_info = self.env['jm.tju.student'].search(
                [('student', '=', stu_base_info.id),
                 ('batch', '=', batch.id)]
            )

            if not stu_info:
                if not inputer_dpt:
                    import_info.state = u'录取人错误'
                    error += 1
                    continue
                if inputer_dpt.categories == 2:
                    import_info.state = u'录入人请明确'
                    error += 1
                    continue
                info['inputer_dpt'] = inputer_dpt.id
                stu_info = self.env['jm.tju.student'].create(info)
                for item in major.items:
                    self.env['jm.charge'].create({
                        'project': item.item.value,
                        'fee': item.money,
                        'school_table': 'jm.tju.student',
                        'school_id': stu_info.id
                    })
                create += 1

            else:
                if inputer_dpt and inputer_dpt.categories != 2:
                    info['inputer_dpt'] = inputer_dpt.id
                stu_info.update(info)
                for item in stu_info.fee_line:
                    for major_item in major.items:
                        if item.project == major_item.item.value:
                            item.fee = major_item.money
                update += 1


            if not self.env['res.users'].search([('login','=',import_info.idcard)]):
                self.env['res.users'].create({
                    'login':import_info.idcard,
                    'password':'123456',
                    'name':import_info.name,
                    'department':u'无',
                })
            import_info.unlink()

        return {
            "type": "ir.actions.client",
            "tag": "action_notify",
            "params": {
                "title": u'学生导入成功',
                "text": u'新增%s条数据,更新%s条数据，%s条数据有误' %(create, update, error),
            }
        }