from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet

from API.models import Actor, Movie
from API.serializers_no_模型类序列化器 import *

#restful framework自带的视图结果集，不再是普通的视图函数，这里集合了curd操作
#为了让接口文档显示文字提示，需要直接在类，类名下面添加注释，必须英文标点，注释方法 参考ctrl+ModelViewSet
class ActorListView(ModelViewSet):
    """
        list:
        显示所有演员信息

        create:
        创建演员

        retrieve:
        查询某个演员具体信息

        update
        partial_update
        destroy

    """
    # 指定要curd的模型类
    queryset = Actor.objects.all()
    # 指定序列化器,对查询到的数据进行序列化，可在前端页面接收Json格式数据
    serializer_class = ActorModelSerializer


class MovieListView(ModelViewSet):
    queryset = Movie.objects.all()

    serializer_class = MovieModelSerializer

    # GenericAPIView