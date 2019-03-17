from twisted.internet.defer import Deferred
'''
addcallbacks函数添加的callback 和 errback位于同一层, 上一层成功调用callback, 失败调用errback
errback处理完如果不传递failure的话会调用下一层的callback, 若failure往下传递则调用下一层errback
主要看 test2 test6 test7
'''


def callback1(res):
    print('Callback 1 said: ' + res)
    return res


def callback2(res):
    print('Callback 2 said: ' + res)


def callback3(res):
    raise Exception('Callback 3')


def errback1(failure):
    print('Err1 had a failure on ' + str(failure))
    return failure


def errback2(failure):
    raise Exception('Err 2')


def errback3(failure):
    print('Err3 took care of ' + str(failure))
    return 'it is fine now'


d = Deferred()


# test1
# d.addCallback(callback1)
# d.addCallback(callback2)
# d.addCallback(callback3)
# d.callback('123')

#test2
# d.addCallback(callback1)
# d.addCallback(callback2)
# d.addCallback(callback3)
# d.addErrback(errback3)
# d.callback('123')

# test3
# d.addErrback(errback1)
# d.errback(123)

# test4
# d.addErrback(errback1)
# d.addErrback(errback3)
# d.errback(123)

#test5
# d.addErrback(errback2)
# d.errback(123)

# test6
# d.addCallback(callback1)
# d.addCallback(callback2)
# d.addCallbacks(callback3, errback3)
# d.callback('123')

#test7
d.addCallback(callback3)
d.addCallbacks(callback2, errback3)
d.addCallbacks(callback1, errback2)
d.callback('123')