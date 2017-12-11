import eventlet

eventlet.monkey_patch(socket=True, select=True, thread=True, time=True)
