import argparse
from aiohttp import web
'''
async def handle(request):
    name = request.match_info.get('name','Anonymous')
    text = "Hello, " + name
    return web.Response(text = text)
'''

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, World")

app = web.Application()
app.add_routes(routes)
web.run_app(app)

'''
parser = argparse.ArgumentParser(description = "aiohttp server example")
parser.add_argument('--path')
parser.add_argument('--port')

if __name__ == '__main__':
    app = web.Application()
    #app.add_routes(routes)
    args = parser.parse_args()
    web.run_app(app , path = args.path , port = args.port)
'''
