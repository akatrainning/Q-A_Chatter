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

assistant = LegalAssistant("cfgs/config.yaml")

with gr.Blocks(

        title="安鉴无界-智能法律助手",
        theme=gr.themes.Soft(primary_hue="blue"),
        css=custom_css
) as demo:
    # 状态变量：追踪决策路径和节点编号
    decision_path_state = gr.State("初始节点")
    node_counter_state = gr.State(1)
    # === 头部 ===
    with gr.Column(elem_classes="header"):
        gr.Markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');
@font-face {
  font-family: 'Alibaba Sans';
  src: url('https://cdn.jsdelivr.net/gh/lxgw/fonts/alibaba/AlibabaSans-Regular.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
}
</style>

<h1 style="text-align: center; line-height: 1.2; margin-bottom: 0.5em;">
  <span style="
      font-family: 'Poppins', sans-serif;
      font-size: 2.8em;
      font-weight: 600;
      letter-spacing: 1.2px;
      background: linear-gradient(90deg, #7dd3fc, #0ea5e9);
      -webkit-background-clip: text;
      color: transparent;
      display: block;
  ">
    Securit<span style="font-weight: 300;">AI</span>
  </span>
  <span style="
      font-family: 'Alibaba Sans', sans-serif;
      font-size: 2.2em;
      color: #f1f5f9;
      display: block;
      font-weight: 500;
      letter-spacing: 4px;
  ">
    安鉴无界
  </span>
</h1>
<p style="text-align: center; color: #cbd5e1; font-size: 1.1em; margin-top: 0.5em;">
    国家安全智能问答系统
</p>
""")




    # === 主内容区 ===
    with gr.Row(elem_classes="main-content"):
        # 输入区
        with gr.Column(elem_classes="input-card"):
            status_display = gr.Textbox(
                label="系统状态",
                value=assistant.status,
                interactive=False
            )

            question_input = gr.Textbox(
                label="请输入法律问题",
                placeholder="例如：如果用户因某平台数据泄露遭遇诈骗，但平台以“已尽安全义务”为由拒绝赔偿。用户如何证明损害与信息泄露存在因果关系？举证责任如何分配？",
                lines=8,
                elem_classes="question-input"
            )

            gr.Examples(
                examples=[
                    "极端主义与宗教活动界定",
                    "数据泄露索赔举证责任",
                    "外卖信息泄露责任划分"
                ],
                inputs=[question_input],
                label="常见问题示例"
            )

            with gr.Row():
                submit_btn = gr.Button(
                    "获取法律分析",
                    variant="primary",
                    elem_classes="btn-primary"
                )

