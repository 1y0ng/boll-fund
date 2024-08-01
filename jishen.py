import sys
import getopt#导入getopt包
import GetDetail
import GetAdvice
import GetImg
argv=sys.argv[1:]
opts,args=getopt.getopt(argv,"i:o:d:a")#除了a以外其余选项都应该带有参数
# print(opts)
i=0
d=0
code=''
opt,arg=opts[0]
for opt,arg in opts:
    if opt=='-i':#显示某一基金的图像
        i=1
        code=arg
    elif opt=='-a':#获取今日基金购买建议
        GetAdvice.run()
    elif opt=='-o':#获取指定基金今日的详细数据
        GetDetail.run(arg)
    elif opt=='-d':
        d=int(arg)
if i==1:
    if d<=0:
        GetImg.run(code)
    else:
        GetImg.run(code,d)