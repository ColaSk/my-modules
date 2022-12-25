from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConflictError

cli = Elasticsearch(
    [
        {"host": "127.0.0.1", "port": 9200}
    ],
    timeout=3600
)

def employee_example():
    """这是一个与员工的例子
    假设我们刚好在Megacorp工作,这时人力资源部门出于某种目的需要让我们创建一个员工目录,
    这个目录用于促进人文关 怀和用于实时协同工作，所以它有以下不同的需求： 
    1. 数据能够包含多个值的标签、数字和纯文本。 
    2. 检索任何员工的所有信息。 
    3. 支持结构化搜索，例如查找30岁以上的员工。 
    4. 支持简单的全文搜索和更复杂的短语(phrase)搜索 
    5. 高亮搜索结果中的关键字
    6. 能够利用图表管理分析这些数据
    """

    # 索引员工文档
    
    # 存储方式的地比
    # Relational DB -> Databases(数据库) -> Tables（表） -> Rows（行） -> Columns （列）
    # Elasticsearch -> Indices（索引） -> Types（类型） -> Documents（文档） -> Fields （属性）
    
    # 1. 定义一个用户文档，包含用户的所有信息
    
    # 定义索引与类型
    index = "megacorp"
    type = "employee"

    users = [
        {"id": 1, "first_name" : "John", "last_name" : "Smith", "age" : 25, "about" : "I love to go rock climbing", "interests": ["sports", "music"]},
        {"id": 2, "first_name" : "Jane", "last_name" : "Smith", "age" : 32, "about" : "I like to collect rock albums", "interests": [ "music" ] },
        {"id": 3, "first_name" : "Douglas", "last_name" : "Fir", "age" : 35, "about": "I like to build cabinets", "interests": [ "forestry" ] }
    ]
    
    # 创建

    for user in users:
        try:
            create_response = cli.create(index=index, id=user['id'], document=user, doc_type=type)
        except ConflictError as e:
            print(e.__str__())
            continue
        print(create_response)

    
    # 检索文档

    get_reponse = cli.get(index, 1, doc_type=type)
    print(get_reponse)

    # 简单搜索

    search_reponse = cli.search(index=index)
    print(search_reponse)

    ## dsl 搜索

    dsl_query = { "query" : { "match" : { "last_name" : "Fir" } } }
    dsl_search_reponse = cli.search(body=dsl_query, index=index)
    print(dsl_search_reponse)


if __name__ == "__main__":
    employee_example()