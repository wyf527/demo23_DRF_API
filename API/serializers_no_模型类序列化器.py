# from typing import re

from rest_framework import serializers
from API.models import Actor, Movie


# 相当于serializers.Serializer(基类)的子类
# class ActorSerializer(serializers.ModelSerializer):
#     """演员序列化器"""
#     class Meta:
#         model = Actor
#         fields = '__all__'

# 【反】序列化数据验证方法【1】：
# def v_age(value):
#     reg=r'^[123]\d{1}$'
#     v=str(value)
#     if not re.match(reg,v):
#         raise serializers.ValidationError('age字段 年龄不在10—40之间')


#创建序列化器，对【模型类】中的数据进行【序列化】，使其可按照前端要求格式返回
#严格按照models.py中属性添加
class ActorModelSerializer(serializers.Serializer):
    GENDER_ID = (
        ('0', '男'),
        ('1', '女')
    )
    #注意：属性不能照搬models.py设置
    # 原因：DRF本身没有对应约束；该约束是针对DRF前台数据页面的修改部分，本身就是赋予用户自由定义的部分
    aid = serializers.IntegerField(label='编号', read_only=True)
    # help_text = 'name field',接口文档
    aname = serializers.CharField(label='姓名', max_length=30,help_text='name field')
    ##【反】序列化数据验证方法1.1：
    # age = serializers.IntegerField(label='年龄', required=False,validators=[v_age])
    age = serializers.IntegerField(label='年龄', required=False)
    agender = serializers.ChoiceField(choices=GENDER_ID, label='性别', required=False)
    birth_date = serializers.DateField(label='出生年月', required=False)
    photo = serializers.ImageField(label='头像', required=False)

    # 【反】序列化数据验证方法【2】:定义一个内部方法
    # def validate_age(self, value):
    #      reg=r'^[123]\d{1}$'
    #     value=str(value)
    #     if not re.match(reg,value):
    #         raise serializers.ValidationError('age字段 不在10—40之间')

    # def validate(self, attrs):
    #     print(attrs)
    #     aname=attrs['aname']
    #     age=attrs['age']
    #
    #     if 'hello' in aname:
    #         raise serializers.ValidationError('aname字段 不能包括hello')
    #
    #     #注意：正则表达式的^ $
    #     reg = r'^[123]\d{1}$'
    #     age = str(age)
    #     if not re.match(reg, age):
    #         raise serializers.ValidationError('age字段 不在10—40之间')
    #
    #     return attrs

    #【反】序列化 保存数据 向序列化对象 传递data时
    def create(self, validated_data):
        return Actor.objects.create(**validated_data)

    #【反】序列化 保存数据 向序列化对象 传递instance，data时
    def update(self, instance, validated_data):
        instance.aid=validated_data.get('aid',instance.aid)
        instance.aname=validated_data.get('aname',instance.aname)
        instance.age=validated_data.get('age',instance.age)
        instance.agender=validated_data.get('agender',instance.agender)
        instance.birth_date=validated_data.get('birth_date',instance.birth_date)
        instance.photo=validated_data.get('photo',instance.photo)
        instance.save()
        return instance

#作为多的一方，还需要注意将外键，即将关联数据也顺利展示出来(3种方法，根据具体情况决定)
class MovieModelSerializer(serializers.Serializer):
    mid = serializers.IntegerField(label='影片编号',read_only=True)
    mname = serializers.CharField(label='影片名称',max_length=30)
    m_pub_date = serializers.DateField(label='上映时间',required=False)
    mread = serializers.IntegerField(label='观影人数',default=0)
    mcomment = serializers.CharField(label='评论',allow_null=True)
    mimage = serializers.ImageField(label='图片',required=False)
    #外键序列化方法1：
    # PrimaryKeyRelatedField，顾名思义，显示外键时，是主键的值
    # 注意：该方法要对【参数进行设置】
    # actors = serializers.PrimaryKeyRelatedField(label='演员',read_only=True)
    # actors = serializers.PrimaryKeyRelatedField(label='演员',queryset=Actor.objects.all())

    #外键序列化方法2：使用【关联对象】的序列化器
    #显示外键时，是OrderedDict
    # actors=ActorModelSerializer()

    # 外键序列化方法3：StringRelatedField
    # 显示外键时，此字段将被序列化为关联对象的字符串表示方式（即__str__方法的返回值）
    # actors = serializers.StringRelatedField()

    #【反】序列化 保存数据 外键设置
    # 注意：由于是朝向数据库的操作，所以，需要将名字改为数据库中的字段名，actors_id,否则，在前端无法显示
    actors_id=serializers.IntegerField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.mid=validated_data.get('mid',instance.mid)
        instance.mname=validated_data.get('mname',instance.mname)
        instance.m_pub_date = validated_data.get('m_pub_date', instance.m_pub_date)
        instance.save()