import frame

def go():
    docpath = input('请输入您的Wechat Files路径（在微信->设置->通用设置中）：')
    zip_here = input('请输入备份的zip路径（包括zip文件名）：')
    if not docpath or not zip_here:
        raise ValueError(
            "The above two inputs cannot be enpty.以上两个输入框不可为空。")
    else:
        frame_ = frame.Framework(docpath,zip_here)
        print('已启动框架！这个过程比较复杂，心焦了可以看以下的日志~')
        try:
            frame_.run()
        except Exception as e:
            raise RuntimeError(
                "An irresistible error occurred.发生不可抗拒错误。错误原因：%s"%e
            )
        finally:
            print('done~')

if __name__ == '__main__':
    print('''CleanWechatFiles Command By Joinsodome [版本 0.1]
Plagiarism is strictly prohibited.严禁抄袭。''')
    go()