import click as c
import frame

@c.command()
@c.option("--docpath",'-dp',type=str)
@c.option("--zip_here",'-zp',type=str)
def go(docpath,zip_here):
    if not docpath or not zip_here:
        raise ValueError(
            "-dp or -zp Cannot be enpty.-dp或-zp不可为空。")
    else:
        frame_ = frame.Framework(docpath,zip_here)
        print('已启动框架！这个过程比较复杂，心焦了可以看以下的日志~')
        try:
            frame_.run()
        except Exception as e:
            raise RuntimeError(
                "An irresistible error occurred.发生不可抗拒错误。",
                "错误原因：%s"%e
            )
        finally:
            print('done~')

if __name__ == '__main__':
    print('''CleanWechatFiles Oneline By Joinsodome [版本 0.1]
Plagiarism is strictly prohibited.严禁抄袭。''')
    go()