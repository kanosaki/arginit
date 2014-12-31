arginit -- Initialize an object by argument 
===========================================

Python向けのシンプルなプログラム引数解析ライブラリ

以下のEchoクラスのような普通のPythonクラスからよしなに引数解析と
ヘルプの生成を行います

```python
class Echo(object):
    "Simple echo tool"

    def __init__(self, msg, repeat=10, interval=0.5):
        """
        Arguments:
            msg -- message body
            repeat -- time to echo
            interval -- interval seconds
        """
        self.message = msg
        self.repeat = int(repeat)
        self.interval = float(interval)

    def start(self):
        for i in range(self.repeat):
            print(self.message)
            time.sleep(self.interval)
        print("Done")
```


```sh
$ ./echo.py -h
usage: echo.py [-h] [-r REPEAT] [-i INTERVAL] msg

Simple echo tool

positional arguments:
  msg                   message body

optional arguments:
  -h, --help            show this help message and exit
  -r REPEAT, --repeat REPEAT
                        time to echo
  -i INTERVAL, --interval INTERVAL
                        interval seconds
```


具体的には，`__init__`メソッドの引数名をそのままオプションとし
各引数のhelpはdocstringから抜き出しています


arginit.createで自動的にsys.argvから引数を受け取り，
それを用いて指定されたクラスをインスタンス化します
```python
if __name__ == '__main__':
    service = arginit.create(Echo)
    service.start()
```
