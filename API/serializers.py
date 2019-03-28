from rest_framework import serializers

from API.models import *

# ModelSerializer与常规的Serializer相同，但提供了：
# 基于模型类自动生成一系列字段
# 包含默认的create()和update()的实现

class ActorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Actor
        # fields='__all__'
        fields=('aname','age','agender')
        read_only_fields=('aid',)


class MovieModelSerializer(serializers.ModelSerializer):
    #设置外键为actor序列对象
    actors = ActorModelSerializer()

    class Meta:
        model=Movie
        fields='__all__'

        # extra_kwargs参数为ModelSerializer添加或修改原有的选项参数
        extra_kwargs={
            'mread':{'min_value':0,'required':False},
            'mcomment': {'required': False}
        }

