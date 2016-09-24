# coding=utf-8
import core
import sys

if __name__ == '__main__':
    if len(sys.argv) is not 2 or sys.argv[1] not in ('slave', 'master'):
        raise Exception('启动错误,　请使用 " /path/to/python /path/to/chin.py master或slave " 启动')
    role = sys.argv[1]
    core.run(role)
