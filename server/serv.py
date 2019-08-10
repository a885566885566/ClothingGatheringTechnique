import asyncio
from aiohttp import web

#FILE_PATH = './public'
#MAIN_INDEX = '/index.html'

async def ClothStatus(request):
    print("Get new req")
    #with open(FILE_PATH + MAIN_INDEX) as f:
    #return web.Response(text=f.read(),content_type='text/html')
    return web.Response(text="Hello World",content_type='text/html')

async def ClothDrying(request):
    global key
    print("Get new req")
    key = request.rel_url.query['key']
    finish = request.rel_url.query['end']
    
    if finish == '0':
        return web.Response(text=key + " not finish",content_type='text/html')
    elif finish == '1':
        return web.Response(text=key + " finish",content_type='text/html')
    elif finish == '2':
        return web.Response(text=key + " next cloth",content_type='text/html')
     

async def ClothGathering(request):
    global key
    print("Get new req")
    key = request.rel_url.query['key']
    pack = request.rel_url.query['group']
    state = request.rel_url.query['state']
    #with open(FILE_PATH + MAIN_INDEX) as f:
    #return web.Response(text=f.read(),content_type='text/html')
    return web.Response(text="Hello World",content_type='text/html')

async def Test():
    while True:
        await asyncio.sleep(1)
        print("test")

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_static('/public','./public')
    #receiving request
    app.router.add_get('/public/status',ClothStatus)
    app.router.add_get('/drying',ClothDrying)
    app.router.add_get('/public/gathering',ClothGathering)
    srv = await loop.create_server(app.make_handler(),host='0.0.0.0',port=11230)
    print("server created")
    return srv

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()

        #create task(can add any function)
        #loop.create_task(Test())
        
        loop.run_until_complete(init(loop))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()
