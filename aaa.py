from pymilvus import connections, utility

try:
    # 连接本地 Milvus
    connections.connect(
        host="localhost",
        port=19530
    )
    
    # 获取版本信息
    print("✅ 连接成功！Milvus 版本:", utility.get_server_version())
    
except Exception as e:
    print(f"❌ 连接失败: {str(e)}")