# 存放配置
# author:KRzhao


class BaseConfig:
    """ 配置基类 """
    SECRET_KEY = 'KARAKARA'


class DevelopmentConfig(BaseConfig):
    """ 开发环境配置 """
    DEBUG = True
    # mysqldb 是一个连接数据库的驱动, '+mysqldb' 可以省略不写使用 mysql 自带的驱动
    # 如果你的 mysql 设置了密码, 在 root 字段后面写上 ':xxxx' 既可
    # 3306 为 mysql 服务的接口, 默认即为 3306, 所以也可以省略
    # '?' 后面连接参数, 设置字符编码格式为 utf8, 处理中文字符
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/website?charset=utf8'
    # 关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    """ 生产环境配置 """
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/website?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
}
