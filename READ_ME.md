# Innage v0.0: HR Salary Management (人事薪酬管理)
Inner management -> Innagement
导入表
- 只导一次, 后续实时更新
花名册: 编号, 姓名, 岗级, 公司, 部门, ...

- 只导一次, 发放月薪前核查 (每月自动生成, 按需修改)
基本薪资: 月薪调整系数
餐补标准: 餐补标准
社保公积金表(每年导入): 员工, 个人申报基数
#TODO: action: 导出与前月不同项
- 每月都导入:
考勤表 (从钉钉导入): 姓名, 工号, 出勤,迟到,早退,上班缺卡, 下班缺卡, 旷工天数,病假,事假
	花名册中没有的人员跳过, 无数据的为零, 考勤表编号要人工添加
个税表 (从官网导入): 员工, 个税 
调整表 (月手工填报): 员工, 调整方向, 调整类型, 调整内容, 金额
    调整类型CHOICE: 当月月薪, 福利, 考核, 税后

#TODO: 行政部门
#TODO: 在职离职的问题SalaryProcess.employees 自动抓取在职人员, 其余人员的增加减少手动修改
#TODO:  完善审核机制
#问题: 每位员工可以看到自己的调整项, 或者导入极简?

计划:
周二: 
1. 修改软件
    - 确定Model
    - 确定SalaryProcess运行逻辑
2. 问周详 (首先保证可以演示)
    - NAS确认可以Docker封装, 对接技术人员, 使用另一个project尝试
    - 导出格式确认 (不同Model的action导出)
3. 向丹丹反馈
4. Docker封装
周三:
1. 在技术人员支持下部署到NAS
2. 修改软件
    - 完成逻辑并接入自动化程序
    - 完善导出格式
3.Docker封装+尝试部署
周四:
1. 部署到NAS
2. 修改软件
    - 完成逻辑并接入自动化程序 
    - (如有时间, 加入审核步骤)
周五:
1. 修改软件
    - 行政部门 和 最后修改 (数据分析/部门分析)

向丹丹: 遗留问题1. 入职转正 2. 离职 3.时间筛选(合同到期和转正)
	相关的model: 1. 花名册, 2.考勤, 3. 社保公积金, 

异常情况: 迟到早退, 缺卡旷工

6/12
需要记录的调整
跟工资相关的都要精确记录 (不需要, 只记录最后的表) 

沈: 工会(当月月薪合计*比率, 作为代扣代缴费用计入) 和 极简导入格式 格式是否可以调整简化

审核人员工作: 审核三张导入表 和 操作日志, 导入个税表

沈讨论报告:
1. 编号问题: 为什么采用新的编号? 因为旧的编号有缺失. 编码不是自动的
2. !!!! 关于成本计算: 沈采用的是excel表的形式, 极简并没有这个功能. 单据配置好以后, 也是要线下进行处理分析. 后期是否要导入其他成本直接在人事薪酬系统中计算
3. !!!! 部门: 现在的解决方法是表单下载下来之后用excel表根据部门名称进行分类计算
4. 名称: 应发工资名字不能改, 其他名字改不改都差不多

向讨论报告:
1. 社保公积金始缴日是怎么判断的? 社保 1. 不缴纳社保的: 实习. 2. 还未开始缴纳: 入职时间在当月15号之后的次月开始缴纳, 所以还没交
1.5 公积金有些人不交
2. 离职入职调岗(人事流程)是否已经满足.  
3. 人事流程与薪水作用时间的不同: 调岗调职都是按月统一调整
4. 离职后也要发工资. 考勤看时间 判断是否发工资: 离职时间> 上月月初
平时增加人员.
月底最后一个工作日补全校准核对

周讨论准备:
1. 主要流程
2. 阐明我的流程
3. 泰宁职级怎么搞 

极简: 调岗人员档案-批量维护里面可以调岗吗?
编号没法排序

用工形式:
合作
全日制
实习生
试用期
退休返聘

入职后还会调整项:
#TODO

极简调整结果: 不变

周讨论结果:
1. 培育期 是正式员工, 但是离职了要扣钱
2. 代发的没有考勤
3. 合作人员不走正常考勤路线
4. Zhangjuping项目部没有考勤, 算是正式员工, 泰宁合作人员 wuxiaohua 
5. 泰宁的合作团队:zhuxun团队
6. Mengtiefeng算华夏合作人员, 在泰宁参保
7. 泰宁职级还未确认, 但是可以按照P0/M0进行自定义

用工形式 / 员工状态 应该修改逻辑
用工形式: 全职, 兼职, 实习, 退休返聘, 培育
员工状态: 在职, 离职, 退休

工资单确认结果:
不同处: 
1. 基本工资（如实际发放金额高于与社保缴纳基数按社保缴纳基数，如低于的按实际发放金额，如不缴纳人员按2000元））

员工: 
岗级
	定岗月薪系数
定岗满勤标准月薪「部门成本」
	月薪增减 (请假)「部门成本」
当月月薪合计
	福利增「部门成本」
考核前当月薪酬
	考核增减「公司成本」
*当月应发薪酬*
	个人承担超额缴纳部分「个人成本」
当月计税薪酬
	代扣代缴费用「个人成本」
	代扣个税「个人成本」
当月税后费后薪酬
	税后增减(车位费)「个人成本」
当月实发薪酬

成本:
部门成本: 薪酬包, 报销款, 部门运行成本, 其他成本
公司成本: 固定资产, 部门成本, 

个人要求超额
社保公积金(个人)代扣代缴
社保公积金缴纳部分

福利:
住房补贴
代扣代缴:
社保公积金(个人)代扣代缴
工会费
税后:
已发放
车位费
其他
实发工资
社保公积金缴纳部分=个人要求超额+社保公积金(个人)代扣代缴
社保公积金(公司)承担

薪酬包成本分析:
月薪成本合计=当月应发薪酬 + 社保公积金(公司)承担
部门列支金额 (列到部门成本的) = 月薪成本合计 - 公司列支金额 
公司列支金额 = 考核增减

工资发放流程:
1. 确认发放人员
2. 导入 考勤表/调整表
4. 财务审核
5. 导入个税表
6. 锁定薪酬表
7. 导出薪酬表

审核流程确认: 社保, 花名册有修改的都要看(当月修改), 所有修改都要线下确认

社保公积金: 首先确定每个公司总数和实际相同, !!补缴

调增: 试用期调整, 给别人交社保, 月中转正产生的, 月中入职


# 持续更新的想法和计划. 
# Innagement v1.0: HR Salary Management (人事薪酬管理)
Project: 核心APP + 公司运营APP + 小型监控APP
核心APP:
数据结构: 组织/个人/成本/预决算
业务逻辑: 工资单计算法则
交互规则: 审核规则

公司运营APP:(对下)
对下工资单(极简格式)
导入系统
日常维护
导出系统
审核系统

小型监控APP:(对上)
对上财报(以工资单形式)

# Innagement v2.0: Group Management System(集团管理系统)


#TODO 历史调整表单child model
历史数据都要有

#TODO: cron 数据库备份

#TODO: redis 缓存 实现审批流程的聊天 (内存读写)

#TODO: 导出导入模版按钮

## 软件系统设计
有三个Projects: 核心软件(Entity), 公司运营软件(Company Operation), 集团监控软件(Group Monitor)
详解:
### Entity Project 核心软件
软件系统的最基本功能. 包括业务核心逻辑的设计, 监控软件和运营软件需要进行沟通统一的部分, 跨软件APP
APP_LIST:
    1. Validation           # 审核APP
    2. Entity               # 主体APP
    3. RuleCalc             # 规则计算APP
    4. Publish/Report       # 任务发布/汇报APP

### Company Operation Project(Management Project) 公司运营软件
添加人事模块和财务模块 (后期可以和外部软件进行连接), 保证业务的可拓展性
APP_LIST:
    1. HR                   # 人事管理APP       (v1.0)
    2. SalaryCalc           # 薪酬计算APP       (v1.0)
    3. CostBudget           # 成本预决算APP     
    4. PaySlip              # 工资单APP         (v1.0)

### Group Monitor Project(Management Project): 集团监控软件
添加监控模块和财报模块, 保证展示效果的可拓展性
APP_LIST:
    1. Financial Report     #财报APP            (v1.5)
    2. CompanyMonitor       #公司监控APP

时间估算: 一个APP一周 4月

## Entity APP
Entity: # 实体
    name = CharField()
    ForeignKey(OrganizationModel, null=True)
    create_time = DateTimeField()
    status

Org(Entity): # 组织
    name
    supervisor = ForeignKey(UserGroup, null=True)
    sup_org = ForeignKey(Org, null=True) # 上级组织, 跨模型的上级, 只有group没有上级组织

Group(Org): # 集团
    id = CharField()

Company(Org): # 公司
    id = CharField()
    group = ForeignKey(Group, null=True)
    sup_company = ForeignKey(Company, null=True) # 上级公司, 模型内的上级, 总公司没有上级公司
    database

Dpt(Org): # 部门
    id = CharField()
    Company = ForeignKey(Company)
    sup_dpt = ForeignKey(Dpt, null=True) # 上级部门
    center = ForeignKey(Center, null=True)

Center(Org): # 中心 (总公司的特有机构)
    id = CharField()
    Company = ForeignKey(Company) # 公司必须没有sup_company

Ind(Entity): # 个人
    org = ForeignKey(Org) # 所属组织
    usr = OneToOneField(auth.User)

Employee(Ind): # 职工
    company = 
    dpt = 


Cooperator(Entity):




ValidationModel: 
    status = booleanField() # CHOICE: null: 未审核, True: 审核通过, False: 审核未通过
    change_model = ForeignKey(ContentType.filter(DataModel))
    change_instance = OneToOneField()
    chang_time = DateTimeField()
    change_type = CharField() # CHOICE: 新增, 修改, 封存
    change_reason = TextField()
    change_user = ForeignKey(User)
    change_content = TextField() # 创建自定义form
        # <修改: instance_str>\n for changed_field: “changed_field: old_value -> new_value\n”
        # <新增: instance_str>\n for field: “field: value\n”
        # <封存: instance_str>\n for field: “field: value\n”
    next_change = ForeignKey(ValidationModel, on_delete=models.CASCADE, null=True) # 下一个修改
    # 提交者
    def submit_for_check(self)
    # 审核者
    def approve(self)
    def reject(self)

ValidationAdmin:
    def get_queryset(self, request) # check user and filter. see GPT
    def view/change/delete/add permission rewrite see GPT



FINANCIAL APP

Entity()                # 包含组织和个人

Organization(Entity)    # 组织, 有预算
    property = DecimalField() #资产


Individual(Entity)      # 个人, 无预算, 但是会有复杂交付关系 

Government(Organization)      # 税款

Company(Organization)

Department(Organization)

Collaboration(Organization)

Employee(Entity)

FinancialTransaction(Entity)
    amount = DecimalField()
    transaction_type = CharField() # CHOICE: 收入, 支出
    transaction_time = DateTimeField()
    transaction_user = ForeignKey(User) 
    money_out = ForeignKey(Entity)  # 支出方
    money_in = ForeignKey(Entity)   # 收入方

Budget(Org)
    amount = DecimalField()
    budget_type = CharField() # CHOICE: 预算, 实际
    budget_duration = CharField() # CHOICE: 年度, 季度, 月度
    budget_user = ForeignKey(User) 
    budget_entity = ForeignKey(Entity)  # 预算方


UserInputModel(): #花名册, 公司规则, 社保公积金, 考勤, 个税, 调整 
    import_time = DateTimeField()
    import_user = ForeignKey(User)

    # 只要有修改, 就会生成一个新的ValidationModel instance
    def save
    def delete # 封存

ComponentField() # 所有可以计算薪资的column

SalaryComponentModel(): 
    name = CharField()
    salary_calc_rule = ForeignKey(SalaryCalcRuleModel)
    operator = CharField() # CHOICE: + - * / = +/-(调整项: 调整表类型选项提取filter:该员工生效SalaryCalcRuleModel对应的所有+/-) 
    previous_component = ForeignKey(SalaryComponentModel, null=True) # 前一个组件
    calc_field = CharField() # model_name-field_name
    is_final = BooleanField() # 是否是最终结果
    rule_str = TextField() # 用于展示方程的字符串

SalaryCalcRuleModel() = SalaryComponentModel.filter(is_final=True)
    name = CharField()
    calc_rule = TextField() # 从 rule_str 中提取出来的方程


ValueField() # 所有需要用户输入数字column
    转变为
    instance of 
VariableModel()
    name = CharField()
    model = ForeignKey(ContentType)
    variable = CharField(ValueField_name) # 或者其他效率更高的形式

ResultModel()
    name = CharField()
    equation = TextField() # 用于展示方程的字符串

DataModel()
OutputModel
Company:
Department: 行政部门, 线上部门

Employee:


#TODO 6/17(v0.0): 
2. 审核(Class for Calc)
4. 个税
5. SalaryProcess 添加每个表单对应修改时间
1. 花名册添加注册类/资格类
6. 极简报销表单
3. 权限配置