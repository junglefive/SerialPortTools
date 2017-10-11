#!/usr/bin/python
# -*- coding: utf-8 -*-
import  os,sys
print("注意：")
print("本程序会自动创建项目目录\n请输入项目名称：")
RootDirName = "智慧健康部"
try:
    os.mkdir(RootDirName)
    os.mkdir(RootDirName+"/01-管理制度")
    os.mkdir(RootDirName+"/01-管理制度/01-部门手册")
    os.mkdir(RootDirName+"/01-管理制度/02-岗位手册")
    os.mkdir(RootDirName+"/01-管理制度/03-会议制度")
    os.mkdir(RootDirName+"/01-管理制度/04-绩效制度")
    #daily
    os.mkdir(RootDirName+"/02-日常管理")
    os.mkdir(RootDirName+"/02-日常管理/01-例会纪要")
    os.mkdir(RootDirName+"/02-日常管理/02-工时统计")
    os.mkdir(RootDirName+"/02-日常管理/03-表格模板")
    #knowledge
    os.mkdir(RootDirName+"/03-知识产权")
    os.mkdir(RootDirName+"/03-知识产权/01-发明专利")
    os.mkdir(RootDirName+"/03-知识产权/02-实用新型专利")
    os.mkdir(RootDirName+"/03-知识产权/03-软件著作权")
    #pro
    os.mkdir(RootDirName+"/04-机密资料")
    os.mkdir(RootDirName+"/05-技术规范")
    os.mkdir(RootDirName+"/05-技术规范/01-汇编程序编写规范")
    os.mkdir(RootDirName+"/05-技术规范/02-C语言程序编写规范")

    # project
    os.mkdir(RootDirName+"/06-技术资料")
    os.mkdir(RootDirName+"/06-技术资料/01-项目资料")
    os.mkdir(RootDirName+"/06-技术资料/01-项目资料/01-客户方案")
    os.mkdir(RootDirName+"/06-技术资料/01-项目资料/02-标准方案")
    os.mkdir(RootDirName+"/06-技术资料/01-项目资料/03-标准模块")
    os.mkdir(RootDirName+"/06-技术资料/01-项目资料/04-测试类项目")
    #chip
    os.mkdir(RootDirName+"/06-技术资料/02-芯片资料")
    os.mkdir(RootDirName+"/06-技术资料/02-芯片资料/01-测脂系列")
    os.mkdir(RootDirName+"/06-技术资料/02-芯片资料/02-SOC 系列")
    os.mkdir(RootDirName+"/06-技术资料/02-芯片资料/03-MTP 系列")
    os.mkdir(RootDirName+"/06-技术资料/02-芯片资料/04-WIFI系列")
    os.mkdir(RootDirName+"/06-技术资料/02-芯片资料/05-BLE 系列")
    os.mkdir(RootDirName+"/06-技术资料/02-芯片资料/06-ADC 系列")
    #tool
    os.mkdir(RootDirName+"/06-技术资料/03-客诉问题")
    os.mkdir(RootDirName+"/06-技术资料/04-技术支持")
    os.mkdir(RootDirName+"/06-技术资料/05-培训资料")
    os.mkdir(RootDirName+"/06-技术资料/06-辅助工具")
    os.mkdir(RootDirName+"/06-技术资料/07-共享资料")
    os.mkdir(RootDirName+"/06-技术资料/08-协议资料")

    os.mkdir(RootDirName+"/07-市场调研")
    os.mkdir(RootDirName+"/07-市场调研/01 市场需求")
    os.mkdir(RootDirName+"/07-市场调研/02 竞品资料")
    os.mkdir(RootDirName+"/07-市场调研/03 行业标准")
    os.mkdir(RootDirName+"/08-临时文件")
    os.mkdir(RootDirName+"/09-外部资料")
    print("目录生成成功，请在当前目录查看！")

except Exception as e:
    print("出现错误，请检查是否已有相关目录:",str(e))
finally:
    print("执行结束,按任意键退出")
    input()

