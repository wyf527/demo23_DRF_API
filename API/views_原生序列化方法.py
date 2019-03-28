
from django.http import JsonResponse, HttpResponse
from django.views import View
from jsonpickle import json

from API.models import Actor

# 原生接口之实现查询所有演员功能
# 此时不再直接生成HttpResponse对象，而是返回Json格式数据给前端
class ActorListView(View):
    def get(self,request):
        #路由格式(查询所有演员)
        # GET  /actors/

        #数据库查询
        actors=Actor.objects.all()

        actorsList=[]

        #以Json格式返回，外层包裹列表
        for actor in actors:
            actorsList.append({
                'aid':actor.aid,
                'aname':actor.aname,
                'age':actor.age,
                'agender':actor.agender,
                'birth_date':actor.birth_date,
                #三目运算，如果没有，赋值空
                'photo':actor.photo.url if actor.photo else ''
                        })

        return JsonResponse(actorsList,safe=False)

    def post(self, request):
        'POST / actors /'
        json_byte = request.body  # b'name=wyf&pwd=123'
        #有无此步骤与版本有关
        json_str = json_byte.decode()  # 'name=wyf&pwd=123'
        actor_dict = json.load(json_str)  # {'name':'wyf','pwd':123}

        # 添加成功后，数据库会返回一个对象
        actor = Actor.objects.create(
            aname=actor_dict.get('aname'),
            age=actor_dict.get('age'),
            agender=actor_dict.get('agender'),
            birth_date=actor_dict.get('birth_date'),
        )

        # 添加成功后，也要将此信息返回给前端页面
        return JsonResponse(
            {
                'aid': actor.aid,
                'aname': actor.aname,
                'age': actor.age,
                'agender': actor.agender,
                'birth_date': actor.birth_date,
                # 三目运算，如果没有，赋值空
                'photo': actor.photo.url if actor.photo else ''
            }
        )

class ActorDetailView(View):
    #增加、更改、删除都是【基于查询】，所以要【先】确定该条数据是否存在
    def put(self,request,pk):
        'PUT  /actors/<pk>/'
        try:
            actor=Actor.objects.get(sid=pk)
        except Actor.DoesNotExist:
            raise HttpResponse(status=404)

        actor.dict=json.loads(request.body)

        #省略put请求方式中的数据类型验证

        actor.aname=actor.dict.get('aname')
        actor.age=actor.dict.get('age')
        actor.save()

        return JsonResponse(
            {
                'aid': actor.aid,
                'aname': actor.aname,
                'age': actor.age,
                'agender': actor.agender,
                'birth_date': actor.birth_date,
                'photo': actor.photo.url if actor.photo else ''
            }
        )

    def delete(self,request,pk):
        'DELETE  /actors/<pk>/'
        try:
            actor=Actor.objects.get(sid=pk)
        except Actor.DoesNotExist:
            raise HttpResponse(status=404)

        actor.delete()

        return JsonResponse({'message':'delete is done'})