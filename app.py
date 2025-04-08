from executor import PipelineExecutor
from cli import CommandLine, read_yaml_config
import gradio as gr
import time
import re
import html

# ===== 配置参数 =====
build_tasks = ["构建索引", "删除索引"]
custom_css = """
/* 清新专业配色方案 */
:root {
    --primary: #3B82F6;    /* 清新蓝，按钮/强调色 */
    --secondary: #F3F4F6;  /* 卡片灰，背景用 */
    --accent: #60A5FA;     /* 点缀蓝，hover时使用 */
    --light: #FFFFFF;      /* 背景白 */
    --text: #1F2937;       /* 主文字深灰蓝 */
    --border: #E5E7EB;     /* 线条淡灰 */
    --card-bg: #FFFFFF;    /* 卡片白底 */
    --highlight: #EF4444;  /* 高亮红（法律条款等） */
}


body {
    font-family: 'LXGW WenKai', 'PingFang SC', sans-serif;
    background: #f1f5f9;
    color: var(--text);
    margin: 0;
    line-height: 1.6;
}

.gradio-container {
    width: 100%;
    max-width: none;
    padding: 0;
    margin: 0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.header {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
    padding: 2rem 1rem;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.main-content {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    padding: 1.5rem;
    width: 100%;
    box-sizing: border-box;
    flex: 1;
}

.input-card, .output-card {
    flex: 1 1 500px;
    background: var(--card-bg);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 15px rgba(0,0,0,0.05);
    border: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    height: 600px; /* 固定高度 */
}

.question-input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(255, 209, 128, 0.3);
    outline: none !important;
}

/* 法律回答专业样式 */
.answer-output {
    border: 1px solid var(--border);
    border-radius: 10px;
    background: #fcfcfc;
    padding: 1rem;
    overflow-y: auto;
    transition: background 0.3s;
    scrollbar-width: thin;
    scrollbar-color: var(--accent) var(--light);
}

.answer-output::-webkit-scrollbar {
    width: 8px;
}

.answer-output::-webkit-scrollbar-thumb {
    background-color: var(--accent);
    border-radius: 8px;
}
.waiting-placeholder {
    text-align: center;
    color: #222; /* 更深更清晰 */
    padding: 2rem;
    font-size: 1.1rem;
    font-weight: 500;
}
.waiting-placeholder p {
    margin-top: 0.5rem;
    font-style: italic;
}

.loader {
    width: 48px;
    height: 48px;
    border: 5px solid #eee;
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}


@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.legal-answer {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    font-family: 'LXGW WenKai', sans-serif;
    line-height: 1.8;
}

.legal-answer h3 {
    color: var(--primary);
    margin: 1.5em 0 0.8em 0;
    font-size: 1.25rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5em;
}

.legal-answer .highlight-item {
    margin: 1em 0;
    padding-left: 1em;
    border-left: 3px solid var(--accent);
    color: var(--text);
}

.legal-answer .legal-clause {
    color: var(--highlight);
    font-weight: 600;
}

.legal-answer .disclaimer {
    margin-top: 2em;
    padding-top: 1em;
    border-top: 1px dashed var(--border);
    color: #666;
    font-size: 0.9rem;
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
    color: white !important;
    padding: 0.75rem 1.5rem;
    border-radius: 10px;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 4px 10px rgba(255, 209, 128, 0.4);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(255, 209, 128, 0.6);
}

@media (max-width: 768px) {
    .main-content {
        flex-direction: column;
        padding: 1rem;
    }
    .input-card, .output-card {
        width: 100%;
        min-height: auto;
    }
}

.law-loader {
    text-align: center;
    color: #222;
    padding: 2rem;
    font-size: 1rem;
}

.law-book {
    display: inline-block;
    width: 180px;
    margin: 0 auto 1rem auto;
}

.law-book .line {
    height: 10px;
    background: #c0d8ff;
    margin: 5px 0;
    border-radius: 5px;
    animation: pulse 1.5s infinite ease-in-out;
}

.law-book .delay1 { animation-delay: 0.1s; }
.law-book .delay2 { animation-delay: 0.3s; }
.law-book .delay3 { animation-delay: 0.5s; }
.law-book .delay4 { animation-delay: 0.7s; }

@keyframes pulse {
    0% { opacity: 0.3; transform: scaleX(0.9); }
    50% { opacity: 1; transform: scaleX(1); }
    100% { opacity: 0.3; transform: scaleX(0.9); }
}

.typing-text {
    font-style: italic;
    font-weight: 500;
    color: #333;
    animation: typing 2s steps(20, end) infinite;
    white-space: nowrap;
    overflow: hidden;
    border-right: 2px solid #333;
}

@keyframes typing {
    from { width: 0 }
    to { width: 100% }
}

"""

class LegalAssistant(CommandLine):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.config_path = cfg
        self._executor = None
        self.is_ready = False
        self.status = "🔄 系统正在初始化..."

    def initialize_system(self):
        """系统初始化"""
        try:
            self.status = "🔄 正在加载配置文件..."
            yield self.status

            conf = read_yaml_config(self.config_path)
            self.status = "🔄 正在初始化执行引擎..."
            yield self.status

            self._executor = PipelineExecutor(conf)
            self.status = "🔄 正在构建查询系统..."
            yield self.status

            self._executor.build_query_engine()
            self.status = "✅ 系统准备就绪"
            self.is_ready = True
            yield self.status

        except Exception as e:
            self.status = f"❌ 初始化失败: {str(e)}"
            yield self.status

    def format_legal_answer(self, text):
        """专业法律回答格式化"""
        # 基本HTML转义
        text = html.escape(text)

        # 转换规则（按优先级排序）
        replacements = [
            # 一级标题 (# 开头)
            (r'#\s*(.+?)(\n|$)', r'<h3>\1</h3>'),
            # 二级标题 (## 开头)
            (r'##\s*(.+?)(\n|$)', r'<h4>\1</h4>'),
            # 重点条目 (* 开头)
            (r'\*\s*(.+?)(\n|$)', r'<div class="highlight-item">• \1</div>'),
            # 法律条款（第XX条）
            (r'(第[零一二三四五六七八九十百千万0-9]+条)', r'<span class="legal-clause">\1</span>'),
            # 星号标记 → 书名号
            (r'\*{1,2}(.+?)\*{1,2}', r'<cite>\1</cite>'),
            # 换行
            (r'\n', '<br>'),
        ]


        for pattern, repl in replacements:
            text = re.sub(pattern, repl, text)

        return text

    def process_question(self, question):
        """处理法律问题"""
        if not question.strip():
            return "⚠️ 请输入有效问题"

        if not self.is_ready or not self._executor:
            return "⚠️ 系统尚未准备好，请稍后再试"

        try:
            start_time = time.time()
            raw_answer = str(self._executor.query(question))
            process_time = time.time() - start_time

            formatted = self.format_legal_answer(raw_answer)

            return f"""
            <div class="legal-answer">
                <h3>法律分析（耗时{process_time:.2f}s）</h3>
                {formatted}
                <div class="disclaimer">
                    以上分析由AI生成，仅供参考。如需法律行动，请咨询专业律师。
                </div>
            </div>
            """

        except Exception as e:
            return f"<div class='legal-answer'>⚠️ 处理出错：{str(e)}</div>"

    def index(self, task, path):
        """索引管理"""
        try:
            if task == "构建索引":
                return f"✅ 已为 {path} 构建索引"
            elif task == "删除索引":
                return f"✅ 已删除 {path} 的索引"
            return "⚠️ 请选择有效操作"
        except Exception as e:
            return f"❌ 操作失败: {str(e)}"


# ===== 创建界面 =====
assistant = LegalAssistant("cfgs/config.yaml")

with gr.Blocks(
        title="智能法律助手",
        theme=gr.themes.Soft(primary_hue="blue"),
        css=custom_css
) as demo:

    # === 头部 ===
    with gr.Column(elem_classes="header"):
        gr.Markdown("""
        <h1>⚖️ 智能法律助手</h1>
        <p>专业法律分析与咨询</p>
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
                placeholder="例如：劳动合同解除后经济补偿如何计算？",
                lines=8,
                elem_classes="question-input"
            )

            gr.Examples(
                examples=[
                    "租房合同违约如何索赔",
                    "交通事故责任认定标准",
                    "离婚财产分割原则"
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

        # 输出区
        with gr.Column(elem_classes="output-card"):
            answer_output = gr.HTML(
                label="分析结果",
                value="""
                    <div class="waiting-placeholder" style="background:#f9fafb; padding: 2rem; border-radius: 12px;">
                        <p style="font-size: 1.1rem; color:#666;">🧠 系统已准备，等待您的提问...</p>
                    </div>

                    """,
                elem_classes="answer-output"
            )

    # === 高级管理 ===
    with gr.Accordion("⚙️ 高级管理", open=False):
        with gr.Row():
            with gr.Column():
                build_task = gr.Dropdown(
                    label="索引操作",
                    choices=build_tasks,
                    value=build_tasks[0]
                )
                file_path = gr.Textbox(
                    label="文档路径",
                    placeholder="输入文件或目录路径"
                )
                build_btn = gr.Button(
                    "执行操作",
                    variant="primary"
                )
                build_status = gr.Textbox(
                    label="操作结果",
                    interactive=False
                )

    # === 事件绑定 ===
    demo.load(
        assistant.initialize_system,
        outputs=[status_display],
        show_progress=False
    )

    # submit_btn.click(
    #     assistant.process_question,
    #     inputs=[question_input],
    #     outputs=[answer_output],
    #     show_progress=False
    # )

    # def show_loading():
    #     return """
    # <div class="waiting-placeholder">
    #     <div class="loader"></div>
    #     <p>正在分析中，请稍候...</p>
    # </div>
    # """
    def with_loading():
        loading_html = """
        <div class="law-loader">
            <div class="law-book">
                <div class="line"></div>
                <div class="line delay1"></div>
                <div class="line delay2"></div>
                <div class="line delay3"></div>
                <div class="line delay4"></div>
            </div>
            <p class="typing-text">📖 正在研读法律条文，请稍候...</p>
        </div>
        """
        yield loading_html  # 立即显示动画

    submit_btn.click(
        with_loading,
        outputs=[answer_output],
        show_progress=False
    ).then(
        fn=assistant.process_question,
        inputs=[question_input],
        outputs=[answer_output],
        show_progress=False
    )

if __name__ == "__main__":
    demo.launch(
        server_port=7860,
        share=True,
        favicon_path="law.ico"
    )